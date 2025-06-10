from rest_framework.routers import DefaultRouter
from .views import CandidatureViewSet, TypeDocumentViewSet, DocumentCandidatureViewSet


app_name = '_inscriptions'

router = DefaultRouter()
router.register(r'candidatures', CandidatureViewSet)
router.register(r'types-documents', TypeDocumentViewSet)
router.register(r'documents-candidatures', DocumentCandidatureViewSet)

urlpatterns = router.urls