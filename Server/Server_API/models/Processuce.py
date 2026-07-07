from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Processuce(models.Model):

    # system
    Date_start = models.DateTimeField(null=True)
    Date_End = models.DateTimeField(null=True)
    State = models.CharField(max_length=20,blank=True)
    Object = models.TextField(default="")
    Def_Processuce = models.ForeignKey("Def_Processuce",on_delete=models.CASCADE,default=1)

class Def_Processuce(models.Model):

    Name = models.CharField(max_length=100,blank=True) # Title
    Num = models.PositiveSmallIntegerField(default=0)
    Description = models.TextField(blank=True,default="")
    auto_delete = models.BooleanField(default=False)

class Tache_P(models.Model):

    State = models.CharField(max_length=20,blank=True,default="")
    Valide = models.BooleanField(default=False)
    Date_start = models.DateTimeField(null=True)
    Date_End = models.DateTimeField(null=True)
    Max_Duration = models.DurationField()
    Comment = models.TextField(blank=True)
    Tache_Def = models.ForeignKey("Tache_Def_P",on_delete=models.CASCADE,default=1)
    Processuce = models.ForeignKey("Processuce",on_delete=models.CASCADE,default=1)


class Tache_Def_P(models.Model):

    Num = models.SmallIntegerField(default=0)
    Name = models.CharField(max_length=100,blank=True)
    Description = models.TextField(blank=True)
    Type = models.CharField(max_length=20,blank=True) ##### select type define for sys // Validate , Forme , condition , template , Documented
    Def_Processuce = models.ForeignKey("Def_Processuce",on_delete=models.CASCADE,default=1)

class Tache_To_P(models.Model):

    Tache_Def =  models.ForeignKey("Tache_Def_P",on_delete=models.CASCADE,default=1)
    Role =  models.ForeignKey("Role",on_delete=models.CASCADE,default=1)

class Tache_receve_P(models.Model):

    Tache_Def =  models.ForeignKey("Tache_Def_P",on_delete=models.CASCADE,default=1)
    Role =  models.ForeignKey("Role",on_delete=models.CASCADE,default=1)

class TacheDependency_P(models.Model): # previous

    previous = models.ForeignKey("Tache_Def_P", on_delete=models.CASCADE, related_name='previous_dependencies_p')
    current = models.ForeignKey("Tache_Def_P", on_delete=models.CASCADE, related_name='current_dependencies_P')

class Tach_Data_P(models.Model):

    Value = models.TextField(default="")
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    Tache = models.ForeignKey("Tache_P",on_delete=models.CASCADE,default=1)
    Tach_Data_def = models.ForeignKey("Tach_Data_def_P",on_delete=models.CASCADE,default=1)

class Tach_Data_def_P(models.Model):
    
    class Type(models.IntegerChoices):
        Simple = 1, 'Simple'
        demande_conge = 2, 'demande_conge'
        User = 3, 'User'
        Project = 4, 'Project'
        Client = 5, 'Client'
        Fournisseur = 6, 'Fournisseur'
    Name = models.CharField(max_length=100,default="",blank=True)
    type = models.IntegerField(choices=Type.choices, default=Type.Simple)
    Type_Acces =  models.CharField(max_length=20,blank=True) ##### select type define for sys / add / update / show / delete
    Tache_Def =  models.ForeignKey("Tache_Def_P",on_delete=models.CASCADE,default=1)

class File_P (models.Model):

    File = models.FileField(upload_to='documents/Processuce/')
    type = models.CharField(max_length=10,default="")
    Description = models.TextField(blank=True)
    Tach_Data = models.ForeignKey("Tach_Data_P",on_delete=models.CASCADE,default=1)

class Template (models.Model):

    Name = models.CharField(max_length=100,default="",blank=True)
    File = models.FileField(upload_to='documents/templates/')
    Tache_Def = models.ForeignKey("Tache_Def_P",on_delete=models.CASCADE,default=1)