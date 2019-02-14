from django.db import models
import uuid


# Create your models here.
class Votant(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(null=False)
    email_sent = models.BooleanField(default=False)
    vote_ok = models.BooleanField(default=False)
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Liste(models.Model):
    nom = models.CharField(max_length=100)
    status = models.IntegerField(default='1')

    def compterPts(self):
        return Vote.objects.filter(liste_1=self).count()*4+Vote.objects.filter(liste_2=self).count()*3+Vote.objects.filter(liste_3=self).count()*2+Vote.objects.filter(liste_4=self).count()

    def __str__(self):
        return self.nom


class Vote(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    liste_1 = models.ForeignKey('Liste', on_delete=models.PROTECT, related_name="list1")
    liste_2 = models.ForeignKey('Liste', on_delete=models.PROTECT, related_name="list2")
    liste_3 = models.ForeignKey('Liste', on_delete=models.PROTECT, related_name="list3")
    liste_4 = models.ForeignKey('Liste', on_delete=models.PROTECT, related_name="list4")

