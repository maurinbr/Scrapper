from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd




def Scrapper(target):
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

    driver = webdriver.Chrome(options=options)

    # Charger la page sans charger la bibliothèque Google Maps JavaScript API
    # Accéder à la page de connexion
    driver.get(url)

    # Remplir les champs de connexion et soumettre le formulaire
    username_field = driver.find_element(By.ID,"email")  
    password_field = driver.find_element(By.ID, "password")  
    submit_button = driver.find_element(By.CLASS_NAME,"btn-login")  

    username_field.send_keys(username)
    password_field.send_keys(password)
    submit_button.click()

    # Attendre que la page suivante se charge (peut-être un tableau de bord ou autre)
    try:
        WebDriverWait(driver, 10).until(
            
            EC.presence_of_element_located((By.CLASS_NAME, "page-trajet-button"))
        )
        print("page 1")

        driver.get(target)
        WebDriverWait(driver, 10).until(
            
            EC.presence_of_element_located((By.CLASS_NAME, "page-trajet-button"))
        )
        print("page 2")

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

        # Parcourir les éléments et extraire les informations
        depart_list = []
        arrivee_list = []
        debut_list = []
        fin_list = []
        distance_list = []
        duree_list = []
        lien_list = []
        prix_list = []

        block_trajets = soup.find_all(class_="block-trajet")
        for block_trajet in block_trajets:
            # Extraire les informations nécessaires
            depart = block_trajet.find(class_="departure").span['title']
            arrivee = block_trajet.find(class_="destination").span['title']
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

        # Créer la DataFrame
        df = pd.DataFrame({
            "Départ": depart_list,
            "Arrivée": arrivee_list,
            "Début": debut_list,
            "Fin": fin_list,
            "Distance": distance_list,
            "Durée": duree_list,
            "Lien": lien_list,
            "Prix": prix_list
        })

        # Afficher la DataFrame
        print(df)

        # Maintenant, vous pouvez commencer à extraire les données de la page
        # Par exemple, trouver des éléments et récupérer leur contenu avec driver.find_element...
        # Assurez-vous d'adapter les sélecteurs aux éléments que vous souhaitez extraire sur votre page
    finally:
        # Fermer le navigateur
        driver.quit()

import urls
Listurls = urls.generate_urls(3)
testurl = "https://www.driiveme.com/rechercher-trajet.html?actionForm=search-trajet&cityDeparture=&cityDepartureId=&cityDepartureSave=&cityDestination=&cityDestinationId=&cityDestinationSave=&desiredDate=25/04/2024"

Scrapper(testurl)