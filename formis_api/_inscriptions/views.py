from rest_framework import viewsets
from .models import Candidature, TypeDocument, DocumentCandidature
from .serializers import CandidatureSerializer, TypeDocumentSerializer, DocumentCandidatureSerializer


# Create your views here.

# Vue pour le modèle Candidature
class CandidatureViewSet(viewsets.ModelViewSet):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer


# Vue pour le modèle TypeDocument
class TypeDocumentViewSet(viewsets.ModelViewSet):
    queryset = TypeDocument.objects.all()
    serializer_class = TypeDocumentSerializer


# Vue pour le modèle DocumentCandidature
class DocumentCandidatureViewSet(viewsets.ModelViewSet):
    queryset = DocumentCandidature.objects.all()
    serializer_class = DocumentCandidatureSerializer
