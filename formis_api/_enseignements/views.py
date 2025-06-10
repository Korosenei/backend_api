from rest_framework import viewsets, permissions
from .models import *
from .serializers import *

class LocaliteViewSet(viewsets.ModelViewSet):
    queryset = Localite.objects.all()
    serializer_class = LocaliteSerializer
    permission_classes = [permissions.IsAuthenticated]

class TypeEtablissementViewSet(viewsets.ModelViewSet):
    queryset = TypeEtablissement.objects.all()
    serializer_class = TypeEtablissementSerializer
    permission_classes = [permissions.IsAuthenticated]

class StatutEtablissementViewSet(viewsets.ModelViewSet):
    queryset = StatutEtablissement.objects.all()
    serializer_class = StatutEtablissementSerializer
    permission_classes = [permissions.IsAuthenticated]

class EtablissementViewSet(viewsets.ModelViewSet):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartementViewSet(viewsets.ModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    permission_classes = [permissions.IsAuthenticated]

class FiliereViewSet(viewsets.ModelViewSet):
    queryset = Filiere.objects.all()
    serializer_class = FiliereSerializer
    permission_classes = [permissions.IsAuthenticated]

class SpecialiteViewSet(viewsets.ModelViewSet):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    permission_classes = [permissions.IsAuthenticated]

class NiveauViewSet(viewsets.ModelViewSet):
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer
    permission_classes = [permissions.IsAuthenticated]

class SemestreViewSet(viewsets.ModelViewSet):
    queryset = Semestre.objects.all()
    serializer_class = SemestreSerializer
    permission_classes = [permissions.IsAuthenticated]

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [permissions.IsAuthenticated]

class RessourcePdfViewSet(viewsets.ModelViewSet):
    queryset = RessourcePdf.objects.all()
    serializer_class = RessourcePdfSerializer
    permission_classes = [permissions.IsAuthenticated]

class RessourceVideoViewSet(viewsets.ModelViewSet):
    queryset = RessourceVideo.objects.all()
    serializer_class = RessourceVideoSerializer
    permission_classes = [permissions.IsAuthenticated]