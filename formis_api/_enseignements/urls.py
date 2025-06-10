from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


app_name = '_enseignements'

router = DefaultRouter()
router.register(r'localites', views.LocaliteViewSet)
router.register(r'types-etablissements', views.TypeEtablissementViewSet)
router.register(r'statuts-etablissements', views.StatutEtablissementViewSet)
router.register(r'etablissements', views.EtablissementViewSet)
router.register(r'departements', views.DepartementViewSet)
router.register(r'filieres', views.FiliereViewSet)
router.register(r'specialites', views.SpecialiteViewSet)
router.register(r'niveaux', views.NiveauViewSet)
router.register(r'semestres', views.SemestreViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'matieres', views.MatiereViewSet)
router.register(r'classes', views.ClasseViewSet)
router.register(r'ressources-pdf', views.RessourcePdfViewSet)
router.register(r'ressources-video', views.RessourceVideoViewSet)

urlpatterns = router.urls
