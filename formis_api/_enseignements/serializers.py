from rest_framework import serializers

from .models import Localite, TypeEtablissement, StatutEtablissement, Etablissement, Departement, Filiere, Specialite, Niveau, Semestre, Module, Matiere, Classe, RessourcePdf, RessourceVideo


# Sérialiseur pour le modèle Localite
class LocaliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localite
        fields = '__all__'  # Sérialise tous les champs du modèle Localite


# Sérialiseur pour le modèle TypeEtablissement
class TypeEtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEtablissement
        fields = '__all__'  # Sérialise tous les champs du modèle TypeEtablissement


# Sérialiseur pour le modèle StatutEtablissement
class StatutEtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutEtablissement
        fields = '__all__'  # Sérialise tous les champs du modèle StatutEtablissement


# Sérialiseur pour le modèle Etablissement
class EtablissementSerializer(serializers.ModelSerializer):
    type_etablissement = TypeEtablissementSerializer(read_only=True)
    statut_etablissement = StatutEtablissementSerializer(read_only=True)
    localite = LocaliteSerializer(read_only=True)

    class Meta:
        model = Etablissement
        fields = '__all__'  # Sérialise tous les champs du modèle Etablissement


# Sérialiseur pour le modèle StatutEtablissement
class DepartementSerializer(serializers.ModelSerializer):
    etablissement = EtablissementSerializer(read_only=True)
    chef = serializers.StringRelatedField()

    class Meta:
        model = Departement
        fields = '__all__'  # Sérialise tous les champs du modèle Departement


# Sérialiseur pour le modèle Filiere
class FiliereSerializer(serializers.ModelSerializer):
    departement = DepartementSerializer(read_only=True)
    responsable = serializers.StringRelatedField()

    class Meta:
        model = Filiere
        fields = '__all__'  # Sérialise tous les champs du modèle Filiere


# Sérialiseur pour le modèle Specialite
class SpecialiteSerializer(serializers.ModelSerializer):
    filiere = FiliereSerializer(read_only=True)

    class Meta:
        model = Specialite
        fields = '__all__'  # Sérialise tous les champs du modèle Specialite


# Sérialiseur pour le modèle Niveau
class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = '__all__'  # Sérialise tous les champs du modèle Niveau


# Sérialiseur pour le modèle Semestre
class SemestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semestre
        fields = '__all__'  # Sérialise tous les champs du modèle Semestre


# Sérialiseur pour le modèle Module
class ModuleSerializer(serializers.ModelSerializer):
    niveau = NiveauSerializer(read_only=True)
    semestre = SemestreSerializer(read_only=True)
    specialite = SpecialiteSerializer(read_only=True)
    responsable = serializers.StringRelatedField()

    class Meta:
        model = Module
        fields = '__all__'  # Sérialise tous les champs du modèle Module


# Sérialiseur pour le modèle Matiere
class MatiereSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)
    enseignant = serializers.StringRelatedField()

    class Meta:
        model = Matiere
        fields = '__all__'  # Sérialise tous les champs du modèle Matiere


# Sérialiseur pour le modèle Classe
class ClasseSerializer(serializers.ModelSerializer):
    niveau = NiveauSerializer(read_only=True)
    filiere = FiliereSerializer(read_only=True)
    matieres = MatiereSerializer(many=True, read_only=True)

    class Meta:
        model = Classe
        fields = '__all__'  # Sérialise tous les champs du modèle Classe


# Sérialiseur pour le modèle RessourcePdf
class RessourcePdfSerializer(serializers.ModelSerializer):
    matiere = MatiereSerializer(read_only=True)
    auteur = serializers.StringRelatedField()

    class Meta:
        model = RessourcePdf
        fields = '__all__'  # Sérialise tous les champs du modèle RessourcePdf


# Sérialiseur pour le modèle RessourceVideo
class RessourceVideoSerializer(serializers.ModelSerializer):
    matiere = MatiereSerializer(read_only=True)
    auteur = serializers.StringRelatedField()

    class Meta:
        model = RessourceVideo
        fields = '__all__'  # Sérialise tous les champs du modèle RessourceVideo
