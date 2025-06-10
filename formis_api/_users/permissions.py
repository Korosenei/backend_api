from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """Seuls les SuperAdmins peuvent exécuter certaines actions."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "SUPER_ADMIN"

class IsAdmin(BasePermission):
    """Seuls les Admins peuvent ajouter des enseignants et chefs de département."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["ADMIN", "SUPER_ADMIN"]

class IsChefDepartement(BasePermission):
    """Seuls les chefs de département peuvent ajouter des enseignants et apprenants."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["CHEF_DEPARTEMENT", "ADMIN", "SUPER_ADMIN"]
