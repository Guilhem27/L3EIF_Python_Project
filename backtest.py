#module Python qui permet la programmation asynchrone. Il fournit une infrastructure pour définir des coroutines, qui sont des fonctions asynchrone
import asyncio

#appel du module de trade journalier qui analyse les données de la journée en considération des données passées
from output import daily_trade

#appel du module de récupération de données (dans un cache au nom de l'action backtestée) dans le fichier data_recovery
from local_data import main_data_recovery  #'from data_recovery' normalement


#programme appelant les différents modules externes de récupération de données, de trade, de calcul de résultats afin de réaliser le backtest de pmanière asynchrone
async def main_backtest(symbol, time_interval,length_in_months): 
    
    raw_data=await main_data_recovery(symbol, time_interval, length_in_months) 
    
    #informations de trade initiales sur lenext(iter(dico.values()))squelles vont se baser l'analyse technique intraday 
    last_infos = {
        #argent sur le compte initial
        'cash': 1000,
        #on crée une liste contenant les 100 dernières données OHLC FICTIVES qui prennent 1 (pour éviter les divisions par 0) qui seront progressivement remplacées par celles itérées dans le programme
        'last_ohlc': [{'1. open': '1', '2. high': '1', '3. low': '1', '4. close': '1', '5. volume': '1'}] * 100,
        'movement': {'length': 0, 'move': 0},
        'pivots': {'pp': 0, 's1': 0, 's2': 0, 'r1': 0, 'r2': 0},
        'indic_stoch': [{'%K': 1, '%D': 1}]*16,
        'indic_RSI': [1]*16,
        'indic_bolling': [{"bande_superieure": 1,"moyenne_mobile": 1,"bande_inferieure": 1}]*2,
        'indic_ATR': 0,
        'trend':{'value_growth': 1, 'volume_mean':1 },
        'max': 0,
        'min': 0,
        'closing': 0
    }


    #création d'un jour 0 avec les informations initiales au sein d'un dictionnaire daily results qui contiendra à terme les éléments d'analyse technique
    #afin de ne pas perdre le flux quotidien d'infos d'un jour à l'autre, mais également les résultats/performances des prises de position, résumées avant
    #tout par la variable 'cash'

    daily_results = {'0':{'last_infos': last_infos, 'yield':1, 'trade_infos':[]}} 

    
    #ième jour de trade calculé pour le développement du dictionnaire de résultats, on commencera directement à 1 avec (i+=1)
    i=0 
    #data_day prend les données ohlc de la ième journée du backtest 
    for data_day in raw_data.values():
        i+=1
        #if i%20==0 and i>5:
             #daily_results[str(i-1)]['last_infos']['cash']+=400
        print(i)
        #récupération des résultats de la ième journée en utilisant la fonction daily_trade du module output
        #en utilisant notamment les données ohlc de la ième journée mais également toutes les informations antérieures 
        #stockées dans le dictionnaire 'last_infos' de la i-1ème journée, lui-même stocké dans les résultats de la journée précédente
        daily_results[str(i)]=daily_trade(data_day, daily_results[str(i-1)]['last_infos'])
        
    print(analysis(daily_results))
    return analysis(daily_results)


def analysis(daily_results):
    analysis={'total_yield':1.0 , 
        'cash':0,'long_total':0, 'long_mean': 0, 'long_profit': 0, 'long_profit_mean': 0, 'long_loss': 0, 'long_loss_mean': 0,
        'short_total':0, 'short_mean': 0, 'short_profit': 0, 'short_profit_mean': 0, 'short_loss': 0, 'short_loss_mean': 0,
        'total_gain':{'0': 1}}
        #'retournement_baisse':{'total':0, 'total_mean': 0, 'profit': 0, 'profit_mean': 0, 'loss': 0, 'loss_mean': 0},
        #'retournement_hausse':{'total':0, 'total_mean': 0, 'profit': 0, 'profit_mean': 0, 'loss': 0, 'loss_mean': 0},
    

    for day, results in daily_results.items():

        if 'yield' in results:
            
            analysis['total_yield']*=results['yield']

            cash=str(results['last_infos']['cash'])
            analysis['cash']=cash.replace('.',',')[:8]

            for trade in results['trade_infos']:
                
                analysis['total_gain'][day]=trade['gains']+1

                analysis[trade['trade']+'_total']+= 1
                analysis[trade['trade']+'_mean']+= trade['gains']

                if trade['gains']<0:
                    analysis[trade['trade']+'_loss_mean']+= trade['gains']
                    analysis[trade['trade']+'_loss']+= 1

                else:
                    analysis[trade['trade']+'_profit']+= 1
                    analysis[trade['trade']+'_profit_mean']+= trade['gains']

            cash=str(results['last_infos']['cash'])
            analysis['cash']=cash.replace('.',',')
    if analysis['long_loss']>0:
        analysis['long_loss_mean']= analysis['long_loss_mean']/analysis['long_loss']
    if analysis['long_profit']>0:
        analysis['long_profit_mean']= analysis['long_profit_mean']/analysis['long_profit']
    if analysis['long_total']>0:    
        analysis['long_mean']= analysis['long_mean']/analysis['long_total']

    if analysis['short_loss']>0:    
        analysis['short_loss_mean']= analysis['short_loss_mean']/analysis['short_loss']
    if analysis['short_profit']>0:
        analysis['short_profit_mean']= analysis['short_profit_mean']/analysis['short_profit']
    if analysis['short_total']>0:
        analysis['short_mean']= analysis['short_mean']/analysis['short_total']

            #analysis['retournement_baisse']['loss_mean']= analysis['retournement_baisse']['loss_mean']/analysis['retournement_baisse']['loss']
            #analysis['retournement_baisse']['profit_mean']= analysis['retournement_baisse']['profit_mean']/analysis['retournement_baisse']['profit']

            #analysis['retournement_hausse']['loss_mean']= analysis['retournement_hausse']['loss_mean']/analysis['retournement_hausse']['loss']
            #analysis['retournement_hausse']['profit_mean']= analysis['retournement_hausse']['profit_mean']/analysis['retournement_hausse']['profit']
    for key, result in analysis.items():
        if key!='total_gain':
            analysis[key]=str(result).replace('.',',')

    return analysis

### paramètres du backtest qu'on va utiliser pour tester notre programm  
#time_interval ="15min"    #en minutes (5,15,30)
#length_in_months=36     #nombre de mois sur lesquels est réalisé le backtest
#symbol='IBM'      

#lancement du programme principal de backtest avec 
#asyncio.run(main_backtest(symbol, time_interval, length_in_months))

import csv

async def extraction(time_interval, period, universe):

    filename='backtest_results_'+time_interval+'_'+str(period)+'.csv'

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['action', 'total_yield', 'cash', 
                      'long_total', 'long_mean',
                      'long_profit', 'long_profit_mean',
                      'long_loss', 'long_loss_mean',
                      'short_total', 'short_mean',
                      'short_profit', 'short_profit_mean',
                      'short_loss', 'short_loss_mean',

                      #'retournement_baisse_total', 'retournement_baisse_mean',
                      #'retournement_baisse_profit', 'retournement_baisse_profit_mean',
                      #'retournement_baisse_loss', 'retournement_baisse_loss_mean',
                      #'retournement_hausse_total', 'retournement_hausse_mean',
                      #'retournement_hausse_profit', 'retournement_hausse_profit_mean',
                      #'retournement_hausse_loss', 'retournement_hausse_loss_mean'
                      'total_gain'
                      ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        trades=[]

        for action in universe:
            
            result=await main_backtest(action['symbole'], time_interval, period)

            trades.append(result['total_gain'])

            row = {'action': action}
            row.update(result)
            row['total_gain']=0
            writer.writerow(row)
        
        total=1

        for i in range(period*25):
            i=str(i)
            for stock in trades:
                for day, gains in stock.items():
                    if i==day:
                        total=total*gains
        print(total)


### paramètres du backtest qu'on va utiliser pour tester notre programm  
time_interval ="30min"    #en minutes (5,15,30)
length_in_months=12    #nombre de mois sur lesquels est réalisé le backtest
universe=[
    {"nom": "Microsoft", "symbole": "MSFT", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Apple", "symbole": "AAPL", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "NVIDIA", "symbole": "NVDA", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Alphabet", "symbole": "GOOGL", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Amazon", "symbole": "AMZN", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Meta", "symbole": "META", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Eli Lilly", "symbole": "LLY", "secteur": "Pharmaceutique", "liquidite": "Moyenne"},
    {"nom": "Broadcom", "symbole": "AVGO", "secteur": "Technologie", "liquidite": "Moyenne"},
    {"nom": "JPMorgan Chase", "symbole": "JPM", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "Tesla", "symbole": "TSLA", "secteur": "Automobile", "liquidite": "Haute"},
    {"nom": "Visa", "symbole": "V", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "Walmart", "symbole": "WMT", "secteur": "Grande distribution", "liquidite": "Haute"},
    {"nom": "UnitedHealth", "symbole": "UNH", "secteur": "Assurance santé", "liquidite": "Moyenne"},
    {"nom": "ExxonMobil", "symbole": "XOM", "secteur": "Énergie", "liquidite": "Moyenne"},
    {"nom": "Mastercard", "symbole": "MA", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "Johnson & Johnson", "symbole": "JNJ", "secteur": "Pharmaceutique", "liquidite": "Haute"},
    {"nom": "Advanced Micro Devices", "symbole": "AMD", "secteur": "Technologie", "liquidite": "Moyenne"},
    {"nom": "PepsiCo", "symbole": "PEP", "secteur": "Alimentation et boissons", "liquidite": "Moyenne"},
    {"nom": "AstraZeneca", "symbole": "AZN", "secteur": "Pharmaceutique", "liquidite": "Moyenne"},
    {"nom": "Royal Dutch Shell", "symbole": "SHEL", "secteur": "Énergie", "liquidite": "Moyenne"},
    {"nom": "Thermo Fisher Scientific", "symbole": "TMO", "secteur": "Science et technologie", "liquidite": "Haute"},
    {"nom": "Adobe", "symbole": "ADBE", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Qualcomm", "symbole": "QCOM", "secteur": "Technologie", "liquidite": "Moyenne"},
    {"nom": "Cisco", "symbole": "CSCO", "secteur": "Technologie", "liquidite": "Moyenne"},
    {"nom": "McDonald's", "symbole": "MCD", "secteur": "Restauration", "liquidite": "Haute"},
    {"nom": "Alibaba", "symbole": "BABA", "secteur": "Commerce en ligne", "liquidite": "Haute"},
    {"nom": "Accenture", "symbole": "ACN", "secteur": "Services informatiques", "liquidite": "Moyenne"},
    {"nom": "Walt Disney", "symbole": "DIS", "secteur": "Divertissement", "liquidite": "Haute"},
    {"nom": "Caterpillar", "symbole": "CAT", "secteur": "Équipements lourds", "liquidite": "Moyenne"},
    {"nom": "General Electric", "symbole": "GE", "secteur": "Industrie", "liquidite": "Moyenne"},
    {"nom": "American Express", "symbole": "AXP", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "TotalEnergies", "symbole": "TTE", "secteur": "Énergie", "liquidite": "Moyenne"},
    {"nom": "Verizon", "symbole": "VZ", "secteur": "Télécommunications", "liquidite": "Moyenne"},
    {"nom": "Morgan Stanley", "symbole": "MS", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "Pfizer", "symbole": "PFE", "secteur": "Pharmaceutique", "liquidite": "Haute"},
    {"nom": "Goldman Sachs", "symbole": "GS", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "IBM", "symbole": "IBM", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Philip Morris", "symbole": "PM", "secteur": "Tabac", "liquidite": "Moyenne"},
    {"nom": "Union Pacific", "symbole": "UNP", "secteur": "Transport ferroviaire", "liquidite": "Haute"},
    {"nom": "Royal Bank of Canada", "symbole": "RY", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "Suncor Energy", "symbole": "SU", "secteur": "Énergie", "liquidite": "Moyenne"},
    {"nom": "Nike", "symbole": "NKE", "secteur": "Vêtements et chaussures", "liquidite": "Haute"},
    {"nom": "Uber", "symbole": "UBER", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Airbus", "symbole": "AIR", "secteur": "Aérospatiale", "liquidite": "Moyenne"},
    {"nom": "Intel", "symbole": "INTC", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Sanofi", "symbole": "SAN", "secteur": "Pharmaceutique", "liquidite": "Moyenne"}
]

#lancement du programme principal de backtest avec 
asyncio.run(extraction(time_interval, length_in_months, universe))
