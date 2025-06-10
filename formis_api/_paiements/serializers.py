from rest_framework import serializers
from .models import TranchePaiement, Paiement, Transaction


# Sérialiseur pour le modèle TranchePaiement
class TranchePaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranchePaiement
        fields = '__all__'  # Sérialise tous les champs du modèle TranchePaiement


# Sérialiseur pour le modèle Paiement
class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'  # Sérialise tous les champs du modèle Paiement


# Sérialiseur pour le modèle Transaction
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  # Sérialise tous les champs du modèle Transaction
