from django.db.models.signals import post_save, post_delete,post_migrate
from django.dispatch import receiver
from .models import *
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Notification)
def send_notification_update(sender, instance, created, **kwargs):

    channel_layer = get_channel_layer()
    data = {
        'action': 'notification_update',
        'id': instance.id,
        'message': instance.Message,
    }
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            'type': 'send_notification_update',
            'data': data
        }
    )

@receiver(post_delete, sender=Notification)
def send_update_on_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    data = {
        'action': 'delete',
        'id': instance.id,
    }
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            'type': 'send_notification_update',
            'data': data
        }
    )

@receiver(post_save, sender=Project)
def send_project_update(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = {
        'action': 'create' if created else 'update',
        'project_id': instance.id,
        'new_state': instance.get_State_display() if not created else None,
    }
    
    # Send notification for create or update
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            'type': 'send_notification_update',
            'data': data
        }
    )
    
    # Only check for state change on update
    if not created:
        old_instance = Project.objects.get(pk=instance.pk)
        if old_instance.State != instance.State:
            state_change_data = {
                'action': 'state_change',
                'project_id': instance.id,
                'new_state': instance.get_State_display(),
            }
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    'type': 'send_notification_update',
                    'data': state_change_data
                }
            )

@receiver(post_delete, sender=Project)
def send_project_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    data = {
        'action': 'delete',
        'project_id': instance.id,
    }
    
    # Send notification for delete
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            'type': 'send_notification_update',
            'data': data
        }
    )