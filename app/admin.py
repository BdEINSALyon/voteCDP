from django.contrib import admin
from app.views import send_email
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
  list_filter = ('vote_ok', 'email_sent')
  search_fields = ('nom', 'prenom')

  actions = ('envoyer_les_mails',)
  def envoyer_les_mails(self, request, queryset):# Union[QuerySet, List[Votant]]):
    for obj in queryset.filter(email_sent=False):
      #obj : Votant = i
      #logger.info("Envoi d'un mail de lien à {}".format(obj.email))
      r = send_email(prenom=obj.prenom, nom=obj.nom, email=obj.email, token=obj.token)
      #logger.info(r.text)
      obj.email_sent=True
      obj.save()
      self.message_user(request,"{} mails envoyé(s), vérifiez les logs Mailgun et le ficher {} en cas de problème".format(queryset.count(), __name__))
  envoyer_les_mails.short_description = "Envoyer les mails"

