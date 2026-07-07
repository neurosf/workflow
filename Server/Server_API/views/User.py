from django.shortcuts import get_object_or_404
from ..models import * 
from ..serializers import * 
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.generics import  ListCreateAPIView,RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView,ListAPIView,DestroyAPIView
from django.http.response import JsonResponse 
from rest_framework.parsers import JSONParser 
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from dateutil.relativedelta import relativedelta
from datetime import date
from scipy.stats import chi2
from rest_framework import status
from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..permissions import *
import os

# 7 class view

class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, HaseUserPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializerPlus(user)
        return Response(serializer.data)
    
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, HaseUserPermission]

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)

        if 'image' in request.FILES:
            if user.image and os.path.isfile(user.image.path):
                os.remove(user.image.path)
            user.image = request.FILES['image']

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserListAPIViewM(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializerPlusMois
    
class UserListAPIViewPM(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializerPlus
    
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HaseUserPermission]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.image and os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
# work_Offer

class work_OfferListCreateView(ListCreateAPIView):
    queryset = work_Offer.objects.all()
    serializer_class = work_OfferSerializer
    permission_classes = [IsAuthenticated]

class work_OfferRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = work_Offer.objects.all()
    serializer_class = work_OfferSerializer
    permission_classes = [IsAuthenticated]

# Formation

class FormationListCreateView(ListCreateAPIView):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    permission_classes = [IsAuthenticated]

class FormationRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    permission_classes = [IsAuthenticated]

# CV

class CVListCreateView(ListCreateAPIView):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]

class CVRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]

# Post

class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

# History_Post

class History_PostListCreateView(ListCreateAPIView):
    queryset = History_Post.objects.all()
    serializer_class = History_PostSerializer
    permission_classes = [IsAuthenticated]

class History_PostRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = History_Post.objects.all()
    serializer_class = History_PostSerializer
    permission_classes = [IsAuthenticated]

# Demmanede_Conge

class Demmanede_CongeListCreateView(ListCreateAPIView):
    queryset = Demmanede_Conge.objects.all()
    serializer_class = Demmanede_CongeSerializer
    permission_classes = [IsAuthenticated]

class Demmanede_CongeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Demmanede_Conge.objects.all()
    serializer_class = Demmanede_CongeSerializer
    permission_classes = [IsAuthenticated]

# Groupe

class GroupeListCreateView(ListCreateAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticated]

class GroupeListView(ListAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializerPlus
    permission_classes = [IsAuthenticated]

class GroupeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticated]

# User_Groupe

class User_GroupeListCreateView(ListCreateAPIView):
    queryset = User_Groupe.objects.all()
    serializer_class = User_GroupeSerializer
    permission_classes = [IsAuthenticated]

class User_GroupeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = User_Groupe.objects.all()
    serializer_class = User_GroupeSerializer
    permission_classes = [IsAuthenticated]
