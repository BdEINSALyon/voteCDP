from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
  list_display = ('nom', 'compterPts')
  #ordering = ('compterPts',)

admin.site.register(Vote)
admin.site.register(Votant)

