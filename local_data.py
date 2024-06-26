import json
import os

#bibliothèque permettant d'effectuer des requêtes HTTP de manière asynchrone
import aiohttp


#main fonction qui va récupérer les données OHLC de l'action donnée (par le symbole) pour des intervalles de temps d'OHLC
#précisés et une durée de backtest donnée.
async def main_local_data_recovery(symbol, time_interval, length_in_months):
    
    #les données sont téléchargées dans une variable data grâce à la fonction telecharger_donnees_alpha_vantage
    data = await telecharger_donnees_alpha_vantage(symbol, time_interval, length_in_months)
    
    return data

async def telecharger_donnees_alpha_vantage(symbol, time_interval, length_in_months):
    data_directory = "data"  # Répertoire pour stocker les données localement
    
    # Vérifier si le répertoire de données existe, sinon le créer
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    
    all_data = {}
    file_path = os.path.join(data_directory, f"{symbol}_{time_interval}_{length_in_months}months.json")
        
    if os.path.exists(file_path):
        # Charger les données à partir du fichier local
        with open(file_path, "r") as file:
            all_data = json.load(file)
    
    else:
        for month in reversed(last_months(length_in_months)):
            
                # Télécharger les données depuis l'API Alpha Vantage
                url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={time_interval}&month={month}&outputsize=full&apikey=40N5RGVOW4H6UJZ4'
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = await response.json()
                
                # Ajouter les données au dictionnaire global
                all_data.update(data_by_day(data[f'Time Series ({time_interval})']))
        # Sauvegarder les données localement
        with open(file_path, "w") as file:
            json.dump(all_data, file)
            
    return all_data

#import de classes permettant de manipuler des durées temporelles
from datetime import datetime, timedelta

def last_months(length):

    #récupération de la date actuelle
    current_date = datetime.now()
    result = []
    #recule d'un mois pour pouvoir y ajouter le précédent 

    #mars current_date -= timedelta(days=current_date.day)

    current_date -= timedelta(days=current_date.day)   #avril
   
    for i in range(length):
        #recule d'un mois pour pouvoir y ajouter le précédent 
        current_date -= timedelta(days=current_date.day)
        #récupère le mois demandé dans le format adapté pour l'API d'Alpha Venture
        month_str = current_date.strftime('%Y-%m')
        result.append(month_str)
   
    return result

print(last_months(1))


#cette fonction sépare les données mensuelles en données journalières
def data_by_day(donnees_brutes):
    # Dictionnaire de récupération des données journalières
    donnees_par_jour = {}

    # Parcours des données brutes
    for timestamp, valeurs in donnees_brutes.items():
        # Séparation de la date et de l'heure
        date, heure = timestamp.split(" ")

        # Création d'une nouvelle journée si elle n'existe pas encore
        if date not in donnees_par_jour:
            donnees_par_jour[date] = {}

        # Ajout des valeurs pour cette heure
        donnees_par_jour[date][heure] = valeurs

    # Inversion de l'ordre des heures dans chaque journée
    for date in donnees_par_jour:
        donnees_par_jour[date] = dict(reversed(list(donnees_par_jour[date].items())))

    # Inversion de l'ordre des jours du plus ancien au plus récent
    donnees_par_jour_inversees = dict(reversed(list(donnees_par_jour.items())))

    return donnees_par_jour_inversees


