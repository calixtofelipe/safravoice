from django.contrib import admin
from safravoice.models import ReqBuilder
# Register your models here.


class ReqBuilderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


admin.site.register(ReqBuilder, ReqBuilderModelAdmin)