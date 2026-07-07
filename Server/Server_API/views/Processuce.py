from ..models import * 
from ..serializers import * 
from rest_framework.generics import  ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import *
# 10 class view
# Processuce

class ProcessuceListCreateView(ListCreateAPIView):
    queryset = Processuce.objects.all()
    serializer_class = ProcessuceSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class ProcessuceRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Processuce.objects.all()
    serializer_class = ProcessuceSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# Def_Processuce
class Def_ProcessuceListView(ListAPIView):
    queryset = Def_Processuce.objects.all()
    serializer_class = Def_ProcessuceSerializerPlus
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class Def_ProcessuceCreateView(CreateAPIView):
    queryset = Def_Processuce.objects.all()
    serializer_class = Def_ProcessuceSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class Def_ProcessuceRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Def_Processuce.objects.all()
    serializer_class = Def_ProcessuceSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# Tache_P

class Tache_PListCreateView(ListCreateAPIView):
    queryset = Tache_P.objects.all()
    serializer_class = Tache_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class Tache_PRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_P.objects.all()
    serializer_class = Tache_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# Tache_Def_P
class Tache_Def_PListView(ListAPIView):
    queryset = Tache_Def_P.objects.all()
    serializer_class = Tache_Def_PSerializerPlus
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
    
class Tache_Def_PCreateView(CreateAPIView):
    queryset = Tache_Def_P.objects.all()
    serializer_class = Tache_Def_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class Tache_Def_PRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_Def_P.objects.all()
    serializer_class = Tache_Def_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# Tache_To_P

class Tache_To_PListCreateView(ListCreateAPIView):
    queryset = Tache_To_P.objects.all()
    serializer_class = Tache_To_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class Tache_To_PRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_To_P.objects.all()
    serializer_class = Tache_To_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# Tache_receve_P

class Tache_receve_PListCreateView(ListCreateAPIView):
    queryset = Tache_receve_P.objects.all()
    serializer_class = Tache_receve_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class Tache_receve_PRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tache_receve_P.objects.all()
    serializer_class = Tache_receve_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# TacheDependency_P

class TacheDependency_PListCreateView(ListCreateAPIView):
    queryset = TacheDependency_P.objects.all()
    serializer_class = TacheDependency_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class TacheDependency_PRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = TacheDependency_P.objects.all()
    serializer_class = TacheDependency_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# Tach_Data_P

class Tach_Data_PListCreateView(ListCreateAPIView):
    queryset = Tach_Data_P.objects.all()
    serializer_class = Tach_Data_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class Tach_Data_PRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tach_Data_P.objects.all()
    serializer_class = Tach_Data_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# Tach_Data_def_P

class Tach_Data_def_PListCreateView(ListCreateAPIView):
    queryset = Tach_Data_def_P.objects.all()
    serializer_class = Tach_Data_def_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class Tach_Data_def_PRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Tach_Data_def_P.objects.all()
    serializer_class = Tach_Data_def_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# File_P

class File_PListCreateView(ListCreateAPIView):
    queryset = File_P.objects.all()
    serializer_class = File_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class File_PRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = File_P.objects.all()
    serializer_class = File_PSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
# Template

class TemplateListCreateView(ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]

class TemplateRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated,HaseProcessucePermission]
