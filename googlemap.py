from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def googlemap(trajets):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Activer le mode headless
    options.add_argument("--disable-gpu")  # Désactiver l'accélération matérielle
    options.add_argument("--disable-dev-shm-usage")  # Désactiver l'utilisation de /dev/shm
    options.add_argument('--blink-settings=imagesEnabled=false') # this will disable image loading
    driver = webdriver.Chrome(options=options)

    # Ouvrir Google Maps
    driver.get("https://www.google.com/maps/dir///@45.6026614,5.2633847,15z?entry=ttu")

    # Attendre que la page charge
    WebDriverWait(driver, 10).until(
                    
                    EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Tout accepter']"))
                )

    # Trouver le bouton "Tout accepter" par sa classe CSS
    bouton_tout_accepter = driver.find_element(By.XPATH, "//button[@aria-label='Tout accepter']")

    # Cliquer sur le bouton "Tout accepter"
    bouton_tout_accepter.click()

    durées = []
    for trajet in trajets:

        WebDriverWait(driver, 10).until(
                        
                        EC.presence_of_element_located((By.CLASS_NAME, "tactile-searchbox-input"))
                    )

        # Trouver tous les champs de recherche
        champs_recherche = driver.find_elements(By.CLASS_NAME, 'tactile-searchbox-input')

        # Saisir le premier point dans le premier champ
        champs_recherche[0].clear()
        champs_recherche[0].send_keys(trajet[0])
        champs_recherche[0].send_keys(Keys.ENTER)

        # Attendre un court instant
        time.sleep(1)

        # Saisir le deuxième point dans le deuxième champ
        champs_recherche[1].clear()
        champs_recherche[1].send_keys(trajet[1])
        champs_recherche[1].send_keys(Keys.ENTER)

        # Trouver le bouton "Trajet en voiture" par sa classe CSS
        WebDriverWait(driver, 10).until(
                        
                        EC.presence_of_element_located((By.CLASS_NAME,'m6Uuef'))
                    )
        trajet_voiture = driver.find_elements(By.CLASS_NAME, 'm6Uuef')
        
        # Cliquer sur le bouton "Tout accepter"
        trajet_voiture[1].click()

        # Attendre que la suggestion se charge
        WebDriverWait(driver, 10).until(
                        
                        EC.presence_of_element_located((By.CLASS_NAME,'Fk3sm'))
                    )
        
        # Trouver l'élément contenant le temps de trajet
        temps_trajet_element = driver.find_element(By.CLASS_NAME,'Fk3sm')
        
        # Récupérer le texte du temps de trajet
        temps_trajet = temps_trajet_element.text

        # Afficher le temps de trajet
        durées.append(durées)
        print(durées, end='\r')

    # Fermer le navigateur
    driver.quit()

    print(durées)
    return durées

# Fonction de test
if __name__ == "__main__":

    # Tester la fonction 2 trajets 
    liste_test = [["Paris","Marseille"],['Lyon','Grenoble']]

    googlemap(liste_test)