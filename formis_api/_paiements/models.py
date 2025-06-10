import uuid

from django.db import models

from _enseignements.models import Filiere
from _users.models import Apprenant


# Create your models here.

# Modèle des Tranches de Paiement
class TranchePaiement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="tranches")
    numero = models.IntegerField()  # Ex: 1ère tranche, 2e tranche, 3e tranche
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        ordering = ['numero']  # Toujours afficher dans l'ordre

    def __str__(self):
        return f"Tranche {self.numero} - {self.montant} FCFA pour {self.filiere}"


# Modèle Paiement
class Paiement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apprenant = models.ForeignKey(Apprenant, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, editable=False)
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    tranche_actuelle = models.ForeignKey(TranchePaiement, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = "Paiements"

    def __str__(self):
        return f"{self.apprenant} - {self.filiere} | Restant: {self.montant_restant} FCFA"

    def initialiser_paiement(self):
        """ Initialise le paiement en assignant la première tranche """
        self.montant_total = self.filiere.montant_total
        self.montant_paye = 0
        self.montant_restant = self.filiere.montant_total
        self.tranche_actuelle = self.filiere.tranches.order_by('numero').first()
        self.save()

    def mettre_a_jour_paiement(self, montant_paye):
        """ Met à jour le paiement après chaque transaction """
        self.montant_paye += montant_paye
        self.montant_restant -= montant_paye

        # Passer à la tranche suivante si le montant payé atteint la somme des tranches précédentes
        tranches = list(self.filiere.tranches.order_by('numero'))
        total_paye_temp = 0

        for tranche in tranches:
            total_paye_temp += tranche.montant
            if self.montant_paye >= total_paye_temp:
                self.tranche_actuelle = tranche  # Mise à jour de la tranche actuelle

        # Vérification si tout est payé
        if self.montant_restant <= 0:
            self.status = False  # Paiement terminé

        self.save()


# Modèle Transaction
class Transaction(models.Model):
    MODE_CHOICES = [('Ligdicash', 'Ligdicash'), ('Espèce', 'Espèce')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.CharField(max_length=100, help_text="Exemple: Frais de scolarité")
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, related_name="transactions")
    modeTransaction = models.CharField(max_length=20, choices=MODE_CHOICES, default="Ligdicash")
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.modeTransaction} - {self.montant} FCFA - {self.paiement}"

    def effectuer_paiement(self):
        """ Effectue un paiement et met à jour le statut du paiement global """
        self.paiement.mettre_a_jour_paiement(self.montant)

