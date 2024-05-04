import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import webbrowser

# Charger les données depuis le fichier Excel
df = pd.read_excel('best.xlsx')

# Convertir les colonnes "Début" et "Fin" en types datetime
df['Début'] = pd.to_datetime(df['Début'])
df['Fin'] = pd.to_datetime(df['Fin'])

# Calculer la durée de chaque tâche et ajouter 1 jour à chaque durée
df['Durée'] = df['Fin'] - df['Début'] + pd.Timedelta(days=1)

# Normaliser les valeurs de "Prix" entre 0 et 1
max_prix = df['Prix'].max()
min_prix = df['Prix'].min()
df['Alpha'] = (df['Prix'] - min_prix) / (max_prix - min_prix)

# Créer le diagramme de Gantt avec une épaisseur de barre augmentée
plt.figure(figsize=(15, 9))
bars = []
for i, row in df.iterrows():
    bar = plt.barh(y=row['Lien'], width=row['Durée'], height=1, left=row['Début'], color='green', alpha=row['Alpha'])
    bars.append(bar[0])

# Ajouter les annotations de texte (Prix) à chaque barre
for bar, prix in zip(bars, df['Prix']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{prix}',
             ha='center', va='center', color='white')  # changer la couleur en blanc

# Ajouter la fonction de clic pour afficher la valeur de la colonne Lien
def on_click(event):
    if event.inaxes is not None:
        for i, bar in enumerate(bars):
            if bar.contains(event)[0]:
                print("Lien:", df['Lien'][i])
                webbrowser.open_new(df['Lien'][i])

# Connecter la fonction de clic à la figure
plt.gcf().canvas.mpl_connect('button_press_event', on_click)

# Formater l'axe des x avec des dates au format mm/jj
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# Spécifier l'intervalle d'affichage des dates (pas de 1 jour)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

# Personnaliser le graphique
plt.xlabel('Durée')
plt.ylabel('Tâche')
plt.title('Calendrier des meilleures missions')
plt.grid(axis='x')

# Afficher le graphique
plt.show()
