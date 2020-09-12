from django.contrib import admin
from safravoice.models import ReqBuilder, TransactionModel
# Register your models here.


class ReqBuilderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'intention', 'valor')


admin.site.register(ReqBuilder, ReqBuilderModelAdmin)
admin.site.register(TransactionModel, TransactionModelAdmin)