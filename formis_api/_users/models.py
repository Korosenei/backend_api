import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.crypto import get_random_string


class Utilisateur(AbstractUser):
    """
    Modèle utilisateur principal qui étend AbstractUser.
    Gère tous les types d'utilisateurs du système avec des rôles spécifiques.
    """

    # Supprimer les champs inutiles d'AbstractUser
    first_name = None
    last_name = None

    # Choix pour le champ rôle
    ROLE_CHOICES = [
        ('SUPER_ADMIN', 'Super Administrateur'),
        ('ADMIN', 'Administrateur'),
        ('ENSEIGNANT', 'Enseignant'),
        ('CHEF_DEPARTEMENT', 'Chef de Département'),
        ('APPRENANT', 'Apprenant'),
    ]

    # Champs personnalisés
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("Adresse email", unique=True)
    role = models.CharField(
        "Rôle dans le système",
        max_length=20,
        choices=ROLE_CHOICES,
        default='APPRENANT'
    )

    # Champs pour la relation générique avec les profils
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    object_id = models.UUIDField(null=True, blank=True)
    profil = GenericForeignKey('content_type', 'object_id')

    is_active = models.BooleanField("Compte actif", default=True)

    # Configuration pour l'authentification
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    # Gestion des permissions
    groups = models.ManyToManyField(
        Group,
        related_name="utilisateurs",
        blank=True,
        verbose_name="groupes",
        help_text="Les groupes auxquels appartient cet utilisateur."
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="utilisateurs",
        blank=True,
        verbose_name="permissions utilisateur",
        help_text="Permissions spécifiques pour cet utilisateur."
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

    @property
    def nom_complet(self):
        """Retourne le nom complet selon le profil associé"""
        if hasattr(self, 'profil_enseignant'):
            return self.profil_enseignant.nom_complet
        elif hasattr(self, 'profil_apprenant'):
            return self.profil_apprenant.nom_complet
        return self.username


class Grade(models.Model):
    """
    Modèle représentant les grades académiques des enseignants
    (ex: Professeur, Maître de conférences, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Nom du grade", max_length=50, unique=True)
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

    def __str__(self):
        return self.nom


class Domaine(models.Model):
    """
    Modèle représentant les domaines d'intervention ou spécialités
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Domaine d'intervention", max_length=255, unique=True)
    experience = models.IntegerField("Expérience requise (années)",
                                     help_text="Durée d'expérience minimale dans ce domaine")
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Domaine"
        verbose_name_plural = "Domaines"

    def __str__(self):
        return self.nom


class TypeEnseignant(models.Model):
    """
    Modèle représentant le type d'enseignant (Titulaire, Vacataire, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Type d'enseignant", max_length=255, unique=True)
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Type d'enseignant"
        verbose_name_plural = "Types d'enseignants"

    def __str__(self):
        return self.nom


class Enseignant(models.Model):
    """
    Modèle représentant le profil d'un enseignant.
    Un compte utilisateur est créé automatiquement lors de la création.
    """
    SEXE_CHOICES = [
        ('H', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='profil_enseignant',
        verbose_name="Compte utilisateur associé",
        null=True,
        blank=True
    )
    matricule = models.CharField("Matricule", max_length=255, unique=True)
    nom = models.CharField("Nom", max_length=255)
    prenom = models.CharField("Prénom", max_length=255)
    date_de_naissance = models.DateField("Date de naissance")
    sexe = models.CharField("Sexe", max_length=1, choices=SEXE_CHOICES)
    telephone = models.CharField("Téléphone", max_length=255)
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Grade académique"
    )
    domaine = models.ForeignKey(
        Domaine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Domaine de spécialisation"
    )
    type_enseignant = models.ForeignKey(
        TypeEnseignant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Type d'enseignant"
    )
    departements = models.ManyToManyField(
        '_enseignements.Departement',
        related_name='enseignants',
        verbose_name="Départements où enseigne",
        blank=True
    )
    piece_identite = models.FileField(
        "Pièce d'identité",
        upload_to='enseignants/pieces_identite/',
        null=True,
        blank=True
    )
    photo = models.FileField(
        "Photo de profil",
        upload_to='enseignants/photos/',
        null=True,
        blank=True
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"

    @property
    def nom_complet(self):
        return f"{self.nom} {self.prenom}"

    def save(self, *args, **kwargs):
        if not self.matricule:
            # Génération du matricule si non fourni
            prefix = "ENS" + str(self.created.year)[2:] if hasattr(self, 'created') else "ENS"
            self.matricule = f"{prefix}-{get_random_string(6, '0123456789').upper()}"

        super().save(*args, **kwargs)

        # Création automatique de l'utilisateur si non existant
        if not self.utilisateur:
            # Utilise l'email fourni ou génère un email par défaut
            email = getattr(self, 'email', None) or f"{self.matricule.lower()}@ecole.edu"
            password = self.matricule  # Mot de passe par défaut = matricule

            user = Utilisateur.objects.create_user(
                username=self.matricule,
                email=email,
                password=password,
                role='ENSEIGNANT',
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.id
            )
            self.utilisateur = user
            self.save()


class ChefDepartement(models.Model):
    """
    Modèle représentant la relation entre un enseignant et un département
    qu'il dirige. Un département ne peut avoir qu'un seul chef.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enseignant = models.OneToOneField(
        Enseignant,
        on_delete=models.CASCADE,
        related_name='departement_dirige',
        verbose_name="Enseignant chef de département"
    )
    departement = models.OneToOneField(
        '_enseignements.Departement',
        on_delete=models.CASCADE,
        related_name='chef_attribue',
        verbose_name="Département dirigé"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Chef de département"
        verbose_name_plural = "Chefs de département"
        constraints = [
            # Un département ne peut avoir qu'un seul chef
            models.UniqueConstraint(
                fields=['departement'],
                name='unique_chef_par_departement'
            ),
            # Un enseignant ne peut être chef que d'un seul département
            models.UniqueConstraint(
                fields=['enseignant'],
                name='unique_departement_par_chef'
            )
        ]

    def __str__(self):
        return f"{self.enseignant.nom_complet} - Chef du {self.departement.nom}"


class Apprenant(models.Model):
    """
    Modèle représentant le profil d'un apprenant.
    Un compte utilisateur est créé automatiquement lors de la création.
    """
    SEXE_CHOICES = [
        ('H', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='profil_apprenant',
        verbose_name="Compte utilisateur associé",
        null=True,
        blank=True
    )
    matricule = models.CharField("Matricule", max_length=255, unique=True)
    photo = models.FileField(
        "Photo de profil",
        upload_to='apprenants/photos/',
        null=True,
        blank=True
    )
    nom = models.CharField("Nom", max_length=255)
    prenom = models.CharField("Prénom", max_length=255)
    sexe = models.CharField("Sexe", max_length=1, choices=SEXE_CHOICES)
    date_de_naissance = models.DateField("Date de naissance")
    telephone = models.CharField("Téléphone", max_length=255)
    personne_a_prevenir = models.CharField(
        "Personne à prévenir en cas d'urgence",
        max_length=255
    )
    numero_prevention = models.CharField(
        "Numéro à contacter en cas d'urgence",
        max_length=255
    )
    frais_paye = models.DecimalField(
        "Frais payés",
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    departement = models.ForeignKey(
        '_enseignements.Departement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apprenants',
        verbose_name="Département d'affiliation"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Apprenant"
        verbose_name_plural = "Apprenants"

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"

    @property
    def nom_complet(self):
        return f"{self.nom} {self.prenom}"

    # Pour Apprenant
    def save(self, *args, **kwargs):
        if not self.matricule:
            # Génération automatique du matricule
            prefix = "APP" + str(self.created.year)[2:] if hasattr(self, 'created') else "APP"
            self.matricule = f"{prefix}-{get_random_string(6, '0123456789').upper()}"

        super().save(*args, **kwargs)

        # Création automatique de l'utilisateur si non existant
        if not self.utilisateur:
            # Utilise l'email fourni ou génère un email par défaut
            email = getattr(self, 'email', None) or f"{self.matricule.lower()}@ecole.edu"
            password = self.matricule  # Mot de passe par défaut = matricule

            user = Utilisateur.objects.create_user(
                username=self.matricule,
                email=email,
                password=password,
                role='APPRENANT',
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.id
            )
            self.utilisateur = user
            self.save()

