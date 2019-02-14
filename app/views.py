from django.shortcuts import render
from .forms import ListForm
from .models import Liste
from .models import Vote
from .models import Votant

# Create your views here.


def index(request):
    token = request.GET.get('uuid', None)
    user = Votant.objects.filter(token=token)
    if not user:
        return render(request, 'wronglink.html')

    elif user[0].vote_ok == True:
        return render(request, 'votedone.html')


    form = ListForm(request.POST or None)
    listesSet = Liste.objects.values()
    listes = []
    for l in listesSet:
        listes.append({
            'id': str(l.get('id')),
            'name': l.get('nom')
        })

    return render(request, 'welcome.html', {'form': form, 'listes': listes})


def post_vote(request):

    form = ListForm(request.POST or None)

    if form.is_valid():
        form.save()


    return render(request, 'confirm.html')
