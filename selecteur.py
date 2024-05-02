import pandas as pd
from datetime import datetime, timedelta

df = pd.read_excel('best.xlsx')

# Convertir les colonnes "Debut" et "Fin" en type datetime si elles ne le sont pas déjà
df['Début'] = pd.to_datetime(df['Début'])
df['Fin'] = pd.to_datetime(df['Fin'])

# Récupérer la date du jour
aujourdhui = datetime.now()

# Initialiser une liste pour stocker les 7 tables de données
tables = []

print(df[['Début','Fin']])
# Boucle sur les valeurs de n de 1 à 7
for n in range(1, 7):
    # Calculer la date J+n
    df['jour'] = aujourdhui + timedelta(days=n)
    # Filtrer les lignes où la date J+n est comprise entre la valeur de Début et la valeur de Fin
    table_n = df[(df['Début'] <= df['jour']) & (df['jour'] <= df['Fin'])]
    
    print(aujourdhui + timedelta(days=n))
    print(table_n[['Départ', 'Arrivée', 'Prix']])

    # Ajouter la table filtrée à la liste des tables
    tables.append(table_n)

# Afficher les 7 tables de données
# for i, table in enumerate(tables):
    # print(f"Table {i+1}:")
    # print(table)
