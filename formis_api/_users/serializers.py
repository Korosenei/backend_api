from rest_framework import serializers
from .models import *
from _enseignements.serializers import DepartementSerializer

from _enseignements.models import Departement


class LightUtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'role', 'is_active']

class UtilisateurSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    profile_type = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'role', 'is_active', 'profile', 'profile_type']
        read_only_fields = fields

    def get_profile(self, obj):
        if hasattr(obj, 'profil_enseignant'):
            return EnseignantSerializer(obj.profil_enseignant, context=self.context).data
        elif hasattr(obj, 'profil_apprenant'):
            return ApprenantSerializer(obj.profil_apprenant, context=self.context).data
        elif hasattr(obj, 'departement_dirige'):
            return ChefDepartementSerializer(obj.departement_dirige, context=self.context).data
        return None

    def get_profile_type(self, obj):
        if hasattr(obj, 'profil_enseignant'):
            return 'enseignant'
        elif hasattr(obj, 'profil_apprenant'):
            return 'apprenant'
        elif hasattr(obj, 'departement_dirige'):
            return 'chef_departement'
        return None


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class DomaineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domaine
        fields = '__all__'


class TypeEnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEnseignant
        fields = '__all__'


class EnseignantSerializer(serializers.ModelSerializer):
    utilisateur = LightUtilisateurSerializer(read_only=True)
    # Champs pour les IDs des relations
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(),
        source='grade',
        write_only=True,
        required=False,
        allow_null=True
    )
    domaine_id = serializers.PrimaryKeyRelatedField(
        queryset=Domaine.objects.all(),
        source='domaine',
        write_only=True,
        required=False,
        allow_null=True
    )
    type_enseignant_id = serializers.PrimaryKeyRelatedField(
        queryset=TypeEnseignant.objects.all(),
        source='type_enseignant',
        write_only=True,
        required=False,
        allow_null=True
    )
    departements_ids = serializers.PrimaryKeyRelatedField(
        queryset=Departement.objects.all(),
        source='departements',
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = Enseignant
        fields = '__all__'
        extra_fields = ['grade_id', 'domaine_id', 'type_enseignant_id', 'departements_ids']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)
        return expanded_fields + getattr(self.Meta, 'extra_fields', [])


class ChefDepartementSerializer(serializers.ModelSerializer):
    enseignant = serializers.PrimaryKeyRelatedField(queryset=Enseignant.objects.all())
    departement = serializers.PrimaryKeyRelatedField(queryset=Departement.objects.all())

    class Meta:
        model = ChefDepartement
        fields = '__all__'


class ApprenantSerializer(serializers.ModelSerializer):
    utilisateur = LightUtilisateurSerializer(read_only=True)

    departement_id = serializers.PrimaryKeyRelatedField(
        queryset=Departement.objects.all(),
        source='departement',
        write_only=True,
        required=False,
        allow_null=True
    )

    departement = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Apprenant
        fields = '__all__'
        extra_fields = ['departement_id']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)
        return expanded_fields + getattr(self.Meta, 'extra_fields', [])


