from django.contrib import admin
from .models import TranchePaiement, Paiement, Transaction

# Register your models here.
admin.site.register(TranchePaiement)

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('apprenant', 'filiere', 'montant_total', 'montant_paye', 'montant_restant', 'status')

    def save_model(self, request, obj, form, change):
        if not obj.id:  # Si c'est une nouvelle entrée
            obj.initialiser_paiement()  # Initialiser le paiement
        super().save_model(request, obj, form, change)

admin.site.register(Transaction)
