from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import urls




def Scrapper(urls):
    """
    Scrappe les données de trajets à partir des URLs fournies en utilisant un navigateur Chrome automatisé.

    Args:
        urls (list): Une liste d'URLs à scraper.

    Returns:
        TODO:retouerner une liste de table

    Remarque:
        Cette fonction utilise Selenium WebDriver avec Chrome pour automatiser l'interaction avec le navigateur.
        Assurez-vous d'avoir les bibliothèques nécessaires installées et un driver Chrome compatible.
        Les données de chaque trajet sont extraites et affichées sous forme de DataFrame pandas.

    Exemple:
        >>> Scrapper(['https://www.driiveme.com/rechercher-trajet.html?actionForm=search-trajet&cityDeparture=&cityDepartureId=&cityDepartureSave=&cityDestination=&cityDestinationId=&cityDestinationSave=&desiredDate=18%2F04%2F2024',
        'https://www.driiveme.com/rechercher-trajet.html?actionForm=search-trajet&cityDeparture=&cityDepartureId=&cityDepartureSave=&cityDestination=&cityDestinationId=&cityDestinationSave=&desiredDate=19%2F04%2F2024'])
        [DataFrame contenant les données de trajets scrapés affiché dans la console]
"""
    
    # Chemin vers le fichier JavaScript pour le script next page
    js_file_path = "nextpage.js"

    # Chemin vers le driver Selenium (ex: Chrome)
    driver_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # URL du site web
    login_url = "https://www.driiveme.com/popup/connexion.html"

    # Identifiants de connexion
    username = "bruno.maurin.mtp@gmail.com"
    password = "Oligo2$$"

    # Configuration du navigateur
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Activer le mode headless
    options.add_argument("--disable-gpu")  # Désactiver l'accélération matérielle
    options.add_argument("--disable-dev-shm-usage")  # Désactiver l'utilisation de /dev/shm

    # Initialiser le navigateur Chrome avec les options spécifiées
    driver = webdriver.Chrome(options=options)


    try:
        # Accéder à la page de connexion
        driver.get(login_url)

        # Remplir les champs de connexion et soumettre le formulaire
        username_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        submit_button = driver.find_element(By.CLASS_NAME, "btn-login")

        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()

        # Attendre que la page suivante se charge (peut-être un tableau de bord ou autre)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "page-trajet-button"))
        )

        # Boucler à travers les URLs fournies et scraper les données pour chaque URL
        for url in urls:
            # Charger l'URL
            driver.get(url)
            
            # Exécuter le script JavaScript pour passer à la page suivante plusieurs fois
            with open(js_file_path, "r") as file:
                next_page_script = file.read()
                for _ in range(4):  # Répéter 4 fois
                    driver.execute_script(next_page_script)
                    sleep(1)  # Attendre 1 seconde entre chaque clic

            # Récupérer le contenu HTML de l'élément avec la classe "list-trajet-item"
            content = driver.find_element(By.ID, "list-trajet-items")
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

            # Créer la DataFrame pour cette URL
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
            print(df.head())

    finally:
        # Fermer le navigateur
        driver.quit()



# test de la fonction de scrap ) partir d'une liste de 14 jours
if __name__ == "main":

    urls = urls.generate_urls(14)

    Scrapper(urls)