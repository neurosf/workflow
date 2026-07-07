from rest_framework.permissions import BasePermission
from django.db.models import Q

class HaseUserPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.User == 1:
            return request.method in ('GET',)
        
        if user_role.User == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    
class HaseRolePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Role == 1:
            return request.method in ('GET',)
        
        if user_role.Role == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    
class HaseServicePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Service == 1:
            return request.method in ('GET',)
        
        if user_role.Service == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseStructure_ProjectPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Structure_Project == 1:
            return request.method in ('GET',)
        
        if user_role.Structure_Project == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseClientPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Client == 1:
            return request.method in ('GET',)
        
        if user_role.Client == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseFournisseurPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Fournisseur == 1:
            return request.method in ('GET',)
        
        if user_role.Fournisseur == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseProjectShowTeamPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role
        
        if user_role.Project_Show >= 1:
            return request.method in ('GET',) 

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view )
    
class HaseProjectShowAllPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role
        
        if user_role.Project_Show >= 1:
            return request.method in ('GET',) 

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view )  
      
class HaseProjectAddPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Project_Add == 1:
            return request.method in ('POST')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view )
    
class HaseProjectMyPermission1(BasePermission):
    """
    Custom permission to allow access to projects based on the user's permissions
    for each Etape_S (Soumission, Affaire, Projet) and team membership.
    """

    def has_permission(self, request, view):
        # Only allow if authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj: the Project instance
        Checks if the user has permission for the project's Etape_S or is a team member.
        """
        user = request.user
        if not user.is_authenticated:
            return False

        # Map Etape_S to user role permission field
        etape_map = {
            1: 'Project_1',
            2: 'Project_2',
            3: 'Project_3',
        }
        etape_field = etape_map.get(getattr(obj, 'Etape_S', None))
        if not etape_field:
            return False

        # Check if user has permission for this Etape_S
        has_etape_perm = getattr(user.Role, etape_field, 0) >= 1

        # Check if user is a team member
        is_team_member = hasattr(obj, 'team_members') and user in obj.team_members.all()

        # Allow GET if user has permission or is a team member
        if request.method in ('GET',):
            return has_etape_perm or is_team_member

        # Allow write if user has permission for this Etape_S
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return has_etape_perm

        return False
    
class HaseProjectMyPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = getattr(request.user, 'Role', None)
        if not user_role:
            return False
        
        if user_role.Etape >= 2 and request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return self.has_permission(request, view)

class HaseEtapeMyPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Etape >= 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        if user_role.Etape >= 1:
            return request.method in ('GET',)
        
        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    
class HaseEtapeALLPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Etape >= 4:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        if user_role.Etape >= 3:
            return request.method in ('GET',)
        
        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    
class HaseEtapeValidePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Etape == 4:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseProcessucePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Processuce == 1:
            return request.method in ('GET',)
        
        if user_role.Processuce == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseFilesPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Files == 1:
            return request.method in ('GET',)
        
        if user_role.Files == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseTeamPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Team == 1:
            return request.method in ('GET',)
        
        if user_role.Team == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseRefancePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Refance == 1:
            return request.method in ('GET',)
        
        if user_role.Refance == 2:
            return request.method in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseStatPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Stat == 1:
            return request.method in ('GET',)

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class HaseHistoriquePermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.Role

        if user_role.Historique == 1:
            return request.method in ('GET',)

        return False
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
