import pandas as pd
import locale
from datetime import timedelta

df = pd.read_excel('best.xlsx')
# Définir la localisation en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Supposons que votre DataFrame s'appelle df

# Convertir les colonnes "Début" et "Fin" en type datetime si elles ne le sont pas déjà
df['Début'] = pd.to_datetime(df['Début'])
df['Fin'] = pd.to_datetime(df['Fin'])

# Fonction pour récupérer les jours de la semaine entre deux dates
def jours_entre_dates(row):
    Début = row['Début']
    fin = row['Fin']
    jours = [Début + timedelta(days=i) for i in range((fin - Début).days + 1)]
    jours_francais = [jour.strftime("%A") for jour in jours]
    jours_voulus = [jour for jour in jours_francais if jour in ['mercredi', 'vendredi', 'samedi']]
    return jours_voulus

# Appliquer la fonction pour créer la nouvelle colonne "Jours"
df['Jours'] = df.apply(jours_entre_dates, axis=1)

# Réinitialiser la localisation
locale.setlocale(locale.LC_TIME, 'C')

# Supprimer les lignes où la colonne "Jours" est vide
df = df[df['Jours'].apply(len) > 0]

# Réinitialiser les index
df.reset_index(drop=True, inplace=True)

# Afficher la DataFrame avec la nouvelle colonne
print(df)

df.to_excel('calendrier_mvs.xlsx')