import uuid

from django.db import models

from _enseignements.models import Filiere
from _users.models import Apprenant


# Create your models here.

# Modèle Candidature
class Candidature(models.Model):
    STATUS_CHOICES = [('Soumis', 'Soumis'), ('Approuvé', 'Approuvé'), ('Rejeté', 'Rejeté')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apprenant = models.ForeignKey(Apprenant, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    date_soumission = models.DateTimeField(auto_now_add=True)
    statutCandidature = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Soumis")
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Inscription'
        verbose_name_plural = "Inscriptions"

    def __str__(self):
        return f"Candidature: {self.apprenant} | Filière: {self.filiere}"


# Modèle TypeDocument
class TypeDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)  # Exemple : Copie CNIB, Diplôme Bac, etc.
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TypeDocument'
        verbose_name_plural = "Types Documents"

    def __str__(self):
        return f"{self.nom}"


# Modèle DocumentCandidature
class DocumentCandidature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE)
    type_document = models.ForeignKey(TypeDocument, on_delete=models.CASCADE)  # Type de document demandé
    fichier = models.FileField(upload_to="documents/")
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DocumentCandidature'
        verbose_name_plural = "DocumentCandidatures"

    def __str__(self):
        return f"Document {self.candidature}"
