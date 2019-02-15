from django.shortcuts import render
from .forms import ListForm
from .models import Liste
from .models import Votant
from voteCDP import settings
from datetime import datetime
import requests
from django.template.loader import get_template
# Create your views here.


def index(request):
    token = request.GET.get('uuid', None)
    user = Votant.objects.filter(token=token)
    if not user:
        return render(request, 'wronglink.html')

    elif user[0].vote_ok == True:
        return render(request, 'votedone.html')

    present=datetime.now()
    max=datetime.strptime(settings.CLOSING, "%m %d %H:%M:%S %Y")#Tue May 29 00:01:00 GMT+2 2018"
    min=datetime.strptime(settings.OPENING, "%m %d %H:%M:%S %Y")
    if max<present:
        return render(request,'toolate.html')
    if min>present:
        return render(request, 'tooearly.html')

    form = ListForm(request.POST or None)
    listesSet = Liste.objects.order_by("nom").values()
    listes = []
    for l in listesSet:
        listes.append({
            'id': str(l.get('id')),
            'name': l.get('nom')
        })

    return render(request, 'welcome.html', {'form': form, 'listes': listes})

def send_link(request):
    user_list = Votant.objects.filter(email_sent=False)[:10]
    for votant in user_list:
        send_email(votant.prenom, votant.nom, votant.email, votant.token)
        votant.email_sent=True
        votant.save()
    user_total = Votant.objects.all().count()
    user_send = Votant.objects.filter(email_sent=True).count()
    return render(request, 'email_admin.html',{"user_total": user_total, "user_send": user_send})

def send_email(prenom, nom, email, token):
    url = settings.RETURN_LINK + "?uuid=" + str(token)
    return requests.post(
        settings.MAILGUN_URL,
        auth=("api", settings.MAILGUN_KEY),
        data={"from": settings.FROM_EMAIL,
              "to": email,
              "subject": "Vote campagne CDP 2019",
              "html": get_template("send_email.html").render({"prenom": prenom, "nom": nom, "url": url})})

def post_vote(request):

    form = ListForm(request.POST or None)

    if form.is_valid():
        form.save()


    return render(request, 'confirm.html')

