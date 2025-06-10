from rest_framework.routers import DefaultRouter
from .views import TranchePaiementViewSet, PaiementViewSet, TransactionViewSet

app_name = '_paiements'

router = DefaultRouter()
router.register(r'tranches-paiement', TranchePaiementViewSet)
router.register(r'paiements', PaiementViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = router.urls
