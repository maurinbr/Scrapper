from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import urls
import re
import concurrent.futures
import time
import googlemap

def Scrapper(target):
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

    # Parcourir les éléments et extraire les informations
    depart_list = []
    arrivee_list = []
    debut_list = []
    fin_list = []
    distance_list = []
    duree_list = []
    lien_list = []
    prix_list = []
    durée_list = []

    # Script next page
    js_file_path = "nextpage.js"

    # Chemin vers le driver Selenium (ex: Chrome)
    driver_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # URL du site web
    url = "https://www.driiveme.com/popup/connexion.html"

    # Identifiants de connexion
    username = "bruno.maurin.mtp@gmail.com"
    password = "Oligo2$$"

    # Configuration du navigateur
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Activer le mode headless
    options.add_argument("--disable-gpu")  # Désactiver l'accélération matérielle
    options.add_argument("--disable-dev-shm-usage")  # Désactiver l'utilisation de /dev/shm
    options.add_argument('--blink-settings=imagesEnabled=false') # this will disable image loading
    driver = webdriver.Chrome(options=options)

    # Accéder à la page de connexion
    driver.get(url)

    # Remplir les champs de connexion et soumettre le formulaire
    username_field = driver.find_element(By.ID,"email")  
    password_field = driver.find_element(By.ID, "password")  
    submit_button = driver.find_element(By.CLASS_NAME,"btn-login")  

    # Envoyer les données 
    username_field.send_keys(username)
    password_field.send_keys(password)
    submit_button.click()

    # Attendre le chargement de la page
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-trajet-button")))

        # Parcourir toutes les urls à scrapper 
        for target_url in target:
            driver.get(target_url)

            # Attendre le chargrement de la page
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-trajet-button")))            

            # Exécuter le script JavaScript pour passer à la page suivante
            with open(js_file_path, "r") as file:
                next_page_script = file.read()
                driver.execute_script(next_page_script)
                sleep(1)
                driver.execute_script(next_page_script)
                sleep(1)
                driver.execute_script(next_page_script)
                sleep(1)
                driver.execute_script(next_page_script) 

            # Récupérer le contenu HTML de l'élément avec la classe "list-trajet-item"
            content = driver.find_element(By.ID,"list-trajet-items")
            
            html_content = content.get_attribute("innerHTML")
                
            # Utiliser BeautifulSoup pour analyser le contenu HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Trouver tous les trajet 
            block_trajets = soup.find_all(class_="block-trajet")

            # Parcourir les trajets
            for block_trajet in block_trajets:
                # Extraire les informations nécessaires
                depart = block_trajet.find(class_="departure").find('span')['data-original-title']
                arrivee = block_trajet.find(class_="destination").find('span')['data-original-title']
                debut = block_trajet.find(class_="availability").find_all('input')[0]['value']
                fin = block_trajet.find(class_="availability").find_all('input')[1]['value']
                duree = block_trajet.find(class_="item").find(class_="value").text.strip()
                distance = block_trajet.find_all(class_="item")[1].find(class_="value").text.strip()
                lien = block_trajet.find(class_="btn-success")['href'] if block_trajet.find(class_="btn-success") else None
                prix = block_trajet.find(class_="price").span.text.strip() if block_trajet.find(class_="price") else None
                
                # Ajouter les données dans les listes
                depart_list.append(depart)
                arrivee_list.append(arrivee)
                debut_list.append(debut)
                fin_list.append(fin)
                distance_list.append(distance)
                duree_list.append(duree)
                lien_list.append(lien)
                prix_list.append(prix)

    finally:
        # Fermer le navigateur
        driver.quit()
    
    # Créer la DataFrame
    df = pd.DataFrame({
        "Départ": depart_list,
        "Arrivée": arrivee_list,
        "Début": debut_list,
        "Fin": fin_list,
        "Distance": distance_list,
        "Durée": duree_list,
        "Lien": lien_list,
        "Prix": prix_list,
    })

    # Supprimer tous les doublons causés par la méthode de recherche par date ou par ville
    df = df.drop_duplicates()

    print("Nombre de trajets: ", len(df))

    # Transformer les prix en valeur numérique 
    df['Prix'] = pd.to_numeric(df['Prix'].values, errors="coerce")
    
    try:
        # Charger les trajets déjà connus pour éviter les requetes inutiles
        df_old = pd.read_excel('Driiveme.xlsx')
        df_old = df_old.drop_duplicates()

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
        
        df2 = df2[['Départ', 'Arrivée', 'Début', 'Fin','Distance','Durée',"Lien",'Prix']]
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

        # Fusionner les 2 nouvelles tables
        df = pd.concat([df2,df_old])

        # Faire la somme des trajet aller - retour au domicile
        df['Somme'] = df.apply(lambda row: sommer_durees(row['Durée (domicile1)'], row['Durée (domicile2)']), axis=1)
        df['Somme'] = df.apply(lambda row: sommer_durees(row['Somme'], row['Durée']), axis=1)

        # Sommer les trajet aller - retour vers le domicile (en minute seulement)
        df['Somme'] = df.apply(lambda row: convert_to_minutes(row['Somme']), axis=1)


    # Continuer au cas ou la table de données n'est pas présente
    except:
        print("une erreur s'est produite")

    # Calculer le trajet avec le plus de rémunération par temps de trajet
    df['Rendement'] = (df['Prix'] / df['Somme']).round(1)

    df = df.filter(regex='^(?!Unnamed)')
    df = df.drop_duplicates()
    df.to_excel('Driiveme.xlsx')
    # Sauvegarder la base 



    # Sélection des meilleurs missions
    try:
        best = df.loc[(df['Rendement']>0.1) & (df['Somme']<800)].drop_duplicates()
        best.to_excel('best.xlsx')
    except:
        print('requete invalide')
    
# Fonction de test
if __name__ == "__main__":

    while(True):
        try:
            # Enregistrer le temps de départ
            debut = time.time()

            # Générer une liste d'url pour les 14 prochains jours
            Listurls = urls.generate_urls(14)

            # Scrapper
            Scrapper(Listurls)

            # Enregistrer le temps de départ    
            fin = time.time()
            temps_execution = fin - debut
            
            # Afficher le temps d'exécution
            print("Temps d'exécution:", temps_execution, "secondes")
        except:
            print("une erreur est produite")
        time.sleep(600)