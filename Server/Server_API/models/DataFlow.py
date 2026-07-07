from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ..models.System import Role
from ..models.User import User
from django.utils import timezone

PERMISSIONS = {
    'Commercial_View': [1, 2, 3, 4, 5, 7, 16],
    'Commercial_View3060':[6, 8, 9, 10, 13, 15],
    'Commercial_Update': [1, 2, 3, 4, 5, 7, 16],
    'Achat_View': [1, 4, 7, 8, 9, 10, 13, 15],
    'Achat_Update': [1, 7, 9, 10],
    'Finance_View': [1, 4, 6, 7, 8, 9, 10, 13, 15],
    'Finance_Update': [1, 6, 7, 9, 10],
    'Create': [1, 2, 4, 5, 7, 10, 16],
    'Supprime': [1, 4, 7, 10],
    'FileExeport': [1, 2, 3, 4, 5, 6, 7, 9, 10, 16],
}

class ProjectDF(models.Model):
    SITUATION_CHOICES = [
        ('Perdus / en previsionnele', 'Perdus / en previsionnele'),
        ('soumission', 'En Soumission'),
        ('short listé', 'Short listé'),
        ('attribue', 'Attribué'),
        ('Gagné', 'Gagné'),
        ('Affaire', 'Affaire'),
    ]
    
    WEIGHTING_CHOICES = [
        (0, '0%'),
        (1, '1%'),
        (10, '10%'),
        (30, '30%'),
        (60, '60%'),
        (100, '100%'),
    ]
    
    LOB_CHOICES = [
        (1, 'Data center'),
        (2, 'Network'),
        (3, 'Security'),
        (4, 'Build DC et cablings'),
        (5, 'Workspace / spare parts'),
        (6, 'Software (application)'),
    ]
    
    PAYMENT_MODE_CHOICES = [
        ('LC', 'LC'),
        ('TL', 'TL'),
        ('remdoc', 'Remdoc'),
    ]

    # Basic Information
    id = models.AutoField(primary_key=True)
    Created_At = models.DateTimeField(auto_now_add=True)
    situation_projet = models.CharField(max_length=25, choices=SITUATION_CHOICES, default='Perdus / en previsionnele', blank=True, null=True)
    comment = models.TextField(blank=True, null=True,default="")
    weightings_points = models.IntegerField(choices=WEIGHTING_CHOICES, default=0, blank=True, null=True)
    LOB = models.IntegerField(choices=LOB_CHOICES, blank=True, null=True,default=1)
    numero_appelle_doffre = models.TextField(unique=True, blank=True, null=True,default="")
    positionnement = models.BooleanField(default=False, blank=True, null=True)
    previsionnel = models.BooleanField(default=False, blank=True, null=True)
    secteur = models.TextField(blank=True, null=True,default="")
    client = models.TextField(blank=True, null=True,default="")
    objet = models.TextField(blank=True, null=True,default="")
    constructeur = models.TextField(blank=True, null=True,default="")
    fournisseur = models.TextField(blank=True, null=True,default="")

    # Dates and Durations
    delais_realisation = models.DurationField(blank=True, null=True)
    echeance = models.DateField(blank=True, null=True)
    previsions_commandes = models.DateField(blank=True, null=True)

    # Financial Information (Original Currency)
    montant_ht_marche = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    total_importation_equipement_usd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # USD
    total_importation_service_usd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # USD
    ps_usd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # USD
    taux_change = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    montant_travaux_realises = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    montant_travaux_restants = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    mt_achats = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    marges_brutes = models.FloatField(default=0.0, blank=True, null=True)  # DZD

    # Banking and Contract Information
    domiciliation_bancaire = models.TextField(blank=True, null=True,default="")
    nantissable = models.BooleanField(default=False, blank=True, null=True)
    montant_dzd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    date_ods = models.DateField(blank=True, null=True)
    delais_execution = models.DurationField(blank=True, null=True)
    taux_realisation_pourcentage = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    montant_facture_dzd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    montant_encaisse_dzd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    montant_travaux_factures_non_encaises_dzd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    montant_travaux_realises_non_factures_dzd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD
    reste_a_realiser_dzd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)], blank=True, null=True)  # DZD

    # Contract Information
    numero_contract = models.TextField(blank=True, null=True,default="")
    admin = models.TextField(blank=True, null=True,default="")
    date_cde = models.DateField(blank=True, null=True)
    date_po_contrat = models.DateField(blank=True, null=True)
    date_livraison_contractuelle = models.DateField(blank=True, null=True)

    _old_situation = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_situation = self.situation_projet

    def save(self, *args, user=None, **kwargs):
        if self.date_cde and self.delais_realisation:
            self.date_livraison_contractuelle = self.date_cde + self.delais_realisation

        is_update = self.pk is not None
        super().save(*args, **kwargs)

        if is_update and self.situation_projet != self._old_situation:
            self.create_status_change_notification(user)

        self._old_situation = self.situation_projet

    def create_status_change_notification(self, user=None):
        situation = self.situation_projet.lower().strip()
        roles_to_notify = set()

        if situation in ['soumission', 'short listé']:
            roles_to_notify.update(PERMISSIONS['Commercial_View'])
        elif situation in ['gagné', 'affaire','attribue']:
            roles_to_notify.update(PERMISSIONS['Commercial_View'])
            roles_to_notify.update(PERMISSIONS['Achat_View'])
            roles_to_notify.update(PERMISSIONS['Finance_View'])
        elif situation == 'perdus / en previsionnele':
            return

        if not roles_to_notify:
            return

        notif = NotificationDF.objects.create(
            project=self,
            Message=f"🔔 Changement statut : le projet {self.client} {self.numero_appelle_doffre} est {self.situation_projet}",
            Date_Time=timezone.now(),
        )

        users = User.objects.filter(Role__id__in=roles_to_notify)
        if user:
            users = users.exclude(id=user.id)

        for u in users:
            Notification_toDF.objects.create(
                Notification=notif,
                To=u,
                Opened=False
            )

    def __str__(self):
        return f"{self.numero_appelle_doffre} - {self.client}"

class ProjectAchatHardware(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('LC', 'LC'),
        ('TL', 'TL'),
        ('remdoc', 'Remdoc'),
    ]

    info_project = models.ForeignKey(ProjectDF, on_delete=models.CASCADE, related_name='achats_hardware')
    numero_po = models.TextField(blank=True,default="")
    date_prev_reception_stock = models.TextField(blank=True, null=True)
    volet = models.TextField(blank=True, null=True)
    fournisseur = models.TextField(blank=True,default="")  # Using Text for simplicity, can be changed to ForeignKey if you have a Supplier model
    mode_paiement = models.CharField(max_length=10, choices=MODE_PAIEMENT_CHOICES,default="LC")
    mt_devises_cmd_a = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    statut = models.TextField(blank=True, null=True)
    prevision_expidition = models.TextField(blank=True, null=True)
    prix_dzd = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    TauxDD = models.FloatField(default=0.0)
    dd = models.FloatField(default=0.0)
    tcs = models.FloatField(default=0.0)
    tva = models.FloatField(default=0.0)
    taxes = models.FloatField(default=0.0)

    def __str__(self):
        return f"Hardware PO: {self.numero_po} - {self.info_project.numero_appelle_doffre}"

class ProjectAchatSoftware(models.Model):
    info_project = models.ForeignKey(ProjectDF, on_delete=models.CASCADE, related_name='achats_software')
    numero_po = models.TextField(blank=True,default="")
    numero_facture_a = models.TextField(blank=True, null=True)
    fournisseur = models.TextField(blank=True,default="")
    statut = models.TextField(blank=True, null=True)
    date_depot_banque = models.DateField(blank=True, null=True)
    date_previsionnelle_reception_atf = models.DateField(blank=True, null=True)
    date_previsionnelle_transfert_fonds = models.DateField(blank=True, null=True)
    numero_facture = models.TextField(blank=True, null=True)
    mt_devises_brut = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    mt_ne = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    mt_total_brut_dz = models.FloatField(default=0.0)
    taux_taxe = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    mt_total_net_dza = models.FloatField(default=0.0)
    dom_bancaire_4percent = models.FloatField(default=0.0)
    ibs = models.FloatField(default=0.0)
    taxe = models.FloatField(default=0.0)
    dom_impot = models.FloatField(default=0.0)
    tva = models.FloatField(default=0.0)
    predom_bancaire = models.FloatField(default=0.0)
    dom_bancaire = models.FloatField(default=0.0)
    depot_dossier_dgi = models.FloatField(default=0.0)
    accord_dgi = models.FloatField(default=0.0)
    transfert_bancaire = models.FloatField(default=0.0)
    OBSERVATION = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Software PO: {self.numero_po} - {self.info_project.numero_appelle_doffre}"

class ProjectFinance(models.Model):
    info_project = models.ForeignKey(ProjectDF, on_delete=models.CASCADE, related_name='finances')
    num_facture_client = models.TextField(blank=True,default="")
    montent = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Finance: {self.num_facture_client} - {self.info_project.numero_appelle_doffre}"
   
class NotificationDF(models.Model):

    project = models.ForeignKey(ProjectDF, on_delete=models.SET_NULL, null=True, blank=True)
    Message  = models.TextField(blank=True, default="")
    Date_Time = models.DateTimeField(null=True,blank=True)

class Notification_toDF(models.Model):

    Notification = models.ForeignKey("NotificationDF", on_delete=models.CASCADE,default=1)
    To = models.ForeignKey("User", on_delete=models.CASCADE,default=1)
    Opened = models.BooleanField(default=False)