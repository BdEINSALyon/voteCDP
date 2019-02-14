from django import forms
from .models import Vote
from .models import Votant
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




