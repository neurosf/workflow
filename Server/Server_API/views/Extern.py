from ..models import * 
from ..serializers import * 
from rest_framework.generics import  ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import *
# 6 class view
# Client

class ClientListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializerPlus
    permission_classes = [IsAuthenticated]

class ClientCreateView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class ClientRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
# Client_Contact

class Client_ContactListCreateView(ListCreateAPIView):
    queryset = Client_Contact.objects.all()
    serializer_class = Client_ContactSerializer
    permission_classes = [IsAuthenticated]

class Client_ContactRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Client_Contact.objects.all()
    serializer_class = Client_ContactSerializer
    permission_classes = [IsAuthenticated]

# Fourniseur
class FourniseurListView(ListAPIView):
    queryset = Fourniseur.objects.all()
    serializer_class = FourniseurSerializerPlus
    permission_classes = [IsAuthenticated]

class FourniseurCreateView(CreateAPIView):
    queryset = Fourniseur.objects.all()
    serializer_class = FourniseurSerializer
    permission_classes = [IsAuthenticated]

class FourniseurRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Fourniseur.objects.all()
    serializer_class = FourniseurSerializer
    permission_classes = [IsAuthenticated]
# Fourniseur_Contact

class Fourniseur_ContactListCreateView(ListCreateAPIView):
    queryset = Fourniseur_Contact.objects.all()
    serializer_class = Fourniseur_ContactSerializer
    permission_classes = [IsAuthenticated]

class Fourniseur_ContactRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Fourniseur_Contact.objects.all()
    serializer_class = Fourniseur_ContactSerializer
    permission_classes = [IsAuthenticated]
# fournisseur_data

class fournisseur_dataListCreateView(ListCreateAPIView):
    queryset = fournisseur_data.objects.all()
    serializer_class = fournisseur_dataSerializer
    permission_classes = [IsAuthenticated]

class fournisseur_dataRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = fournisseur_data.objects.all()
    serializer_class = fournisseur_dataSerializer
    permission_classes = [IsAuthenticated,HaseEtapeMyPermission]

