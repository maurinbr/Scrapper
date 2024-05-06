from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def Scrapper(urls):
    def scrollbar():
            scroll_wrapper = driver.find_element(By.CLASS_NAME, "cdk-virtual-scroll-content-wrapper")
            scroll_percentage = driver.execute_script("return (arguments[0].scrollTop / (arguments[0].scrollHeight - arguments[0].clientHeight)) * 100;", scroll_wrapper)

            return scroll_percentage

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
    options.add_argument("--headless")  # Activer le mode headless
    options.add_argument("--disable-gpu")  # Désactiver l'accélération matérielle
    options.add_argument("--disable-dev-shm-usage")  # Désactiver l'utilisation de /dev/shm
    options.add_argument('--blink-settings=imagesEnabled=false') # this will disable image loading


    # Initialiser le navigateur Chrome avec les options spécifiées
    driver = webdriver.Chrome(options=options)

    try:
        # Accéder à la page de connexion
        driver.get(login_url)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))

      
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

        # Récupérer l'élément cdk-virtual-scroll-viewport
        viewport = driver.find_element(By.CLASS_NAME,'cdk-virtual-scroll-content-wrapper')

        # Scroller vers le bas
        # Exécuter du JavaScript pour faire défiler un élément dans la vue
        

        # Attendre un peu pour que la page ait le temps de scroller
        sleep(2)

        
        # Boucler à travers les URLs fournies et scraper les données pour chaque URL

        content = driver.find_element(By.CLASS_NAME, "cdk-virtual-scroll-content-wrapper")
        
        # Initialiser des listes pour stocker les valeurs de chaque colonne
        jour_list = []
        debut_list = []
        fin_list = []
        misc_list = []
        prix_list = []
        depart_list = []
        arrivee_list = []
        reference_list = []

        # Initialiser la variable jour pour capturer la valeur 'jour' dans les blocs date-label-container
        jour_value = None
        Scroll = True
        
        while(Scroll):

            scrollbar() 
            html_content = content.get_attribute("innerHTML")

            soup = BeautifulSoup(html_content, 'html.parser')

            # Trouver tous les blocs avec la classe "ng-star-inserted"
            blocks = soup.find_all(class_="ng-star-inserted")


            # Parcourir tous les blocs
            for block in blocks:
                # Vérifier si le bloc a la classe "date-label-container"
                if "date-label-container" in block.get("class", []):
                    # Récupérer la valeur 'jour'
                    jour_value = block.get_text(strip=True)
                # Vérifier si le bloc a la classe "mission-container"
                elif "mission-container" in block.get("class", []):
                    # Récupérer les valeurs des balises span dans le bloc
                    spans = block.find_all("span")
                    debut_value = spans[0].get_text(strip=True)
                    fin_value = spans[1].get_text(strip=True)
                    misc_value = spans[2].get_text(strip=True)
                    prix_value = spans[3].get_text(strip=True)
                    depart_value = spans[4].get_text(strip=True)
                    arrivee_value = spans[5].get_text(strip=True)
                    reference_value = block.get("data-mission-reference", "")
                    # Ajouter les valeurs à chaque liste
                    jour_list.append(jour_value)
                    debut_list.append(debut_value)
                    fin_list.append(fin_value)
                    misc_list.append(misc_value)
                    prix_list.append(prix_value)
                    depart_list.append(depart_value)
                    arrivee_list.append(arrivee_value)
                    reference_list.append(reference_value)
                    
            # Faire défiler la page
            try:
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements(By.CLASS_NAME,"mission-container")[12])
                sleep(2)
            except:
                print("fin de page")
                sleep(5)
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements(By.CLASS_NAME,"mission-container")[12])
                    sleep(1)
                except:
                    Scroll = False

        # Créer une DataFrame à partir des listes de valeurs
        df = pd.DataFrame({
            'Jour': jour_list,
            'Début': debut_list,
            'Fin': fin_list,
            'Misc': misc_list,
            'Prix': prix_list,
            'Départ': depart_list,
            'Arrivée': arrivee_list,
            'Référence' : reference_list
        })

        # Effacer les doublons et sauvegarder la base de donnée
        df = df.drop_duplicates()
        df.to_excel('otoqui.xlsx')

    finally:
        # Fermer le navigateur
        sleep(10)

# urls = urls.generate_urls()

urls = "https://partenaire.expedicar.com/journey/list#journeys"

# Fonction de test
if __name__ == "__main__":
    while(True):
        try:
            Scrapper(urls) 
            sleep(300)
        except:
            sleep(300)