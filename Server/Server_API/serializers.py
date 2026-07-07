from rest_framework import serializers
from .models import *

# User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 
                  'first_name', 'last_name', 'Date_Naissance',
                  'Lieu_Naissance', 'sexe', 'Adresse', 'Situation_familiale',
                  'Nom_epouse', 'Nombre_enfants', 'PhoneNum', 'N_RIB',
                  'avantages', 'affectation', 'date_recrutement',
                  'date_start', 'Date_depart', 'Motif_depart',
                  'Post', 'Service', 'nbr_conge', 'image', 'Role')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'username': {'required': False}
            }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            **{field: validated_data.get(field) for field in self.Meta.fields if field not in ['id', 'email', 'username', 'password']}
        )
        return user

    def validate_email(self, value):
        user = self.instance
        if user and user.email == value:
            return value
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        user = self.instance
        if user and user.username == value:
            return value
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class work_OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = work_Offer
        fields = '__all__'
class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'   
class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = '__all__'
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
class History_PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = History_Post
        fields = '__all__'
class Demmanede_CongeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demmanede_Conge
        fields = '__all__'
class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = '__all__'
class User_GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Groupe
        fields = '__all__'

# System

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
class PoseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoseProject
        fields = '__all__'

class Def_data_ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Def_data_Project
        fields = '__all__'
class Data_GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data_Groupe
        fields = '__all__'
class Data_ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data_Project
        fields = '__all__'
class Multy_data_projectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multy_data_project
        fields = '__all__'
class select_ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = select_Values
        fields = '__all__'
class Fill_MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fill_Message
        fields = '__all__'
class Table_strectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table_strecture
        fields = '__all__'
class Table_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table_data
        fields = '__all__'
class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
class Forme_MassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forme_Massage
        fields = '__all__'
class Form_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form_Data
        fields = '__all__'
class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etape
        fields = '__all__'
class Etape_defSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etape_def
        fields = '__all__'
class TacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = '__all__'
class Tache_DefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_Def
        fields = '__all__'
class Tache_DefSerializerP(serializers.ModelSerializer):
    Etape_Def = Etape_defSerializer()
    class Meta:
        model = Tache_Def
        fields = '__all__'
class Tache_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_data
        fields = '__all__'
class Tache_data_DefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_data_Def
        fields = '__all__'
class Tache_data_DefSerializerP(serializers.ModelSerializer):
    class Meta:
        model = Tache_data_Def
        fields = '__all__'
class Tache_ToSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_To
        fields = '__all__'
class Tache_receveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_receve
        fields = '__all__'
class Tache_superviserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_superviser
        fields = '__all__'
class TacheDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TacheDependency
        fields = '__all__'
class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
class Sous_TacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sous_Tache
        fields = '__all__'
class Sous_Tache_DefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sous_Tache_Def
        fields = '__all__'
class Groupe_Tache_DefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe_Tache_Def
        fields = '__all__'
class File_ProjectSerializer(serializers.ModelSerializer):
    def validate_File(self, value):
        if isinstance(value, str) and value.startswith('/documents/Project/'):
            return value
        return value

    def create(self, validated_data):
        return File_Project.objects.create(**validated_data)
    class Meta:
        model = File_Project
        fields = '__all__'
        extra_kwargs = {
            'File': {'required': False},
        }
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'
class Reference_projectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference_project
        fields = '__all__'
class Team_membersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team_members
        fields = '__all__'

# Processuce

class ProcessuceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processuce
        fields = '__all__'
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'
class Def_ProcessuceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Def_Processuce
        fields = '__all__'
class Tache_PSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_P
        fields = '__all__'
class Tache_Def_PSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_Def_P
        fields = '__all__'
class Tache_To_PSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_To_P
        fields = '__all__'
class Tache_receve_PSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache_receve_P
        fields = '__all__'
class Tach_Data_PSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tach_Data_P
        fields = '__all__'
class TacheDependency_PSerializer(serializers.ModelSerializer):
    class Meta:
        model = TacheDependency_P
        fields = '__all__'
class Tach_Data_def_PSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tach_Data_def_P
        fields = '__all__'
class File_PSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_P
        fields = '__all__'
class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'

# Extern

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
class Client_ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client_Contact
        fields = '__all__'
class FourniseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fourniseur
        fields = '__all__'
class Fourniseur_ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fourniseur_Contact
        fields = '__all__'
class fournisseur_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = fournisseur_data
        fields = '__all__'

##############  System ################
class RoleSerializermois(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id','Name')
# User mois 
class UserSerializerMois(serializers.ModelSerializer):

    Post=PostSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username','first_name', 'last_name','image','PhoneNum','Post')
# Grouop Plus
class User_GroupeSerializerPlus(serializers.ModelSerializer):
    User = UserSerializerMois()
    class Meta:
        model = User_Groupe
        fields = '__all__'
class GroupeSerializerPlus(serializers.ModelSerializer):

    Users = User_GroupeSerializerPlus(many=True, read_only=True, source='user_groupe_set')
    class Meta:
        model = Groupe
        fields = '__all__'
# Service Plus
class ServiceSerializerPlus(serializers.ModelSerializer):
    
    Chef_Service=UserSerializerMois()
    class Meta:
        model = Service
        fields = '__all__'
# User Plus 
class UserSerializerPlus(serializers.ModelSerializer):

    Role=RoleSerializer()
    Post=PostSerializer()
    Service=ServiceSerializerPlus()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 
                  'first_name', 'last_name','Date_Naissance'
                  ,'Lieu_Naissance','sexe','Adresse','Situation_familiale',
                  'Nom_epouse','Nombre_enfants','PhoneNum','N_RIB',
                  'avantages','affectation','date_recrutement',
                  'date_start','Date_depart','Motif_depart',
                  'Post','Service','nbr_conge','image','Role')
class UserSerializerPlusMois(serializers.ModelSerializer):

    Post=PostSerializer()
    Service=ServiceSerializerPlus()
    Role=RoleSerializermois()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username','first_name', 'last_name','image','PhoneNum','Post','Service','Role')
        
class UserWithProjectCountSerializer(UserSerializerPlusMois):
    project_count = serializers.IntegerField()

    class Meta(UserSerializerPlusMois.Meta):
        fields = UserSerializerPlusMois.Meta.fields + ('project_count',)
# Notification plus
class ProjectSerializerMoin(serializers.ModelSerializer):
    Client = ClientSerializer()

    class Meta:
        model = Project
        fields = ( 'id', 'Client', 'NumContract', 'Num_Appele_dOffer', 'Etape_S' )

class NotificationSerializerPlus(serializers.ModelSerializer):

    content_type = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = '__all__'

    def get_content_type(self, obj):
        if obj.content_type:
            return {
                #'id': obj.content_type.id,
                #'app_label': obj.content_type.app_label,
                'model': obj.content_type.model
            }
        return None
    
    def get_object_id(self, obj):
        if obj.object_id:
            content_type = obj.content_type.model_class()
            if content_type.objects.filter(id=obj.object_id).exists():
                if content_type == User:
                    serializer = UserSerializerMois(obj.content_object)
                elif content_type == Project:
                    serializer = ProjectSerializerMoin(obj.content_object)
                elif content_type == Processuce:
                    serializer = ProcessuceSerializer(obj.content_object)
                elif content_type == Team_members:
                    serializer = Team_membersSerializer(obj.content_object)
                elif content_type == Etape:
                    serializer = EtapeSerializerPlusMois2(obj.content_object)
                elif content_type == Tache:
                    serializer = TacheSerializerPlusMois(obj.content_object)
                elif content_type == File_Project:
                    serializer = File_ProjectSerializerPlusMois(obj.content_object)
                elif content_type == Tache_P:
                    serializer = Tache_PSerializer(obj.content_object)
                else:
                    return None
                return serializer.data
            else :
                return None
        return None

class Notification_toSerializer(serializers.ModelSerializer):
    Notification = NotificationSerializerPlus()
    class Meta:
        model = Notification_to
        fields = '__all__'
class Notification_toSerializerS(serializers.ModelSerializer):
    
    class Meta:
        model = Notification_to
        fields = '__all__'
# History 
class HistorySerializerPlus(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    relation_display = serializers.CharField(source='get_Relation_display', read_only=True)
    
    User = UserSerializerMois()

    class Meta:
        model = History
        fields = '__all__'
        extra_fields = ['type_display', 'relation_display']

##############  Project STR ################

# Tache Dependency Plus
class TacheDependencySerializerPlus(serializers.ModelSerializer):
    Tache_display = serializers.SerializerMethodField()
    previous = Tache_DefSerializer()
    
    class Meta:
        model = TacheDependency
        fields = '__all__'

    def get_Tache_display(self, obj):
        previous_tache = obj.previous
        current_tache = obj.current

        previous_display = f"{previous_tache.Etape_Def.Num}.{previous_tache.Num}"
        current_display = f"{current_tache.Etape_Def.Num}.{current_tache.Num}"

        return f"{previous_display}"
class Tache_ToSerializerPlus(serializers.ModelSerializer):

    Role = RoleSerializermois()

    class Meta:
        model = Tache_To
        fields = '__all__'
class Tache_receveSerializerPlus(serializers.ModelSerializer):

    Role = RoleSerializermois()

    class Meta:
        model = Tache_receve
        fields = '__all__'
class Tache_superviserSerializerPlus(serializers.ModelSerializer):

    Role = RoleSerializermois()

    class Meta:
        model = Tache_superviser
        fields = '__all__'
class Tache_data_DefSerializerPlus(serializers.ModelSerializer):

    Data_Project = Def_data_ProjectSerializer()

    class Meta:
        model = Tache_data_Def
        fields = '__all__'

# Groupe_Tache_Def Plus
class Groupe_Tache_DefSerializerPlus(serializers.ModelSerializer):
    Groupe = GroupeSerializer()
    class Meta:
        model = Groupe_Tache_Def
        fields = '__all__'

# Tache_Def_Plus
class Tache_DefSerializerPlus(serializers.ModelSerializer):

    sous_tache_defs = Sous_Tache_DefSerializer(many=True, read_only=True, source='sous_tache_def_set')
    tache_receve = Tache_receveSerializerPlus(many=True, read_only=True, source='tache_receve_set')
    tache_superviser = Tache_superviserSerializerPlus(many=True, read_only=True, source='tache_superviser_set')
    tache_dependency = TacheDependencySerializerPlus(many=True, read_only=True, source='current_dependencies')
    tache_data_Def = Tache_data_DefSerializerPlus(many=True, read_only=True, source='tache_data_def_set')
    tache_To = Tache_ToSerializerPlus(many=True, read_only=True, source='tache_to_set')
    groupe_tache = Groupe_Tache_DefSerializerPlus(many=True, read_only=True, source='groupe_tache_def_set')

    class Meta:
        model = Tache_Def
        fields = '__all__'

class Tache_DefSerializerPlusMoins(serializers.ModelSerializer):

    tache_receve = Tache_receveSerializerPlus(many=True, read_only=True, source='tache_receve_set')
    tache_superviser = Tache_superviserSerializerPlus(many=True, read_only=True, source='tache_superviser_set')
    tache_previous = TacheDependencySerializerPlus(many=True, read_only=True, source='current_dependencies')
    tache_next = TacheDependencySerializer(many=True, read_only=True, source='previous_dependencies')
    tache_To = Tache_ToSerializerPlus(many=True, read_only=True, source='tache_to_set')
    groupe_tache = Groupe_Tache_DefSerializerPlus(many=True, read_only=True, source='groupe_tache_def_set')

    class Meta:
        model = Tache_Def
        fields = '__all__'
# Etape Def Plus
class Etape_defSerializerPlus(serializers.ModelSerializer):
    
    tache_defs = Tache_DefSerializerPlus(many=True, read_only=True, source='tache_def_set')

    class Meta:
        model = Etape_def
        fields = '__all__'

# Data Def Plus

class Def_data_ProjectSerializerPlus(serializers.ModelSerializer):

    select_Values =select_ValuesSerializer(many=True, read_only=True, source='select_values_set')
    Fill_Message = Fill_MessageSerializer(many=True, read_only=True, source='fill_message_set')
    Table_strecture = Table_strectureSerializer(many=True, read_only=True, source='table_strecture_set')

    class Meta:
        model = Def_data_Project
        fields = '__all__'

# Form_DataSerializer Plus
class Form_DataSerializerPlus (serializers.ModelSerializer):

    Def_data_Project = Def_data_ProjectSerializer()

    class Meta:
        model = Form_Data
        fields = '__all__'

# Form Plus

class FormSerializerPlus(serializers.ModelSerializer):

    Forme_Massage = Forme_MassageSerializer(many=True, read_only=True, source='forme_massage_set')
    Form_Data = Form_DataSerializerPlus(many=True, read_only=True, source='form_data_set')

    class Meta:
        model = Form
        fields = '__all__'

######################  Processuce ############################
class TacheDependency_PSerializerPlus(serializers.ModelSerializer):

    previous = Tache_Def_PSerializer()

    class Meta:
        model = TacheDependency_P
        fields = '__all__'
class Tache_To_PSerializerPlus(serializers.ModelSerializer):

    Role = RoleSerializermois()

    class Meta:
        model = Tache_To_P
        fields = '__all__'
class Tache_receve_PSerializerPlus(serializers.ModelSerializer):

    Role = RoleSerializermois()

    class Meta:
        model = Tache_receve_P
        fields = '__all__'

class Tach_Data_def_PSerializerPlus(serializers.ModelSerializer):
    type_display = serializers.SerializerMethodField()

    class Meta:
        model = Tach_Data_def_P
        fields = '__all__'

    def get_type_display(self, obj):
        return obj.get_type_display()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type_display'] = instance.get_type_display()
        return representation
    
# Tache_Def_P_Plus
class Tache_Def_PSerializerPlus(serializers.ModelSerializer):

    Template = TemplateSerializer(many=True, read_only=True, source='template_set')
    tache_receve = Tache_receve_PSerializerPlus(many=True, read_only=True, source='tache_receve_p_set')
    tache_dependency = TacheDependency_PSerializerPlus(many=True, read_only=True, source='current_dependencies_P')
    tache_data_Def = Tach_Data_def_PSerializerPlus(many=True, read_only=True, source='tach_data_def_p_set')
    tache_To = Tache_To_PSerializerPlus(many=True, read_only=True, source='tache_to_p_set')

    class Meta:
        model = Tache_Def_P
        fields = '__all__'

# Etape Def Plus
class Def_ProcessuceSerializerPlus(serializers.ModelSerializer):
    
    tache_defs = Tache_Def_PSerializerPlus(many=True, read_only=True, source='tache_def_p_set')

    class Meta:
        model = Def_Processuce
        fields = '__all__'

################## Project #############################
# File Plus 
class Data_ProjectSerializerP(serializers.ModelSerializer):

    Def_data_Project = Def_data_ProjectSerializerPlus()

    class Meta:
        model = Data_Project
        fields = '__all__'
class File_ProjectSerializerP(serializers.ModelSerializer):
    Data_Project = Data_ProjectSerializerP()
    History = serializers.SerializerMethodField()
    class Meta:
        model = File_Project
        fields = '__all__'
        extra_kwargs = {
            'File': {'required': False},
        }
    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(File_Project),
                                            object_id=obj.id,
                                            Relation = History.relation.File_Project)
        return HistorySerializerPlus(history_qs, many=True).data
class File_ProjectSerializerPlus(serializers.ModelSerializer):
    History = serializers.SerializerMethodField()
    class Meta:
        model = File_Project
        fields = '__all__'
        extra_kwargs = {
            'File': {'required': False},
        }
    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(File_Project),
                                            object_id=obj.id,
                                            Relation = History.relation.File_Project)
        return HistorySerializerPlus(history_qs, many=True).data
class File_ProjectSerializerPlusMois(serializers.ModelSerializer):
    Data_Project = Data_ProjectSerializer()
    class Meta:
        model = File_Project
        fields = '__all__'
        extra_kwargs = {
            'File': {'required': False},
        }

# Client Plus
class ProjectSerializerPTeam(serializers.ModelSerializer):

    Team_members = Team_membersSerializer(many=True, read_only=True, source='team_members_set')

    class Meta:
        model = Project
        fields = '__all__'
class ClientSerializerPlus(serializers.ModelSerializer):
    Client_Contact = Client_ContactSerializer(many=True, read_only=True, source='client_contact_set')
    Project = ProjectSerializerPTeam(many=True, read_only=True, source='project_set')
    class Meta:
        model = Client
        fields = '__all__'
# Fourniseur Plus
class FourniseurSerializerPlus(serializers.ModelSerializer):

    Fourniseur_Contact = Fourniseur_ContactSerializer(many=True, read_only=True, source='fourniseur_contact_set')
    class Meta:
        model = Fourniseur
        fields = '__all__'
class fournisseur_dataSerializerPlus(serializers.ModelSerializer):

    Fourniseur = FourniseurSerializerPlus()
    class Meta:
        model = fournisseur_data
        fields = '__all__'
# reference Plus
class Reference_projectSerializerPlus(serializers.ModelSerializer):

    reference = ReferenceSerializer()
    
    class Meta:
        model = Reference_project
        fields = '__all__'

# Data_Project Plus 
class EtapeSerializerPlusMois(serializers.ModelSerializer):

    Etape_def = Etape_defSerializer()

    class Meta:
        model = Etape
        fields = '__all__'

class EtapeSerializerPlusMois2(serializers.ModelSerializer):

    Project_info = serializers.SerializerMethodField()

    def get_Project_info(self, obj):
        if obj.Project:
            return ProjectSerializerMoin(obj.Project).data
        return None
    Etape_def = Etape_defSerializer()

    class Meta:
        model = Etape
        fields = '__all__'
class Data_ProjectSerializerPlus(serializers.ModelSerializer):
    Def_data_Project = Def_data_ProjectSerializerPlus()
    Multy_data_project = Multy_data_projectSerializer(many=True, read_only=True, source='multy_data_project_set')
    File_Project = File_ProjectSerializerPlus(many=True, read_only=True, source='file_project_set')
    fournisseur_data = fournisseur_dataSerializerPlus(many=True, read_only=True, source='fournisseur_data_set')
    Table_data = Table_dataSerializer(many=True, read_only=True, source='table_data_set')
    Etape = serializers.SerializerMethodField()

    class Meta:
        model = Data_Project
        fields = '__all__'

    def get_Etape(self, obj):
        if not obj.Def_data_Project or not obj.Def_data_Project.Etape_def:
            return None 
        
        if not obj.Def_data_Project.Etape_def.Loop:
            return None  

        tache_data = Tache_data.objects.filter(Data_Project=obj)
        etape = Etape.objects.filter(tache__in=tache_data.values_list('Tache', flat=True)).first()

        if etape:
            return EtapeSerializerPlusMois(etape).data
        
        return None

# Problem Plus 
class ProblemSerializerPlus(serializers.ModelSerializer):

    User = UserSerializerMois()
    type_display = serializers.CharField(source='get_Type_display', read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'
        extra_fields = ['type_display']
# Sous_Tache Plus
class Sous_TacheSerializerPlus(serializers.ModelSerializer):

    Sous_Tache_Def = Sous_Tache_DefSerializer()
    History = serializers.SerializerMethodField()
    class Meta:
        model = Sous_Tache
        fields = '__all__'
    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(Sous_Tache),
                                            object_id=obj.id,
                                            Relation = History.relation.Sous_Tache)
        return HistorySerializerPlus(history_qs, many=True).data
    
# Tache data plus
class Tache_dataSerializerPlus(serializers.ModelSerializer):
    
    Tache_data_Def = Tache_data_DefSerializer()
    Data_Project = Data_ProjectSerializerPlus()

    class Meta:
        model = Tache_data
        fields = '__all__'

# Tache Plus  
class EtapeSerializerPPlusMois(serializers.ModelSerializer):

    Etape_def = Etape_defSerializer()
    Taches = serializers.SerializerMethodField()
    History = serializers.SerializerMethodField()

    class Meta:
        model = Etape
        fields = '__all__'
    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(Etape),
                                            object_id=obj.id,
                                            Relation = History.relation.Etape)
        return HistorySerializerPlus(history_qs, many=True).data
    def get_Taches(self, obj):
        return []
class TacheSerializerPlus(serializers.ModelSerializer):
    
    Tache_Def = Tache_DefSerializerPlusMoins()
    Tache_data = serializers.SerializerMethodField() # Tache_dataSerializerPlus(many=True, read_only=True, source='tache_data_set')
    Sous_Tache = serializers.SerializerMethodField() # Sous_TacheSerializerPlus(many=True, read_only=True, source='sous_tache_set')
    History = serializers.SerializerMethodField()
    Problems = ProblemSerializerPlus(many=True, read_only=True, source='problem_set')

    class Meta:
        model = Tache
        fields = '__all__'
    
    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(Tache),
                                            object_id=obj.id,
                                            Relation = History.relation.Tache)
        return HistorySerializerPlus(history_qs, many=True).data
    def get_Tache_data(self, obj):
        return []
    def get_Sous_Tache(self, obj):
        return []
class TacheSerializerPlusPlus(serializers.ModelSerializer):
    
    Tache_Def = Tache_DefSerializerPlusMoins()
    Tache_data = Tache_dataSerializerPlus(many=True, read_only=True, source='tache_data_set')
    Problems = ProblemSerializerPlus(many=True, read_only=True, source='problem_set')
    Sous_Tache = Sous_TacheSerializerPlus(many=True, read_only=True, source='sous_tache_set')
    History = serializers.SerializerMethodField()

    class Meta:
        model = Tache
        fields = '__all__'
    
    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(Tache),
                                            object_id=obj.id,
                                            Relation = History.relation.Tache)
        return HistorySerializerPlus(history_qs, many=True).data

class TacheSerializerPlusMois(serializers.ModelSerializer):
    
    Tache_Def = Tache_DefSerializerPlusMoins()
    Etape = EtapeSerializerPlusMois2()
    class Meta:
        model = Tache
        fields = '__all__'

# Team_members Plus 
class Team_membersSerializerPlus(serializers.ModelSerializer):

    User = UserSerializerMois()
    History = serializers.SerializerMethodField()
    
    class Meta:
        model = Team_members
        fields = '__all__'
    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(Team_members),
                                            object_id=obj.id,
                                            Relation = History.relation.Team)
        return HistorySerializerPlus(history_qs, many=True).data

# Etape Plus  
class EtapeSerializerPlus(serializers.ModelSerializer):

    Etape_def = Etape_defSerializer()
    Taches = TacheSerializerPlus(many=True, read_only=True, source='tache_set')
    History = serializers.SerializerMethodField()

    class Meta:
        model = Etape
        fields = '__all__'

    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(Etape),
                                            object_id=obj.id,
                                            Relation = History.relation.Etape)
        return HistorySerializerPlus(history_qs, many=True).data

class ProjectSerializerPlus(serializers.ModelSerializer):

    References = Reference_projectSerializerPlus(many=True, read_only=True, source='reference_project_set')
    Team_members = Team_membersSerializerPlus(many=True, read_only=True, source='team_members_set')
    Client = ClientSerializer()
    Status_display = serializers.CharField(source='get_Status_display', read_only=True)
    State_display = serializers.CharField(source='get_State_display', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectSituationSerializer(serializers.ModelSerializer):
    References = Reference_projectSerializerPlus(many=True, read_only=True, source='reference_project_set')
    Team_members = Team_membersSerializerPlus(many=True, read_only=True, source='team_members_set')
    Client = ClientSerializer()
    Status_display = serializers.CharField(source='get_Status_display', read_only=True)
    State_display = serializers.CharField(source='get_State_display', read_only=True)

    # === new fields ===
    Last_Tache = serializers.SerializerMethodField()
    Problems = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_Last_Tache(self, obj):
        # Try: In progress
        last_tache = (
            Tache.objects
            .filter(Etape__Project=obj, State=Tache.state.In_progress)
            .select_related('Tache_Def')
            .order_by('-Tache_Def__Num')
            .first()
        )

        # If none found → Finished
        if not last_tache:
            last_tache = (
                Tache.objects
                .filter(Etape__Project=obj, State=Tache.state.Finished)
                .select_related('Tache_Def')
                .order_by('-Tache_Def__Num')
                .first()
            )

        # If still none → Waiting
        if not last_tache:
            last_tache = (
                Tache.objects
                .filter(Etape__Project=obj, State=Tache.state.Waiting)
                .select_related('Tache_Def')
                .order_by('-Tache_Def__Num')
                .first()
            )

        return TacheSerializerPlusMois(last_tache).data if last_tache else None

    def get_Problems(self, obj):
        problems = (
            Problem.objects
            .filter(Tache__Etape__Project=obj)
            .select_related('User', 'Tache')
            .order_by('State', 'Date')
        )

        problems = sorted(
            problems,
            key=lambda p: (p.State != Problem.state.Not_Solved, p.Date or 0)
        )

        return ProblemSerializerHome(problems, many=True).data

class ProjectSerializerPlusPlus(serializers.ModelSerializer):
    
    References = Reference_projectSerializerPlus(many=True, read_only=True, source='reference_project_set')
    Data_Projects = serializers.SerializerMethodField() # Data_ProjectSerializerPlus(many=True, read_only=True, source='data_project_set')
    Etape = EtapeSerializerPPlusMois(many=True, read_only=True, source='etape_set')
    Team_members = Team_membersSerializerPlus(many=True, read_only=True, source='team_members_set')
    Client = ClientSerializerPlus()
    History = serializers.SerializerMethodField()
    PoseProject = PoseProjectSerializer(many=True, read_only=True, source='poseproject_set')
    Status_display = serializers.CharField(source='get_Status_display', read_only=True)
    Etape_S_display = serializers.CharField(source='get_Etape_S_display', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    def get_History(self, obj):
        history_qs = History.objects.filter(content_type=ContentType.objects.get_for_model(Project),
                                            object_id=obj.id,
                                            Relation = History.relation.Project)
        return HistorySerializerPlus(history_qs, many=True).data
    def get_Data_Projects(self, obj):
        return []

class ProjectSerializerHome(serializers.ModelSerializer):
    Client = ClientSerializer()
    PredictedProgress = serializers.SerializerMethodField()
    RealProgress = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ( 'id',  'Client', 'NumContract', 'Num_Appele_dOffer', 'Etape_S', 'PredictedProgress', 'RealProgress', )

    def get_PredictedProgress(self, obj):
        return obj.get_predicted_progress()

    def get_RealProgress(self, obj):
        return obj.get_real_progress()
    
# Home
class ProblemSerializerHome(serializers.ModelSerializer):

    User = UserSerializerMois()
    Tache = TacheSerializerPlusMois()
    type_display = serializers.CharField(source='get_Type_display', read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'
        extra_fields = ['type_display']


# DataFlow

class ProjectDFSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectDF
        fields = '__all__'
        read_only_fields = ('date_livraison_contractuelle',)

class ProjectAchatHardwareSerializer(serializers.ModelSerializer):
    info_project_name = serializers.CharField(source='info_project.numero_appelle_doffre', read_only=True)
    
    class Meta:
        model = ProjectAchatHardware
        fields = '__all__'

class ProjectAchatSoftwareSerializer(serializers.ModelSerializer):
    info_project_name = serializers.CharField(source='info_project.numero_appelle_doffre', read_only=True)
    
    class Meta:
        model = ProjectAchatSoftware
        fields = '__all__'

class ProjectFinanceSerializer(serializers.ModelSerializer):
    info_project_name = serializers.CharField(source='info_project.numero_appelle_doffre', read_only=True)
    
    class Meta:
        model = ProjectFinance
        fields = '__all__'

# Nested serializers for detailed views
class ProjectFinanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFinance
        fields = '__all__'

class ProjectAchatHardwareListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAchatHardware
        fields = '__all__'

class ProjectAchatSoftwareListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAchatSoftware
        fields = '__all__'

class ProjectDFDetailSerializer(serializers.ModelSerializer):
    achats_hardware = ProjectAchatHardwareListSerializer(many=True, read_only=True)
    achats_software = ProjectAchatSoftwareListSerializer(many=True, read_only=True)
    finances = ProjectFinanceListSerializer(many=True, read_only=True)
    LOB_display = serializers.CharField(source='get_LOB_display', read_only=True)
    
    class Meta:
        model = ProjectDF
        fields = '__all__'

class ProjectDFDetailSerializerMoin(serializers.ModelSerializer):

    class Meta:
        model = ProjectDF
        fields = ('id', 'numero_appelle_doffre', 'client')

class NotificationDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationDF
        fields = '__all__'


class Notification_toDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification_toDF
        fields = '__all__'

class NotificationDFSerializerPlus(serializers.ModelSerializer):

    project = ProjectDFDetailSerializerMoin(read_only=True)
    class Meta:
        model = NotificationDF
        fields = '__all__'

class NotificationToDFSerializerPlus(serializers.ModelSerializer):
    Notification = NotificationDFSerializerPlus(read_only=True)

    class Meta:
        model = Notification_toDF
        fields = ['id', 'Notification', 'Opened']