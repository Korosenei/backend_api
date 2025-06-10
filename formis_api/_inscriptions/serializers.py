from rest_framework import serializers
from .models import Candidature, TypeDocument, DocumentCandidature


# Sérialiseur pour le modèle Candidature
class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = '__all__'  # Sérialise tous les champs du modèle Candidature


# Sérialiseur pour le modèle TypeDocument
class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDocument
        fields = '__all__'  # Sérialise tous les champs du modèle TypeDocument


# Sérialiseur pour le modèle DocumentCandidature
class DocumentCandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCandidature
        fields = '__all__'  # Sérialise tous les champs du modèle DocumentCandidature
