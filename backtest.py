#module Python qui permet la programmation asynchrone. Il fournit une infrastructure pour définir des coroutines, qui sont des fonctions asynchrone
import asyncio

#appel du module de trade journalier qui analyse les données de la journée en considération des données passées
from output import daily_trade

#appel du module de récupération de données (dans un cache au nom de l'action backtestée) dans le fichier data_recovery
from local_data import main_local_data_recovery  
from data_recovery import main_data_recovery


#programme appelant les différents modules externes de récupération de données, de trade, de calcul de résultats afin de réaliser le backtest de pmanière asynchrone
async def main_backtest(symbol, time_interval,length_in_months,strat,rsi, rate, vol, sl, tp, len_EMA, len_trend, viz): 
    
    if viz=='first_backtest':
        raw_data=await main_local_data_recovery(symbol, time_interval, length_in_months) 
    elif viz=='second_backtest':
        raw_data= await main_data_recovery(symbol, time_interval, 1)

    #informations de trade initiales sur lenext(iter(dico.values()))squelles vont se baser l'analyse technique intraday 
    last_infos = {
        #argent sur le compte initial
        'cash': 1000,
        #on crée une liste contenant les 100 dernières données OHLC FICTIVES qui prennent 1 (pour éviter les divisions par 0) qui seront progressivement remplacées par celles itérées dans le programme
        'last_ohlc': [{'1. open': '1', '2. high': '1', '3. low': '1', '4. close': '1', '5. volume': '1'}] * 500,
        'movement': {'length': 0, 'move': 0},
        'pivots': {'pp': 0, 's1': 0, 's2': 0, 'r1': 0, 'r2': 0},
        'indic_RSI': 1,
        'indic_ATR': 0,
        'EMA':0,
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
        
        #récupération des résultats de la ième journée en utilisant la fonction daily_trade du module output
        #en utilisant notamment les données ohlc de la ième journée mais également toutes les informations antérieures 
        #stockées dans le dictionnaire 'last_infos' de la i-1ème journée, lui-même stocké dans les résultats de la journée précédente
        daily_results[str(i)]=daily_trade(data_day, daily_results[str(i-1)]['last_infos'],strat,rsi, rate, vol, sl, tp, len_EMA, len_trend)
    
    print(analysis(daily_results))  
    return analysis(daily_results)

    

    

def analysis(daily_results):
    analysis={'total_yield':1.0 , 'ratio': 0.5,
        'cash':0,'long_total':0, 'long_mean': 0, 'long_profit': 0, 'long_profit_mean': 0, 'long_loss': 0, 'long_loss_mean': 0,
        'short_total':0, 'short_mean': 0, 'short_profit': 0, 'short_profit_mean': 0, 'short_loss': 0, 'short_loss_mean': 0,
        'trades':{'0': 1}}
    

    for day, results in daily_results.items():

        if 'yield' in results:
            
            analysis['total_yield']*=results['yield']

            analysis['cash']=results['last_infos']['cash']

            for trade in results['trade_infos']:
                
                if day not in analysis['trades']:
                    analysis['trades'][day]=trade['gains']+1
                else:
                    analysis['trades'][day]=(trade['gains']+1)*analysis['trades'][day]

                analysis[trade['trade']+'_total']+= 1
                analysis[trade['trade']+'_mean']+= trade['gains']

                if trade['gains']<0:
                    analysis[trade['trade']+'_loss_mean']+= trade['gains']
                    analysis[trade['trade']+'_loss']+= 1

                else:
                    analysis[trade['trade']+'_profit']+= 1
                    analysis[trade['trade']+'_profit_mean']+= trade['gains']

            
            analysis['cash']=results['last_infos']['cash']
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

    if (analysis['short_total']+analysis['long_total'])>0:
        analysis['ratio']=(analysis['short_profit']+analysis['long_profit'])/(analysis['short_total']+analysis['long_total'])
    else:
        analysis['ratio']=0 
    for key, result in analysis.items():
        if key!='trades':
            analysis[key]=result

    return analysis


import csv

async def extraction(time_interval, period, action):
    straat=['short_trend']#, 'long_trend'] 
    rsii = [25,30,35,40,45,50,55,60,65,70,75]
    raate =[1,1.5,2,2.5,3,3.5,4] 
    vool = [5.5,6,6.5,7] 
    sll =[0.5,1, 1.5, 2,2.5,3,3.5,4]
    tpp =[1,1.5,2,2.5,3,3.5,4,4.5]
    lens= [2, 50, 100, 200, 300, 400]
    lenss=[100]

    filename = 'backtest_results_' + time_interval + '_' + str(period) + '.csv'
    
    # Ouverture du fichier en mode ajout ('a') pour ne pas écraser les données existantes
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['action', 'total_yield', 'ratio', 'cash', 
                      'long_total', 'long_mean', 'long_profit', 'long_profit_mean',
                      'long_loss', 'long_loss_mean', 'short_total', 'short_mean',
                      'short_profit', 'short_profit_mean', 'short_loss', 'short_loss_mean', 'trades', 'parameters', 'strat_ratio', 'results']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Écrire l'en-tête une seule fois si le fichier est vide
        if csvfile.tell() == 0:
            writer.writeheader()
        
        final_result = {'total_yield': 1.0, 
                        'cash': 0, 'long_total': 0, 'long_mean': 0, 'long_profit': 0, 'long_profit_mean': 0, 
                        'long_loss': 0, 'long_loss_mean': 0, 'short_total': 0, 'short_mean': 0, 
                        'short_profit': 0, 'short_profit_mean': 0, 'short_loss': 0, 'short_loss_mean': 0, 
                        'trades': {'0': 1}}
        
        
        for strat in straat:
            rsi_dict={'25':0, '30':0,'35':0, '40':0,'45':0, '50':0,'55':0, '60':0,'65':0, '70':0,'75':0}
            raate_dict={'1':0, '1.5':0,'2':0, '2.5':0,'3':0, '3.5':0,'4':0}
            vool_dict={'4.5':0, '5':0,'5.5':0, '6':0,'6.5':0, '7':0}
            sll_dict={'0.5':0, '1':0,'1.5':0, '2':0,'2.5':0, '3':0,'3.5':0, '4':0}
            tpp_dict={ '1':0,'1.5':0, '2':0,'2.5':0, '3':0,'3.5':0, '4':0, '4.5':0}
            lenEMA_dict={'100':0, '200':0,'300':0, '400':0, '500': 0}
            lenTrend_dict={'100':0, '200':0,'300':0, '400':0}
            best_parameters = {}
            i=0
            j=0
            for len_EMA in lens:
                for len_trend in lenss:
                    for rsi in rsii:
                        for rate in raate:
                            for vol in vool:
                                for sl in sll:
                                    for tp in tpp:
                                        
                                        i+=1
                                        result = await main_backtest(action['symbole'], time_interval, period, strat, rsi, rate, vol, sl, tp, len_EMA,len_trend, 'first_backtest')
                                        
                                        # Condition pour choisir le meilleur résultat
                                        if result['total_yield'] > final_result['total_yield'] and result['ratio'] > 0.6 and sl<tp and result['short_total']>5:
                                            final_result = result
                                            best_parameters = {'strat': strat, 'rsi': rsi, 'rate': rate,  'vol': vol, 'sl': sl, 'tp': tp, 'len_EMA': len_EMA, 'len_trend': len_trend}
                                            
                                        if result['total_yield'] > 1 and result['ratio'] > 0.6 and sl<=tp and result['short_total']>5:
                                            j+=1
                                            rsi_dict[str(rsi)]+=1
                                            raate_dict[str(rate)]+=1
                                            vool_dict[str(vol)]+=1
                                            sll_dict[str(sl)]+=1
                                            tpp_dict[str(tp)]+=1
                                            lenEMA_dict[str(len_EMA)]+=1
                                            lenTrend_dict[str(len_trend)]+=1
                                           

            
            # Préparation de la ligne à écrire
            row = {'action': action['symbole'], 'parameters': best_parameters, 'strat_ratio':(j/i), 'results':{'strat': strat, 'rsi':rsi_dict, 'rate':raate_dict, 'vol': vool_dict, 'sll': sll_dict, 'tp': tpp_dict, 'lenEMA': lenEMA_dict}}
            row.update(final_result)
            writer.writerow(row)
            
            if best_parameters:
                row = {'action': action['symbole'], 'parameters': best_parameters, 'strat_ratio':(j/i), 'results':0}
                second_result=await main_backtest(action['symbole'], time_interval, period, best_parameters['strat'], best_parameters['rsi'], best_parameters['rate'], best_parameters['vol'], best_parameters['sl'], best_parameters['tp'],best_parameters['len_EMA'], best_parameters['len_trend'], 'second_backtest')
                row.update(second_result)
                writer.writerow(row)
            else:
                print('No results') 



### paramètres du backtest qu'on va utiliser pour tester notre programm xeeeezzæææ 
time_interval ="30min"    #en minutes (5,15,30)
length_in_months=1   #nombre de mois sur lesquels est réalisé le backtest

action={"nom": "Johnson & Johnson", "symbole": "JNJ", "secteur": "Pharmaceutique", "liquidite": "Haute"}
universe=[
    {"nom": "Microsoft", "symbole": "MSFT", "secteur": "Technologie", "liquidite": "Haute"},
    #{"nom": "Apple", "symbole": "AAPL", "secteur": "Technologie", "liquidite": "Haute"},
    #{"nom": "NVIDIA", "symbole": "NVDA", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Alphabet", "symbole": "GOOGL", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Amazon", "symbole": "AMZN", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Eli Lilly", "symbole": "LLY", "secteur": "Pharmaceutique", "liquidite": "Moyenne"},
    {"nom": "Broadcom", "symbole": "AVGO", "secteur": "Technologie", "liquidite": "Moyenne"},
    #{"nom": "JPMorgan Chase", "symbole": "JPM", "secteur": "Services financiers", "liquidite": "Haute"},
    #{"nom": "Tesla", "symbole": "TSLA", "secteur": "Automobile", "liquidite": "Haute"},
    #{"nom": "Visa", "symbole": "V", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "Walmart", "symbole": "WMT", "secteur": "Grande distribution", "liquidite": "Haute"},
    {"nom": "UnitedHealth", "symbole": "UNH", "secteur": "Assurance santé", "liquidite": "Moyenne"},
    {"nom": "ExxonMobil", "symbole": "XOM", "secteur": "Énergie", "liquidite": "Moyenne"},
    {"nom": "Mastercard", "symbole": "MA", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "Johnson & Johnson", "symbole": "JNJ", "secteur": "Pharmaceutique", "liquidite": "Haute"},
    {"nom": "Advanced Micro Devices", "symbole": "AMD", "secteur": "Technologie", "liquidite": "Moyenne"},
    #{"nom": "PepsiCo", "symbole": "PEP", "secteur": "Alimentation et boissons", "liquidite": "Moyenne"},
    {"nom": "AstraZeneca", "symbole": "AZN", "secteur": "Pharmaceutique", "liquidite": "Moyenne"},
    {"nom": "Royal Dutch Shell", "symbole": "SHEL", "secteur": "Énergie", "liquidite": "Moyenne"},
    {"nom": "Thermo Fisher Scientific", "symbole": "TMO", "secteur": "Science et technologie", "liquidite": "Haute"},
    {"nom": "Adobe", "symbole": "ADBE", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Qualcomm", "symbole": "QCOM", "secteur": "Technologie", "liquidite": "Moyenne"},
    {"nom": "Cisco", "symbole": "CSCO", "secteur": "Technologie", "liquidite": "Moyenne"},
    {"nom": "Accenture", "symbole": "ACN", "secteur": "Services informatiques", "liquidite": "Moyenne"},
    {"nom": "Walt Disney", "symbole": "DIS", "secteur": "Divertissement", "liquidite": "Haute"},
    {"nom": "General Electric", "symbole": "GE", "secteur": "Industrie", "liquidite": "Moyenne"},
    {"nom": "American Express", "symbole": "AXP", "secteur": "Services financiers", "liquidite": "Haute"},
    #{"nom": "TotalEnergies", "symbole": "TTE", "secteur": "Énergie", "liquidite": "Moyenne"},
    {"nom": "Verizon", "symbole": "VZ", "secteur": "Télécommunications", "liquidite": "Moyenne"},
    {"nom": "Morgan Stanley", "symbole": "MS", "secteur": "Services financiers", "liquidite": "Haute"},
    #{"nom": "Pfizer", "symbole": "PFE", "secteur": "Pharmaceutique", "liquidite": "Haute"},
    {"nom": "Goldman Sachs", "symbole": "GS", "secteur": "Services financiers", "liquidite": "Haute"},
    #{"nom": "IBM", "symbole": "IBM", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Philip Morris", "symbole": "PM", "secteur": "Tabac", "liquidite": "Moyenne"},
    {"nom": "Union Pacific", "symbole": "UNP", "secteur": "Transport ferroviaire", "liquidite": "Haute"},
    {"nom": "Royal Bank of Canada", "symbole": "RY", "secteur": "Services financiers", "liquidite": "Haute"},
    {"nom": "Suncor Energy", "symbole": "SU", "secteur": "Énergie", "liquidite": "Moyenne"},
    #{"nom": "Nike", "symbole": "NKE", "secteur": "Vêtements et chaussures", "liquidite": "Haute"},
    #{"nom": "Uber", "symbole": "UBER", "secteur": "Technologie", "liquidite": "Haute"},
    #{"nom": "Airbus", "symbole": "AIR", "secteur": "Aérospatiale", "liquidite": "Moyenne"},
    {"nom": "Intel", "symbole": "INTC", "secteur": "Technologie", "liquidite": "Haute"},
    #{"nom": "Meta", "symbole": "META", "secteur": "Technologie", "liquidite": "Haute"},
    #{"nom": "Netflix", "symbole": "NFLX", "secteur": "Services de diffusion en continu", "liquidite": "Moyenne"},
    {"nom": "PayPal", "symbole": "PYPL", "secteur": "Services financiers", "liquidite": "Moyenne"},
    {"nom": "Square", "symbole": "SQ", "secteur": "Technologie financière", "liquidite": "Moyenne"},
    {"nom": "Salesforce", "symbole": "CRM", "secteur": "Logiciels", "liquidite": "Moyenne"},
    {"nom": "Zoom", "symbole": "ZM", "secteur": "Technologie de communication", "liquidite": "Moyenne"},
    {"nom": "DocuSign", "symbole": "DOCU", "secteur": "Technologie d'entreprise", "liquidite": "Moyenne"},
    {"nom": "Shopify", "symbole": "SHOP", "secteur": "Commerce électronique", "liquidite": "Moyenne"},
    #{"nom": "Adobe", "symbole": "ADBE", "secteur": "Technologie", "liquidite": "Haute"},
    {"nom": "Palantir Technologies", "symbole": "PLTR", "secteur": "Analytique de données", "liquidite": "Moyenne"},
    {"nom": "Roblox", "symbole": "RBLX", "secteur": "Jeux vidéo", "liquidite": "Moyenne"},
    {"nom": "Unity Software", "symbole": "U", "secteur": "Technologie", "liquidite": "Moyenne"},
    {"nom": "Snowflake", "symbole": "SNOW", "secteur": "Informatique en nuage", "liquidite": "Moyenne"},
    {"nom": "Asana", "symbole": "ASAN", "secteur": "Logiciels", "liquidite": "Moyenne"},
    {"nom": "Twilio", "symbole": "TWLO", "secteur": "Technologie de communication", "liquidite": "Moyenne"},
    {"nom": "Fastly", "symbole": "FSLY", "secteur": "Technologie de l'information", "liquidite": "Moyenne"},
    {"nom": "PagerDuty", "symbole": "PD", "secteur": "Logiciels", "liquidite": "Moyenne"},
    {"nom": "Datadog", "symbole": "DDOG", "secteur": "Logiciels", "liquidite": "Moyenne"},
    {"nom": "Etsy", "symbole": "ETSY", "secteur": "Commerce électronique", "liquidite": "Moyenne"}

]


import time

start_time=time.time()
#lancement du programme principal de backtest avec 
asyncio.run(extraction(time_interval, length_in_months, action))
end_time=time.time()

print(end_time-start_time)