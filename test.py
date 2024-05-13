import pandas as pd
import re
import googlemap
import concurrent.futures
import time
import locale



''''''''''''''''''''''''''''''''''''''''''''

''''''''''''''''''''''''''''''''''''''''''''

# Fonction pour convertir une durée en minutes
def convert_to_minutes(duree):
    heures = re.search(r'(\d+)\s*h', duree)
    minutes = re.search(r'(\d+)\s*min', duree)
    total_minutes = 0
    if heures:
        total_minutes += int(heures.group(1)) * 60
    if minutes:
        total_minutes += int(minutes.group(1))
    return total_minutes

def sommer_durees(duree1, duree2):
    total_minutes = convert_to_minutes(duree1) + convert_to_minutes(duree2)
    heures = total_minutes // 60
    minutes = total_minutes % 60
    return f"{heures} h {minutes} min"
# Charger les trajets déjà connus pour éviter les requetes inutiles
df = pd.read_excel('./otoqui.xlsx').head(2)

df_old = df.head(1)


# Ajout de l'année actuelle aux dates
current_year = pd.Timestamp.now().year
df['Jour'] = df['Jour'] + " " + str(current_year)

# Conversion en objets datetime
df['Jour'] = pd.to_datetime(df['Jour'], format='%d %B %Y')


# Formater les colonnes 'Début' et 'Fin' au format 'yyyy-mm-jj'
df['Début'] = df['Jour'].apply(lambda x: x.strftime('%Y-%m-%d'))
df['Fin'] = df['Jour'].apply(lambda x: x.strftime('%Y-%m-%d'))
# Formater la case des prix 
df['Prix'] = df['Prix'].str.replace('€', '').astype(int)
df['Prix'] = pd.to_numeric(df['Prix'].values, errors="coerce")


colonnes_fusion = ['Départ', 'Arrivée', 'Début', 'Fin']

# Toutes les colonnes des deux DataFrames
colonnes_df = df.columns
colonnes_df_old = df_old.columns

# Colonnes redondantes (présentes dans les deux DataFrames sauf celles utilisées pour la fusion)
colonnes_redondantes = set(colonnes_df).intersection(colonnes_df_old) - set(colonnes_fusion)
df_old = df_old.drop(columns=colonnes_redondantes)

# Supprimer les données de table2 qui ne sont pas présentes dans table1
df_old = pd.merge(df, df_old, on=colonnes_fusion, how='inner')
print("Trajet déja connus: ", len(df_old))

# Garder uniquement les nouvelles données de la table df pour faire le calcul de distance
merged_df = pd.merge(df, df_old.drop(columns=colonnes_redondantes), on=['Départ', 'Arrivée', 'Début', 'Fin'], how='left', indicator=True)
df2 = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

df2 = df2[['Départ', 'Arrivée', 'Début', 'Fin','Prix']]
print("Nouveaux trajets: ", len(df2))
print(df2)

# Construction de la liste de tuple pour les calculs de temps de trajet
domicile_départ = [["Bourgoin-Jallieu", row['Départ']] for index, row in df2.iterrows()]
arrivée_domicile = [["Bourgoin-Jallieu", row['Arrivée']] for index, row in df2.iterrows()]

# Calcul du temps de trajet vers le point de récupération du véhicule
durée_domicile1 = googlemap.googlemap(domicile_départ)
df2['Durée (domicile1)'] = durée_domicile1

# Calcul du temps de retour au domicile après livraison
durée_domicile2 = googlemap.googlemap(arrivée_domicile)
df2['Durée (domicile2)'] = durée_domicile2

# Calcul de la durée de la mission
Durée_mission = [[row['Départ'], row['Arrivée']] for index, row in df2.iterrows()]
Durée_mission = googlemap.googlemap(Durée_mission)
df2['Durée'] = Durée_mission
# Fusionner les 2 nouvelles tables
df = pd.concat([df2,df_old])

# Faire la somme des trajet aller - retour au domicile
df['Somme'] = df.apply(lambda row: sommer_durees(row['Durée (domicile1)'], row['Durée (domicile2)']), axis=1)
df['Somme'] = df.apply(lambda row: sommer_durees(row['Somme'], row['Durée']), axis=1)

# Sommer les trajet aller - retour vers le domicile (en minute seulement)
df['Somme'] = df.apply(lambda row: convert_to_minutes(row['Somme']), axis=1)    

# Calculer le trajet avec le plus de rémunération par temps de trajet
df['Rendement'] = (df['Prix'] / df['Somme']).round(1)

# Supprimer les colonnes inutiles et doublons 
df = df.filter(regex='^(?!Unnamed)')
df = df.drop_duplicates()

# Afficher les trajet avec erreur d'estimation
print("Erreur dans l'estimation du temps de trajet")
print(df.loc[df["Somme"]>6000])

# Eliminer les données avec erreur (Somme > 6000)
df = df.loc[df["Somme"]<6000]

# Sauvegarder la base 
df.to_excel('./otoqui.xlsx')

print(df)
# Sélection des meilleurs missions
try:
    best = df.loc[(df['Rendement']>=0) & (df['Somme']<1000)].drop_duplicates()
    best.to_excel('./best2.xlsx')
except Exception as e :
    print('requete invalide', e)