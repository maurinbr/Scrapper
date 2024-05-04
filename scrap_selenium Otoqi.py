from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def Scrapper(urls):
    # Chemin vers le fichier JavaScript pour le script next page
    js_file_path = "nextpage.js"

    # Chemin vers le driver Selenium (ex: Chrome)
    driver_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # URL du site web
    login_url = "https://drivers.otoqi.com/login"

    # Identifiants de connexion
    username = "bruno.maurin.mtp@gmail.com"
    password = "Oligo2$$"

    # Configuration du navigateur
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Activer le mode headless
    options.add_argument("--disable-gpu")  # Désactiver l'accélération matérielle
    options.add_argument("--disable-dev-shm-usage")  # Désactiver l'utilisation de /dev/shm
    options.add_argument('--blink-settings=imagesEnabled=false') # this will disable image loading


    # Initialiser le navigateur Chrome avec les options spécifiées
    driver = webdriver.Chrome(options=options)

    try:
        # Accéder à la page de connexion
        driver.get(login_url)
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "mat-input-0")))


        # html_content = driver.find_element(By.ID, "g-dirty").get_attribute("innerHTML")
        # Utiliser BeautifulSoup pour analyser le contenu HTML
        # soup = BeautifulSoup(html_content, "html.parser")

        print('ok')
        
        # Remplir les champs de connexion et soumettre le formulaire
        username_field = driver.find_element(By.ID, "mat-input-0")
        password_field = driver.find_element(By.ID, "mat-input-1")
        submit_button = driver.find_element(By.CLASS_NAME, "mat-raised-button")

        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()

        # Attendre que la page suivante se charge (peut-être un tableau de bord ou autre)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mission-status-rect"))
        )

        
        # Boucler à travers les URLs fournies et scraper les données pour chaque URL

        content = driver.find_element(By.CLASS_NAME, "cdk-virtual-scroll-content-wrapper")
        html_content = content.get_attribute("innerHTML")

        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Trouve toutes les divs avec la classe "date-label-container"
        date_labels = soup.find_all('div', class_='date-label-container')

        # Crée une liste pour stocker les données
        data = []

        # Parcourt chaque div de date
        for date_label in date_labels:
            date = date_label.get_text(strip=True)
            # Trouve les spans suivants dans la structure HTML
            spans = date_label.find('div', class_='mission-container')
            print(spans)
            print(date_label.find_next_siblings)
            print(date_label.next_element)
            print(date_label.next_sibling)
            '''
            for span in spans:
                mission_info = span.find_all('span')
                debut = mission_info[0].get_text(strip=True)
                fin = mission_info[1].get_text(strip=True)
                prix = mission_info[3].get_text(strip=True)
                depart = mission_info[4].find('strong').get_text(strip=True)
                arrivee = mission_info[5].find('strong').get_text(strip=True)
'''
            data.append([date])
        # Crée une DataFrame avec les données extraites
        df = pd.DataFrame(data, columns=['Date'])
        print(df)



    finally:
        # Fermer le navigateur
        sleep(10)



# urls = urls.generate_urls()

urls = "https://partenaire.expedicar.com/journey/list#journeys"
Scrapper(urls)