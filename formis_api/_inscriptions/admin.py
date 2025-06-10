from django.contrib import admin

from .models import Candidature, TypeDocument, DocumentCandidature

# Register your models here.

admin.site.register(Candidature)
admin.site.register(TypeDocument)
admin.site.register(DocumentCandidature)