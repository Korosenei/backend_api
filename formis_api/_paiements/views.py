from rest_framework import viewsets
from .models import TranchePaiement, Paiement, Transaction
from .serializers import TranchePaiementSerializer, PaiementSerializer, TransactionSerializer

# Create your views here.

# Vue pour le modèle TranchePaiement
class TranchePaiementViewSet(viewsets.ModelViewSet):
    queryset = TranchePaiement.objects.all()
    serializer_class = TranchePaiementSerializer


# Vue pour le modèle Paiement
class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer


# Vue pour le modèle Transaction
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
