#bibliothèque permettant d'effectuer des requêtes HTTP de manière asynchrone
import aiohttp
#import de classes permettant de manipuler des durées temporelles
from datetime import datetime, timedelta
from aiocache import Cache
cache = Cache()

#main fonction qui va récupérer les données OHLC de l'action donnée (par le symbole) pour des intervalles de temps d'OHLC
#précisés et une durée de backtest donnée.
async def main_data_recovery(symbol, time_interval, length_in_months):
    
    #les données sont téléchargées dans une variable data grâce à la fonction telecharger_donnees_alpha_vantage
    data = await telecharger_donnees_alpha_vantage(symbol, time_interval, length_in_months)
    
    #on crée un cache avec ces données nommé selon le nom de l'action 
    name= symbol
    print(data)
    stocker_donnees_dans_cache(name, data)



#la fonction récupère dans l'API d'alpha venture les données demandées 
async def telecharger_donnees_alpha_vantage(symbol, time_interval, length_in_months):

        
        #récupération de la liste des mois voulus pour le backtest
        months=await last_months(length_in_months)

        #dictionnaire réunississant l'ensemble des données à récupérer
        all_data={}

        #boucle récupérant les données OHLC pour chaque mois en commencant par le dernier(ordre chronologique)
        for month in (reversed(months)):
            print(month)
            #récupération du lien de l'APi d'Alpha Venture en prennant les arguments symbol: action,time_interval: pour avoir des intervalles d'OHLC précises, month: mois de données recherchées, outputsize=full: pour avoir l'entiereté des données du mois voulu
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={time_interval}&month={month}&outputsize=full&apikey=D7U8ZS51ROCMQM79'
            
            #garantit que la session HTTP est correctement ouverte et fermée après utilisation
            async with aiohttp.ClientSession() as session:

                #réalisation d'une requête HTTP GET vers l'URL spécifiée. 
                #"async with" garantit que la réponse est correctement gérée et que toutes les ressources sont libérées après utilisation
                async with session.get(url) as response:

                    #extraction des données JSON de la réponse
                    data = await response.json()
                    #data[month]="OOOOOOoooooooooooerrrrrrrrrrrrrrrrrOOOOOOoooooooooooerrrrrrrrrrrrrrrrrOOOOOOoooooooooooerrrrrrrrrrrrrrrrrOOOOOOoooooooooooerrrrrrrrrrrrrrrrrOOOOOOoooooooooooerrrrrrrrrrrrrrrrrOOOOOOoooooooooooerrrrrrrrrrrrrrrrr"

            #reversed_data = {key: data[key] for key in reversed(data)}

            #ajout des données dans le dictionnaire
            all_data[month]=data
            print(all_data)
            
        #séparation des données regroupées par mois dans un dictionnaire dont la clé est 'Time Series ({time_interval})', en données journalières 
        all_data = await data_by_day(all_data[f'Time Series ({time_interval})'])
        
        return(all_data)  



#la fonction détermine une liste des mois correspondants au nderniers mois demandés du plus ancien au dernier en date, dans le format adapté pour récupérer les données OHLC de chaque mois
async def last_months(length):

    #récupération de la date actuelle
    current_date = datetime.now()
    result = []
    
    for i in range(length):
        #récupère le mois demandé dans le format adapté pour l'API d'Alpha Venture
        month_str = current_date.strftime('%Y-%m')
        result.append(month_str)
        #recule d'un mois pour pouvoir y ajouter le précédent 
        current_date -= timedelta(days=current_date.day)
    return result

#cette fonction sépare les données mensuelles en données journalières
async def data_by_day(donnees_brutes):

    #dictionnaire de récupération des données journalières
    donnees_par_jour = {}

    #timestamp la clé prend la forme: "2024-04-11 12:35:00"
    for timestamp, valeurs in donnees_brutes.items():
        
        #on sépare donc la date de l'heure
        date, heure = timestamp.split(" ")

        #si la date n'existe pas encore dans les données journalières, on crée un nouvelle journée (dictionnaire contenant les valeurs de celle-ci)
        if date not in donnees_par_jour:
            donnees_par_jour[date] = {}
        #on crée le dictionnaire de la journée contenant les OHLC correspondants basés sur les intervales de temps définis
        donnees_par_jour[date][heure] = valeurs

        # Inversion de l'ordre des jours du plus ancien au plus récent
        donnees_par_jour_inversees = dict(reversed(list(donnees_par_jour.items())))
         # Inversion de l'ordre des données intraday pour chaque jour
        for jour in donnees_par_jour_inversees.values():
            jour_inverse = dict(reversed(list(jour.items())))
            jour.clear()
            jour.update(jour_inverse)

    #on inverse les données pour les avoir dans l'ordre chronologique
    return (donnees_par_jour)




async def stocker_donnees_dans_cache(name, data):
    await cache.set(name, data, ttl=3600)  # TTL (Time To Live) en secondes


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

