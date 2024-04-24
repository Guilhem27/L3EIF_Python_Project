#module Python qui permet la programmation asynchrone. Il fournit une infrastructure pour définir des coroutines, qui sont des fonctions asynchrone
import asyncio

#appel du module de trade journalier qui analyse les données de la journée en considération des données passées
from output import daily_trade

#appel du module de récupération de données (dans un cache au nom de l'action backtestée) dans le fichier data_recovery
from data_recovery import main_data_recovery


from data_recovery import cache


### paramètres du backtest
risk_reward_ratio=2   
time_interval ="60min"    #en minutes (5,15,30)
length_in_months= 3        #nombre de mois sur lesquels est réalisé le backtest
symbol='IBM'      



#programme appelant les différents modules externes de récupération de données, de trade, de calcul de résultats afin de réaliser le backtest de pmanière asynchrone
async def main_backtest(symbol, time_interval, risk_reward_ratio, length_in_months): 
    
    
    await main_data_recovery(symbol, time_interval, length_in_months) 
    #récupération des données contenues dans le cache
    raw_data = await recuperer_donnees_cache(symbol) 
    
    #informations de trade initiales sur lesquelles vont se baser l'analyse technique intraday 
    last_infos = {
        'cash': 1000,
        'last_ohlc': [],
        'movement': {'length': 0, 'move': 0, 'last_trends': []},
        'pivots': {'pp': 0, 's1': 0, 's2': 0, 's3': 0, 'r1': 0, 'r2': 0, 'r3': 0},
        'indic_stoch': [],
        'indic_RSI': [],
        'indic_bolling': [],
        'max': 0,
        'min': 0,
        'closing': 0
    }

    #création d'un jour 0 avec les informations initiales au sein d'un dictionnaire daily results qui contiendra à terme les éléments d'analyse technique
    #afin de ne pas perdre le flux quotidien d'infos d'un jour à l'autre, mais également les résultats/performances des prises de position, résumées avant
    #tout par la variable 'cash'
    daily_results = {'0':{'last_infos': last_infos}} 

    

    i=0 
    for data_day in raw_data.values():
        i+=1
        daily_results[str(i)]=daily_trade(risk_reward_ratio, data_day, daily_results[str(i-1)]['last_infos'])
        
        if daily_results[str(i)]=='fail':
            print('fail')
            return 

    print(daily_results)
    #print(analysis(daily_results))



async def recuperer_donnees_cache(name):
    
    # Récupérer les données à partir du cache
    data = await cache.get(name)
    return data


def analysis(daily_results):
    analysis={'total_yield':0, 
        'total_gain':1000,
        'sortie_consolid_hausse':0,
        'sortie_consolid_baisse':0,
        'retournement_haussier':0,
        'retournement_baissier':0,
    }

    for results in daily_results.values():
        analysis['total_yield']*=results['yield']
        for trade in results['trade_infos']:
            analysis[trade['trade']]+= trade['gains']
    analysis['total_gain']=1000*analysis['total_yield']

asyncio.run(main_backtest(symbol, time_interval, risk_reward_ratio, length_in_months))

