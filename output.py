#appel des modules indicateurs qui permettent de mettre quotidiennement à jour les informations d'AT qu'on utilisera pour nos prises de positions
from indicators import movement, pivots, stochastic_oscillator, RSI, ATR, trend

#appel des modules de trading, c'est-à-dire de décision concernant une prise de position en deux temps, un signal d'achat/de vente, et une confirmation de cette position
from trading_strategy import strat, strat_confirmation

#ROUTINE DE TRADING ALGORITHMIQUE
#fonction principale du programme appelée quotidiennement avec les données de trading du jour. 
#Elle prend en compte les mouvements de prix, calcule les indicateurs techniques, prend des décisions 
#de trading basées sur une stratégie pré-définie, et gère les positions ouvertes en conséquence
def daily_trade(raw_data, last_infos):

    #liste des rendements (ainsi que du type de trade) réalisés sur chaque position prise dans la journée de trade
    trade_infos=[]

    #récupère le montant encore disponible dans le compte en fermeture de la veille
    initial_cash=last_infos['cash']

    #vérifie s'il reste encore de l'argent sur le compte, dans le cas contraire le programme s'arrête
    if last_infos['cash']<=0:
        return 'fail'

    #initialisation des positions de trade en situation d'absence de position
    positions={'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None ,'type_trade':None}
    
    #signaux d'achat ou de vente
    buy=None
    sell=None

    #calcul des points pivots en reprennant le niveau max, min et le closing de la veille
    last_infos['pivots']=pivots(last_infos['max'], last_infos['min'], last_infos['closing'])

    #on les réinitialise pour pouvoir les recalculer sur la nouvelle journée
    last_infos['max']=0
    last_infos['min']=100000000000
    last_infos['closing']=0

    #récupération des 100 dernières données ohlc en date (celles de la veille), la variable permet de simplifier le code
    last_ohlc=last_infos['last_ohlc']

    #délai d'attente de confirmation d'une prise de position initialisé à 0,
    #si il se passe 5 bougies sans confirmation, on considère que la position n'est pas confirmée
    waiting_confirmation=0

    #boucle sur l'ensemble des données de la journée en extrayant le dictionnaire avec les seules valeurs ohlc
    for time, ohlc in raw_data.items():
        
        #les valeurs ohlc sont récupérées en valeurs string, on les passe en valeurs décimales arrondies à 5 chiffres après la virgule
        ohlc['1. open'] = round(float(ohlc['1. open']),5)
        ohlc['2. high'] = round(float(ohlc['2. high']),5)
        ohlc['3. low'] = round(float(ohlc['3. low']),5)
        ohlc['4. close'] = round(float(ohlc['4. close']),5)

        #pour le calcul quotidien des points pivots, on stocke dans le dictionnaire 'last_infos' les valeurs maximale, minimale et le closing de cette journée
        if ohlc['2. high']>last_infos['max']:
            last_infos['max']=ohlc['2. high']
        if ohlc['3. low']<last_infos['min']:
            last_infos['min']=ohlc['3. low']
        last_infos['closing']=ohlc['4. close']

        #suppression de la 100ème valeur ohlc listée et ajout de la nouvelle valeur   
        last_ohlc.pop()
        last_ohlc.insert(0,ohlc)
        #mise à jour dans le dictionnaire last_infos pour pouvoir être récupéré le lendemain
        last_infos['last_ohlc']=last_ohlc

        #calcul des indicateurs

        last_infos['trend']=trend(last_ohlc[:100])

        #'indic_ATR' rend une valeur qui permet d'évaluer les TP et SL (sorte d'écart-type), calculé sur les 14 derniers ohlc
        last_infos['indic_ATR']=ATR(last_ohlc[:14])
        
        #'indic_RSI' prend 16 valeurs de la plus récente à la plus ancienne, calculées sur les 14 dernières valeurs OHLC
        #permet d'évaluer des situations de surachat/survente
        last_infos['indic_RSI'].pop()
        last_infos['indic_RSI'].insert(0,RSI(last_ohlc[:14]))

        #'indic_RSI' prend 16 valeurs de la plus récente à la plus ancienne, calculées sur les 14 dernières valeurs OHLC
        #permet d'évaluer des situations de surachat/survente
        last_infos['indic_stoch'].pop()
        last_infos['indic_stoch'].insert(0, stochastic_oscillator(last_ohlc[:14]))


        #'movement' rend compte du mouvement en cours (e.g.:{'length': 4, 'move': 0.04} signifie 
        #qu'il y aun mouvement haussier de 4 pourcents ininterrompu sur 4 ohlc) 
        last_infos['movement']=movement(ohlc, last_infos['movement'])



        #considération d'une position d'achat (prend en compte une position "short"), pour considérer une potentielle sortie de position ou non
        if positions['buy']==True:
            
            #fermeture de position

            #dépassement haussier du TP en position longue ou dépassement baissier du TP eb position courte
            if (ohlc['2. high']>=positions['takeProfit'] and positions['type_position']=='buy') or (ohlc['3. low']<=positions['takeProfit'] and positions['type_position']=='sell'):
                sell=buy['units']*positions['takeProfit']

            #dépassement baissier du SL en position longue ou dépassement haussier du SL en position courte
            elif (ohlc['3. low']<=positions['stopLoss'] and positions['type_position']=='buy') or (ohlc['2. high']>=positions['stopLoss'] and positions['type_position']=='sell'):
                sell=buy['units']*positions['stopLoss']  
            
            #sortie de position avant la fin de la journée car daytrading, afin d'éviter le gap de marché
            elif time=='19:30:00' or time=='19:35:00' or time=='19:40:00' or time=='19:45:00' or time=='19:50:00' or time=='19:55:00' or time=='20:00:00':
                sell=buy['units']*ohlc['4. close']


            #si fermeture de position, sell prend alors le money out de la position
            if sell!=None:

                print(sell, (sell/buy['units']))
                print(time, 'vendre')

                #récupération de la valeur du compte avant la prise position pour le calcul de rendement
                last_cash=last_infos['cash']

                #considération du gain/perte de la position sur le compte investisseur 
                #calcul différent selon qu'on soit sur une position longue ou courte
                if positions['type_position']=="sell":
                    last_infos['cash']-=sell-buy['units']*buy['price']
                else:  
                    last_infos['cash']+=sell-buy['units']*buy['price']
                
                #récupération de la performance (rendement sur la position et type de trade (retournement haussier, conitnuation baissière....))
                trade_infos.append({'gains':round(last_infos['cash']/last_cash-1, 8), 'trade': positions['type_trade']})
                
                #réinitialisation du dictionnaire 'positions' pour se remettre en position d'analyse technique
                positions={'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None,'type_trade':None}
                
                sell=None
                buy=None



        #pas de position prise, on est en situation d'analyse ou d'attente de confirmation d'une prise de position
        if positions['buy']==False:
        #prise de décision

            #recherche de position interessante en fonction du prix si pas de position existante
            if positions=={'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False,'type_position': None, 'type_trade':None}:
                positions=strat(ohlc, last_infos, last_ohlc)
                
            
            #attente de confirmation avec un délai de 5 candlestick, sinon on cherche une nouvelle position
            else:
                
                positions=strat_confirmation(ohlc, positions, last_infos['pivots'], last_ohlc[0:3], last_infos['trend'])
                waiting_confirmation+=1
                

            #annulation de la position après 5 ohlc
            if waiting_confirmation==8:
                positions={'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False,'type_position': None, 'type_trade':None}
                waiting_confirmation=0
    
            #confirmation et prise de position
            if positions['confirmation']==2:

                #idem que précédemment
                buy={'price':ohlc['4. close'], 'units': round(last_infos['cash']/ohlc['1. open'],3)}
                positions['buy']=True
                waiting_confirmation=0
                print(buy)
                print(time, 'achat')
                
    print(trade_infos)
    #renvoi des dernières informations, du rendement réalisé sur la journée et des informations sur le(s) trade(s) réalisé(s) sur la journée
    return  {'last_infos': last_infos, 'yield':last_infos['cash']/initial_cash, 'trade_infos':trade_infos}




