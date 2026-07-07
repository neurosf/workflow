from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import Tache, Notification, Notification_to
from django.contrib.contenttypes.models import ContentType
from .models import * 

@shared_task
def check_tache_alerts():
    current_time = now()

    for tache in Tache.objects.all():
        if tache.State != 2 or not tache.Date_start:
            continue  # Skip tasks that haven't started

        # Determine duration
        duration = tache.Tache_Def.Duration if tache.Tache_Def.Duration_const else tache.Max_Duration
        if not duration or duration.total_seconds() <= 0:
            continue

        time_passed = current_time - tache.Date_start
        alert_start_time = (tache.Tache_Def.Alert_Start_after / 100) * duration.total_seconds()
        if tache.Tache_Def.Alert_Start_after and time_passed.total_seconds() >= alert_start_time:
            alert_duration_seconds = tache.Tache_Def.Alert_Duration.total_seconds() if tache.Tache_Def.Alert_Duration else 0

            if alert_duration_seconds > 0:
                i = int((time_passed.total_seconds() - alert_start_time) // alert_duration_seconds)
            else:
                i = 0

            alert_time = alert_start_time + i * alert_duration_seconds
            # Check if time passed is close to alert time (within alert_duration_seconds)
            window_start = tache.Date_start + timedelta(seconds=alert_time)
            window_end   = tache.Date_start + timedelta(seconds=alert_time + alert_duration_seconds)

            # Check if notification already exists in this alert window
            already_sent = Notification.objects.filter(
                Relation=Notification.relation.Tache,
                object_id=tache.id,
                Date_Time__range=(window_start, window_end)
            ).exists()
            if not already_sent:

                message = (
                    "Tache time passed, you are late!"
                    if time_passed >= duration
                    else "Tache duration is almost over!"
                )

                # Create Notification
                notification = Notification.objects.create(
                    Relation=Notification.relation.Tache,
                    content_type=ContentType.objects.get_for_model(Tache),
                    object_id=tache.id,
                    Message=message,
                    Date_Time=current_time,
                )

                # Assign Notification to users
                team_members_ids = Team_members.objects.filter(Project=tache.Etape.Project).values_list("User_id", flat=True)
                To_Role = Tache_To.objects.filter(Tache_Def=tache.Tache_Def).values_list('Role', flat=True)
                To_id = User.objects.filter(Role__in=To_Role).values_list("id", flat=True)
                team_members_ids = list(set(team_members_ids) & set(To_id))
                notified_users = set()

                for user_id in team_members_ids:
                    if user_id not in notified_users:
                        try:
                            U = User.objects.get(id=user_id)
                            Notification_to.objects.create(
                                Notification=notification,
                                To=U,
                                Opened=False,
                            )
                            notified_users.add(user_id)
                        except User.DoesNotExist:
                            continue

@shared_task
def remind_projects_to_update():
    """
    Sends a reminder notification every 3 months for each project 
    if last MAJ reminder is older than 3 months or doesn't exist.
    """
    now = timezone.now()
    three_months_ago = now - timedelta(days=90)  # roughly 3 months

    projects = ProjectDF.objects.filter(weightings_points__lt=100)

    for project in projects:
        # Get last MAJ notification
        last_notif = NotificationDF.objects.filter(
            project=project,
            Message__icontains="MAJ"  # identify your reminder notifications
        ).order_by('-Date_Time').first()

        # Check if we should send a new one
        should_notify = False
        if not last_notif:
            # No prior notification — send first reminder if project older than 3 months
            if project.Created_At < three_months_ago:
                should_notify = True
        elif last_notif.Date_Time < three_months_ago:
            # Last notification is older than 3 months
            should_notify = True

        if not should_notify:
            continue

        # Build role-based logic
        situation = (project.situation_projet or "").lower().strip()
        roles_to_notify = set()

        if situation in ['perdus / en previsionnele','soumission', 'short listé']:
            roles_to_notify.update(PERMISSIONS['Commercial_View'])
        elif situation in ['gagné', 'affaire','attribue']:
            roles_to_notify.update(PERMISSIONS['Commercial_View'])
            roles_to_notify.update(PERMISSIONS['Achat_View'])
            roles_to_notify.update(PERMISSIONS['Finance_View'])

        if not roles_to_notify:
            continue

        notif = NotificationDF.objects.create(
            project=project,
            Message=f"🔔 MAJ Rappel : Veuillez mettre à jour les informations du projet {project.client} ({project.numero_appelle_doffre})",
            Date_Time=now,
        )

        users = User.objects.filter(Role__id__in=roles_to_notify)
        for u in users:
            Notification_toDF.objects.create(
                Notification=notif,
                To=u,
                Opened=False
            )