from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    ####
    # civil
    Date_Naissance = models.DateField(null=True)
    Lieu_Naissance = models.CharField(max_length=255,default="",blank=True)
    sexe = models.CharField(max_length=10,default="",blank=True) # Homme Femme
    Adresse = models.CharField(max_length=200,default="",blank=True)
    Situation_familiale = models.CharField(max_length=100,default="",blank=True)
    Nom_epouse = models.CharField(max_length=200,default="",blank=True)
    Nombre_enfants = models.IntegerField(default=0, blank=True, null=True)
    # coordonnées
    PhoneNum = models.CharField(max_length=20,default="",blank=True)
    # Social
    N_RIB = models.CharField(max_length=100,default="",blank=True)
    avantages = models.CharField(max_length=200,default="",blank=True)
    # professionnel
    affectation = models.CharField(max_length=100,default="",blank=True)
    date_recrutement = models.DateField(null=True)
    date_start = models.DateField(null=True)
    Date_depart = models.DateField(null=True,blank=True)
    Motif_depart = models.CharField(max_length=100,default="",blank=True)
    Post = models.ForeignKey("Post",on_delete=models.SET_NULL,null=True)
    Service = models.ForeignKey("Service",on_delete=models.SET_NULL,null=True)
    # system 
    nbr_conge = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/User/',default="images/User/default.jpg", blank=True, null=True)
    Role = models.ForeignKey("Role",on_delete=models.SET_NULL,null=True)
    ####
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class work_Offer(models.Model):

    Title = models.CharField(max_length=100,default="",blank=True)
    Discription = models.CharField(max_length=200,default="",blank=True)
    Date = models.DateField(null=True)

class Formation(models.Model):

    Titre = models.CharField(max_length=100,default="",blank=True)
    place = models.CharField(max_length=100,default="",blank=True)
    date = models.DateField(null=True)
    duration = models.DurationField() # [DD] [HH:[MM:]]ss[.uuuuuu] use number input for days Time input for HH:MM:SS

class CV (models.Model):

    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    phone_num = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    link_CV = models.CharField(max_length=200, blank=True)
    CV_File = models.FileField(upload_to='documents/CV/')

class Post(models.Model):

    Name = models.CharField(max_length=100,blank=True,default="")
    abbreviation = models.CharField(max_length=100,blank=True,default="")
    degree =  models.CharField(max_length=100,blank=True,default="")

class History_Post(models.Model):

    Date_Start = models.DateField(null=True)
    Date_End = models.DateField(null=True)
    User = models.ForeignKey("User",on_delete=models.CASCADE,default=1)
    Service = models.ForeignKey("Post",on_delete=models.CASCADE,default=1)

class Demmanede_Conge(models.Model):

    Date = models.DateField(null=True)
    Date_Start = models.DateField(null=True)
    Duration = models.DurationField()
  
class Groupe(models.Model):

    Name = models.CharField(max_length=100,default="",blank=True)
    Abbreviation = models.CharField(max_length=50,default="",blank=True)
    Discription = models.CharField(max_length=200,default="",blank=True)

class User_Groupe(models.Model):

    Groupe = models.ForeignKey("Groupe",on_delete=models.CASCADE,default=1)
    User = models.ForeignKey("User",on_delete=models.CASCADE,default=1)
