from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
  list_display = ('nom', 'compterPts')
  #ordering = ('compterPts',)


admin.site.register(Vote)
@admin.register(Votant)
class VotantAdmin(admin.ModelAdmin):
  list_display = ('token', 'nom', 'prenom', 'vote_ok', 'email_sent')

