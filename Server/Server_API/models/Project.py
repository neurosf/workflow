from django.db import models
from django.utils import timezone
from datetime import timedelta

## Project

class Project(models.Model):

    NumContract = models.TextField(blank=True,default="")
    Num_Appele_dOffer = models.TextField(blank=True,default="")#,unique=True)
    Editeur_constructeur = models.TextField(blank=True,default="")
    Client = models.ForeignKey("Client",on_delete=models.SET_NULL,null=True)
    observation = models.TextField(blank=True,default="")
    class status(models.IntegerChoices):
        en_cours = 1 ,'en cours'
        gagner = 2, 'Gagner'
        perdue = 3, 'Perdue'
        shortliste = 4, 'Shortlisté'
        non_depose = 5, 'Non déposé'
        infructueux = 6, 'Infructueux'
    Status = models.IntegerField(choices=status.choices, default=status.en_cours)
    class type(models.IntegerChoices):
        appel_offre = 1, 'appel d\'offre'
        consultation = 2, 'consultation'
    Type = models.IntegerField(choices=type.choices, default=type.appel_offre)
    Date_Depot = models.DateTimeField(null=True)
    # system
    class state(models.IntegerChoices):
        Init = 1, 'Initiale'
        In_progress = 2, 'En exécution'
        Pose = 3 ,'en arrêt'
        Finished = 4, 'Termine'
        Deleted = 5, 'Supprime'
    State = models.IntegerField(choices=state.choices, default=state.Init)
    class etape(models.IntegerChoices):
        Non = 0, ''
        Soumission = 1, 'Soumission'
        Affaire = 2 ,'Affaire'
        project_realisation = 3, 'Projet en realisation'
        project_garantie = 4, 'Projet en cours de garantie'
        project_close = 5, 'Projet closé'
    Etape_S = models.IntegerField(choices=etape.choices, default=etape.Non)
    Date_start = models.DateTimeField(null=True)
    Date_End = models.DateTimeField(null=True)
    Object = models.TextField(default="")
    # ------------------------------
    # Progress calculation functions
    # ------------------------------
    def get_progress(self, current_date=None):
        """
        Returns a tuple: (real_progress %, predicted_progress %)
        """
        if current_date is None:
            current_date = timezone.now()

        totale_project_duration = 0
        real_p_progress = 0
        predicted_p_progress = 0

        # only étapes that started
        started_etapes = self.etape_set.filter(
            Date_start__isnull=False,
            Date_start__lte=current_date
        )

        for etape in started_etapes:
            totale_etape_duration = 0
            totale_task_finished_duration = 0
            real_progress = 0
            predicted_progress = 0
            start_date = etape.Date_start

            for task in etape.tache_set.all():
                start_date = task.Date_start or etape.Date_start
                if start_date and start_date.tzinfo is None:
                    start_date = start_date.replace(tzinfo=timezone.utc)

                duration = task.Tache_Def.Duration or task.Max_Duration or timedelta(seconds=0)

                # build end_date
                end_date = start_date + duration

                tache_duration = (end_date - start_date).total_seconds()

                # adjust with pauses
                total_pause_time = sum(
                    (min(pose.Date_End, end_date) - max(pose.Date_start, start_date)).total_seconds()
                    for pose in self.poseproject_set.all()
                    if pose.Date_start and pose.Date_End and pose.Date_start <= end_date and pose.Date_End >= start_date
                )

                adjusted_duration = tache_duration + total_pause_time
                totale_etape_duration += adjusted_duration

                if task.State >= 3:
                    totale_task_finished_duration += adjusted_duration

            time_passed = (current_date - start_date).total_seconds() if start_date else 0

            if time_passed > 0 and totale_etape_duration > 0:
                predicted_progress = min((time_passed / totale_etape_duration) * 100, 100)
                real_progress = min((totale_task_finished_duration / totale_etape_duration) * 100, 100)

            totale_project_duration += totale_etape_duration
            real_p_progress += real_progress
            predicted_p_progress += predicted_progress

        num_etapes = started_etapes.count()
        real_avg = (real_p_progress / num_etapes) if num_etapes else 0
        predicted_avg = (predicted_p_progress / num_etapes) if num_etapes else 0

        return round(real_avg, 2), round(predicted_avg, 2)

    def get_real_progress(self):
        return self.get_progress()[0]

    def get_predicted_progress(self):
        return self.get_progress()[1]
    
class PoseProject(models.Model):
    
    Date_start = models.DateTimeField(null=True)
    Date_End = models.DateTimeField(null=True)
    Project = models.ForeignKey("Project",on_delete=models.CASCADE,null=True)

class Def_data_Project(models.Model):

    Num = models.SmallIntegerField(default=0)
    Name = models.CharField(max_length=100,blank=True)
    Type = models.CharField(max_length=30,blank=True) ##### select type define for sys
    Etape_def = models.ForeignKey("Etape_def",on_delete=models.SET_NULL,null=True)
    Data_Groupe = models.ForeignKey("Data_Groupe",on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering = ['Num']
class Data_Groupe(models.Model):

    Name = models.CharField(max_length=100,blank=True)

class NonNullDefDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(Def_data_Project__isnull=True)
   
class Data_Project(models.Model):

    Value = models.TextField(blank=True)
    X = models.TextField(blank=True)
    Project = models.ForeignKey("Project",on_delete=models.CASCADE,default=1)
    Def_data_Project = models.ForeignKey("Def_data_Project",on_delete=models.SET_NULL,null=True)
    
    # objects = models.Manager()  # Default manager
    objects = NonNullDefDataManager()  # Custom manager

class Multy_data_project(models.Model):

    Num = models.PositiveSmallIntegerField(default=0)
    Value = models.TextField(blank=True)
    X = models.TextField(blank=True,default="")
    Data_Project = models.ForeignKey("Data_Project",on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering = ['Num']
class select_Values(models.Model): # data select fill 

    Value = models.TextField(blank=True)
    Def_data_Project = models.ForeignKey("Def_data_Project",on_delete=models.CASCADE,default=1)

class Fill_Message(models.Model): # data type fill 

    Num = models.PositiveSmallIntegerField(default=0)
    Message = models.TextField(blank=True)
    Def_data_Project = models.ForeignKey("Def_data_Project",on_delete=models.CASCADE,default=1)

class Table_strecture(models.Model):

    Col = models.IntegerField()
    Name = models.CharField(max_length=100,blank=True)
    class type(models.IntegerChoices):
        Text = 1, 'Text'
        Number = 2, 'Number'
        Date = 3, 'Date'
        DateTime = 4, 'DateTime'
        File = 5, 'File'
    Type = models.IntegerField(choices=type.choices, default=type.Text)
    Def_data_Project = models.ForeignKey("Def_data_Project",on_delete=models.CASCADE,default=1)
    class Meta:
        ordering = ['Col']
class Table_data(models.Model):

    Row = models.IntegerField()
    Value = models.TextField(blank=True)
    Table_strecture = models.ForeignKey("Table_strecture",on_delete=models.SET_NULL,null=True)
    Data_Project = models.ForeignKey("Data_Project",on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering = ['Row']
## Form

class Form(models.Model):

    Title = models.CharField(max_length=100,blank=True)
    Type = models.CharField(max_length=10,blank=True) # Show or Message

class Forme_Massage(models.Model):

    Value = models.CharField(max_length=100,blank=True) 
    Form = models.ForeignKey("Form",on_delete=models.SET_NULL,null=True)

class Form_Data(models.Model):

    Def_data_Project = models.ForeignKey("Def_data_Project",on_delete=models.CASCADE,default=1)
    Form = models.ForeignKey("Form",on_delete=models.CASCADE,default=1)
    Order_in_form = models.SmallIntegerField(default=0)
    class Meta:
        ordering = ['Order_in_form']
## Etape

class Etape(models.Model):

    Num = models.SmallIntegerField(default=0)
    class state(models.IntegerChoices):
        Waiting = 1, 'Waiting'
        In_progress = 2, 'In progress'
        Finished = 3, 'Finished'
    State = models.IntegerField(choices=state.choices, default=state.Waiting)
    Valide = models.BooleanField(default=False)
    Date_start = models.DateTimeField(null=True)
    Date_End = models.DateTimeField(null=True)
    Comment = models.TextField(blank=True)
    Etape_def = models.ForeignKey("Etape_def",on_delete=models.SET_NULL,null=True)
    Project = models.ForeignKey("Project",on_delete=models.CASCADE,default=1)

class Etape_def(models.Model):

    Num = models.SmallIntegerField(default=0)
    Name = models.CharField(max_length=100,blank=True)
    Description = models.TextField(blank=True)
    Loop = models.BooleanField(default=False)
    Created_with_Project = models.BooleanField(default=False)
    Start_with_Project = models.BooleanField(default=False)
    Show_Time = models.BooleanField(default=False)
    class etape(models.IntegerChoices):
        Non = 0, ''
        Soumission = 1, 'Soumission'
        Affaire = 2 ,'Affaire'
        project_realisation = 3, 'Projet en realisation'
        project_garantie = 4, 'Projet en cours de garantie'
        project_close = 5, 'Projet closé'
    Etape_S = models.IntegerField(choices=etape.choices, default=etape.Soumission)
    deleted = models.BooleanField(default=False)
    class Meta:
        ordering = ['Num']
## Tache
class Tache(models.Model):

    class state(models.IntegerChoices):
        Waiting = 1, 'Waiting'
        In_progress = 2, 'In progress'
        Finished = 3, 'Finished'
        Pass = 4, 'Pass'

    State = models.IntegerField(choices=state.choices, default=state.Waiting )
    Valide = models.BooleanField(default=False)
    Date_start = models.DateTimeField(null=True)
    Date_End = models.DateTimeField(null=True)
    Max_Duration = models.DurationField()
    Comment = models.TextField(blank=True)
    Problem = models.BooleanField(default=False)
    Tache_Def = models.ForeignKey("Tache_Def",on_delete=models.CASCADE,default=1)
    Etape = models.ForeignKey("Etape",on_delete=models.CASCADE,default=1)

    def can_start(self):

        dependencies = TacheDependency.objects.filter(current=self.Tache_Def)

        if not dependencies.exists():
            return True  # no dependencies, always start

        if self.Tache_Def.Start_after_all_Prev:
            has_finished_parent = False

            for dep in dependencies:
                prev_taches = Tache.objects.filter(
                    Etape=self.Etape,
                    Tache_Def=dep.previous
                )

                if not prev_taches.filter(State__in=[Tache.state.Finished, Tache.state.Pass]).exists():
                    return False

                if prev_taches.filter(State=Tache.state.Finished).exists():
                    has_finished_parent = True

            return has_finished_parent

        else:
            # Relaxed mode: only one parent Finished is enough
            for dep in dependencies:
                if Tache.objects.filter(
                    Etape=self.Etape,
                    Tache_Def=dep.previous,
                    State=Tache.state.Finished
                ).exists():
                    return True
            return False
    
    class Meta:
        ordering = ['Tache_Def__Num']   
class Tache_Def(models.Model):

    Num = models.SmallIntegerField(default=0)
    Name = models.CharField(max_length=100,blank=True)
    Description = models.TextField(blank=True)
    Note = models.TextField(blank=True,default="")
    Type = models.CharField(max_length=20,blank=True) ##### select type define for sys
    Duration = models.DurationField()
    Alert_Duration = models.DurationField()
    Alert_Start_after = models.FloatField(default=0.0)
    Duration_const = models.BooleanField(default=False)
    Must_validate = models.BooleanField(default=False)
    Start_after_all_Prev = models.BooleanField(default=True)
    Etape_Def = models.ForeignKey("Etape_Def",on_delete=models.CASCADE,default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        ordering = ['Etape_Def','Num']

class Tache_data(models.Model):

    Tache = models.ForeignKey("Tache",on_delete=models.CASCADE,default=1)
    Tache_data_Def = models.ForeignKey("Tache_data_Def",on_delete=models.CASCADE,default=1)
    Data_Project = models.ForeignKey("Data_Project",on_delete=models.CASCADE,default=1)

class Tache_data_Def(models.Model):

    class type(models.IntegerChoices):
        read = 1, 'read'
        write = 2, 'write'
        execute = 3, 'execute'
    Order = models.IntegerField(default=0)
    Type = models.IntegerField(choices=type.choices, default=type.read )
    Tache_Def = models.ForeignKey("Tache_Def",on_delete=models.CASCADE,default=1)
    Data_Project = models.ForeignKey("Def_data_Project",on_delete=models.CASCADE,default=1)
    class Meta:
        ordering = ['Order']
class Tache_To(models.Model):

    Tache_Def =  models.ForeignKey("Tache_Def",on_delete=models.CASCADE,default=1)
    Role =  models.ForeignKey("Role",on_delete=models.CASCADE,default=1)

class Tache_receve(models.Model):

    Tache_Def =  models.ForeignKey("Tache_Def",on_delete=models.CASCADE,default=1)
    Role =  models.ForeignKey("Role",on_delete=models.CASCADE,default=1)

class Tache_superviser(models.Model):

    Tache_Def =  models.ForeignKey("Tache_Def",on_delete=models.CASCADE,default=1)
    Role =  models.ForeignKey("Role",on_delete=models.CASCADE,default=1)

class TacheDependency(models.Model): # previous

    previous = models.ForeignKey("Tache_Def", on_delete=models.CASCADE, related_name='previous_dependencies')
    current = models.ForeignKey("Tache_Def", on_delete=models.CASCADE, related_name='current_dependencies')

class Problem(models.Model):

    Tache = models.ForeignKey("Tache", on_delete=models.CASCADE)
    User = models.ForeignKey("User", on_delete=models.CASCADE)
    Note_Problem  = models.TextField(blank=True)
    class state(models.IntegerChoices):
        Sloved = 1, 'Sloved'
        Not_Solved = 2, 'Not Solved'

    State = models.IntegerField(choices=state.choices, default=state.Not_Solved )
    class type(models.IntegerChoices):
        Banque = 1, 'Banque'
        Fournisseur = 2, 'Fournisseur'
        necessite_avenant = 3,"nécessite d'avenant"
        Autre = 4,'Autre'
    Type = models.IntegerField(choices=type.choices, default=type.Banque )
    Date = models.DateTimeField(null=True)

class Sous_Tache(models.Model):

    class state(models.IntegerChoices):
        Waiting = 1, 'Waiting'
        In_progress = 2, 'In progress'
        Finished = 3, 'Finished'

    State = models.IntegerField(choices=state.choices, default=state.Waiting )
    Valide = models.BooleanField(default=False)
    Date_Start = models.DateTimeField(null=True)
    Date_End =  models.DateTimeField(null=True)
    Sous_Tache_Def = models.ForeignKey("Sous_Tache_Def",on_delete=models.CASCADE,default=1)
    Tache =  models.ForeignKey("Tache",on_delete=models.CASCADE,default=1)
    class Meta:
        ordering = ['Sous_Tache_Def__Num']

class Sous_Tache_Def(models.Model):

    Num = models.SmallIntegerField(default=0)
    Name = models.CharField(max_length=100,blank=True)
    Duration = models.DurationField()
    Tache_Def =  models.ForeignKey("Tache_Def",on_delete=models.CASCADE,default=1)
    deleted = models.BooleanField(default=False)
    class Meta:
        ordering = ['Num']
# Groupe_Tache_Def
class Groupe_Tache_Def(models.Model):

    Groupe = models.ForeignKey("Groupe",on_delete=models.CASCADE,default=1)
    Tache_Def = models.ForeignKey("Tache_Def",on_delete=models.CASCADE,default=1)
    class Meta:
        ordering = ['id']    
## File

class File_Project(models.Model):

    Link = models.TextField(blank=True,default="")
    type = models.TextField(default="")
    Description = models.TextField(blank=True)
    Data_Project = models.ForeignKey("Data_project",on_delete=models.CASCADE,default=1)

## Reference (Domain)

class Reference(models.Model): 

    Ref = models.TextField(blank=True)
    class Meta:
        ordering = ['id']

class Reference_project(models.Model):

    reference = models.ForeignKey("reference",on_delete=models.CASCADE,default=1)
    project = models.ForeignKey("project",on_delete=models.CASCADE,default=1)

# Team
class Team_members(models.Model):

    User = models.ForeignKey("User",on_delete=models.CASCADE,default=1)
    Project = models.ForeignKey("Project",on_delete=models.CASCADE,default=1)
    Comment = models.TextField(blank=True)
    class Meta:
        ordering = ['User__username']
