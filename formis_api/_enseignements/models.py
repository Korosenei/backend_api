import uuid
from django.db import models
from tinymce.models import HTMLField
from .validators import validate_file_extension_for_image


class Localite(models.Model):
    """
    Modèle représentant une localité géographique (ville, région)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Nom de la localité", max_length=100, unique=True)
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = 'Localité'
        verbose_name_plural = "Localités"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class TypeEtablissement(models.Model):
    """
    Catégorie d'établissement (Université, Grande École, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(
        "Type d'établissement",
        max_length=100,
        unique=True,
        help_text="Ex: Université, Grande École, Institut"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Type d'établissement"
        verbose_name_plural = "Types d'établissements"

    def __str__(self):
        return self.nom


class StatutEtablissement(models.Model):
    """
    Statut juridique de l'établissement (Public, Privé, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(
        "Statut",
        max_length=100,
        unique=True,
        help_text="Ex: Public, Privé, Confessionnel"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Statut d'établissement"
        verbose_name_plural = "Statuts d'établissements"

    def __str__(self):
        return self.nom


class Etablissement(models.Model):
    """
    Modèle principal représentant un établissement d'enseignement
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Nom de l'établissement", max_length=100)
    sigle = models.CharField("Sigle", max_length=10, help_text="Ex: UJKZ")
    contact = models.CharField("Téléphone", max_length=20, blank=True, null=True)
    email = models.EmailField("Email", max_length=100, blank=True, null=True)
    site = models.URLField("Site web", max_length=100, blank=True, null=True)
    logo = models.FileField(
        "Logo",
        upload_to='etablissement/logo/',
        validators=[validate_file_extension_for_image],
        null=True,
        blank=True
    )
    type_etablissement = models.ForeignKey(
        TypeEtablissement,
        on_delete=models.PROTECT,
        related_name='etablissements',
        verbose_name="Type d'établissement"
    )
    statut_etablissement = models.ForeignKey(
        StatutEtablissement,
        on_delete=models.PROTECT,
        related_name='etablissements',
        verbose_name="Statut juridique"
    )
    localite = models.ForeignKey(
        Localite,
        on_delete=models.PROTECT,
        related_name='etablissements',
        verbose_name="Localisation"
    )
    directeur_general = models.CharField(
        "Directeur général",
        max_length=50,
        help_text="Nom complet du directeur"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"
        ordering = ['nom']
        constraints = [
            models.UniqueConstraint(
                fields=['nom', 'localite'],
                name='unique_etablissement_localite'
            )
        ]

    def __str__(self):
        return f"{self.nom} ({self.sigle}) - {self.localite.nom}"


class Departement(models.Model):
    """
    Département académique au sein d'un établissement
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Nom du département", max_length=100)
    sigle = models.CharField("Sigle", max_length=50)
    etablissement = models.ForeignKey(
        Etablissement,
        on_delete=models.CASCADE,
        related_name="departements",
        null=True,
        blank=True,
        verbose_name="Établissement de rattachement"
    )
    # chef = models.OneToOneField(
    #     '_users.ChefDepartement',
    #     on_delete=models.SET_NULL,
    #     related_name="departement_dirige",
    #     null=True,
    #     blank=True,
    #     verbose_name="Chef de département"
    # )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ['nom']
        constraints = [
            models.UniqueConstraint(
                fields=['nom', 'etablissement'],
                name='unique_departement_etablissement'
            ),
            models.UniqueConstraint(
                fields=['sigle', 'etablissement'],
                name='unique_sigle_departement'
            )
        ]

    def __str__(self):
        return f"{self.nom} ({self.sigle}) - {self.etablissement.sigle}"


class Filiere(models.Model):
    """
    Filière de formation proposée par un département
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Nom de la filière", max_length=100)
    sigle = models.CharField("Sigle", max_length=50)
    departement = models.ForeignKey(
        Departement,
        on_delete=models.CASCADE,
        related_name="filieres",
        verbose_name="Département responsable"
    )
    montant_total = models.DecimalField(
        "Frais de formation",
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    responsable = models.ForeignKey(
        '_users.Enseignant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="filieres_responsables",
        verbose_name="Responsable pédagogique"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom']
        constraints = [
            models.UniqueConstraint(
                fields=['nom', 'departement'],
                name='unique_filiere_departement'
            )
        ]

    def __str__(self):
        return f"{self.nom} ({self.departement.sigle})"


class Specialite(models.Model):
    """
    Spécialisation au sein d'une filière
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Nom de la spécialité", max_length=100)
    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.CASCADE,
        related_name="specialites",
        verbose_name="Filière parente"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ['nom']
        constraints = [
            models.UniqueConstraint(
                fields=['nom', 'filiere'],
                name='unique_specialite_filiere'
            )
        ]

    def __str__(self):
        return f"{self.nom} ({self.filiere.nom})"


class Niveau(models.Model):
    """
    Niveau académique (Licence, Master, Doctorat...)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(
        "Nom du niveau",
        max_length=50,
        help_text="Ex: BTS, Licence, Master, Doctorat"
    )
    ordre = models.PositiveSmallIntegerField(
        "Ordre d'affichage",
        default=0,
        help_text="Pour le tri des niveaux"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Niveau académique"
        verbose_name_plural = "Niveaux académiques"
        ordering = ['ordre']

    def __str__(self):
        return self.nom


class Semestre(models.Model):
    """
    Semestre académique (S1, S2...)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(
        "Nom du semestre",
        max_length=50,
        help_text="Ex: Semestre 1, Semestre 2"
    )
    code = models.CharField(
        "Code",
        max_length=10,
        unique=True,
        help_text="Code court (ex: S1)"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Semestre académique"
        verbose_name_plural = "Semestres académiques"
        ordering = ['code']

    def __str__(self):
        return f"{self.nom} ({self.code})"


class Module(models.Model):
    """
    Module d'enseignement regroupant plusieurs matières
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField("Code du module", max_length=20, unique=True)
    nom = models.CharField("Nom du module", max_length=100)
    niveau = models.ForeignKey(
        Niveau,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name="Niveau académique"
    )
    semestre = models.ForeignKey(
        Semestre,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name="Semestre"
    )
    filiere = models.ForeignKey(
        Filiere,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name="Filière concernée"
    )
    description = HTMLField("Description", blank=True, null=True)
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['code']
        constraints = [
            models.UniqueConstraint(
                fields=['nom', 'filiere', 'niveau', 'semestre'],
                name='unique_module_in_context'
            )
        ]

    def __str__(self):
        return f"{self.nom} ({self.code})"


class Matiere(models.Model):
    """
    Matière enseignée dans un module
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField("Code matière", max_length=20)
    intitule = models.CharField("Intitulé", max_length=100)
    objectif = models.TextField("Objectifs pédagogiques")
    duree = models.PositiveIntegerField(
        "Durée totale (heures)",
        help_text="Durée totale en heures"
    )
    temps_cours_magistral = models.PositiveIntegerField(
        "Heures de cours magistral",
        default=0
    )
    temps_travaux_dirige = models.PositiveIntegerField(
        "Heures de travaux dirigés",
        default=0
    )
    temps_travaux_pratique = models.PositiveIntegerField(
        "Heures de travaux pratiques",
        default=0
    )
    credit = models.PositiveIntegerField("Crédits ECTS", default=0)
    enseignant = models.ForeignKey(
        '_users.Enseignant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matieres",
        verbose_name="Enseignant responsable"
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="matieres",
        verbose_name="Module parent"
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['code']
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'module'],
                name="unique_matiere_module"
            )
        ]

    def __str__(self):
        return f"{self.code} - {self.intitule} ({self.module})"


class Classe(models.Model):
    """
    Classe regroupant des étudiants d'une même promotion
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField("Nom de la classe", max_length=100)
    niveau = models.ForeignKey(
        Niveau,
        on_delete=models.CASCADE,
        related_name="classes",
        verbose_name="Niveau académique"
    )
    filiere = models.ForeignKey(
        Filiere,
        on_delete=models.CASCADE,
        related_name="classes",
        verbose_name="Filière"
    )
    annee_scolaire = models.CharField(
        "Année scolaire",
        max_length=9,
        help_text="Format: 2023-2024"
    )
    matieres = models.ManyToManyField(
        Matiere,
        related_name="classes",
        blank=True,
        verbose_name="Matières enseignées"
    )
    effectif = models.PositiveIntegerField(
        "Effectif",
        default=0
    )
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"
        ordering = ['annee_scolaire', 'nom']
        constraints = [
            models.UniqueConstraint(
                fields=['nom', 'filiere', 'annee_scolaire'],
                name="unique_classe_annee"
            )
        ]

    def __str__(self):
        return f"{self.nom} - {self.filiere} ({self.annee_scolaire})"


class RessourcePdf(models.Model):
    """
    Ressource pédagogique au format PDF
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField("Titre", max_length=100)
    description = models.TextField("Description", blank=True)
    fichier = models.FileField(
        "Fichier PDF",
        upload_to='ressources/pdfs/%Y/%m/%d/',
        validators=[validate_file_extension_for_image]
    )
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name="ressources_pdf",
        verbose_name="Matière associée"
    )
    auteur = models.ForeignKey(
        '_users.Enseignant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Auteur"
    )
    date_publication = models.DateField("Date de publication", auto_now_add=True)
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Ressource PDF"
        verbose_name_plural = "Ressources PDF"
        ordering = ['-date_publication']

    def __str__(self):
        return f"{self.titre} - {self.matiere}"


class RessourceVideo(models.Model):
    """
    Ressource pédagogique vidéo (lien externe)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField("Titre", max_length=100)
    description = models.TextField("Description", blank=True)
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name="ressources_video",
        verbose_name="Matière associée"
    )
    url = models.URLField("URL de la vidéo", max_length=200)
    auteur = models.ForeignKey(
        '_users.Enseignant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Auteur"
    )
    date_publication = models.DateField("Date de publication", auto_now_add=True)
    status = models.BooleanField("Actif", default=True)
    created = models.DateTimeField("Date de création", auto_now_add=True)
    date_update = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Ressource vidéo"
        verbose_name_plural = "Ressources vidéo"
        ordering = ['-date_publication']

    def __str__(self):
        return f"{self.titre} - {self.matiere}"