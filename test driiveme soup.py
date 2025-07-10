import requests
from bs4 import BeautifulSoup

# Informations d'identification
login_data = {
    "actionForm": "login",
    "actionAjax": "/action/connexion.html",
    "returnUrl": "",
    "email": "",
    "password": "$$"
}
# Ajouter l'en-tête X-Requested-With: XMLHttpRequest
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Language":"fr-FR,en-US;q=0.5",
    "Accept-Encoding":"gzip, deflate, br",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With":"XMLHttpRequest",
    "Content-Length":"161",
    "Origin":"https://www.driiveme.com",
    "DNT":"1",
    "Connection":"keep-alive",
    "Referer":"https://www.driiveme.com/",
    "Cookie":"__stripe_mid=6c9da7c9-e17f-4288-b23c-0e978968184ef3f7a1; cookieAuth=true; PHPSESSID=4f5953e18e89633ce9468d3fa1d95d0b",
    "Sec-Fetch-Dest":"empty",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"same-origin",
    "TE":"trailers"
}

cookies = {
    "__stripe_mid": "6c9da7c9-e17f-4288-b23c-0e978968184ef3f7a1",
    "cookieAuth": "true",
    "PHPSESSID": "4f5953e18e89633ce9468d3fa1d95d0b"
}

# URL de connexion
login_url = 'https://www.driiveme.com/fr/action/connexion.html'
# URL de la page à analyser après la connexion
url = "https://www.driiveme.com/rechercher-trajet.html?actionForm=search-trajet&desiredDate=15/04/2024"

# Envoyer la requête POST pour la connexion avec l'en-tête ajouté

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Créer des listes pour stocker les données
depart_list = []
arrivee_list = []
debut_list = []
fin_list = []
distance_list = []
duree_list = []
lien_list = []
prix_list = []

# Créer une session
with requests.Session() as session:
    # Effectuer la connexion
    response = requests.post(url=login_url, data=login_data, headers=headers, cookies=cookies)

    # Extraire le contenu JSON de la réponse

    # Afficher le contenu JSON
    

    print(response.text)

    # Faire une requête GET pour obtenir le contenu HTML de la page
    response = session.get(url)

    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trouver tous les éléments avec la classe 'block-trajet'
        block_trajets = soup.find_all(class_="block-trajet")
        
        # Parcourir les éléments et extraire les informations
        for block_trajet in block_trajets:
            print(block_trajet.find_all(class_="item"))
            # Extraire les informations nécessaires
            depart = block_trajet.find(class_="departure").span['title']
            arrivee = block_trajet.find(class_="destination").span['title']
            debut = block_trajet.find(class_="availability").find_all('input')[0]['value']
            fin = block_trajet.find(class_="availability").find_all('input')[1]['value']
            duree = block_trajet.find(class_="item").find(class_="value").text.strip()
            distance = block_trajet.find_all(class_="item")[1].find(class_="value").text.strip()
            lien = block_trajet.find(class_="btn-success")['href']
            prix = block_trajet.find(class_="price").span.text.strip()
            
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
    else:
        print("Échec de la requête. Statut :", response.status_code)
