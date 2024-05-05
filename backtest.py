#module Python qui permet la programmation asynchrone. Il fournit une infrastructure pour définir des coroutines, qui sont des fonctions asynchrone
import asyncio

#appel du module de trade journalier qui analyse les données de la journée en considération des données passées
from output import daily_trade

#appel du module de récupération de données (dans un cache au nom de l'action backtestée) dans le fichier data_recovery
from data_recovery import main_data_recovery

#importation de la classe 'Cache' depuis aiocache
from aiocache import Cache
#création d'une instance 'cache' qui récupèrera les données du cache créé dans data_recovery
cache = Cache()

#programme appelant les différents modules externes de récupération de données, de trade, de calcul de résultats afin de réaliser le backtest de pmanière asynchrone
async def main_backtest(symbol, time_interval,length_in_months): 
    
    raw_data=await main_data_recovery(symbol, time_interval, length_in_months) 
    
    #récupération des données contenues dans le cache
    #raw_data = await cache.get('IBM')   'cela ne fonctionne pas

    #informations de trade initiales sur lenext(iter(dico.values()))squelles vont se baser l'analyse technique intraday 
    last_infos = {
        #argent sur le compte initial
        'cash': 1000,
        #on crée une liste contenant les 100 dernières données OHLC FICTIVES qui prennent 1 (pour éviter les divisions par 0) qui seront progressivement remplacées par celles itérées dans le programme
        'last_ohlc': [{'1. open': '1', '2. high': '1', '3. low': '1', '4. close': '1', '5. volume': '1'}] * 100,
        'movement': {'length': 0, 'move': 0, 'last_trends': []},
        'pivots': {'pp': 0, 's1': 0, 's2': 0, 's3': 0, 'r1': 0, 'r2': 0, 'r3': 0},
        'indic_stoch': [{'%K': 1, '%D': 1}]*16,
        'indic_RSI': [1]*16,
        'indic_bolling': [{"bande_superieure": 1,"moyenne_mobile": 1,"bande_inferieure": 1}]*2,
        'indic_ATR': 0,
        'trend':{'growth_rate': 1},
        'max': 0,
        'min': 0,
        'closing': 0
    }


    #création d'un jour 0 avec les informations initiales au sein d'un dictionnaire daily results qui contiendra à terme les éléments d'analyse technique
    #afin de ne pas perdre le flux quotidien d'infos d'un jour à l'autre, mais également les résultats/performances des prises de position, résumées avant
    #tout par la variable 'cash'
    daily_results = {'0':{'last_infos': last_infos}} 

    
    #ième jour de trade calculé pour le développement du dictionnaire de résultats, on commencera directement à 1 avec (i+=1)
    i=0 
    #data_day prend les données ohlc de la ième journée du backtest 
    for data_day in raw_data.values():
        i+=1

        #récupération des résultats de la ième journée en utilisant la fonction daily_trade du module output
        #en utilisant notamment les données ohlc de la ième journée mais également toutes les informations antérieures 
        #stockées dans le dictionnaire 'last_infos' de la i-1ème journée, lui-même stocké dans les résultats de la journée précédente
        daily_results[str(i)]=daily_trade(data_day, daily_results[str(i-1)]['last_infos'])
    
        #Fin du backtest lorsque le programme de daily_trade renvoie 'fail' ce qui signifie que le compte est vide, donc que la stratégie a été déficitaire
        if daily_results[str(i)]=='fail':
            print("La stratégie est inadaptée, le fonds s'est vide")
            return 
    
    return


def analysis(daily_results):
    analysis={'total_yield':0, 
        'total_gain':1000,
        'sortie_consolid_hausse':0,
        'sortie_consolid_baisse':0,
        'retournement_haussier':0,
        'retournement_baissier':0,
    }

    for day, results in daily_results.items():
        print(day)
        print(results)
        analysis['total_yield']*=results['yield']
        for trade in results['trade_infos']:
            analysis[trade['trade']]+= trade['gains']
    analysis['total_gain']=1000*analysis['total_yield']




### paramètres du backtest qu'on va utiliser pour tester notre programm  
time_interval ="30min"    #en minutes (5,15,30)
length_in_months= 1      #nombre de mois sur lesquels est réalisé le backtest
symbol='IBM'      

#lancement du programme principal de backtest avec 
asyncio.run(main_backtest(symbol, time_interval, length_in_months))


