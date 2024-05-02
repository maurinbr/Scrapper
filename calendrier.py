import pandas as pd
import locale
from datetime import timedelta

df = pd.read_excel('best.xlsx')
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Convertir les colonnes "Début" et "Fin" en type datetime si elles ne le sont pas déjà
df['Début'] = pd.to_datetime(df['Début'])
df['Fin'] = pd.to_datetime(df['Fin'])

# Fonction pour récupérer les jours de la semaine entre deux dates
def jours_entre_dates(row):
    Début = row['Début']
    fin = row['Fin']
    jours = [Début + timedelta(days=i) for i in range((fin - Début).days + 1)]
    return [jour.strftime("%A") for jour in jours]

# Appliquer la fonction pour créer la nouvelle colonne "Jours"
df['Jours'] = df.apply(jours_entre_dates, axis=1)

# Afficher la DataFrame avec la nouvelle colonne
print(df)

df.to_excel('best_calendrier.xlsx')
