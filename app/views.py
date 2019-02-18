from django.shortcuts import render
from .forms import ListForm, UploadFileForm
from .models import Liste
from .models import Votant
from .models import Vote
from voteCDP import settings
from datetime import datetime
import requests
from django.template.loader import get_template
import csv

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

    return render(request, 'welcome.html', {'form': form, 'listes': listes, 'prenom':user[0].prenom})

def send_link(request, send):
    if send == "first":
        if(settings.SEND_EMAIL=="1"):
            user_list = Votant.objects.filter(email_sent=False)[:10]
            for votant in user_list:
                send_email_first(votant.prenom, votant.nom, votant.email, votant.token)
                votant.email_sent=True
                votant.save()
    elif send == "remind":
        if (settings.SEND_EMAIL == "1"):
            user_list = Votant.objects.filter(vote_ok=False).filter(email_reminder_sent=False)[:10]
            for votant in user_list:
                send_email_reminder(votant.prenom, votant.nom, votant.email, votant.token)
                votant.email_reminder_sent=True
                votant.save()
    user_total = Votant.objects.all().count()
    user_send = Votant.objects.filter(email_sent=True).count()
    reminder_send = Votant.objects.filter(email_reminder_sent=True).count()
    nb_vote = Vote.objects.count()
    nb_votant = Votant.objects.filter(vote_ok=True).count()
    participation = int(nb_votant/user_total * 100)
    return render(request, 'email_admin.html',{"user_total": user_total, "user_send": user_send, "nb_vote":nb_vote, "nb_votant":nb_votant, "reminder_send": reminder_send, 'participation': participation})

def send_email_first(prenom, nom, email, token):
    url = settings.RETURN_LINK + "?uuid=" + str(token)
    return requests.post(
        settings.MAILGUN_URL,
        auth=("api", settings.MAILGUN_KEY),
        data={"from": settings.FROM_EMAIL,
              "to": email,
              "subject": "Vote campagne CDP 2019",
              "html": get_template("first_email.html").render({"prenom": prenom, "nom": nom, "url": url})})

def send_email_reminder(prenom, nom, email, token):
    url = settings.RETURN_LINK + "?uuid=" + str(token)
    return requests.post(
        settings.MAILGUN_URL,
        auth=("api", settings.MAILGUN_KEY),
        data={"from": settings.FROM_EMAIL,
              "to": email,
              "subject": "DERNIER RAPPEL : Vote campagne CDP 2019",
              "html": get_template("reminder_email.html").render({"prenom": prenom, "nom": nom, "url": url})})

def post_vote(request):
    form = ListForm(request.POST or None)
    if form.is_valid():
        if(Votant.objects.get(token=form.cleaned_data['user_uuid']).vote_ok==False):
            form.save()
            return render(request, 'confirm.html')
        else:
            return render(request, 'votedone.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            strfile=str(request.FILES['file'].read())
            strfile=strfile[2:-1]
            liste=strfile.split(';')
            for perso in liste:
                info = perso.split(',')
                user = Votant()
                user.prenom = info[0]
                user.nom = info[1]
                user.email=info[2]
                user.save()

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})