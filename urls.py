from datetime import datetime, timedelta
import urllib.parse


def generate_urls(num_days=14):
    """
    Génère une liste d'URLs pour la recherche de trajets sur le site web driiveme.com
    à partir de la date actuelle et pour les jours suivants.

    Args:
        num_days (int): Le nombre de jours à inclure dans la liste d'URLs.
                        Par défaut, la valeur est 14 pour les 14 prochains jours.

    Returns:
        list: Une liste d'URLs pour la recherche de trajets, chaque URL correspondant à un jour différent.

    Exemple:
        >>> generate_urls(14)
        ['https://www.driiveme.com/rechercher-trajet.html?actionForm=search-trajet&cityDeparture=&cityDepartureId=&cityDepartureSave=&cityDestination=&cityDestinationId=&cityDestinationSave=&desiredDate=18%2F04%2F2024',
        ...
        'https://www.driiveme.com/rechercher-trajet.html?actionForm=search-trajet&cityDeparture=&cityDepartureId=&cityDepartureSave=&cityDestination=&cityDestinationId=&cityDestinationSave=&desiredDate=01%2F05%2F2024']
"""
    # Liste p
    # Liste pour stocker les URLs
    urls = []

    # Définir la date d'aujourd'hui
    date_today = datetime.now().strftime('%d/%m/%Y')

    # Construire l'URL pour la date d'aujourd'hui
    url_today = f"https://www.driiveme.com/rechercher-trajet.html?actionForm=search-trajet&cityDeparture=&cityDepartureId=&cityDepartureSave=&cityDestination=&cityDestinationId=&cityDestinationSave=&desiredDate={urllib.parse.quote(date_today)}"
    urls.append(url_today)

    # Construire les URLs pour les jours suivants
    for i in range(num_days):
        # Obtenir la date pour le jour suivant
        next_date = datetime.now() + timedelta(days=i+1)
        formatted_date = next_date.strftime('%d/%m/%Y')
        # Construire l'URL pour le jour suivant
        url_next_day = f"https://www.driiveme.com/rechercher-trajet.html?actionForm=search-trajet&cityDeparture=&cityDepartureId=&cityDepartureSave=&cityDestination=&cityDestinationId=&cityDestinationSave=&desiredDate={urllib.parse.quote(formatted_date)}"
        urls.append(url_next_day)

    return urls

# Utilisation de la fonction pour générer une liste d'URLs pour les 14 prochains jours
urls_next_14_days = generate_urls(14)

# Afficher les URLs générées
for url in urls_next_14_days:
    print(url)
