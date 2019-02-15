from django import forms
from .models import Vote
from .models import Votant
from .models import Liste
import logging

logger = logging.getLogger(__name__)

class ListForm(forms.ModelForm):

    user_uuid = forms.UUIDField()

    class Meta:
        model = Vote
        fields = '__all__'

    def save(self, commit=True):
        user = Votant.objects.get(token=self.cleaned_data['user_uuid'])
        logger.info("The value of var is %s", user)
        if user is not None:
            if not user.vote_ok:
                user.vote_ok = True
                print(user.vote_ok)
                user.save()
                return super(ListForm, self).save(commit=commit)

    def clean(self):

        cleaned_data = super(ListForm, self).clean()

        liste_1 = cleaned_data.get('liste_1')
        liste_2 = cleaned_data.get('liste_2')
        liste_3 = cleaned_data.get('liste_3')
        liste_4 = cleaned_data.get('liste_4')

        vote = [liste_1, liste_2, liste_3, liste_4]
        if len(vote) != len(set(vote)):# si oui -> doublons
            raise forms.ValidationError("listes identiques")

        listesSet = Liste.objects.all()
        listes = []
        for l in listesSet:
            listes.append(l)

        if not set(vote).issubset(set(listes)):
            raise forms.ValidationError("liste(s) inexistantes")

        return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK


