from .models import Votant
import csv

def load_csv(file):

    with open(file) as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            user = Votant()
            user.prenom = row['prenom']
            user.nom = row['nom']
            user.email = row['email']
            user.save()


