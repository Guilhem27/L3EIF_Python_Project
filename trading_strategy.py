#strats de confirmation intradays
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


#strats de positionnement (global)

def mouvement_haussier_stoch(stoch):
    bool=False
    #Surachat suivi d'un repli 
    for i in range(15, -1, -1):
        if stoch[i]['K%']>=80:  #surachat
            for j in range(i, -1, -1):
                if stoch[j]['K%']<60: #repli
                    if stoch[0]['K%']>70: 
                        bool=True
                        return bool
    #Croisement haussier
    for i in range(15, -1, -1):
        if stoch[i]['K%']<stoch[i]['D%']:  
            for j in range(i, 2, -1):
                if stoch[j]['K%']>stoch[j]['D%']:
                    bool=True
                    for y in range(j, -1, -1):
                        if stoch[y]['K%']<stoch[y]['D%']:
                            bool=False
                    return bool
    return bool

def mouvement_baissier_stoch(stoch):
    bool=False
    #Surachat suivi d'un repli 
    for i in range(15, -1, -1):
        if stoch[i]['K%']<=20:  #surachat
            for j in range(i, -1, -1):
                if stoch[j]['K%']>40: #repli
                    if stoch[0]['K%']<30: 
                        bool=True
                        return bool
    #Croisement haussier
    for i in range(15, -1, -1):
        if stoch[i]['K%']>stoch[i]['D%']:  
            for j in range(i, 2, -1):
                if stoch[j]['K%']<stoch[j]['D%']:
                    bool=True
                    for y in range(j, -1, -1):
                        if stoch[y]['K%']>stoch[y]['D%']:
                            bool=False
                    return bool
    return bool

def mouvement_haussier_RSI(RSI):
    return_value=0
    if RSI[0]>70:
        return_value+=1
    #Croisement haussier
    for i in range(15, -1, -1):
        if RSI[i]<50:  
            for j in range(i, 2, -1):
                if RSI[j]>50:
                    return_value+=1
                    for y in range(j, -1, -1):
                        if RSI[y]<50:
                            return_value-=1
                            return return_value
                    return return_value
    return return_value

def mouvement_baissier_RSI(RSI):
    return_value=0
    if RSI[0]<30:
        return_value+=1
    #Croisement haussier
    for i in range(15, -1, -1):
        if RSI[i]<50:  
            for j in range(i, 2, -1):
                if RSI[j]<50:
                    return_value+=1
                    for y in range(j, -1, -1):
                        if RSI[y]>50:
                            return_value-=1
                            return return_value
                    return return_value
    
def mouvement_bollinger(bandes):
    diff=0
    return_value=2
    for values in bandes:
        if values["bande_superieure"]-values["bande_inférieure"]<diff:
            return_value=1
        diff=values["bande_superieure"]-values["bande_inférieure"]
    if (bandes[0]["bande_superieure"]-bandes[0]["bande_inférieure"])<(bandes[-1]["bande_superieure"]-bandes[-1]["bande_inférieure"]):
        return_value-=1
    return return_value



 #strat globale   

def strat(candlestick, infos):
    trade=0

    #consolidation (on peut trade à la hausse comme à la baisse en c)
    if infos['trend']['growth_rate']<=5 or infos['trend']['growth_rate']>=-5:

        #à la hausse
        if infos['last_OCLH'][1]['4. close']>infos['pivots']['pp'] and candlestick['4. close']<infos['pivots']['r1'] and infos['last_OCLH'][1]['1. open']<infos['pivots']['r1'] and candlestick['1. open']>infos['pivots']['pp']: #position entre pp et r

            if infos['movement']['move']>0 and infos['movement']['length']>1:
                trade+=1

            if candlestick['4. close']<infos['trend']['long_trend']:  #sous_evaluation
                trade+=1

            if mouvement_haussier_stoch(infos['indic_stoch'][:16]):
                trade+=2

            trade+=mouvement_haussier_RSI(infos['indic_RSI'][:16])

            trade+=mouvement_bollinger(infos['indic_bolling'][:10])

        if trade>=5:
            return {'stopLoss':infos['pivots']['r1']-infos['indic_ATR'], 'takeProfit': infos['pivots']['r2'], 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"sortie_consolid_hausse"}
        else:
            trade=0  

        #à la baisse
        if infos['last_OCLH'][1]['4. close']<infos['pivots']['pp'] and candlestick['4. close']>infos['pivots']['s1'] and infos['last_OCLH'][1]['1. open']<infos['pivots']['pp'] and candlestick['1. open']>infos['pivots']['s1']: #position entre pp et r

            if infos['movement']['move']<0 and infos['movement']['length']>1:
                trade+=1

            if candlestick['4. close']>infos['trend']['long_trend']:  #sous_evaluation
                trade+=1

            if mouvement_baissier_stoch(infos['indic_stoch'][:16]):
                trade+=2

            trade+=mouvement_baissier_RSI(infos['indic_RSI'][:16])

            trade+=mouvement_bollinger(infos['indic_bolling'][:10])

        if trade>=5:
            return {'stopLoss':infos['pivots']['s1']+infos['indic_ATR'], 'takeProfit': infos['pivots']['s2'], 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"sortie_consolid_baisse"}
        else:
            trade=0  

    #retournement haussier 
    if infos['trend']['growth_rate']>5:

        if infos['last_OCLH'][1]['2. low']>infos['pivots']['pp'] and candlestick['3. low']<infos['pivots']['pp']: #l'avant dernière ne traverse pas mais la dernière si

            if infos['movement']['move']<0 and infos['movement']['length']>1:
                

                if candlestick['4. close']<infos['trend']['long_trend']:  #sous_evaluation
                    trade+=1

                if mouvement_haussier_stoch(infos['indic_stoch'][:16]):
                    trade+=2

                trade+=mouvement_haussier_RSI(infos['indic_RSI'][:16])

                trade+=mouvement_bollinger(infos['indic_bolling'][:10])


        if trade>=5:

            return {'stopLoss':infos['pivots']['pp']-2*infos['indic_ATR'], 'takeProfit': infos['pivots']['r1'], 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"retournement_haussier"}
        
        else:
            trade=0  
        
        #retournement baissier 

    if infos['trend']['growth_rate']<-5:

        if infos['last_OCLH'][1]['3. high']<infos['pivots']['pp'] and candlestick['3. high']>infos['pivots']['pp']: #l'avant dernière ne traverse pas mais la dernière si

            if infos['movement']['move']>0 and infos['movement']['length']>1:
            
                if candlestick['4. close']>infos['trend']['long_trend']:  #sur_evaluation
                    trade+=1                                                #voir si utilisation des croisements ema et sma

                if mouvement_baissier_stoch(infos['indic_stoch'][:16]):
                    trade+=2

                trade+=mouvement_baissier_RSI(infos['indic_RSI'][:16])

                trade+=mouvement_bollinger(infos['indic_bolling'][:10])


        if trade>=5:

            return {'stopLoss':infos['pivots']['pp']+2*infos['indic_ATR'], 'takeProfit': infos['pivots']['s1'], 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"retournement_baissier"}
        
        else:
            trade=0  



#strat de confirmation
                    
def strat_confirmation(candlestick, positions, level, last_ohlc):

    if positions['type_trade']=="sortie_consolid_hausse":

        if positions['confirmation']==0:
            for price in candlestick.values():
                if price>level['r1']:
                   positions['confirmation']+=1

        if positions['confirmation']==1:
            if candlestick['4. close']<level['r1']:
                positions['confirmation']=0
        
            if marubozu(candlestick) or soldats_blancs(last_ohlc):
                positions['confirmation']=2


    if positions['type_trade']=="sortie_consolid_baisse":

        if positions['confirmation']==0:
            for price in candlestick.values():
                if price<level['s1']:
                   positions['confirmation']=1

        if positions['confirmation']==1:
            if candlestick['4. close']>level['s1']:
                positions['confirmation']=0
        
            if marubozu(candlestick) or corbeaux_rouges(last_ohlc):
                positions['confirmation']=2
        
    if positions['type_trade']=="retournement_haussier":

        if positions['confirmation']==0:
            if candlestick['2. high']>level['pp']  and last_ohlc[1]['4. closing']<level['pp'] :
                positions['confirmation']=1

            if englobante_hauss(last_ohlc):
                positions['confirmation']=2

            elif hammer(last_ohlc):
                positions['confirmation']=2
                positions['stopLoss']=last_ohlc[0]['3. low']


        positions['type_position']=="buy"


    if positions['type_trade']=="retournement_baissier":

        if positions['confirmation']==0:
            if candlestick['3. low']<level['pp']  and last_ohlc[1]['4. closing']>level['pp'] :
                positions['confirmation']=1

            if englobante_baiss(last_ohlc):
                positions['confirmation']=2

            elif hammer(last_ohlc):
                positions['confirmation']=2
                positions['stopLoss']=last_ohlc[0]['2. high']


        positions['type_position']=="sell"






