from django.db import models

## Client

class Client(models.Model):

    Name  = models.CharField(max_length=100,blank=True)
    Email = models.CharField(max_length=100,blank=True)
    image = models.ImageField(upload_to='images/Client/',default="images/Client/default.jpg", blank=True, null=True)

class Client_Contact(models.Model): #(Interlocutor)

    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    PhoneNum = models.CharField(max_length=20,default="",blank=True)
    Email = models.CharField(max_length=100,default="",blank=True)
    Titre = models.CharField(max_length=100,default="",blank=True)
    Client  = models.ForeignKey("Client",on_delete=models.CASCADE,default=1)

## Fourniseur

class Fourniseur(models.Model):

    Name  = models.CharField(max_length=100,blank=True)
    Email = models.CharField(max_length=100,blank=True)
    image = models.ImageField(upload_to='images/Fourniseur/',default="images/Fourniseur/default.jpg", blank=True, null=True)

class Fourniseur_Contact(models.Model): # (Interlocutor)

    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    PhoneNum = models.CharField(max_length=20,default="",blank=True)
    Email = models.CharField(max_length=100,default="",blank=True)
    Titre = models.CharField(max_length=100,default="",blank=True)
    Fourniseur  = models.ForeignKey("Fourniseur",on_delete=models.CASCADE,default=1)

class fournisseur_data(models.Model):

    Fourniseur  = models.ForeignKey("Fourniseur",on_delete=models.CASCADE,default=1)
    Data_Project  = models.ForeignKey("Data_Project",on_delete=models.CASCADE,default=1)

