from ..models import * 
from ..serializers import * 
from rest_framework.generics import  ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import *
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# 4 class view

# Role
class RoleListView(ListAPIView):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializermois
    permission_classes = [IsAuthenticated,HaseRolePermission]
    
class RoleCreateView(ListCreateAPIView):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated,HaseRolePermission]

class RoleRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated,HaseRolePermission]

# Service
class ServiceListView(ListAPIView):
    queryset = Service.objects.all().order_by('id')
    serializer_class = ServiceSerializerPlus
    permission_classes = [IsAuthenticated,HaseServicePermission]

class ServiceCreateView(CreateAPIView):
    queryset = Service.objects.all().order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated,HaseServicePermission]

class ServiceRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all().order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated,HaseServicePermission]

# Notification

class NotificationListView(ListAPIView):
    serializer_class = Notification_toSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification_to.objects.filter(To=user).exclude(Notification_id__object_id=None).order_by('Notification__Date_Time') # ?????
    
class NotificationRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Notification_to.objects.all().order_by('Notification__Date_Time')
    serializer_class = Notification_toSerializerS
    permission_classes = [IsAuthenticated]

###
@api_view(['POST'])
def request_email_sending_authorization(request):
    try:
        # Step 1: Get access token from Auth0
        token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        token_payload = {
            "client_id": settings.AUTH0_CLIENT_ID,
            "client_secret": settings.AUTH0_CLIENT_SECRET,
            "audience": settings.AUTH0_API_AUDIENCE,
            "grant_type": "client_credentials"
        }

        token_response = requests.post(token_url, json=token_payload)
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")

        if not access_token:
            return Response({"error": "Failed to retrieve access token."}, status=500)

        # Step 2: Send the authorization request to the external API
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        api_payload = {
            "requested_by": request.user.email if request.user.is_authenticated else "unknown",
            "reason": "Enable sending automated workflow notifications via email"
        }

        api_response = requests.post(settings.AUTH0_AUTH_ENDPOINT, json=api_payload, headers=headers)
        api_response.raise_for_status()

        return Response({
            "message": "Authorization request sent successfully.",
            "response": api_response.json()
        })

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)