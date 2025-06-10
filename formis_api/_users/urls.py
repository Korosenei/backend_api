from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'utilisateurs'

# Router DRF
router = DefaultRouter()
router.register(r'grades', views.GradeViewSet)
router.register(r'domaines', views.DomaineViewSet)
router.register(r'types-enseignants', views.TypeEnseignantViewSet)
router.register(r'enseignants', views.EnseignantViewSet)
router.register(r'chefs-departement', views.ChefDepartementViewSet)
router.register(r'apprenants', views.ApprenantViewSet)
router.register(r'utilisateurs', views.UtilisateurViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('current-user/', views.UtilisateurViewSet.as_view({'get': 'current_user'}), name='current-user'),
]
