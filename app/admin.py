from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.resources import ModelResource

from .models import *

# Register your models here.

@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
  list_display = ('nom', 'compterPts')
  #ordering = ('compterPts',)


admin.site.register(Vote)

class VotantRessource(ModelResource):
  class Meta:
    model = Votant
    fields = ('nom', 'prenom', 'email')
    import_id_fields=('email',) #pour que import_export puisse trouver les nouvelles entrées
  vote_ok = Field(attribute='vote_ok',readonly=True)
  email_sent = Field(attribute='email_sent',readonly=True)
  token = Field(attribute='token', readonly=True)

@admin.register(Votant)
class VotantAdmin(ImportExportModelAdmin):
  list_display = ('token', 'nom', 'prenom', 'vote_ok', 'email_sent')
  resource_class = VotantRessource

