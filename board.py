import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import webbrowser
import locale
import time

while(True):
    
    # Ajouter la fonction de clic pour afficher la valeur de la colonne Lien
    def on_click(event):
        if event.inaxes is not None:
            for i, bar in enumerate(bars):
                if bar.contains(event)[0]:
                    print("Lien:", df['Lien'][i])
                    webbrowser.open_new(df['Lien'][i])

    
    try:
        # Définir la localisation en français
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


        # Charger les données depuis le fichier Excel
        df = pd.read_excel('best.xlsx')

        # Convertir les colonnes "Début" et "Fin" en types datetime
        df['Début'] = pd.to_datetime(df['Début'])
        df['Fin'] = pd.to_datetime(df['Fin'])

        # Calculer la Temps de chaque tâche et ajouter 1 jour à chaque Temps
        df['Temps'] = df['Fin'] - df['Début'] + pd.Timedelta(days=1)

        # Normaliser les valeurs de "Prix" entre 0 et 1
        max_prix = df['Prix'].max()
        min_prix = df['Prix'].min()
        df['Alpha'] = (df['Prix'] - min_prix) / (max_prix - min_prix)

        # Créer le diagramme de Gantt avec une épaisseur de barre augmentée
        plt.figure(figsize=(15, len(df)*0.5))  # Ajuster la taille de la figure en fonction du nombre de tâches
        bars = []
        y_labels = []  # Stocker les valeurs des colonnes "Départ -> Arrivée"
        for i, row in df.iterrows():
            bar = plt.barh(y=i, width=row['Temps'], height=1, left=row['Début'], color='green', alpha=row['Alpha'])
            
            bars.append(bar[0])
            y_labels.append(f"{row['Départ']} -> {row['Arrivée']}")  # Créer les étiquettes pour l'axe des y

        # Ajouter les annotations de texte (Prix : Temps) à chaque barre
        for bar, prix, duree in zip(bars, df['Prix'], df['Durée']):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{prix} € - {duree}',
                    ha='center', va='center', color='black')  # Changer la couleur en blanc et afficher "Prix: Temps"

        # Définir les étiquettes pour l'axe des y avec rotation
        plt.yticks(range(len(df)), y_labels, rotation=1, ha='right')  # Rotation des étiquettes avec alignement à droite


        # Connecter la fonction de clic à la figure
        plt.gcf().canvas.mpl_connect('button_press_event', on_click)

        # Formater l'axe des x avec des dates au format mm/jj
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%A \n %m-%d')) 
        # Spécifier l'intervalle d'affichage des dates (pas de 1 jour)
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().tick_params(axis='x', labelsize=8)

        # Personnaliser le graphique
        plt.xlabel('Temps')
        plt.ylabel('Tâche')
        plt.title('Calendrier des meilleures missions')
        plt.grid(axis='x')
        

        # Afficher le graphique
        plt.tight_layout()  # Pour éviter que les étiquettes ne se chevauchent

        # Sauvegarder le graphique au format PNG
        plt.savefig('Calendrier des missions.png')
        plt.show()
        time.sleep(30)
        plt.close()
        time.sleep(30)
    except Exception as e :
        print("une erreur s'est produite", e)
        raise

