from ..models import * 
from ..serializers import * 
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..permissions import *
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models import Max, Count, F, ExpressionWrapper, FloatField, Func, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce, Now
import os
from django.db import transaction
from itertools import chain
from django.conf import settings
from django.core.mail import send_mail
from auth0.authentication import GetToken
from auth0.management import Auth0
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import requests
from django.shortcuts import get_object_or_404
from math import ceil
from itertools import chain
from rest_framework.pagination import PageNumberPagination
import math
# 26 class view
# Project

class ProjectPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.get_page_size(self.request))
        return Response({
            "count": self.page.paginator.count,
            "total_pages": total_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })

class ProjectListView(ListAPIView):
    serializer_class = ProjectSerializerPlus
    permission_classes = [IsAuthenticated, HaseProjectShowAllPermission]
    pagination_class = ProjectPagination

    def get_queryset(self):
        user = self.request.user

        # === Base condition (role-based access) ===
        if user.Role.Project_Show == 2:
            role_conditions = {
                (True, True, False): Q(Etape_S__in=[1, 2]) | Q(team_members__User=user),
                (True, False, True): Q(Etape_S__in=[1, 3]) | Q(team_members__User=user),
                (True, False, False): Q(Etape_S=1) | Q(team_members__User=user),
                (False, True, True): Q(Etape_S__in=[2, 3]) | Q(team_members__User=user),
                (False, True, False): Q(Etape_S=2) | Q(team_members__User=user),
                (False, False, True): Q(Etape_S=3) | Q(team_members__User=user),
            }
            condition = role_conditions.get(
                (
                    user.Role.Project_1 >= 1,
                    user.Role.Project_2 >= 1,
                    user.Role.Project_3 >= 1,
                    user.Role.Project_4 >= 1,
                    user.Role.Project_5 >= 1,
                ),
                Q(),
            )
            queryset = Project.objects.filter(condition).distinct()
        else:
            queryset = Project.objects.filter(Q(team_members__User=user)).distinct()

        # === State filter ===
        What_param = self.request.query_params.get("What", "1")
        if What_param == "1":
            queryset = queryset.filter(State__in=[1, 2, 3])
        elif What_param == "2":
            queryset = queryset.filter(State=4)
        else:
            queryset = queryset.filter(State=5)

        etape_s = int(self.request.query_params.get("Etape_S", 1))
        queryset = queryset.filter(Etape_S=etape_s)

        View = int(self.request.query_params.get("View", 0))
        if View == 0:
            search_num = self.request.query_params.get("SearchNum")
            search_owner = self.request.query_params.get("SearchOwner")
            search_date = self.request.query_params.get("SearchDate")
            search_status = int(self.request.query_params.get("SearchStatus",'0'))
            search_state = int(self.request.query_params.get("SearchState",'0'))
            search_type = int(self.request.query_params.get("SearchType",'0'))
            search_techno = self.request.query_params.get("SearchTechno")
            
            if search_num:
                queryset = queryset.filter(
                    Q(NumContract__icontains=search_num) |
                    Q(Num_Appele_dOffer__icontains=search_num)
                )

            if search_owner:
                queryset = queryset.filter(Client__Name=search_owner)

            if search_date:
                queryset = queryset.filter(Date_Depot__icontains=search_date)

            if search_status and search_status!=0:
                queryset = queryset.filter(Status=search_status)

            if search_state and search_state!=0:
                queryset = queryset.filter(State=search_state)

            if search_type and search_type!=0:
                queryset = queryset.filter(Type=search_type)

            if search_techno:
                tech_list = [int(t) for t in search_techno.split(",")]
                queryset = queryset.filter(reference_project__reference__id__in=tech_list)
        elif View == 1:
            search = self.request.query_params.get("Search", "").strip()
            print("🔎 Search param:", search)

            if search:
                queryset = queryset.filter(
                    Q(NumContract__icontains=search) |
                    Q(Num_Appele_dOffer__icontains=search) |
                    Q(Object__icontains=search) |
                    Q(Client__Name__icontains=search) |
                    Q(Date_Depot__icontains=search)
                ).distinct()
                print("🔎 SQL:", queryset.query)
            
        return queryset.order_by('-Date_Depot','id')

class ProjectSituationListView(ListAPIView):
    serializer_class = ProjectSituationSerializer
    permission_classes = [IsAuthenticated, HaseProjectShowAllPermission]
    pagination_class = ProjectPagination

    def get_queryset(self):
        user = self.request.user

        # === Base condition (role-based access) ===
        if user.Role.Project_Show == 2:
            role_conditions = {
                (True, True, False): Q(Etape_S__in=[1, 2]) | Q(team_members__User=user),
                (True, False, True): Q(Etape_S__in=[1, 3]) | Q(team_members__User=user),
                (True, False, False): Q(Etape_S=1) | Q(team_members__User=user),
                (False, True, True): Q(Etape_S__in=[2, 3]) | Q(team_members__User=user),
                (False, True, False): Q(Etape_S=2) | Q(team_members__User=user),
                (False, False, True): Q(Etape_S=3) | Q(team_members__User=user),
            }
            condition = role_conditions.get(
                (
                    user.Role.Project_1 >= 1,
                    user.Role.Project_2 >= 1,
                    user.Role.Project_3 >= 1,
                    user.Role.Project_4 >= 1,
                    user.Role.Project_5 >= 1,
                ),
                Q(),
            )
            queryset = Project.objects.filter(condition).distinct()
        else:
            queryset = Project.objects.filter(Q(team_members__User=user)).distinct()

        # === State filter ===
        What_param = self.request.query_params.get("What", "1")
        if What_param == "1":
            queryset = queryset.filter(State__in=[1, 2, 3])
        elif What_param == "2":
            queryset = queryset.filter(State=4)
        else:
            queryset = queryset.filter(State=5)

        etape_s = int(self.request.query_params.get("Etape_S", 1))
        queryset = queryset.filter(Etape_S=etape_s)

        View = int(self.request.query_params.get("View", 0))
        if View == 0:
            search_num = self.request.query_params.get("SearchNum")
            search_owner = self.request.query_params.get("SearchOwner")
            search_date = self.request.query_params.get("SearchDate")
            search_status = int(self.request.query_params.get("SearchStatus",'0'))
            search_state = int(self.request.query_params.get("SearchState",'0'))
            search_type = int(self.request.query_params.get("SearchType",'0'))
            search_techno = self.request.query_params.get("SearchTechno")
            
            if search_num:
                queryset = queryset.filter(
                    Q(NumContract__icontains=search_num) |
                    Q(Num_Appele_dOffer__icontains=search_num)
                )

            if search_owner:
                queryset = queryset.filter(Client__Name=search_owner)

            if search_date:
                queryset = queryset.filter(Date_Depot__icontains=search_date)

            if search_status and search_status!=0:
                queryset = queryset.filter(Status=search_status)

            if search_state and search_state!=0:
                queryset = queryset.filter(State=search_state)

            if search_type and search_type!=0:
                queryset = queryset.filter(Type=search_type)

            if search_techno:
                tech_list = [int(t) for t in search_techno.split(",")]
                queryset = queryset.filter(reference_project__reference__id__in=tech_list)
        elif View == 1:
            search = self.request.query_params.get("Search", "").strip()
            print("🔎 Search param:", search)

            if search:
                queryset = queryset.filter(
                    Q(NumContract__icontains=search) |
                    Q(Num_Appele_dOffer__icontains=search) |
                    Q(Object__icontains=search) |
                    Q(Client__Name__icontains=search) |
                    Q(Date_Depot__icontains=search)
                ).distinct()
                print("🔎 SQL:", queryset.query)
            
        return queryset.order_by('-Date_Depot','id')

class ProjectAPIPOST(APIView):
    permission_classes = [IsAuthenticated ,HaseProjectAddPermission]

    def post(self, request):
        project_data = request.data.get('Project')
        reference_ids = request.data.get('reference', [])
        team_members_ids = request.data.get('Team', [])

        # Create the project
        project_serializer = ProjectSerializer(data=project_data)
        if project_serializer.is_valid():
            project = project_serializer.save()

            # Add References to the project
            for ref_id in reference_ids:
                Reference_project.objects.create(reference_id=ref_id, project=project)

            # Add Team members to the project
            for team_member_id in team_members_ids:
                Team_members.objects.create(User_id=team_member_id, Project=project ,Comment="")
            # create Data
            
            Def_data_Projects = Def_data_Project.objects.filter(Etape_def__Created_with_Project=True,Etape_def__Loop=False)
            
            for Ds in Def_data_Projects :
                Data_Project.objects.create(Value="" , X="" ,Project=project , Def_data_Project=Ds)
            # Create Etapes

            Etape_Defs = Etape_def.objects.filter(deleted=False).order_by('Num')

            for E in Etape_Defs :
                if E.Created_with_Project:
                    
                    StateE = 2 if E.Start_with_Project else 1
                    Date_Start = None if StateE==1 else timezone.now()
                    etape = Etape.objects.create(Num=1 , State=StateE , Valide=0 ,
                                                Date_start=Date_Start , Date_End=None ,
                                                Comment = "",Etape_def=E , Project = project)
                    data_project = Data_Project.objects.filter(Project=project)
                    if StateE == 2 :
                        CreateTaches(E,etape, data_project)

            History.objects.create(
                type=History.Type.CREATE,
                content_type=ContentType.objects.get_for_model(project),
                object_id=project.id,
                Relation=History.relation.Project,
                User=request.user
            )
            
            NotifieCreateProject(request,project,team_members_ids)

            return Response({"message": "Project created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectAPIPUT(APIView):
    permission_classes = [IsAuthenticated ,HaseProjectMyPermission]

    def put(self, request):
        project_data = request.data.get('Project')
        reference_ids = request.data.get('reference', [])
        team_members_ids = request.data.get('Team', [])

        try:
            project_id = project_data.get('id')
            project = Project.objects.get(id=project_id)

            project_serializer = ProjectSerializer(project, data=project_data, partial=True)
            if project_serializer.is_valid():
                project = project_serializer.save()

                Reference_project.objects.filter(project=project).delete()
                Team_members.objects.filter(Project=project).delete()

                for ref_id in reference_ids:
                    Reference_project.objects.create(reference_id=ref_id, project=project)

                for team_member_id in team_members_ids:
                    Team_members.objects.create(User_id=team_member_id, Project=project, Comment="")

                History.objects.create(
                    type=History.Type.UPDATE,
                    content_type=ContentType.objects.get_for_model(project),
                    object_id=project.id,
                    Relation=History.relation.Project,
                    User=request.user
                )
                
                NotifieUpdateProject(request, project, team_members_ids,0)

                return Response({"message": "Project updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Project.DoesNotExist:
            return Response({"message": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

def CreateTaches(E,etape,data_project):
    Tache_Defs = Tache_Def.objects.filter(deleted=False,Etape_Def=E).order_by('Num')
    for T in Tache_Defs :
        tache = Tache.objects.create(State=1 , Valide=0 ,
                                    Date_start=None , Date_End=None , Max_Duration=timedelta(0),
                                    Comment = "",Problem=0,Tache_Def=T , Etape = etape)
        if T.Type == 'Complex': 
            Sous_Tache_Defs = Sous_Tache_Def.objects.filter(deleted=False,Tache_Def=T)
            for Ts in Sous_Tache_Defs :
                Sous_Tache.objects.create(State=1 , Valide=0 ,
                                Date_Start=None , Date_End=None, Sous_Tache_Def=Ts , Tache = tache)
        
        tache_data_Def = Tache_data_Def.objects.filter(Tache_Def=tache.Tache_Def)
        for Tdd in tache_data_Def:
            Dpa = None
            for Dp in data_project:
                if Dp.Def_data_Project == Tdd.Data_Project:
                    Dpa = Dp
            if Dpa != None :
                Tache_data.objects.create(Tache=tache , Tache_data_Def=Tdd , Data_Project=Dpa )

class SyncProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Sync a project with the latest definitions (Etape_def, Tache_Def, Sous_Tache_Def, etc.)
        """
        project = get_object_or_404(Project, pk=pk)

        #try:
        sync_project_definitions(project)
        return Response({"message": f"Project {project.id} synced successfully."})
        #except Exception as e:
        #    return Response({"error": str(e)}, status=404)

def sync_project_definitions(project):
    # Data_Projects created with project (non-loop only)
    def_data_projects = Def_data_Project.objects.filter(
        Etape_def__Created_with_Project=True,
        Etape_def__Loop=False,
    )
    for ds in def_data_projects:
        obj = Data_Project.objects.filter(Project=project, Def_data_Project=ds).first()
        if not obj:
            Data_Project.objects.create(
                Project=project,
                Def_data_Project=ds,
                Value="",
                X=""
            )

    base_data_projects = list(Data_Project.objects.filter(Project=project, Def_data_Project__Etape_def__Loop=False))
    etape_loops = Etape_def.objects.filter(Loop=True).values_list("id", flat=True)
    All_loop_defs = Def_data_Project.objects.filter(Etape_def_id__in=etape_loops)
    All_Data_Project = Data_Project.objects.filter(Project=project).values_list("Def_data_Project_id", flat=True)
    loop_defs = All_loop_defs.exclude(id__in=All_Data_Project)
    # Ensure Etapes exist
    etape_defs = Etape_def.objects.filter(deleted=False).order_by("Num")
    for e_def in etape_defs:
        etape, created = Etape.objects.get_or_create(
            Project=project,
            Etape_def=e_def,
            defaults={
                "Num": 1,
                "State": 2 if e_def.Start_with_Project else 1,
                "Valide": 0,
                "Date_start": timezone.now() if e_def.Start_with_Project else None,
                "Date_End": None,
                "Comment": "",
            },
        )

        if etape.State > 1:
            if e_def.Loop:
                loop_defs_=loop_defs.filter(Etape_def=e_def)
                loop_data_projects = []
                for ds in loop_defs_:
                    obj = Data_Project.objects.filter(Project=project, Def_data_Project=ds).first()
                    if not obj:
                        obj = Data_Project.objects.create(
                            Project=project,
                            Def_data_Project=ds,
                            Value="",
                            X=""
                        )
                    loop_data_projects.append(obj)

                data_project_use = list(chain(loop_data_projects, base_data_projects))
            else:
                data_project_use = base_data_projects

            tache_defs = Tache_Def.objects.filter(deleted=False, Etape_Def=e_def).order_by("Num")
            for t_def in tache_defs:
                tache, _ = Tache.objects.get_or_create(
                    Etape=etape,
                    Tache_Def=t_def,
                    defaults={
                        "State": 1,
                        "Valide": 0,
                        "Date_start": None,
                        "Date_End": None,
                        "Max_Duration": timedelta(0),
                        "Comment": "",
                        "Problem": 0,
                    },
                )

                # Ensure Tache_data exist
                for tdd in Tache_data_Def.objects.filter(Tache_Def=t_def):
                    dpa = next((dp for dp in data_project_use if dp.Def_data_Project == tdd.Data_Project), None)
                    if dpa:
                        Tache_data.objects.get_or_create(
                            Tache=tache,
                            Tache_data_Def=tdd,
                            defaults={"Data_Project": dpa},
                        )

                # Ensure Sous-Taches exist if Complex
                if t_def.Type == "Complex":
                    for st_def in Sous_Tache_Def.objects.filter(deleted=False, Tache_Def=t_def):
                        Sous_Tache.objects.get_or_create(
                            Tache=tache,
                            Sous_Tache_Def=st_def,
                            defaults={
                                "State": 1,
                                "Valide": 0,
                                "Date_Start": None,
                                "Date_End": None,
                            },
                        )

    # -------------------------------
    # CLEANUP PART
    # -------------------------------
    valid_etape_defs = set(Etape_def.objects.filter(deleted=False).values_list("id", flat=True))
    Etape.objects.filter(Project=project).exclude(Etape_def_id__in=valid_etape_defs).delete()

    valid_tache_defs = set(Tache_Def.objects.filter(deleted=False).values_list("id", flat=True))
    Tache.objects.filter(Etape__Project=project).exclude(Tache_Def_id__in=valid_tache_defs).delete()

    valid_sous_defs = set(Sous_Tache_Def.objects.filter(deleted=False).values_list("id", flat=True))
    Sous_Tache.objects.filter(Tache__Etape__Project=project).exclude(Sous_Tache_Def_id__in=valid_sous_defs).delete()

    valid_tache_data_defs = set(Tache_data_Def.objects.all().values_list("id", flat=True))
    Tache_data.objects.filter(Tache__Etape__Project=project).exclude(Tache_data_Def_id__in=valid_tache_data_defs).delete()

class ProjectRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, HaseProjectMyPermission]

    def perform_update(self, serializer):
        project = serializer.save()
        
        team_members_ids = Team_members.objects.filter(Project=project).values_list('User_id', flat=True)
        #NotifieUpdateProject(self.request, project, team_members_ids,project.State)

class ProjectRetrieve(RetrieveAPIView):
    queryset = Project.objects.all().order_by('id')
    serializer_class = ProjectSerializerPlusPlus
    permission_classes = [IsAuthenticated,HaseProjectShowTeamPermission]

def SendNotifications1(notification,user,team_members_ids,Title,Contant,send_email=True,Notifie_super=False,opened=False):
    Users_Email = []
    notified_users = set()
    Users = User.objects.filter(Role__Etape__gte=4)

    if Notifie_super:
        for U in Users:
            if U.id not in notified_users and user.id != U.id:
                Notification_to.objects.create(
                    Notification=notification,
                    To=U,
                    Opened=opened
                )
                notified_users.add(U.id)
                Users_Email.append(U.email)
    
    for user_id in team_members_ids:
        if user_id not in notified_users and user.id != user_id:
            try:
                U = User.objects.get(id=user_id)
                Notification_to.objects.create(
                    Notification=notification,
                    To=U,
                    Opened=opened
                )
                notified_users.add(user_id)
                Users_Email.append(U.email)
            except User.DoesNotExist:
                continue
    
    if Users_Email and send_email:
        try:
            send_mail(
                Title, 
                Contant, 
                '****@****.com',
                Users_Email,
                fail_silently=False
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

def SendNotifications(notification, user, team_members_ids, Title, Content, send_email=True, Notifie_super=False,opened=False):
    Users_Email = []
    notified_users = set()
    Users = User.objects.filter(Role__Etape__gte=4)

    if Notifie_super:
        for U in Users:
            if U.id not in notified_users and user.id != U.id:
                Notification_to.objects.create(
                    Notification=notification,
                    To=U,
                    Opened=opened
                )
                notified_users.add(U.id)
                Users_Email.append(U.email)
    
    for user_id in team_members_ids:
        if user_id not in notified_users and user.id != user_id:
            try:
                U = User.objects.get(id=user_id)
                Notification_to.objects.create(
                    Notification=notification,
                    To=U,
                    Opened=opened
                )
                notified_users.add(user_id)
                Users_Email.append(U.email)
            except User.DoesNotExist:
                continue
    
    if Users_Email and send_email:
        date = timezone.now().strftime("%Y-%m-%d")
        safe_content = Content.replace('\n', '<br>')
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <div style="background-color: #2c3e50; padding: 15px; text-align: center; margin-bottom: 20px; border-radius: 6px;">
                <h2 style="color: white; margin: 0;">Workflow Notification</h2>
            </div>
            
            <h3 style="color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px;">{Title}</h3>
            
            <div style="background-color: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 6px;">
                {safe_content}
            </div>
            
            <div style="font-size: 14px; color: #555;">
                <p><strong>Initiated by:</strong> app_name</p>
                <p><strong>Date:</strong> {date}</p>
            </div>
            
            <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #e0e0e0; font-size: 13px; color: #777;">
                <p>This is an automated notification from Workflow System.</p>
                <p>Please do not reply directly to this message.</p>
            </div>
        </div>
        """
        text_content = f"""
        Workflow Notification
        =========================
        
        {Title}
        
        {safe_content}
        
        Initiated by: app_name
        Date: {date}
        
        ---
        This is an automated notification. Please do not reply.
        """
        try:
            # 1. Get Auth0 Token
            auth0_response = requests.post(
                f"https://{settings.AUTH0_DOMAIN}/oauth/token",
                headers={"content-type": "application/json"},
                json={
                    "client_id": settings.AUTH0_CLIENT_ID,
                    "client_secret": settings.AUTH0_CLIENT_SECRET,
                    "audience": f"https://{settings.AUTH0_DOMAIN}/api/v2/",
                    "grant_type": "client_credentials"
                },
                timeout=10
            )
            auth0_response.raise_for_status()
            auth0_token = auth0_response.json()["access_token"]

            # 2. Send Emails via Auth0
            for email in Users_Email:
                try:
                    requests.post(
                        f"https://{settings.AUTH0_DOMAIN}/api/v2/emails/provider",
                        headers={
                            "Authorization": f"Bearer {auth0_token}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "to": email,
                            "subject": f"[app_name] {Title}",
                            "text": text_content,
                            "html": html_content,
                            "from": "****@****.com"
                        },
                        timeout=10
                    ).raise_for_status()
                except Exception as email_error:
                    print(f"Failed to send to {email}: {str(email_error)}")
                    continue  # Skip failed emails but continue with others

        except Exception as main_error:
            print(f"Notification system failed: {str(main_error)}")

def NotifieCreateProject(request, project, team_members_ids): # Trun mailing true
    user = request.user
    
    notification = Notification.objects.create(
        Relation=Notification.relation.Project,
        content_type=ContentType.objects.get_for_model(project),
        object_id=project.id,
        Message=f"{user.first_name} {user.last_name} created a new project: {project.Num_Appele_dOffer} {project.Client.Name}",
        Date_Time=timezone.now(),
    )
    SendNotifications(notification,user,team_members_ids,
                      f"New Project {project.Num_Appele_dOffer} {project.Client.Name}",
                      f"{user.first_name} {user.last_name} created a new project: {project.Num_Appele_dOffer} {project.Client.Name}"
                      ,True,True,False)

def NotifieUpdateProject(request, project, team_members_ids, State):
    user = request.user

    if State == 0: TypeMessage = "updated"
    elif State == 2: TypeMessage = "restarted the"
    elif State == 3: TypeMessage = "posed the"
    elif State == 4: TypeMessage = "finished the"
    else: TypeMessage = "updated"

    Notifie_super=False
    if team_members_ids != [] or Notifie_super:
        notification = Notification.objects.create(
            Relation=Notification.relation.Project,
            content_type=ContentType.objects.get_for_model(project),
            object_id=project.id,
            Message=f"{user.first_name} {user.last_name} {TypeMessage} project {project.Num_Appele_dOffer} {project.Client.Name}",
            Date_Time=timezone.now(),
        )
        SendNotifications(notification,user,team_members_ids,
                        f"Project {project.Num_Appele_dOffer} {project.Client.Name}",
                        f"{user.first_name} {user.last_name} {TypeMessage} project {project.Num_Appele_dOffer} {project.Client.Name}"
                        ,False,Notifie_super,True)

#PoseProject
class PoseProjectListCreateView(ListCreateAPIView):
    queryset = PoseProject.objects.all().order_by('id')
    serializer_class = PoseProjectSerializer
    permission_classes = [IsAuthenticated]

class PoseProjectRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = PoseProject.objects.all().order_by('id')
    serializer_class = PoseProjectSerializer
    permission_classes = [IsAuthenticated]

# Def_data_Project
class Def_data_ProjectListView(ListAPIView):
    queryset = Def_data_Project.objects.all().order_by('id')
    serializer_class = Def_data_ProjectSerializerPlus
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
    
class Def_data_ProjectCreateView(CreateAPIView):
    queryset = Def_data_Project.objects.all().order_by('id')
    serializer_class = Def_data_ProjectSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Def_data_ProjectRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Def_data_Project.objects.all().order_by('id')
    serializer_class = Def_data_ProjectSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Data_Groupe
class Data_GroupeListView(ListAPIView):
    queryset = Data_Groupe.objects.all().order_by('id')
    serializer_class = Data_GroupeSerializer
    permission_classes = [IsAuthenticated]
    
class Data_GroupeListCreateView(ListCreateAPIView):
    queryset = Data_Groupe.objects.all().order_by('id')
    serializer_class = Data_GroupeSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Data_GroupeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Data_Groupe.objects.all().order_by('id')
    serializer_class = Data_GroupeSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Data_Project

class Data_ProjectListCreateView(ListCreateAPIView):
    queryset = Data_Project.objects.all().order_by('id')
    serializer_class = Data_ProjectSerializer
    permission_classes = [IsAuthenticated]

class Data_ProjectRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Data_Project.objects.all().order_by('id')
    serializer_class = Data_ProjectSerializer
    permission_classes = [IsAuthenticated]

# Multy_data_project

class Multy_data_projectListCreateView(ListCreateAPIView):
    queryset = Multy_data_project.objects.all().order_by('id')
    serializer_class = Multy_data_projectSerializer
    permission_classes = [IsAuthenticated]

class Multy_data_projectRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Multy_data_project.objects.all().order_by('id')
    serializer_class = Multy_data_projectSerializer
    permission_classes = [IsAuthenticated]

class multy_data_project(APIView):

    def post(self, request, Num, Data_Project):

        Multy_data_project.objects.filter(Data_Project=Data_Project).delete()

        for i in range(Num):
            Multy_data_project.objects.create(
                Num=i+1,
                Value="",
                X="",
                Data_Project_id=Data_Project,
            )
        return Response({"message": "Multy data project created successfully."})
# Table_data

class Table_dataListCreateView(ListCreateAPIView):
    queryset = Table_data.objects.all().order_by('id')
    serializer_class = Table_dataSerializer
    permission_classes = [IsAuthenticated]

class Table_dataRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Table_data.objects.all().order_by('id')
    serializer_class = Table_dataSerializer
    permission_classes = [IsAuthenticated]

class UpdateTableDataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        table_data_dict = request.data.get("table_data", {})
        
        if not isinstance(table_data_dict, dict):
            return Response({"error": "Invalid data format, expected a dictionary of table data"}, status=status.HTTP_400_BAD_REQUEST)

        table_data_list = list(table_data_dict.values())
        
        if not table_data_list:
            return Response({"error": "Table data is empty"}, status=status.HTTP_200_OK)

        data_project_id = table_data_list[0].get("Data_Project")
        if not data_project_id:
            return Response({"error": "Data_Project ID is missing in table data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_project = Data_Project.objects.get(id=data_project_id)
        except Data_Project.DoesNotExist:
            return Response({"error": "Data_Project not found"}, status=status.HTTP_404_NOT_FOUND)

        incoming_ids = {entry.get("id") for entry in table_data_list if "id" in entry}

        try:
            with transaction.atomic():
                Table_data.objects.filter(Data_Project=data_project).exclude(id__in=incoming_ids).delete()

                for entry in table_data_list:
                    table_data_id = entry.get("id")
                    if table_data_id:
                        Table_data.objects.filter(id=table_data_id, Data_Project=data_project).update(**entry)
                    else:
                        entry["Data_Project"] = data_project.id
                        serializer = Table_dataSerializer(data=entry)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Table data updated successfully"}, status=status.HTTP_200_OK)

# select_Values 
 
class select_ValuesListCreateView(ListCreateAPIView):
    queryset = select_Values.objects.all().order_by('id')
    serializer_class = select_ValuesSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class select_ValuesRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = select_Values.objects.all().order_by('id')
    serializer_class = select_ValuesSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Table_strecture

class Table_strectureListCreateView(ListCreateAPIView):
    queryset = Table_strecture.objects.all().order_by('id')
    serializer_class = Table_strectureSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Table_strectureRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Table_strecture.objects.all().order_by('id')
    serializer_class = Table_strectureSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Fill_Message

class Fill_MessageListCreateView(ListCreateAPIView):
    queryset = Fill_Message.objects.all().order_by('id')
    serializer_class = Fill_MessageSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Fill_MessageRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Fill_Message.objects.all().order_by('id')
    serializer_class = Fill_MessageSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Form

class FormListView(ListAPIView):
    queryset = Form.objects.all().order_by('id')
    serializer_class = FormSerializerPlus
    permission_classes = [IsAuthenticated]

class FormCreateView(CreateAPIView):
    queryset = Form.objects.all().order_by('id')
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class FormRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all().order_by('id')
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Forme_Massage

class FormMessageView(APIView):

    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
    def post(self, request, form_id):

        try:
            form_instance = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)

        long_text = request.data.get('text', '')

        Forme_Massage.objects.filter(Form=form_instance).delete()

        max_length = 100
        chunks = [long_text[i:i+max_length] for i in range(0, len(long_text), max_length)]

        for chunk in chunks:
            Forme_Massage.objects.create(Value=chunk, Form=form_instance)

        return Response({"message": "Messages updated successfully"}, status=status.HTTP_200_OK)
# Form_Data

class Form_DataListCreateView(ListCreateAPIView):
    queryset = Form_Data.objects.all().order_by('id')
    serializer_class = Form_DataSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Form_DataRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Form_Data.objects.all().order_by('id')
    serializer_class = Form_DataSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Etape

class EtapeListCreateView(ListCreateAPIView):
    queryset = Etape.objects.all().order_by('id')
    serializer_class = EtapeSerializer
    permission_classes = [IsAuthenticated,HaseEtapeMyPermission]

class EtapeRetrieveView(RetrieveAPIView):
    queryset = Etape.objects.all().order_by('id')
    serializer_class = EtapeSerializerPlus
    permission_classes = [IsAuthenticated,HaseEtapeMyPermission]

class EtapeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Etape.objects.all().order_by('id')
    serializer_class = EtapeSerializer
    permission_classes = [IsAuthenticated,HaseEtapeMyPermission]

    def perform_update(self, serializer,request, type_value):
        etape = serializer.save()

        if etape.State == Etape.state.In_progress and (not Tache.objects.filter(Etape=etape).exists()):
            E = Etape_def.objects.get(id=etape.Etape_def_id)
            project = Project.objects.get(id=etape.Project_id)
            
            if etape.Etape_def.Loop == True:
                Def_data_Projects = Def_data_Project.objects.filter(Etape_def=E)
                new_data_project = [
                    Data_Project.objects.create(Value="", X="", Project=project, Def_data_Project=Ds)
                    for Ds in Def_data_Projects
                ]

                existing_data_project = Data_Project.objects.filter(Project=project).exclude(Def_data_Project__Etape_def=E)
                data_project = list(chain(new_data_project, existing_data_project))
            else :
                data_project = Data_Project.objects.filter(Project=project)
            CreateTaches(E, etape, data_project)

        if type_value and int(type_value) != 0:
            content_type = ContentType.objects.get_for_model(Etape)
            Hist, _ = History.objects.update_or_create(
                content_type=content_type,
                object_id=etape.id,
                type=type_value,
                defaults={
                    'Relation': History.relation.Etape,
                    'User': self.request.user,
                    'Date': timezone.now()
                }
            )
            Hist.refresh_from_db()
            
            type_display = Hist.get_type_display()
            team_members_ids = Team_members.objects.filter(Project=etape.Project).values_list('User_id', flat=True)
            NotifieUpdateEtape(request, etape, team_members_ids,type_display)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        type_value = request.query_params.get('Type')

        self.perform_update(serializer,request, type_value) or 0

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

def NotifieUpdateEtape(request, etape, team_members_ids, Type_Action):
    user = request.user

    Notifie_super=False
    if team_members_ids != [] or Notifie_super:
        notification = Notification.objects.create(
            Relation=Notification.relation.Etape,
            content_type=ContentType.objects.get_for_model(etape),
            object_id=etape.id,
            Message=f"{user.first_name} {user.last_name} {Type_Action} etape {etape.Etape_def.Name}",
            Date_Time=timezone.now(),
        )

        SendNotifications(notification,user,team_members_ids,
                        f"Update Etape {etape.Etape_def.Name}",
                        f"{user.first_name} {user.last_name} {Type_Action} etape {etape.Etape_def.Name} in the project {etape.Project.Num_Appele_dOffer} {etape.Project.Client.Name}"
                        ,False,Notifie_super,True)

# Etape_def
class Etape_defListMinView(ListAPIView):
    queryset = Etape_def.objects.all().order_by('id')
    serializer_class = Etape_defSerializer
    permission_classes = [IsAuthenticated]

class Etape_defListView(ListAPIView):
    queryset = Etape_def.objects.all().order_by('Num') 
    serializer_class = Etape_defSerializerPlus
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Etape_defCreateView(CreateAPIView):
    queryset = Etape_def.objects.all().order_by('id')
    serializer_class = Etape_defSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Etape_defRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Etape_def.objects.all().order_by('id')
    serializer_class = Etape_defSerializer
    permission_classes = [IsAuthenticated, HaseStructure_ProjectPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if any Etape uses this Etape_def as a foreign key
        if Etape.objects.filter(Etape_def=instance).exists():
            # If yes, set deleted to True (soft delete)
            instance.deleted = True
            instance.save()
            return Response({"detail": "Etape_def is referenced by Etape(s), set deleted=True instead of deleting."}, status=status.HTTP_200_OK)
        else:
            # If not, proceed with normal delete
            return super().destroy(request, *args, **kwargs)
# Tache

class TacheListCreateView(ListCreateAPIView):
    queryset = Tache.objects.all().order_by('id')
    serializer_class = TacheSerializer
    permission_classes = [IsAuthenticated]

class TacheRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache.objects.all().order_by('id')
    serializer_class = TacheSerializer
    permission_classes = [IsAuthenticated, HaseEtapeMyPermission]

    def perform_update(self, serializer,request, type_value):
        tache = serializer.save()

        if type_value and int(type_value) != 0:
            content_type = ContentType.objects.get_for_model(Tache)
            Hist , _ =History.objects.update_or_create(
                content_type=content_type,
                object_id=tache.id,
                type=type_value,
                defaults={
                    'Relation': History.relation.Tache,
                    'User': self.request.user,
                    'Date': timezone.now()
                }
            )
            Hist.refresh_from_db()

            type_display = Hist.get_type_display()
            team_members_ids = Team_members.objects.filter(Project=tache.Etape.Project).values_list('User_id', flat=True)
            NotifieUpdateTache(request, tache, team_members_ids,type_display)
            if tache.State == 3 or tache.State == 4:
                NotifieNextTache(request,tache,team_members_ids)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        type_value = request.query_params.get('Type') or 0

        self.perform_update(serializer,request, type_value)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

class TacheApi(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        tache_id = request.query_params.get('Tache')

        if tache_id:
            taches = Tache.objects.filter(id=tache_id)

            serializer = TacheSerializerPlusPlus(taches, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Tache ID is missing"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        tache_data = request.data
        
        for td in tache_data:
            d = td.get('Data_Project', {})
            data_project_id = d.get('id')
            
            try:
                data = Data_Project.objects.get(id=data_project_id)
            except Data_Project.DoesNotExist:
                return Response({"error": "Data_Project not found"}, status=404)
            
            # Update Value and X fields
            data.Value = d.get('Value', data.Value)
            data.X = d.get('X', data.X)
            data.save()
            
            multy_data = d.get('Multy_data_project', [])
            multy_data_ids = []  # List to store IDs of received multy_data_project entries

            for md in multy_data:
                md_id = md.get('id')
                num = md.get('Num')
                value = md.get('Value')
                X = md.get('X')

                if md_id:
                    try:
                        multy_data_entry = Multy_data_project.objects.get(id=md_id)
                        multy_data_entry.Num = num
                        multy_data_entry.Value = value
                        multy_data_entry.X = X
                        multy_data_entry.save()
                        multy_data_ids.append(md_id)
                    except Multy_data_project.DoesNotExist:
                        return Response({"error": "Multy_data_project not found"}, status=404)
                else:
                    new_entry = Multy_data_project.objects.create(
                        Data_Project=data,
                        Num=num,
                        Value=value,
                        X=X
                    )
                    multy_data_ids.append(new_entry.id)

            Multy_data_project.objects.filter(Data_Project=data).exclude(id__in=multy_data_ids).delete()

        if len(tache_data) > 0:
            tache = Tache.objects.get(id=tache_data[0].get('Tache', {}))
            team_members_ids = Team_members.objects.filter(Project=tache.Etape.Project).values_list('User_id', flat=True)
            #NotifieUpdateTache(request, tache, team_members_ids,"Updated data of ")
        return Response({"status": "success"})
    
class Data_ProjectApi(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        project_id = request.query_params.get('Project')

        if project_id:
            data_projects = Data_Project.objects.filter(Project=project_id)

            serializer = Data_ProjectSerializerPlus(data_projects, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Project ID is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        Data_Projects = request.data
        
        for d in Data_Projects:
            data_project_id = d.get('id')
            
            try:
                data = Data_Project.objects.get(id=data_project_id)
            except Data_Project.DoesNotExist:
                return Response({"error": "Data_Project not found"}, status=404)
            
            # Update Value and X fields
            data.Value = d.get('Value', data.Value)
            data.X = d.get('X', data.X)
            data.save()
            
            multy_data = d.get('Multy_data_project', [])
            multy_data_ids = []

            for md in multy_data:
                md_id = md.get('id')
                num = md.get('Num')
                value = md.get('Value')
                X = md.get('X')
                if md_id:
                    try:
                        multy_data_entry = Multy_data_project.objects.get(id=md_id)
                        multy_data_entry.Num = num
                        multy_data_entry.Value = value
                        multy_data_entry.X = X
                        multy_data_entry.save()
                        multy_data_ids.append(md_id)
                    except Multy_data_project.DoesNotExist:
                        return Response({"error": "Multy_data_project not found"}, status=404)
                else:
                    new_entry = Multy_data_project.objects.create(
                        Data_Project=data,
                        Num=num,
                        Value=value,
                        X=X
                    )
                    multy_data_ids.append(new_entry.id)

            Multy_data_project.objects.filter(Data_Project=data).exclude(id__in=multy_data_ids).delete()
        return Response(status=200)

def NotifieUpdateTache(request, tache, team_members_ids, Type_Action):
    user = request.user
    # notifie supervisor
    Superviser_Role = Tache_superviser.objects.filter(Tache_Def=tache.Tache_Def).values_list('Role', flat=True)
    Superviser_id = User.objects.filter(Role__in=Superviser_Role).values_list('id', flat=True)
    team_members_ids = list(set(team_members_ids) & set(Superviser_id))

    Notifie_super = False
    Send_mail = False

    if team_members_ids != [] or Notifie_super:
        notification = Notification.objects.create(
            Relation=Notification.relation.Tache,
            content_type=ContentType.objects.get_for_model(tache),
            object_id=tache.id,
            Message=f"{user.first_name} {user.last_name} {Type_Action} tache {tache.Tache_Def.Name}",
            Date_Time=timezone.now(),
        )

        SendNotifications(notification,user,team_members_ids,
                        f"Task changes {tache.Tache_Def.Name}",
                        f"{user.first_name} {user.last_name} {Type_Action} tache {tache.Tache_Def.Name} in the project {tache.Etape.Project.Num_Appele_dOffer} {tache.Etape.Project.Client.Name}"
                        ,Send_mail,Notifie_super,True)
        
def NotifieNextTache(request, tache, team_members_ids):

    tache_next = TacheDependency.objects.filter(previous=tache.Tache_Def).values_list('current', flat=True)

    for tn in tache_next:
        T = Tache_Def.objects.get(id=tn)
        NotifieUsersNextTache(request, T,tache, team_members_ids)

def NotifieUsersNextTache(request, Tnext, tache, team_members_ids):
    user = request.user

    PrjEtapes_ids = Etape.objects.filter(Project=tache.Etape.Project).values_list('id', flat=True)
    T = Tache.objects.filter(Tache_Def_id=Tnext, Etape__in=PrjEtapes_ids).first()
    if T and T.can_start():
        
        To_Role = Tache_To.objects.filter(Tache_Def=Tnext).values_list('Role', flat=True)
        To_id = User.objects.filter(Role__in=To_Role).values_list('id', flat=True)
        team_members_ids = list(set(team_members_ids) & set(To_id))

        Notifie_super = False
        Send_mail = False # True
        if team_members_ids != [] or Notifie_super:
            notification = Notification.objects.create(
                Relation=Notification.relation.Tache,
                content_type=ContentType.objects.get_for_model(T),
                object_id=T.id,
                Message=f"You can start Tache {Tnext.Name}",
                Date_Time=timezone.now(),
            )

            SendNotifications(notification,user,team_members_ids,
                            f"Tast Ready {tache.Tache_Def.Name}",
                            f"You can start Tache {tache.Tache_Def.Name} in the project {tache.Etape.Project.Num_Appele_dOffer} {tache.Etape.Project.Client.Name}"
                            ,Send_mail,Notifie_super,False)
# Tache_Def
class Tache_DefListView(ListCreateAPIView):
    queryset = Tache_Def.objects.all().order_by('id') 
    serializer_class = Tache_DefSerializerP
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Tache_DefListCreateView(ListCreateAPIView):
    queryset = Tache_Def.objects.all().order_by('id')
    serializer_class = Tache_DefSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Tache_DefRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_Def.objects.all().order_by('id') 
    serializer_class = Tache_DefSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Tache.objects.filter(Tache_Def=instance).exists():
            instance.deleted = True
            instance.save()
            return Response({"detail": "Tache_Def is referenced by Tache(s), set deleted=True instead of deleting."}, status=status.HTTP_200_OK)
        else:
            return super().destroy(request, *args, **kwargs)
# Tache_data

class Tache_dataListCreateView(ListCreateAPIView):
    queryset = Tache_data.objects.all().order_by('id')
    serializer_class = Tache_dataSerializer
    permission_classes = [IsAuthenticated]

class Tache_dataRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_data.objects.all().order_by('id')
    serializer_class = Tache_dataSerializer
    permission_classes = [IsAuthenticated]
# Tache_data_Def

class Tache_data_DefListCreateView(ListCreateAPIView):
    queryset = Tache_data_Def.objects.all().order_by('id')
    serializer_class = Tache_data_DefSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Tache_data_DefRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_data_Def.objects.all().order_by('id')
    serializer_class = Tache_data_DefSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Tache_To

class Tache_ToListCreateView(ListCreateAPIView):
    queryset = Tache_To.objects.all().order_by('id')
    serializer_class = Tache_ToSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Tache_ToRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_To.objects.all().order_by('id')
    serializer_class = Tache_ToSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Tache_receve

class Tache_receveListCreateView(ListCreateAPIView):
    queryset = Tache_receve.objects.all().order_by('id')
    serializer_class = Tache_receveSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Tache_receveRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_receve.objects.all().order_by('id')
    serializer_class = Tache_receveSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Tache_superviser

class Tache_superviserListCreateView(ListCreateAPIView):
    queryset = Tache_superviser.objects.all().order_by('id')
    serializer_class = Tache_superviserSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Tache_superviserRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_superviser.objects.all().order_by('id')
    serializer_class = Tache_superviserSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# TacheDependency

class TacheDependencyListCreateView(ListCreateAPIView):
    queryset = TacheDependency.objects.all().order_by('id')
    serializer_class = TacheDependencySerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class TacheDependencyRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = TacheDependency.objects.all().order_by('id')
    serializer_class = TacheDependencySerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]
# Problem

class ProblemListCreateView(ListCreateAPIView):
    queryset = Problem.objects.all().order_by('id')
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        problem = serializer.save()
        team_members_ids = Team_members.objects.filter(Project=problem.Tache.Etape.Project).values_list('User_id', flat=True)
        NotifieaddProblem(self.request, problem.Tache, problem, team_members_ids)
                
def NotifieaddProblem(request, tache,problem, team_members_ids):
    user = request.user
    Notifie_super = False
    Send_mail = False

    if team_members_ids != [] or Notifie_super:
        notification = Notification.objects.create(
            Relation=Notification.relation.Tache,
            content_type=ContentType.objects.get_for_model(tache),
            object_id=tache.id,
            Message=f"{user.first_name} {user.last_name} a ajoute un problem '{problem.Note_Problem}' tache {tache.Tache_Def.Name}",
            Date_Time=timezone.now(),
        )

        SendNotifications(notification,user,team_members_ids,
                        f"Task changes {tache.Tache_Def.Name}",
                        f"{user.first_name} {user.last_name} a ajoute un problem '{problem.Note_Problem}' tache {tache.Tache_Def.Name}"
                        ,Send_mail,Notifie_super,False)
class ProblemRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Problem.objects.all().order_by('id')
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]
# Sous_Tache

class Sous_TacheListCreateView(ListCreateAPIView):
    queryset = Sous_Tache.objects.all().order_by('id')
    serializer_class = Sous_TacheSerializer
    permission_classes = [IsAuthenticated]

class Sous_TacheRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Sous_Tache.objects.all().order_by('id')
    serializer_class = Sous_TacheSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer, type_value):
        sous_tache = serializer.save()

        if type_value and int(type_value) != 0:
            content_type = ContentType.objects.get_for_model(Sous_Tache)
            History.objects.update_or_create(
                content_type=content_type,
                object_id=sous_tache.id,
                type=type_value,
                defaults={
                    'Relation': History.relation.Sous_Tache,
                    'User': self.request.user,
                    'Date': timezone.now()
                }
            )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        type_value = request.query_params.get('Type') or 0

        self.perform_update(serializer, type_value)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

# Sous_Tache_Def

class Sous_Tache_DefListCreateView(ListCreateAPIView):
    queryset = Sous_Tache_Def.objects.all().order_by('id')
    serializer_class = Sous_Tache_DefSerializer
    permission_classes = [IsAuthenticated,HaseStructure_ProjectPermission]

class Sous_Tache_DefRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Sous_Tache_Def.objects.all().order_by('id')
    serializer_class = Sous_Tache_DefSerializer
    permission_classes = [IsAuthenticated, HaseStructure_ProjectPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Sous_Tache.objects.filter(Sous_Tache_Def=instance).exists():
            instance.deleted = True
            instance.save()
            return Response({"detail": "Sous_Tache_Def is referenced by Sous_Tache(s), set deleted=True instead of deleting."}, status=status.HTTP_200_OK)
        else:
            return super().destroy(request, *args, **kwargs)

# Groupe_Tache_Def

class Groupe_Tache_DefListView(ListAPIView):
    queryset = Groupe_Tache_Def.objects.all().order_by('id')
    serializer_class = Groupe_Tache_DefSerializerPlus
    permission_classes = [IsAuthenticated]

class Groupe_Tache_DefCreateView(CreateAPIView):
    queryset = Groupe_Tache_Def.objects.all().order_by('id')
    serializer_class = Groupe_Tache_DefSerializer
    permission_classes = [IsAuthenticated]

class Groupe_Tache_DefRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Groupe_Tache_Def.objects.all().order_by('id')
    serializer_class = Groupe_Tache_DefSerializer
    permission_classes = [IsAuthenticated]

# File_Project
class File_ProjectListView(ListAPIView):
    queryset = File_Project.objects.all().order_by('id')
    serializer_class = File_ProjectSerializerP
    permission_classes = [IsAuthenticated]

class File_ProjectListCreateView(ListCreateAPIView):
    queryset = File_Project.objects.all().order_by('id')
    serializer_class = File_ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        content_type = ContentType.objects.get_for_model(File_Project)
        
        History.objects.create(
            content_type=content_type,
            object_id=instance.id,
            type=History.Type.CREATE,
            Relation=History.relation.File_Project,
            User=self.request.user,
            Date=timezone.now()
        )
        team_members_ids = Team_members.objects.filter(Project=instance.Data_Project.Project).values_list('User_id', flat=True)

        #NotifieUpdateFile(self.request, instance, team_members_ids, "Added a file")

class File_ProjectRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = File_Project.objects.all().order_by('id')
    serializer_class = File_ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = self.get_object()
        
        serializer.save()

        content_type = ContentType.objects.get_for_model(File_Project)
        History.objects.update_or_create(
            content_type=content_type,
            object_id=instance.id,
            type=History.Type.UPDATE,
            defaults={
                'Relation': History.relation.File_Project,
                'User': self.request.user,
                'Date': timezone.now()
            }
        )
        team_members_ids = Team_members.objects.filter(Project=instance.Data_Project.Project).values_list('User_id', flat=True)

        #NotifieUpdateFile(self.request, instance, team_members_ids, "Updated file")

def NotifieUpdateFile(request, file, team_members_ids, Action): # --
    user = request.user

    notification = Notification.objects.create(
        Relation=Notification.relation.File_Project,
        content_type=ContentType.objects.get_for_model(File_Project),
        object_id=file.id,
        Message=f"{user.first_name} {user.last_name} {Action} {file.Description} in project {file.Data_Project.Project.Num_Appele_dOffer} {file.Data_Project.Project.Client.Name}",
        Date_Time=timezone.now(),
    )
    SendNotifications(notification,user,team_members_ids,
                      f"File changes {file.Description}",
                      f"{user.first_name} {user.last_name} {Action} {file.Description} in project {file.Data_Project.Project.Num_Appele_dOffer} {file.Data_Project.Project.Client.Name} "
                      ,False,False,True)

# Reference
class ReferenceListView(ListAPIView):
    queryset = Reference.objects.all().order_by('id')
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated]

class ReferenceListCreateView(ListCreateAPIView):
    queryset = Reference.objects.all().order_by('id')
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated,HaseRefancePermission]

class ReferenceRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Reference.objects.all().order_by('id')
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated,HaseRefancePermission]
# Reference_project

class Reference_projectListCreateView(ListCreateAPIView):
    queryset = Reference_project.objects.all().order_by('id')
    serializer_class = Reference_projectSerializer
    permission_classes = [IsAuthenticated]

class Reference_projectRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Reference_project.objects.all().order_by('id')
    serializer_class = Reference_projectSerializer
    permission_classes = [IsAuthenticated]
# Team_members

class Team_membersListCreateView(ListCreateAPIView):
    queryset = Team_members.objects.all().order_by('id')
    serializer_class = Team_membersSerializer
    permission_classes = [IsAuthenticated, HaseTeamPermission]

    def perform_create(self, serializer,request):
        teamM = serializer.save()

        History.objects.create(
            type=History.Type.ADD,
            content_type=ContentType.objects.get_for_model(Team_members),
            object_id=teamM.id,
            Relation=History.relation.Team,
            User=self.request.user
        )
        team_members_ids = Team_members.objects.filter(Project=teamM.Project).values_list('User_id', flat=True)
        NotifieCreateTeam(request, teamM, team_members_ids)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer,request)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class Team_membersRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Team_members.objects.all().order_by('id')
    serializer_class = Team_membersSerializer
    permission_classes = [IsAuthenticated, HaseTeamPermission]
        
    def perform_update(self, serializer,request):
        teamM = serializer.save()

        History.objects.create(
            type=History.Type.UPDATE,
            content_type=ContentType.objects.get_for_model(Team_members),
            object_id=teamM.id,
            Relation=History.relation.Team,
            User=self.request.user
        )
        team_members_ids = Team_members.objects.filter(Project=teamM.Project).values_list('User_id', flat=True)
        #NotifieUpdateTeam(request, teamM, team_members_ids)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer,request)

        # Clear prefetched objects cache if it exists
        if hasattr(instance, '_prefetched_objects_cache'):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)
    
def NotifieCreateTeam(request, team, team_members_ids):
    user = request.user
    
    notification = Notification.objects.create(
        Relation=Notification.relation.Team,
        content_type=ContentType.objects.get_for_model(Team_members),
        object_id=team.id,
        Message=f"{user.first_name} {user.last_name} Added {team.User.first_name} {team.User.last_name} to {team.Project.Num_Appele_dOffer} {team.Project.Client.Name} team",
        Date_Time=timezone.now(),
    )
    SendNotifications(notification,user,team_members_ids,
                      f"Team changes {team.Project.Num_Appele_dOffer} {team.Project.Client.Name}",
                      f"{user.first_name} {user.last_name} Added {team.User.first_name} {team.User.last_name} to {team.Project.Num_Appele_dOffer} {team.Project.Client.Name} team"
                      ,False,False,True)

def NotifieUpdateTeam(request, team, team_members_ids): # --
    user = request.user

    notification = Notification.objects.create(
        Relation=Notification.relation.Team,
        content_type=ContentType.objects.get_for_model(Team_members),
        object_id=team.id,
        Message=f"{user.first_name} {user.last_name} Add Note to {team.User.first_name} {team.User.last_name} in {team.Project.Num_Appele_dOffer} {team.Project.Client.Name} team",
        Date_Time=timezone.now(),
    )
    SendNotifications(notification,user,team_members_ids,
                      f"Team changes {team.Project.Num_Appele_dOffer} {team.Project.Client.Name}",
                      f"{user.first_name} {user.last_name} Add Note to {team.User.first_name} {team.User.last_name} in {team.Project.Num_Appele_dOffer} {team.Project.Client.Name} team"
                      ,False,False,True)

# Home Page
class HomePageViewTache(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        current_date = timezone.now()

        if user.Role.Project_Show == 2:
            role_conditions = {
                (True, True, False): Q(Etape_S__in=[1, 2]) | Q(team_members__User=user),
                (True, False, True): Q(Etape_S__in=[1, 3]) | Q(team_members__User=user),
                (True, False, False): Q(Etape_S=1) | Q(team_members__User=user),
                (False, True, True): Q(Etape_S__in=[2, 3]) | Q(team_members__User=user),
                (False, True, False): Q(Etape_S=2) | Q(team_members__User=user),
                (False, False, True): Q(Etape_S=3) | Q(team_members__User=user),
            }

            condition = role_conditions.get(
                (
                    user.Role.Project_1 >= 1,
                    user.Role.Project_2 >= 1,
                    user.Role.Project_3 >= 1,
                    user.Role.Project_4 >= 1,
                    user.Role.Project_5 >= 1,
                ),
                Q()
            )
            Team_Projects = Project.objects.filter(condition, State__in=[1, 2, 3]).distinct()
        else:
            Team_Projects = Project.objects.filter(team_members__User=user, State__in=[1, 2, 3]).distinct()

        Etapes_Project_ids = Etape.objects.filter(Project__in=Team_Projects).values_list("id", flat=True)

        Tache_To_id = set(Tache_To.objects.filter(Role=user.Role).values_list("Tache_Def", flat=True))
        Tache_receve_id = set(Tache_receve.objects.filter(Role=user.Role).values_list("Tache_Def", flat=True))
        Tache_superviser_id = set(Tache_superviser.objects.filter(Role=user.Role).values_list("Tache_Def", flat=True))

        all_tache_defs = Tache_To_id | Tache_receve_id | Tache_superviser_id

        Your_Taches_Q = (
            Tache.objects.filter(Etape__in=Etapes_Project_ids, Tache_Def__in=Tache_To_id)
            .select_related("Etape", "Tache_Def")
        )

        Your_Taches = list(
            Your_Taches_Q.order_by("Date_start")
        )

        in_progress = [t for t in Your_Taches if t.State == Tache.state.In_progress]
        can_start   = [t for t in Your_Taches if t.State == Tache.state.Waiting and t.can_start()]
        finished    = [t for t in Your_Taches if t.State == Tache.state.Finished]

        Your_Taches = in_progress + can_start + finished

        All_Taches_qs = (
            Tache.objects.filter(Etape__in=Etapes_Project_ids, Tache_Def__in=all_tache_defs)
            .select_related("Etape", "Tache_Def")
            .annotate(
                priority=Case(
                    When(State=Tache.state.In_progress, then=0),
                    When(State=Tache.state.Waiting, then=1),
                    When(State=Tache.state.Finished, then=2),
                    output_field=IntegerField(),
                )
            )
            .order_by("priority", "Date_start")
        )

        if All_Taches_qs.count() > 100:
            # Only keep a limited number of tasks (fast slicing)
            All_Taches = list(All_Taches_qs[:150])
            # still check can_start() only for waiting ones
            waiting_tasks = [t for t in All_Taches if t.State == Tache.state.Waiting and t.can_start()]
            All_Taches = [t for t in All_Taches if t.State != Tache.state.Waiting] + waiting_tasks
        else:
            All_Taches = list(All_Taches_qs)

        Tache_Types = ["Initial", "Instent", "Final", "Documented", "Forme", "Decision", "mail", "Simple", "Complex", "Info"]
        tachedef_ids = Tache_Def.objects.filter(deleted=False, Type__in=Tache_Types).values_list("id", flat=True)
        start_of_month = current_date.replace(day=1)

        stats = Tache.objects.filter(Date_start__gte=start_of_month, Tache_Def__in=tachedef_ids).aggregate(
            Completed_Taches=Count("id", filter=Q(State=Tache.state.Finished)),
            ToDo_Taches=Count("id", filter=Q(State=Tache.state.In_progress)),
        )

        your_stats = Your_Taches_Q.filter(Date_start__gte=start_of_month, Tache_Def__in=tachedef_ids).aggregate(
            Your_Taches_count=Count("id"),
            Your_Completed_Taches=Count("id", filter=Q(State=Tache.state.Finished)),
            Your_ToDo_Taches=Count("id", filter=Q(State=Tache.state.In_progress)),
        )

        data = {
            "Totale_Taches": stats["Completed_Taches"] + stats["ToDo_Taches"],
            "Completed_Taches": stats["Completed_Taches"],
            "ToDo_Taches": stats["ToDo_Taches"],
            "Your_Taches_count": your_stats["Your_Taches_count"],
            "Your_Completed_Taches": your_stats["Your_Completed_Taches"],
            "Your_ToDo_Taches": your_stats["Your_ToDo_Taches"],
            "Your_Taches": TacheSerializerPlusMois(Your_Taches, many=True).data,
            "All_Taches": TacheSerializerPlusMois(All_Taches, many=True).data,
        }

        return Response(data)

class HomePageViewProject(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Projects Filter
        if user.Role.Project_Show == 2:
            role_conditions = {
                (True, True, False): Q(Etape_S__in=[1, 2]) | Q(team_members__User=user),
                (True, False, True): Q(Etape_S__in=[1, 3]) | Q(team_members__User=user),
                (True, False, False): Q(Etape_S=1) | Q(team_members__User=user),
                (False, True, True): Q(Etape_S__in=[2, 3]) | Q(team_members__User=user),
                (False, True, False): Q(Etape_S=2) | Q(team_members__User=user),
                (False, False, True): Q(Etape_S=3) | Q(team_members__User=user),
            }

            condition = role_conditions.get(
                (user.Role.Project_1 >= 1, 
                 user.Role.Project_2 >= 1, 
                 user.Role.Project_3 >= 1),
                Q()
            )

            Team_Projects = Project.objects.filter(condition, State__in=[1,2,3]).distinct()
        else:
            Team_Projects = Project.objects.filter(team_members__User=user, State__in=[1,2,3]).distinct()

        Team_ProjectsF = Team_Projects.order_by("-Date_Depot",'id')[:100]

        return Response(ProjectSerializerHome(Team_ProjectsF, many=True).data)

class HomePageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        current_year = timezone.now().year

        if user.Role.Project_Show == 2:
            role_conditions = {
                (True, True, False): Q(Etape_S__in=[1, 2]) | Q(team_members__User=user),
                (True, False, True): Q(Etape_S__in=[1, 3]) | Q(team_members__User=user),
                (True, False, False): Q(Etape_S=1) | Q(team_members__User=user),
                (False, True, True): Q(Etape_S__in=[2, 3]) | Q(team_members__User=user),
                (False, True, False): Q(Etape_S=2) | Q(team_members__User=user),
                (False, False, True): Q(Etape_S=3) | Q(team_members__User=user),
            }

            condition = role_conditions.get(
                (user.Role.Project_1 >= 1, 
                 user.Role.Project_2 >= 1, 
                 user.Role.Project_3 >= 1),
                Q()
            )

            Team_Projects = Project.objects.filter(condition, State__in=[1,2,3]).distinct()
        else:
            Team_Projects = Project.objects.filter(team_members__User=user, State__in=[1,2,3]).distinct()

        unfixed_problems = Problem.objects.filter(
            Tache__Etape__Project__in=Team_Projects,
            State=1
        ).select_related(
            "Tache", "Tache__Etape", "Tache__Etape__Project"
        ).order_by("-Date")[:100]

        remaining_count = 100 - unfixed_problems.count()
        if remaining_count > 0:
            fixed_problems = Problem.objects.filter(
                Tache__Etape__Project__in=Team_Projects
            ).exclude(State=1).select_related(
                "Tache", "Tache__Etape", "Tache__Etape__Project"
            ).order_by("-Date")[:remaining_count]
        else:
            fixed_problems = Problem.objects.none()

        problems = list(unfixed_problems) + list(fixed_problems)

        # Generale numericale stat
        Totale_Projects = Project.objects.count()
        Year_Projects = Project.objects.filter(Date_start__year=current_year).count()
        Your_Projects = Team_Projects.count()
        Your_Year_Projects = Team_Projects.filter(Date_start__year=current_year).count()
        shortliste_Projects = Project.objects.filter(Status=4).count()
        shortliste_Projects_year = Project.objects.filter(Status=4, Date_start__year=current_year).count()
        Positionne_Projects = Project.objects.filter(
            data_project__Def_data_Project__Name="Positionne ?", data_project__Value="1"
        ).distinct().count()
        Positionne_Projects_year = Project.objects.filter(
            data_project__Def_data_Project__Name="Positionne ?", data_project__Value="1",
            Date_start__year=current_year
        ).distinct().count()
        clients = Client.objects.all()
        fourniseur = Fourniseur.objects.all()

        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        top_users = History.objects.filter(Date__gte=start_of_week).values('User').annotate(
            activity_count=Count('User')
        ).order_by('-activity_count')[:10]
        top_users_data = [
            {
                "user": UserSerializerMois(User.objects.get(id=user['User'])).data,
                "activity_count": user['activity_count']
            }
            for user in top_users
        ]

        Team_ProjectsF = Team_Projects.order_by("-Date_Depot",'id')[:50]

        data = {
            "Totale_Projects": Totale_Projects,
            "Year_Projects": Year_Projects,
            "Your_Projects": Your_Projects,
            "Your_Year_Projects": Your_Year_Projects,
            "shortliste_Projects": shortliste_Projects,
            "shortliste_Projects_year": shortliste_Projects_year,
            "Positionne_Projects": Positionne_Projects,
            "Positionne_Projects_year": Positionne_Projects_year,
            "clients": ClientSerializer(clients, many=True).data,
            "fourniseur": FourniseurSerializer(fourniseur, many=True).data,
            "Team_Project": ProjectSerializerMoin(Team_ProjectsF, many=True).data,
            "problems": ProblemSerializerHome(problems, many=True).data,
            "top_users": top_users_data,
        }

        return Response(data)

class HomePageViewChart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Type = request.GET.get("Type", "1")
        page_param = request.GET.get("Page")
        try:
            page = int(page_param) if page_param and page_param.isdigit() else 1
        except (TypeError, ValueError):
            page = 1
        order = request.GET.get("order", "-Date_start")  # default order
        user = self.request.user

        if user.Role.Project_Show == 2:
            role_conditions = {
                (True, True, False): Q(Etape_S__in=[1, 2]) | Q(team_members__User=user),
                (True, False, True): Q(Etape_S__in=[1, 3]) | Q(team_members__User=user),
                (True, False, False): Q(Etape_S=1) | Q(team_members__User=user),
                (False, True, True): Q(Etape_S__in=[2, 3]) | Q(team_members__User=user),
                (False, True, False): Q(Etape_S=2) | Q(team_members__User=user),
                (False, False, True): Q(Etape_S=3) | Q(team_members__User=user),
            }

            condition = role_conditions.get(
                (user.Role.Project_1 >= 1, 
                 user.Role.Project_2 >= 1, 
                 user.Role.Project_3 >= 1,
                 user.Role.Project_4 >= 1,
                 user.Role.Project_5 >= 1,),
                Q()
            )

            Team_Projects = Project.objects.filter(condition, State__in=[1,2,3]).distinct()
        else:
            Team_Projects = Project.objects.filter(team_members__User=user, State__in=[1,2,3]).distinct()

        if Type == "1":
            queryset = Team_Projects.filter(Etape_S=1)
        elif Type == "2":
            queryset = Team_Projects.filter(Etape_S=2)
        elif Type == "3":
            queryset = Team_Projects.filter(Etape_S=3)
        elif Type == "4":
            queryset = Team_Projects.filter(Etape_S=4)
        elif Type == "5":
            queryset = Team_Projects.filter(Etape_S=5)
        else:
            queryset = Team_Projects

        queryset = queryset.order_by(order)

        page_size = 10
        start = (page - 1) * page_size
        end = page * page_size
        Projects = queryset[start:end]

        labels = [
            (project.Client.Name + ' ' + project.Num_Appele_dOffer)[:17] + '...'
            if len(project.Client.Name + ' ' + project.Num_Appele_dOffer) > 20
            else (project.Client.Name + ' ' + project.Num_Appele_dOffer)
            for project in Projects
        ]

        real_progress_data = []
        predicted_progress_data = []
        current_date = timezone.now()

        for project in Projects:
            real, predicted = project.get_progress(current_date)
            real_progress_data.append(real)
            predicted_progress_data.append(predicted)

        chart_data = {
            "labels": labels,
            "datasets": [
                {"label": "Progress", "data": real_progress_data, "backgroundColor": "#089B9B"},
                {"label": "Time Passed", "data": predicted_progress_data, "backgroundColor": "#F8988B"},
            ],
        }
        total_items = queryset.count()
        total_pages = ceil(total_items / page_size) if page_size else 1

        return Response({
            "chart": {"bar_chart_data": chart_data},
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages
            }
        })

class HomePageViewPie(APIView):
    def get(self, request):
        Type = request.GET.get("Type", "Status")
        
        type_mapping = {
            "Status": "Status",
            "State": "State",
            "Etape_S": "Etape_S"
        }

        if Type not in type_mapping:
            return Response({"error": "Invalid Type"}, status=400)

        chart_data = Project.objects.values(type_mapping[Type]).annotate(count=Count("id"))

        labels = []
        data = []
        backgroundColors = ["#a75c82","#c9a7be","#DACDDC","#ebf2fa", "#97b6ce" ]

        for entry in chart_data:
            category_value = entry[type_mapping[Type]]
            count = entry["count"]

            if Type == "Status":
                label = Project.status(category_value).label
            elif Type == "State":
                label = Project.state(category_value).label
            elif Type == "Etape_S":
                label = Project.etape(category_value).label
            else:
                label = str(category_value)

            labels.append(label)
            data.append(count)

        response_data = {
            "labels": labels,
            "datasets": [
                {
                    "label": f"Project {Type}",
                    "data": data,
                    "backgroundColor": backgroundColors[:len(data)],
                }
            ]
        }

        return Response(response_data)

class ExtractEpoch(Func):
    function = "EXTRACT"
    template = "%(function)s(EPOCH FROM %(expressions)s)"
    output_field = FloatField()
qs = Tache.objects.annotate(
    duration_seconds=ExtractEpoch(F("Date_End") - F("Date_start"))
)
class NullIf(Func):
    function = 'NULLIF'
    arity = 2 
class GetProblemPie(APIView):
    def get(self, request):
        chart_type = request.GET.get("Type", "")

        colors = ["#BF9CB1","#B690A7", "#AE849E", "#A67794", "#A67794"]

        if chart_type == "Problem Prj":
            project_problems = (
                Problem.objects.values(
                    "Tache__Etape__Project__id",
                    "Tache__Etape__Project__Num_Appele_dOffer",
                    "Tache__Etape__Project__Client__Name"
                )
                .annotate(problem_count=Count("id"))
                .order_by("-problem_count")[:5]
            )

            data = {
                "labels": [
                    p["Tache__Etape__Project__Num_Appele_dOffer"] + " " +
                    p["Tache__Etape__Project__Client__Name"]
                    for p in project_problems
                ],
                "datasets": [
                    {
                        "label": "Top 5 Projects with Problems",
                        "data": [p["problem_count"] for p in project_problems],
                        "backgroundColor": colors[:len(project_problems)],
                    }
                ],
            }

        elif chart_type == "Problem cat":
            problem_categories = (
                Problem.objects.values("Type")
                .annotate(problem_count=Count("id"))
                .order_by("-problem_count")
            )

            type_labels = {1: "Banque", 2: "Fournisseur", 3:"nécessite d'avenant", 4:"Autre"}

            data = {
                "labels": [type_labels.get(p["Type"], "Unknown") for p in problem_categories],
                "datasets": [
                    {
                        "label": "Problems by Category",
                        "data": [p["problem_count"] for p in problem_categories],
                        "backgroundColor": colors[:len(problem_categories)],
                    }
                ],
            }

        elif chart_type == "Problem Etp":
            etape_defs = (
                Etape.objects.values("Etape_def__Name")
                .annotate(etape_count=Count("id"))
                .order_by("-etape_count")[:5]
            )

            data = {
                "labels": [e["Etape_def__Name"] for e in etape_defs],
                "datasets": [
                    {
                        "label": "Most Etapes",
                        "data": [e["etape_count"] for e in etape_defs],
                        "backgroundColor": colors[:len(etape_defs)],
                    }
                ],
            }

        elif chart_type == "retard Prj":
            projects = (
                Project.objects.annotate(
                    total_tache_duration=Coalesce(
                        Sum(
                            ExtractEpoch(
                                Coalesce(
                                    F("etape__tache__Max_Duration"),
                                    F("etape__tache__Tache_Def__Duration")
                                )
                            )
                        ),
                        0.0,
                        output_field=FloatField()
                    ),
                    total_real_duration = Coalesce(
                        Sum(
                            Case(
                                When(
                                    etape__tache__Date_start__isnull=False,
                                    then=ExtractEpoch(
                                        Coalesce(F("etape__tache__Date_End"), Now()) - F("etape__tache__Date_start")
                                    )
                                ),
                                default=Value(0.0),
                                output_field=FloatField(),
                            )
                        ),
                        0.0,
                        output_field=FloatField()
                    )
                )
                .annotate(
                    progress_diff=ExpressionWrapper(
                        (F("total_real_duration") - F("total_tache_duration")) * 100.0 /
                        NullIf(F("total_tache_duration"), 0.0),
                        output_field=FloatField()
                    )
                )
                .order_by("-progress_diff")[:5]
            )
            data = {
                "labels": [p.Num_Appele_dOffer+" "+p.Client.Name for p in projects],
                "datasets": [
                    {
                        "label": "Top 5 Projects with Delay",
                        "data": [p.progress_diff for p in projects],
                        "backgroundColor": colors[:len(projects)],
                    }
                ],
            }
        else:
            return Response({"error": "Invalid Type parameter"}, status=400)

        return Response(data)

# Stat page
class StatePageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_year = timezone.now().year

        Totale_Projects = Project.objects.count()
        Year_Projects = Project.objects.filter(Date_start__year=current_year).count()
        Perdus_Projects = Project.objects.filter(Status=3).count()
        Year_Perdus_Projects = Project.objects.filter(Status=3, Date_start__year=current_year).count()
        shortliste_Projects = Project.objects.filter(Status=4).count()
        shortliste_Projects_year = Project.objects.filter(Status=4, Date_start__year=current_year).count()
        Positionne_Projects = Project.objects.filter(
            data_project__Def_data_Project__Name="Positionne ?", data_project__Value="1"
        ).distinct().count()
        Positionne_Projects_year = Project.objects.filter(
            data_project__Def_data_Project__Name="Positionne ?", data_project__Value="1",
            Date_start__year=current_year
        ).distinct().count()

        Roles = ['AM','AV']
        users = User.objects.annotate(
            project_count=Count("team_members__Project", distinct=True)
        ).filter(Role__Name__in=Roles)

        users_serialized = UserWithProjectCountSerializer(users, many=True).data

        data = {
            "Totale_Projects": Totale_Projects,
            "Year_Projects": Year_Projects,
            "Perdus_Projects": Perdus_Projects,
            "Year_Perdus_Projects": Year_Perdus_Projects,
            "shortliste_Projects": shortliste_Projects,
            "shortliste_Projects_year": shortliste_Projects_year,
            "Positionne_Projects": Positionne_Projects,
            "Positionne_Projects_year": Positionne_Projects_year,
            "Users_Projects": users_serialized,
        }

        return Response(data)


