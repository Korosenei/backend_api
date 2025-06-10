from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import *


class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'profile_link')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    readonly_fields = ('last_login', 'date_joined', 'profile_link')
    actions = ['activate_users', 'deactivate_users']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('email', 'role')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'is_staff'),
        }),
    )

    def profile_link(self, obj):
        if hasattr(obj, 'profil_enseignant'):
            url = f'/admin/utilisateurs/enseignant/{obj.profil_enseignant.id}/change/'
            return format_html('<a href="{}">Profil Enseignant</a>', url)
        elif hasattr(obj, 'profil_apprenant'):
            url = f'/admin/utilisateurs/apprenant/{obj.profil_apprenant.id}/change/'
            return format_html('<a href="{}">Profil Apprenant</a>', url)
        return "-"

    profile_link.short_description = "Profil associé"

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    activate_users.short_description = "Activer les utilisateurs sélectionnés"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_users.short_description = "Désactiver les utilisateurs sélectionnés"


class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom',  'grade', 'type_enseignant', 'user_link')
    list_filter = ('grade', 'type_enseignant', 'domaine', 'status')
    search_fields = ('matricule', 'nom', 'prenom', 'utilisateur__email')
    list_select_related = ('grade', 'type_enseignant', 'domaine', 'utilisateur')
    filter_horizontal = ('departements',)
    readonly_fields = ('matricule', 'created', 'date_update', 'user_link')
    fieldsets = (
        (None, {'fields': ('matricule', 'nom', 'prenom')}),
        ('Informations personnelles', {
            'fields': ('date_de_naissance', 'sexe', 'telephone', 'piece_identite', 'photo')
        }),
        ('Informations professionnelles', {
            'fields': ('grade', 'domaine', 'type_enseignant', 'departements')
        }),
        ('Compte utilisateur', {'fields': ('user_link',)}),
        ('Statut', {'fields': ('status', 'created', 'date_update')}),
    )

    def user_link(self, obj):
        if obj.utilisateur:
            url = f'/admin/utilisateurs/utilisateur/{obj.utilisateur.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.utilisateur.username)
        return "-"

    user_link.short_description = "Compte utilisateur"

    def nom_complet(self, obj):
        return f"{obj.nom} {obj.prenom}"

    nom_complet.short_description = "Nom complet"

    def save_model(self, request, obj, form, change):
        if not obj.matricule:
            prefix = "ENS" + str(obj.created.year)[2:] if obj.created else "ENS"
            obj.matricule = f"{prefix}-{get_random_string(6, '0123456789').upper()}"

        # Création du compte utilisateur si nécessaire
        if not obj.utilisateur:
            email = form.cleaned_data.get('email') or f"{obj.matricule.lower()}@ecole.edu"
            user = Utilisateur.objects.create_user(
                username=obj.matricule,
                email=email,
                password=obj.matricule,  # Mot de passe par défaut
                role='ENSEIGNANT'
            )
            obj.utilisateur = user

        super().save_model(request, obj, form, change)


class ApprenantAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom',  'departement', 'user_link')
    list_filter = ('departement', 'sexe', 'status')
    search_fields = ('matricule', 'nom', 'prenom', 'utilisateur__email')
    list_select_related = ('departement', 'utilisateur')
    readonly_fields = ('matricule', 'created', 'date_update', 'user_link')
    fieldsets = (
        (None, {'fields': ('matricule', 'nom', 'prenom')}),
        ('Informations personnelles', {
            'fields': ('date_de_naissance', 'sexe', 'telephone', 'photo',
                       'personne_a_prevenir', 'numero_prevention')
        }),
        ('Informations académiques', {
            'fields': ('departement', 'frais_paye')
        }),
        ('Compte utilisateur', {'fields': ('user_link',)}),
        ('Statut', {'fields': ('status', 'created', 'date_update')}),
    )

    def user_link(self, obj):
        if obj.utilisateur:
            url = f'/admin/utilisateurs/utilisateur/{obj.utilisateur.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.utilisateur.username)
        return "-"

    user_link.short_description = "Compte utilisateur"

    def nom_complet(self, obj):
        return f"{obj.nom} {obj.prenom}"

    nom_complet.short_description = "Nom complet"

    def save_model(self, request, obj, form, change):
        if not obj.matricule:
            prefix = "APP" + str(obj.created.year)[2:] if obj.created else "APP"
            obj.matricule = f"{prefix}-{get_random_string(6, '0123456789').upper()}"

        # Création du compte utilisateur si nécessaire
        if not obj.utilisateur:
            email = form.cleaned_data.get('email') or f"{obj.matricule.lower()}@ecole.edu"
            user = Utilisateur.objects.create_user(
                username=obj.matricule,
                email=email,
                password=obj.matricule,  # Mot de passe par défaut
                role='APPRENANT'
            )
            obj.utilisateur = user

        super().save_model(request, obj, form, change)


class ChefDepartementAdmin(admin.ModelAdmin):
    list_display = ('enseignant', 'departement', 'created', 'date_update')
    list_filter = ('departement',)
    search_fields = ('enseignant__nom', 'enseignant__prenom', 'departement__nom')
    autocomplete_fields = ['enseignant', 'departement']
    readonly_fields = ('created', 'date_update')


# Enregistrement des modèles
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Grade)
admin.site.register(Domaine)
admin.site.register(TypeEnseignant)
admin.site.register(Enseignant, EnseignantAdmin)
admin.site.register(ChefDepartement, ChefDepartementAdmin)
admin.site.register(Apprenant, ApprenantAdmin)