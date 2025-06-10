from django.contrib import admin
from .models import *


@admin.register(Localite)
class LocaliteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'status')
    list_filter = ('status',)
    search_fields = ('nom',)


@admin.register(TypeEtablissement)
class TypeEtablissementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'status')
    list_filter = ('status',)
    search_fields = ('nom',)


@admin.register(StatutEtablissement)
class StatutEtablissementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'status')
    list_filter = ('status',)
    search_fields = ('nom',)


@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sigle', 'type_etablissement', 'localite', 'status')
    list_filter = ('type_etablissement', 'statut_etablissement', 'localite', 'status')
    search_fields = ('nom', 'sigle', 'directeur_general')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        return obj.logo.url if obj.logo else "Aucun logo"

    logo_preview.short_description = "Aperçu du logo"


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sigle', 'etablissement', 'status')
    list_filter = ('etablissement', 'status')
    search_fields = ('nom', 'sigle')


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sigle', 'departement', 'responsable', 'montant_total', 'status')
    list_filter = ('departement', 'status')
    search_fields = ('nom', 'sigle')
    raw_id_fields = ('responsable',)


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'filiere', 'status')
    list_filter = ('filiere', 'status')
    search_fields = ('nom',)


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre', 'status')
    list_filter = ('status',)
    search_fields = ('nom',)
    ordering = ('ordre',)


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'status')
    list_filter = ('status',)
    search_fields = ('nom', 'code')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'niveau', 'semestre', 'status')
    list_filter = ('niveau', 'semestre', 'status')
    search_fields = ('code', 'nom')
    filter_horizontal = ()


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('code', 'intitule', 'module', 'enseignant', 'duree', 'credit', 'status')
    list_filter = ('module', 'status')
    search_fields = ('code', 'intitule')
    raw_id_fields = ('enseignant',)


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'filiere', 'annee_scolaire', 'effectif', 'status')
    list_filter = ('niveau', 'filiere', 'annee_scolaire', 'status')
    search_fields = ('nom', 'annee_scolaire')
    filter_horizontal = ('matieres',)


@admin.register(RessourcePdf)
class RessourcePdfAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'auteur', 'date_publication', 'status')
    list_filter = ('matiere', 'date_publication', 'status')
    search_fields = ('titre', 'description')
    raw_id_fields = ('auteur', 'matiere',)


@admin.register(RessourceVideo)
class RessourceVideoAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'auteur', 'date_publication', 'status')
    list_filter = ('matiere', 'date_publication', 'status')
    search_fields = ('titre', 'description')
    raw_id_fields = ('auteur', 'matiere',)