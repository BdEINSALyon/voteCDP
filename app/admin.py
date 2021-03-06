from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.resources import ModelResource
from app.views import send_email_first
from .models import *
# Register your models here.

@admin.register(Liste)
class ListeAdmin(admin.ModelAdmin):
  list_display = ('nom', 'nb_vote1', 'nb_vote2', 'nb_vote3', 'nb_vote4', 'compterPts')
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
  resource_class = VotantRessource
  list_display = ('token', 'nom', 'prenom', 'vote_ok', 'email_sent')
  list_filter = ('vote_ok', 'email_sent')
  search_fields = ('nom', 'prenom')
  actions = ('envoyer_les_mails',)
  def envoyer_les_mails(self, request, queryset):
    for obj in queryset.filter(email_sent=False):
      send_email_first(prenom=obj.prenom, nom=obj.nom, email=obj.email, token=obj.token)
      obj.email_sent=True
      obj.save()
      self.message_user(request,"{} mails envoyé(s), vérifiez les logs Mailgun et le ficher {} en cas de problème".format(queryset.count(), __name__))
  envoyer_les_mails.short_description = "Envoyer les mails"