#fonction de prise de position principale
#prend comme arguments la bougie actuelle et les informations précédentes (bougies et indicateurs)
#compare la situation réelle avec des stratégies de prise de position précises
def strat(candlestick, infos, last_ohlc):

    if float(last_ohlc[1]['2. high'])<infos['pivots']['pp'] and candlestick['2. high']<infos['pivots']['pp']:
        #on regarde si l'on est dans un mouvement d'au moins 2 bougies haussières
        if infos['movement']['move']>0 and infos['movement']['length']>2:
            
            if mouvement_haussier_RSI(infos['indic_RSI'][:16])==1 and infos['trend']['value_growth']>0:
                
                print({'stopLoss':(infos['pivots']['s1']+3*infos['indic_ATR']), 'takeProfit': (infos['pivots']['r2']-2*infos['indic_ATR']), 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"sortie_consolid_hausse"})
                print(candlestick)
                return {'stopLoss':(infos['pivots']['s1']+5*infos['indic_ATR']), 'takeProfit': (infos['pivots']['r2']-2*infos['indic_ATR']), 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"sortie_consolid_hausse"}

            if mouvement_baissier_RSI(infos['indic_RSI'][:16])==2 and infos['trend']['value_growth']<0:
                
                print({'stopLoss':(infos['pivots']['s1']+3*infos['indic_ATR']), 'takeProfit': (infos['pivots']['r2']-2*infos['indic_ATR']), 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"retournement_baisse"})
                print(candlestick)                
                return {'stopLoss':(infos['pivots']['s1']+5*infos['indic_ATR']), 'takeProfit': (infos['pivots']['r2']-2*infos['indic_ATR']), 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"retournement_baisse"}



    #on regarde si l'on est dans un mouvement d'au moins 2 bougies baissières
    if infos['movement']['move']<0 and infos['movement']['length']>2:

        if float(last_ohlc[1]['3. low'])>infos['pivots']['pp'] and candlestick['3. low']>infos['pivots']['pp']:            
            
            if mouvement_baissier_RSI(infos['indic_RSI'][:16])==1 and infos['trend']['value_growth']<0:
                
                print({'stopLoss':(infos['pivots']['r1']-5*infos['indic_ATR']), 'takeProfit': (infos['pivots']['s2']+2*infos['indic_ATR']), 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"sortie_consolid_baisse"})
                print(candlestick)
                return {'stopLoss':(infos['pivots']['r1']-5*infos['indic_ATR']), 'takeProfit': (infos['pivots']['s2']+2*infos['indic_ATR']), 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"sortie_consolid_baisse"}
        
            if mouvement_haussier_RSI(infos['indic_RSI'][:16])==2 and infos['trend']['value_growth']>0:
                
                print({'stopLoss':(infos['pivots']['r1']-5*infos['indic_ATR']), 'takeProfit': (infos['pivots']['s2']+2*infos['indic_ATR']), 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"retournement_baisse"})
                print(candlestick)
                return {'stopLoss':(infos['pivots']['r1']-5*infos['indic_ATR']), 'takeProfit': (infos['pivots']['s2']+2*infos['indic_ATR']), 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"retournement_baisse"}


    #renvoie d'une situation neutre, sans position, si aucune stratégie ne correspond à la situation
    return {'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None,'type_trade':None}  



#fonctions d'analyse de positions
def mouvement_haussier_RSI(RSI):
    #compteur renvoyé à l'issue pour évaluer l'évidence du mouvement haussier
    return_value=0
    
    if RSI[0]<50:
        return_value=1

    #situation de survente (potentiel retournement)
    if RSI[0]<30:
        return_value=2

    #Croisement haussier
    #Parcours des données stochastiques dans l'ordre décroissant (de la plus ancienne à la plus récente)
    for i in range(15, -1, -1):
        
        #on cherche une situation en dessous de la moyenne (avant un croisement)
        if RSI[i]<50:  
            #on itère sur les valeurs suivantes
            for j in range(i, 2, -1):
                #on observe un croisement: le RSI a dépassé la moyenne
                if RSI[j]>50:
                    #on valide le croisement
                    return_value=1

                    #on vérifie sur les valeurs les plus récentes si ce croisement n'a pas été annulé
                    for y in range(j, -1, -1):
                        if RSI[y]<50:
                            #dans ce cas on invalide en enlevant 1
                            return_value=0
                            
                    return return_value
    #aucun situation n'a été observée on renvoie 0
    return return_value

def mouvement_baissier_RSI(RSI):

    #compteur renvoyé à l'issue pour évaluer l'évidence du mouvement haussier
    return_value=0

    if RSI[0]<50:
        return_value=1

    #situation de survente (potentiel retournement)
    if RSI[0]>70:
        return_value=2

    #Croisement baissier
    #Parcours des données stochastiques dans l'ordre décroissant (de la plus ancienne à la plus récente)
    for i in range(15, -1, -1):

        #on cherche une situation au dessus de la moyenne (avant un croisement)
        if RSI[i]<50:  
           
           #on itère sur les valeurs suivantes
            for j in range(i, 2, -1):

                #on observe un croisement: le RSI est passé sous la moyenne
                if RSI[j]<50:
                    return_value=1
                     
                    #on vérifie sur les valeurs les plus récentes si ce croisement n'a pas été annulé
                    for y in range(j, -1, -1):
                        if RSI[y]>50:
                            #dans ce cas on invalide en enlevant 1
                            return_value=0
                
    #aucun situation n'a été observée on renvoie 0
    return return_value



 
#Fonction de confirmation de prise de position
#Prend en arguments la dernière bougie, la position que l'on veut confirmer, les points pivots et les 100 dernières bougies   
def strat_confirmation(candlestick, positions, level, last_ohlc, trend):

    #confirmation d'une position de sortie de phase de consolidation haussière
    if positions['type_trade']=="sortie_consolid_hausse":
        
        if positions['confirmation']==0:

            for type, price in candlestick.items():
                if float(price)>level['pp'] and type!='5. volume':
                    positions['confirmation']=1
                    print('touchup', price)

        elif positions['confirmation']==1:
            if (float(last_ohlc[0]['5. volume'])+float(last_ohlc[1]['5. volume'])+float(last_ohlc[2]['5. volume']))/3>1.4*trend['volume_mean']:
                positions['confirmation']=2
                print(candlestick)
    #confirmation d'une position de retournement baissier
    if positions['type_trade']=="retournement_baisse":
        
        if positions['confirmation']==0:
            for type, price in candlestick.items():
                if float(price)>level['pp'] and type!='5. volume':
                    positions['confirmation']=1
                    print('touchdown', price)
            
        elif positions['confirmation']==1:
            
            for type, price in candlestick.items():
                if float(price)<level['pp'] and type!='5. volume':
                    positions['confirmation']=2
                    print(candlestick)

    #confirmation d'une position de sortie de phase de consolidation baissière
    if positions['type_trade']=="sortie_consolid_baisse":
        
        if positions['confirmation']==0:
            for type, price in candlestick.items():
                if float(price)<level['pp'] and type!='5. volume':
                    positions['confirmation']=1
                    print('touchdown', price)
                    

        elif positions['confirmation']==1:
            if (float(last_ohlc[0]['5. volume'])+float(last_ohlc[1]['5. volume'])+float(last_ohlc[2]['5. volume']))/3>1.4*(trend['volume_mean']):
                positions['confirmation']=2
                print(candlestick)

    #confirmation d'une position de retournement haussier
    if positions['type_trade']=="retournement_hausse":
        
        if positions['confirmation']==0:
            for type, price in candlestick.items():
                if float(price)<level['pp'] and type!='5. volume':
                    positions['confirmation']=1
                    print('touchdown', price)
            
        elif positions['confirmation']==1:
            print('ok')
            for type, price in candlestick.items():
                if float(price)>level['pp'] and type!='5. volume':
                    positions['confirmation']=2
                    print(candlestick)
                

    return positions
    

#fonctions de confirmation des stratégies en considération de motifs intradays

def marubozu(ohlc):
    # Calcul de la taille du corps de la bougie
    corps_bougie = abs(ohlc['1. open'] - ohlc['4. close'])
    
    # Calcul de la taille des ombres de la bougie
    ombre_haute = ohlc['2. high'] - max(ohlc['1. open'], ohlc['4. close'])
    ombre_basse = min(ohlc['1. open'], ohlc['4. close']) - ohlc['3. low']
    
    # Vérification des conditions pour un marubozu blanc
    if corps_bougie >= 0.9 * (ohlc['2. high'] - ohlc['3. low']) and ombre_haute <= 0.05 * (ohlc['2. high'] - ohlc['3. low']) and ombre_basse <= 0.05 * (ohlc['2. high'] - ohlc['3. low']):
        return True
    else:
        return False
      
def soldats_blancs(last_ohlc):

    # Calculer les plages (ranges) des trois bougies
    ranges = [ohlc['2. high'] - ohlc['3. low'] for ohlc in last_ohlc[:2]]
    
    # Vérifier que chaque bougie a un corps relativement grand
    for r in ranges:
        if r < 0.5 * max([ohlc['2. high'] - ohlc['3. low'] for ohlc in last_ohlc[:2]]):
            return False
    
    # Vérifier que les plages des bougies sont approximativement égales
    range_mean = sum(ranges) / len(ranges)
    for r in ranges:
        if abs(r - range_mean) > 0.2 * range_mean:
            return False
    
    # Vérifier que chaque bougie est haussière
    for ohlc in last_ohlc:
        if ohlc['4. close'] < ohlc['1. open']:
            return False
    
    # Vérifier que chaque bougie se ferme plus haut que la précédente
    for i in range(0, 2):
        if last_ohlc[i]['4. close'] > last_ohlc[i + 1]['4. close']:
            return False
    
    return True

def corbeaux_rouges(last_ohlc):

    # Calculer les plages (ranges) des trois bougies
    ranges = [ohlc['3. low'] - ohlc['2. high'] for ohlc in last_ohlc[:2]]
    
    # Vérifier que chaque bougie a un corps relativement grand
    for r in ranges:
        if r < 0.5 * max([ohlc['3. low'] - ohlc['2. high'] for ohlc in last_ohlc[:2]]):
            return False
    
    # Vérifier que les plages des bougies sont approximativement égales
    range_mean = sum(ranges) / len(ranges)
    for r in ranges:
        if abs(r - range_mean) > 0.2 * range_mean:
            return False
    
    # Vérifier que chaque bougie est baissière
    for ohlc in last_ohlc:
        if ohlc['4. close'] < ohlc['1. open']:
            return False
    
    # Vérifier que chaque bougie se ferme plus haut que la précédente
    for i in range(0, 2):
        if last_ohlc[i]['4. close'] < last_ohlc[i + 1]['4. close']:
            return False
    
    return True

def hammer(last_ohlc):
    body_size = abs(last_ohlc[1]['4. close'] - last_ohlc[1]['1. open'])
    upper_shadow_size = last_ohlc[1]['2. high'] - max(last_ohlc[1]['1. open'], last_ohlc[1]['4. close'])
    lower_shadow_size = min(last_ohlc[1]['1. open'], last_ohlc[1]['4. close']) - last_ohlc[1]['3. low']
    # Conditions pour identifier un marteau
    if (body_size <= 2 * lower_shadow_size and upper_shadow_size <= 0.2 * body_size) or (body_size >= 2 * lower_shadow_size and upper_shadow_size >= 0.2 * body_size):
        return True
    else:
        return False

def englobante_hauss(last_ohlc):
    if last_ohlc[1]['4. close'] < last_ohlc[1]['1. open'] and last_ohlc[0]['4. close'] > last_ohlc[0]['1. open']:
        # Vérifier si la période actuelle englobe complètement la période précédente
        if last_ohlc[0]['4. close'] > last_ohlc[1]['2. high'] and last_ohlc[0]['1. open'] <last_ohlc[1]['3. low']:
            return True   
    return False

def englobante_baiss(last_ohlc):
    if last_ohlc[1]['4. close'] > last_ohlc[1]['1. open'] and last_ohlc[0]['4. close'] < last_ohlc[0]['1. open']:
        # Vérifier si la période actuelle englobe complètement la période précédente
        if last_ohlc[0]['4. close'] < last_ohlc[1]['3. low'] and last_ohlc[0]['1. open'] >last_ohlc[1]['1. open']:
            return True   
    return False






