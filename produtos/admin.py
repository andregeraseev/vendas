from django.contrib import admin
from produtos.models import Juice




def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate_event.short_description = "Duplicar"

class JuiceList(admin.ModelAdmin):
    list_display = ['id', 'nome', 'mls', 'mg']
    list_editable = ('mg',)

    actions = [duplicate_event]
admin.site.register(Juice,JuiceList)