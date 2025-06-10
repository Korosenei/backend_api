from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Utilisateur, Grade, Domaine, TypeEnseignant, Enseignant, ChefDepartement, Apprenant
from .serializers import (
    UtilisateurSerializer, GradeSerializer, DomaineSerializer, TypeEnseignantSerializer,
    EnseignantSerializer, ChefDepartementSerializer, ApprenantSerializer
)
from .permissions import IsSuperAdmin, IsAdmin, IsChefDepartement

# Create your views here.

# Vue API pour les utilisateurs
class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def current_user(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
        }

        # Ajouter les données spécifiques au profil
        if hasattr(user, 'profil_enseignant'):
            enseignant = user.profil_enseignant
            data['profil_enseignant'] = {
                'utilisateur': enseignant.utilisateur.username,
                'matricule': enseignant.matricule,
                'nom': enseignant.nom,
                'prenom': enseignant.prenom,
                'grade': enseignant.grade.nom if enseignant.grade else None,
                'domaine': enseignant.domaine.nom if enseignant.domaine else None,
                'type_enseignant': enseignant.type_enseignant.nom if enseignant.type_enseignant else None,
                'photo': request.build_absolute_uri(enseignant.photo.url) if enseignant.photo else None
            }
        elif hasattr(user, 'profil_apprenant'):
            apprenant = user.profil_apprenant
            data['profil_apprenant'] = {
                'utilisateur': apprenant.utilisateur.username,
                'matricule': apprenant.matricule,
                'nom': apprenant.nom,
                'prenom': apprenant.prenom,
                'departement': apprenant.departement.nom if apprenant.departement else None,
                'photo': request.build_absolute_uri(apprenant.photo.url) if apprenant.photo else None,
                'frais_paye': apprenant.frais_paye
            }

        return Response(data)


# Vue API pour les grades
class GradeViewSet(viewsets.ModelViewSet):
    """
    Gestion des grades des enseignants.
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]


# Vue API pour les domaines
class DomaineViewSet(viewsets.ModelViewSet):
    """
    Gestion des domaines d'enseignement.
    """
    queryset = Domaine.objects.all()
    serializer_class = DomaineSerializer
    permission_classes = [permissions.IsAuthenticated]


# Vue API pour les types d’enseignants
class TypeEnseignantViewSet(viewsets.ModelViewSet):
    """
    Gestion des types d'enseignants.
    """
    queryset = TypeEnseignant.objects.all()
    serializer_class = TypeEnseignantSerializer
    permission_classes = [permissions.IsAuthenticated]


# Vue API pour les enseignants
class EnseignantViewSet(viewsets.ModelViewSet):
    """
    Gestion des enseignants (ajouté par l'Admin ou Chef de Département).
    """
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer
    permission_classes = [IsAdmin | IsChefDepartement]  # Seul un Admin ou un Chef de Département peut ajouter

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['grade', 'domaine']  # Permet de filtrer par grade ou domaine

# Vue API pour les chefs de département
class ChefDepartementViewSet(viewsets.ModelViewSet):
    """
    Gestion des Chefs de Département (ajouté par l'Admin).
    """
    queryset = ChefDepartement.objects.all()
    serializer_class = ChefDepartementSerializer
    permission_classes = [IsAdmin]  # Seuls les Admins peuvent gérer les chefs de département


# Vue API pour les apprenants
class ApprenantViewSet(viewsets.ModelViewSet):
    """
    Gestion des apprenants (ajouté par le Chef de Département uniquement).
    """
    queryset = Apprenant.objects.all()
    serializer_class = ApprenantSerializer
    permission_classes = [IsChefDepartement]  # Seul le Chef de Département peut ajouter des apprenants

