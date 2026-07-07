from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Role(models.Model):

    Name = models.CharField(max_length=50,default="")
    # .....
    Role = models.PositiveSmallIntegerField(default=0)
    Structure_Project = models.PositiveSmallIntegerField(default=0)
    User = models.PositiveSmallIntegerField(default=0)
    Service = models.PositiveSmallIntegerField(default=0)
    Client = models.PositiveSmallIntegerField(default=0)
    Fournisseur = models.PositiveSmallIntegerField(default=0)
    Project_Show = models.PositiveSmallIntegerField(default=0)
    Project_Add = models.PositiveSmallIntegerField(default=0)
    Project_1 = models.PositiveSmallIntegerField(default=0) # Soumission
    Project_2 = models.PositiveSmallIntegerField(default=0) # Affaire
    Project_3 = models.PositiveSmallIntegerField(default=0) # Projet en realisation
    Project_4 = models.PositiveSmallIntegerField(default=0) # Projet en cours de Garantie
    Project_5 = models.PositiveSmallIntegerField(default=0) # Projet Close
    Etape = models.PositiveSmallIntegerField(default=0)
    Processuce = models.PositiveSmallIntegerField(default=0)
    Files = models.PositiveSmallIntegerField(default=0)
    Team = models.PositiveSmallIntegerField(default=0)
    Refance = models.PositiveSmallIntegerField(default=0)
    Stat = models.PositiveSmallIntegerField(default=0)
    Historique = models.PositiveSmallIntegerField(default=0)

class Service(models.Model):

    Name = models.CharField(max_length=100,blank=True,default="")
    abbreviation = models.CharField(max_length=100,blank=True,default="")
    Chef_Service = models.ForeignKey("User", on_delete=models.SET_NULL,null=True)

class History(models.Model):
    Date = models.DateTimeField(auto_now_add=True)
    class Type(models.IntegerChoices):
        CREATE = 1, 'Created'
        UPDATE = 2, 'Updated'
        START = 3, 'Started'
        FINISHED = 4, 'Finished'
        VALIDATE = 5, 'Validated'
        ADD = 6, 'Added'
        DELETE = 7, 'Deleted'

    type = models.IntegerField(choices=Type.choices, default=Type.CREATE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class relation(models.IntegerChoices):
        Project = 1, 'Project'
        Etape = 2, 'Etape'
        Tache = 3, 'Tache'
        Team = 4, 'Team'
        File_Project = 5 ,'File_Project'
        Sous_Tache = 6 , 'Sous_Tache' 
    Relation = models.IntegerField(choices=relation.choices, default=relation.Project)
    User = models.ForeignKey("User", on_delete=models.CASCADE,default=1)

class Notification(models.Model):

    class relation(models.IntegerChoices):
        Project = 1, 'Project'
        Etape = 2, 'Etape'
        Tache = 3, 'Tache'
        Team = 4, 'Team'
        File_Project = 5 ,'File_Project'
        User = 6 , 'User' ,
        Processuce = 7 , 'Processuce' ,
        Tache_P = 8 , 'Tache_P' ,
    Relation = models.IntegerField(choices=relation.choices, default=relation.Project)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    Message  = models.TextField(blank=True, default="")
    Date_Time = models.DateTimeField(null=True,blank=True)


class Notification_to(models.Model):

    Notification = models.ForeignKey("Notification", on_delete=models.CASCADE,default=1)
    To = models.ForeignKey("User", on_delete=models.CASCADE,default=1)
    Opened = models.BooleanField(default=False)