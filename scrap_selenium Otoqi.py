from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
import googlemap
import locale

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

def Scrapper():
    def scrollbar():
            scroll_wrapper = driver.find_element(By.CLASS_NAME, "cdk-virtual-scroll-content-wrapper")
            scroll_percentage = driver.execute_script("return (arguments[0].scrollTop / (arguments[0].scrollHeight - arguments[0].clientHeight)) * 100;", scroll_wrapper)

            return scroll_percentage
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


    # Chemin vers le driver Selenium (ex: Chrome)
    driver_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # URL du site web
    login_url = "https://drivers.otoqi.com/login"

    # Identifiants de connexion
    username = ""
    password = ""

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
        sleep(5)

        
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
        lien_list = []

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
                    lien_value = str("https://drivers.otoqi.com/a/mission/") + str(reference_value)
                    # Ajouter les valeurs à chaque liste
                    jour_list.append(jour_value)
                    debut_list.append(debut_value)
                    fin_list.append(fin_value)
                    misc_list.append(misc_value)
                    prix_list.append(prix_value)
                    depart_list.append(depart_value)
                    arrivee_list.append(arrivee_value)
                    reference_list.append(reference_value)
                    lien_list.append(lien_value)
                    
            Scroll = False
            # Faire défiler la page
            try:
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements(By.CLASS_NAME,"mission-container")[12])
                sleep(2)
            except:
                print("fin de page")
                sleep(5)
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements(By.CLASS_NAME,"mission-container")[12])
                    sleep(5)
                except:
                    Scroll = False

    finally:
        # Fermer le navigateur
        sleep(10)
        driver.quit()


    # Créer une DataFrame à partir des listes de valeurs
    df = pd.DataFrame({
        'Jour': jour_list,
        'Début': debut_list,
        'Fin': fin_list,
        'Misc': misc_list,
        'Prix': prix_list,
        'Départ': depart_list,
        'Arrivée': arrivee_list,
        'Référence' : reference_list,
        'Lien' : lien_list
    })
    
    # Effacer les doublons et sauvegarder la base de donnée
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset='Référence', keep='first')
    df.to_excel('otoqui_brut.xlsx')
    
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

    print(df.head(5))
    print("1ere correction")
    # Charger les trajets déjà connus pour éviter les requetes inutiles
    df = df
    df_old = pd.read_excel('otoqui.xlsx')
    df.to_excel('otoqui.xlsx')

    print("données sauvegardées")


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
    print("#########################")
    print(df_old)

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
    df.to_excel('otoqui.xlsx')


    # Sélection des meilleurs missions
    try:
        best = df.loc[(df['Rendement']>=0) & (df['Somme']<1000)].drop_duplicates()
        best.to_excel('best2.xlsx')
    except Exception as e :
        print('requete invalide', e)



# Fonction de test
if __name__ == "__main__":
    while(True):
        try:
            Scrapper() 
            sleep(60)
        except Exception as e:
            print("Une erreur s'est produite:", e)
            sleep(60)
