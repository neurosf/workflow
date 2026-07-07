from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView,)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projectsDF', ProjectDFViewSet, basename='projectdf')
router.register(r'hardware-purchases', ProjectAchatHardwareViewSet, basename='hardware-purchase')
router.register(r'software-purchases', ProjectAchatSoftwareViewSet, basename='software-purchase')
router.register(r'project-finances', ProjectFinanceViewSet, basename='project-finance')

urlpatterns = [
    # User
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail_admin'),
    path('user/', UserListAPIViewPM.as_view(), name='user_detail_admin'),
    path('userAll/', UserListAPIViewM.as_view(), name='user_detail_admin'),
    path('userU/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('Employes/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    # work_Offer
    #path('work_Offer/', work_OfferListCreateView.as_view(), name='work_Offer-list-create'), # not used
    #path('work_Offer/<int:pk>/', work_OfferRetrieveUpdateDeleteView.as_view(), name='work_Offer-retrieve-update-delete'), # not used
    # Formation
    #path('Formation/', FormationListCreateView.as_view(), name='Formation-list-create'), # not used
    #path('Formation/<int:pk>/', FormationRetrieveUpdateDeleteView.as_view(), name='Formation-retrieve-update-delete'), # not used
    # CV
    #path('CV/', CVListCreateView.as_view(), name='CV-list-create'), # not used
    #path('CV/<int:pk>/', CVRetrieveUpdateDeleteView.as_view(), name='CV-retrieve-update-delete'), # not used
    # Post
    path('Post/', PostListCreateView.as_view(), name='Post-list-create'),
    path('Post/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='Post-retrieve-update-delete'),
    # History_Post
    path('History_Post/', History_PostListCreateView.as_view(), name='History_Post-list-create'),
    path('History_Post/<int:pk>/', History_PostRetrieveUpdateDeleteView.as_view(), name='History_Post-retrieve-update-delete'),
    # Demmanede_Conge
    path('Demmanede_Conge/', Demmanede_CongeListCreateView.as_view(), name='Demmanede_Conge-list-create'),
    path('Demmanede_Conge/<int:pk>/', Demmanede_CongeRetrieveUpdateDeleteView.as_view(), name='Demmanede_Conge-retrieve-update-delete'),
    # Groupe
    path('Groupe/', GroupeListCreateView.as_view(), name='Groupe-list-create'),
    path('GroupeGET/', GroupeListView.as_view(), name='Groupe-list-create'),
    path('Groupe/<int:pk>/', GroupeRetrieveUpdateDeleteView.as_view(), name='Groupe-retrieve-update-delete'),
    # Groupe_Tache_Def
    path('Groupe_Tache_Def/', Groupe_Tache_DefCreateView.as_view(), name='Groupe_Tache_Def-create'),
    path('Groupe_Tache_DefGET/', Groupe_Tache_DefListView.as_view(), name='Groupe_Tache_Def-list'),
    path('Groupe_Tache_Def/<int:pk>/', Groupe_Tache_DefRetrieveUpdateDeleteView.as_view(), name='Groupe_Tache_Def-retrieve-update-delete'),
    # User_Groupe
    path('User_Groupe/', User_GroupeListCreateView.as_view(), name='User_Groupe-list-create'),
    path('User_Groupe/<int:pk>/', User_GroupeRetrieveUpdateDeleteView.as_view(), name='User_Groupe-retrieve-update-delete'),
    # Role
    path('Role/', RoleListView.as_view(), name='Role-list-create'),
    path('Roleadd/', RoleCreateView.as_view(), name='Role-list-create'),
    path('Role/<int:pk>/', RoleRetrieveUpdateDeleteView.as_view(), name='Role-retrieve-update-delete'),
    # Service
    path('Service/', ServiceListView.as_view(), name='Service-list-create'),
    path('ServiceAdd/', ServiceCreateView.as_view(), name='Service-list-create'),
    path('Service/<int:pk>/', ServiceRetrieveUpdateDeleteView.as_view(), name='Service-retrieve-update-delete'),
    # Notification
    path('Notification/', NotificationListView.as_view(), name='Notification-list-create'),
    path('Notification/<int:pk>/', NotificationRetrieveUpdateDeleteView.as_view(), name='Notification-list-create'),
    # Project
    path('Project/', ProjectListView.as_view(), name='Project-list1-'),
    path('ProjectSituation/', ProjectSituationListView.as_view(), name='Project-list1-'),
    path('ProjectThis/<int:pk>/', ProjectRetrieve.as_view(), name='Project-retrieve-'),
    path('ProjectCreate/', ProjectAPIPOST.as_view(), name='Project-'),
    path('ProjectPUT/', ProjectAPIPUT.as_view(), name='Project-'),
    path('Project/<int:pk>/', ProjectRetrieveUpdateDeleteView.as_view(), name='Project-retrieve-update-delete'),
    # Def_data_Project
    path('Def_data_Project/', Def_data_ProjectListView.as_view(), name='Def_data_Project-list'),
    path('Def_data_Projectadd/', Def_data_ProjectCreateView.as_view(), name='Def_data_Project-create'),
    path('Def_data_Project/<int:pk>/', Def_data_ProjectRetrieveUpdateDeleteView.as_view(), name='Def_data_Project-retrieve-update-delete'),
    # Data_Groupe
    path('Data_GroupeGet/', Data_GroupeListView.as_view(), name='Data_Groupe-list-'),
    path('Data_Groupe/', Data_GroupeListCreateView.as_view(), name='Data_Groupe-list-create'),
    path('Data_Groupe/<int:pk>/', Data_GroupeRetrieveUpdateDeleteView.as_view(), name='Data_Groupe-retrieve-update-delete'),
    # PoseProject
    path('Pose_Project/', PoseProjectListCreateView.as_view(), name='PoseProject-list-create'),
    path('Pose_Project/<int:pk>/', PoseProjectRetrieveUpdateDeleteView.as_view(), name='PoseProject-retrieve-update-delete'),
    # Data_Project
    path('Data_Project/', Data_ProjectListCreateView.as_view(), name='Data_Project-list-create'),
    path('Data_Project/<int:pk>/', Data_ProjectRetrieveUpdateDeleteView.as_view(), name='Data_Project-retrieve-update-delete'),
    # Multy_data_project 
    path('Multy_data_project/', Multy_data_projectListCreateView.as_view(), name='Multy_data_project-list-create'),
    path('Multy_data_project/<int:pk>/', Multy_data_projectRetrieveUpdateDeleteView.as_view(), name='Multy_data_project-retrieve-update-delete'),
    path('Create_Fill_Mul/<int:Num>/<int:Data_Project>/', multy_data_project.as_view(), name='Multy_data_project-'),
    # Table_data 
    path('Table_data/', Table_dataListCreateView.as_view(), name='Table_data-list-create'),
    path('Table_data/<int:pk>/', Table_dataRetrieveUpdateDeleteView.as_view(), name='Table_data-retrieve-update-delete'),
    path('Table_data_Change/', UpdateTableDataView.as_view(), name='Table_data-retrieve-update-delete'),
    # select_Values
    path('select_Values/', select_ValuesListCreateView.as_view(), name='select_Values-list-create'),
    path('select_Values/<int:pk>/', select_ValuesRetrieveUpdateDeleteView.as_view(), name='select_Values-retrieve-update-delete'),
    # Fill_Message
    path('Fill_Message/', Fill_MessageListCreateView.as_view(), name='Fill_Message-list-create'),
    path('Fill_Message/<int:pk>/', Fill_MessageRetrieveUpdateDeleteView.as_view(), name='Fill_Message-retrieve-update-delete'),
    # Table_strecture
    path('Table_strecture/', Table_strectureListCreateView.as_view(), name='Table_strecture-list-create'),
    path('Table_strecture/<int:pk>/', Table_strectureRetrieveUpdateDeleteView.as_view(), name='Table_strecture-retrieve-update-delete'),
    # Form
    path('Form/', FormListView.as_view(), name='Form-list'),
    path('Formadd/', FormCreateView.as_view(), name='Form-create'),
    path('Form/<int:pk>/', FormRetrieveUpdateDeleteView.as_view(), name='Form-retrieve-update-delete'),
    # Form_Data 
    path('Form_Data/', Form_DataListCreateView.as_view(), name='Form_Data-list-create'),
    path('Form_Data/<int:pk>/', Form_DataRetrieveUpdateDeleteView.as_view(), name='Form_Data-retrieve-update-delete'),
    # Form Message
    path('Form_Message/<int:form_id>/', FormMessageView.as_view(), name='form-messages'),
    # Etape
    path('Etape/', EtapeListCreateView.as_view(), name='Etape-list-create'),
    path('Etapeget/<int:pk>/', EtapeRetrieveView.as_view(), name='Etape-Retrieve'),
    path('Etape/<int:pk>/', EtapeRetrieveUpdateDeleteView.as_view(), name='Etape-retrieve-update-delete'),
    # Etape_def
    path('Etape_defMin/', Etape_defListMinView.as_view(), name='Etape_def-listMin'),
    path('Etape_def/', Etape_defListView.as_view(), name='Etape_def-list'),
    path('Etape_defadd/', Etape_defCreateView.as_view(), name='Etape_def-create'),
    path('Etape_def/<int:pk>/', Etape_defRetrieveUpdateDeleteView.as_view(), name='Etape_def-retrieve-update-delete'),
    # Tache
    path('Tache/', TacheListCreateView.as_view(), name='Tache-list-create'),
    path('UpdateTache/', TacheApi.as_view(), name='Tache-list-create'),
    path('UpdateData_Project/', Data_ProjectApi.as_view(), name='Tache-list-create'),
    path('Tache/<int:pk>/', TacheRetrieveUpdateDeleteView.as_view(), name='Tache-retrieve-update-delete'),
    path('projects/<int:pk>/sync/', SyncProjectAPIView.as_view(), name='sync-project'),
    # Tache_Def
    path('Tache_DefGet/', Tache_DefListView.as_view(), name='Tache_Def-list-create'),
    path('Tache_Def/', Tache_DefListCreateView.as_view(), name='Tache_Def-list-create'),
    path('Tache_Def/<int:pk>/', Tache_DefRetrieveUpdateDeleteView.as_view(), name='Tache_Def-retrieve-update-delete'),
    # Tache_data
    path('Tache_data/', Tache_dataListCreateView.as_view(), name='Tache_data-list-create'),
    path('Tache_data/<int:pk>/', Tache_dataRetrieveUpdateDeleteView.as_view(), name='Tache_data-retrieve-update-delete'),
    # Tache_data_Def
    path('Tache_data_Def/', Tache_data_DefListCreateView.as_view(), name='Tache_data_Def-list-create'),
    path('Tache_data_Def/<int:pk>/', Tache_data_DefRetrieveUpdateDeleteView.as_view(), name='Tache_data_Def-retrieve-update-delete'),
    # Tache_To
    path('Tache_To/', Tache_ToListCreateView.as_view(), name='Tache_To-list-create'),
    path('Tache_To/<int:pk>/', Tache_ToRetrieveUpdateDeleteView.as_view(), name='Tache_To-retrieve-update-delete'),
    # Tache_receve
    path('Tache_receve/', Tache_receveListCreateView.as_view(), name='Tache_receve-list-create'),
    path('Tache_receve/<int:pk>/', Tache_receveRetrieveUpdateDeleteView.as_view(), name='Tache_receve-retrieve-update-delete'),
    # Tache_superviser
    path('Tache_superviser/', Tache_superviserListCreateView.as_view(), name='Tache_superviser-list-create'),
    path('Tache_superviser/<int:pk>/', Tache_superviserRetrieveUpdateDeleteView.as_view(), name='Tache_superviser-retrieve-update-delete'),
    # TacheDependency
    path('TacheDependency/', TacheDependencyListCreateView.as_view(), name='TacheDependency-list-create'),
    path('TacheDependency/<int:pk>/', TacheDependencyRetrieveUpdateDeleteView.as_view(), name='TacheDependency-retrieve-update-delete'),
    # Problem
    path('Problem/', ProblemListCreateView.as_view(), name='Problem-list-create'),
    path('Problem/<int:pk>/', ProblemRetrieveUpdateDeleteView.as_view(), name='Problem-retrieve-update-delete'),
    # Sous_Tache
    path('Sous_Tache/', Sous_TacheListCreateView.as_view(), name='Sous_Tache-list-create'),
    path('Sous_Tache/<int:pk>/', Sous_TacheRetrieveUpdateDeleteView.as_view(), name='Sous_Tache-retrieve-update-delete'),
    # Sous_Tache_Def
    path('Sous_Tache_Def/', Sous_Tache_DefListCreateView.as_view(), name='Sous_Tache_Def-list-create'),
    path('Sous_Tache_Def/<int:pk>/', Sous_Tache_DefRetrieveUpdateDeleteView.as_view(), name='Sous_Tache_Def-retrieve-update-delete'),
    # File_Project 
    path('File_ProjectView/', File_ProjectListView.as_view(), name='File_Project-list-'),
    path('File_Project/', File_ProjectListCreateView.as_view(), name='File_Project-list-create'),
    path('File_Project/<int:pk>/', File_ProjectRetrieveUpdateDeleteView.as_view(), name='File_Project-retrieve-update-delete'),
    # Reference
    path('Reference/', ReferenceListCreateView.as_view(), name='Reference-list-create'),
    path('ReferenceList/', ReferenceListView.as_view(), name='Reference-list-create'),
    path('Reference/<int:pk>/', ReferenceRetrieveUpdateDeleteView.as_view(), name='Reference-retrieve-update-delete'),
    # Reference_project
    path('Reference_project/', Reference_projectListCreateView.as_view(), name='Reference_project-list-create'),
    path('Reference_project/<int:pk>/', Reference_projectRetrieveUpdateDeleteView.as_view(), name='Reference_project-retrieve-update-delete'),
    # Team_members
    path('Team_members/', Team_membersListCreateView.as_view(), name='Team_members-list-create'),
    path('Team_members/<int:pk>/', Team_membersRetrieveUpdateDeleteView.as_view(), name='Team_members-retrieve-update-delete'),
    # Processuce
    path('Processuce/', ProcessuceListCreateView.as_view(), name='Processuce-list-create'),
    path('Processuce/<int:pk>/', ProcessuceRetrieveUpdateDeleteView.as_view(), name='Processuce-retrieve-update-delete'),
    # Def_Processuce
    path('Def_Processuce/', Def_ProcessuceListView.as_view(), name='Def_Processuce-list'),
    path('Def_Processuceadd/', Def_ProcessuceCreateView.as_view(), name='Def_Processuce-create'),
    path('Def_Processuce/<int:pk>/', Def_ProcessuceRetrieveUpdateDeleteView.as_view(), name='Def_Processuce-retrieve-update-delete'),
    # Tache_P
    path('Tache_P/', Tache_PListCreateView.as_view(), name='Tache_P-list-create'),
    path('Tache_P/<int:pk>/', Tache_PRetrieveUpdateDeleteView.as_view(), name='Tache_P-retrieve-update-delete'),
    # Tache_Def_P
    path('Tache_Def_P/', Tache_Def_PListView.as_view(), name='Tache_Def_P-list'),
    path('Tache_Def_Padd/', Tache_Def_PCreateView.as_view(), name='Tache_Def_P-create'),
    path('Tache_Def_P/<int:pk>/', Tache_Def_PRetrieveUpdateDeleteView.as_view(), name='Tache_Def_P-retrieve-update-delete'),
    # Tache_To_P
    path('Tache_To_P/', Tache_To_PListCreateView.as_view(), name='Tache_To_P-list-create'),
    path('Tache_To_P/<int:pk>/', Tache_To_PRetrieveUpdateDeleteView.as_view(), name='Tache_To_P-retrieve-update-delete'),
    # Tache_receve_P
    path('Tache_receve_P/', Tache_receve_PListCreateView.as_view(), name='Tache_receve_P-list-create'),
    path('Tache_receve_P/<int:pk>/', Tache_receve_PRetrieveUpdateDeleteView.as_view(), name='Tache_receve_P-retrieve-update-delete'),
    # TacheDependency_P
    path('TacheDependency_P/', TacheDependency_PListCreateView.as_view(), name='TacheDependency_P-list-create'),
    path('TacheDependency_P/<int:pk>/', TacheDependency_PRetrieveUpdateDeleteView.as_view(), name='TacheDependency_P-retrieve-update-delete'),
    # Tach_Data_P
    path('Tach_Data_P/', Tach_Data_PListCreateView.as_view(), name='Tach_Data_P-list-create'),
    path('Tach_Data_P/<int:pk>/', Tach_Data_PRetrieveUpdateDeleteView.as_view(), name='Tach_Data_P-retrieve-update-delete'),
    # Tach_Data_def_P
    path('Tach_Data_def_P/', Tach_Data_def_PListCreateView.as_view(), name='Tach_Data_def_P-list-create'),
    path('Tach_Data_def_P/<int:pk>/', Tach_Data_def_PRetrieveUpdateDeleteView.as_view(), name='Tach_Data_def_P-retrieve-update-delete'),
    # File_P
    path('File_P/', File_PListCreateView.as_view(), name='File_P-list-create'),
    path('File_P/<int:pk>/', File_PRetrieveUpdateDeleteView.as_view(), name='File_P-retrieve-update-delete'),
    # Template
    path('Template/', TemplateListCreateView.as_view(), name='Template-list-create'),
    path('Template/<int:pk>/', TemplateRetrieveUpdateDeleteView.as_view(), name='Template-retrieve-update-delete'),
    # Client
    path('Client/', ClientListView.as_view(), name='Client-list-'),
    path('Clientadd/', ClientCreateView.as_view(), name='Client--create'),
    path('Client/<int:pk>/', ClientRetrieveUpdateDeleteView.as_view(), name='Client-retrieve-update-delete'),
    # Client_Contact
    path('Client_Contact/', Client_ContactListCreateView.as_view(), name='Client_Contact-list-create'),
    path('Client_Contact/<int:pk>/', Client_ContactRetrieveUpdateDeleteView.as_view(), name='Client_Contact-retrieve-update-delete'),
    # Fourniseur
    path('Fourniseur/', FourniseurListView.as_view(), name='Fourniseur-list-'),
    path('Fourniseuradd/', FourniseurCreateView.as_view(), name='Fourniseur--create'),
    path('Fourniseur/<int:pk>/', FourniseurRetrieveUpdateDeleteView.as_view(), name='Fourniseur-retrieve-update-delete'),
    # Fourniseur_Contact
    path('Fourniseur_Contact/', Fourniseur_ContactListCreateView.as_view(), name='Fourniseur_Contact-list-create'),
    path('Fourniseur_Contact/<int:pk>/', Fourniseur_ContactRetrieveUpdateDeleteView.as_view(), name='Fourniseur_Contact-retrieve-update-delete'),
    # fournisseur_data
    path('fournisseur_data/', fournisseur_dataListCreateView.as_view(), name='fournisseur_data-list-create'),
    path('fournisseur_data/<int:pk>/', fournisseur_dataRetrieveUpdateDeleteView.as_view(), name='fournisseur_data-retrieve-update-delete'),
    # Home Data
    path('GetHomeData/', HomePageView.as_view(), name='Home-list'),
    path('GetHomeDataTache/', HomePageViewTache.as_view(), name='Home-list'),
    path('GetHomeDataProject/', HomePageViewProject.as_view(), name='Home-list'),
    path('GetHomeDataChart/', HomePageViewChart.as_view(), name='Home-list-Chart'),
    path('GetHomeDataPie/', HomePageViewPie.as_view(), name='Home-list-Pie'),
    path('GetProblemPie/', GetProblemPie.as_view(), name='Home-list-Pie-Problem'),

    path('GetStatsData/', StatePageView.as_view(), name='Home-list'),

    path('request-auth/', request_email_sending_authorization, name='request_auth'),

    # Data flow
    path('DataFlow/', include(router.urls)),
    path('permissionsDF/', PermissionViewDF.as_view(), name='permissions'),
    path('DataFlow/notifications/', UserNotificationsView.as_view(), name='user-notifications'),
    path('DataFlow/notifications/<int:pk>/', Notification_toDFRetrieveUpdateView.as_view(), name='notification-update'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
