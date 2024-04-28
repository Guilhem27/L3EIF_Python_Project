#fonction de prise de position principale
#prend comme arguments la bougie actuelle et les informations précédentes (bougies et indicateurs)
#compare la situation réelle avec des stratégies de prise de position précises
def strat(candlestick, infos, last_ohlc):
    
    #compteur permettant d'évaluer la validité d'une position
    trade=0
    
    #stratégie de sortie de consolidation (on peut trade à la hausse comme à la baisse en sortie d'une phase de consolidation matérialisée par des taux de croissance [-3%:3%]
    if infos['trend']['growth_rate']<=3 or infos['trend']['growth_rate']>=-3:

        #sortie de phase à la hausse si la bougie précédente et celle actuelle sont comprises entre le point pivot et le niveau de résistance 1
        if float(last_ohlc[1]['4. close'])>infos['pivots']['pp'] and candlestick['4. close']<infos['pivots']['r1'] and float(last_ohlc[1]['1. open'])<infos['pivots']['r1'] and candlestick['1. open']>infos['pivots']['pp']: 
            
            #on regarde si l'on est dans un mouvement d'au moins 2 bougies haussières
            if infos['movement']['move']>0 and infos['movement']['length']>1:
                #dans ce cas notre "score" de validité de position prend +1
                trade+=1

            #analyse de l'indicateur Stochastique avec un potentiel croisement haussier ou d'un mouvement de surachat suivi d'un repli qui annoncent une potentielle hausse 
            if mouvement_haussier_stoch(infos['indic_stoch'][:16]):
                #ajout de 2 dans le cas où la fonction 'mouvement_haussier_stoch' renvoie True
                trade+=2

            #analyse de l'indicateur RSI avec un potentiel croisement haussier ou une situation de survente qui annoncent une potentielle hausse
            trade+=mouvement_haussier_RSI(infos['indic_RSI'][:16])

            #analyse des bandes de bollinger pour chercher un potentiel écartement des bandes synonyme d'un potentiel mouvement 
            trade+=mouvement_bollinger(infos['indic_bolling'][:10])
        
        #si le score dépasse 5 on évalue un potentiel mouvement haussier 
        if trade>=5:
            #on annonce des niveaux de TP et SL en s'appuyant sur les points pivots et l'ATR, en attendant une confirmation mais en annonçant le type de trade qui serait alors réalisé
            return {'stopLoss':(infos['pivots']['r1']-infos['indic_ATR']), 'takeProfit': infos['pivots']['r2'], 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"sortie_consolid_hausse"}
        
        #dans le cas contraire on réinitialise le score pour tester d'autres stratégies
        else:
            trade=0  

        
        
        
        #sortie de phase à la baisse si la bougie précédente et celle actuelle sont comprises entre le point pivot et le niveau de support 1
        if float(last_ohlc[1]['4. close'])<infos['pivots']['pp'] and candlestick['4. close']>infos['pivots']['s1'] and float(last_ohlc[1]['1. open'])<infos['pivots']['pp'] and candlestick['1. open']>infos['pivots']['s1']: #position entre pp et r
            
            #on regarde si l'on est dans un mouvement d'au moins 2 bougies baissières
            if infos['movement']['move']<0 and infos['movement']['length']>1:
                trade+=1

            #analyse de l'indicateur Stochastique avec un potentiel croisement baissier ou d'un mouvement de survente suivi d'un repli qui annoncent une potentielle baisse             
            if mouvement_baissier_stoch(infos['indic_stoch'][:16]):
                trade+=2

            #analyse de l'indicateur RSI avec un potentiel croisement baissier ou une situation de surachat qui annoncent une potentielle hausse
            trade+=mouvement_baissier_RSI(infos['indic_RSI'][:16])

            #analyse des bandes de bollinger pour chercher un potentiel écartement des bandes synonyme d'un potentiel mouvement 
            trade+=mouvement_bollinger(infos['indic_bolling'][:10])

        #si le score dépasse 5 on évalue un potentiel mouvement haussier 
        if trade>=5:
            #on annonce des niveaux de TP et SL en s'appuyant sur les points pivots et l'ATR, en attendant une confirmation mais en annonçant le type de trade qui serait alors réalisé
            return {'stopLoss':(infos['pivots']['s1']+infos['indic_ATR']), 'takeProfit': infos['pivots']['s2'], 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"sortie_consolid_baisse"}
        
        #dans le cas contraire on réinitialise le score pour tester d'autres stratégies
        else:
            trade=0



    #"retournement" haussier (en trend haussière avec plus de 3% de croissance pour ne pas trade contre la trend)(retournement sur le PP)
    if infos['trend']['growth_rate']>3:

        #la dernière bougie est au dessus du point pivot mais la nouvelle traverse le niveau
        if float(last_ohlc[1]['3. low'])>infos['pivots']['pp'] and candlestick['3. low']<infos['pivots']['pp']: #l'avant dernière ne traverse pas mais la dernière si
        
            #analyse de l'indicateur Stochastique avec un potentiel croisement haussier ou d'un mouvement de surachat suivi d'un repli qui annoncent une potentielle hausse             
            if mouvement_haussier_stoch(infos['indic_stoch'][:16]):
                trade+=2

            #analyse de l'indicateur RSI avec un potentiel croisement haussier ou une situation de survente qui annoncent une potentielle hausse
            trade+=mouvement_haussier_RSI(infos['indic_RSI'][:16])

            #analyse des bandes de bollinger pour chercher un potentiel écartement des bandes synonyme d'un potentiel mouvement 
            trade+=mouvement_bollinger(infos['indic_bolling'][:10])

            #analyse d'un potentiel rebond sur la bande inférieur de bollinger
            if float(last_ohlc['3. low'])<infos['indic_bolling']["bande_inférieure"]:
                trade+=1

        #si le score dépasse 5 on évalue un potentiel mouvement haussier 
        if trade>=5:
            #on annonce des niveaux de TP et SL en s'appuyant sur les points pivots et l'ATR, en attendant une confirmation mais en annonçant le type de trade qui serait alors réalisé
            return {'stopLoss':(infos['pivots']['pp']-2*infos['indic_ATR']), 'takeProfit': infos['pivots']['r1'], 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"retournement_haussier"}
        
        else:
            trade=0  




    #"retournement" baissier (en trend baissière avec moins de 3% de croissance pour ne pas trade contre la trend)(retournement sur le PP)
    if infos['trend']['growth_rate']<-3:

        #la dernière bougie est en dessous du point pivot mais la nouvelle traverse le niveau
        if float(last_ohlc[1]['2. high'])<infos['pivots']['pp'] and candlestick['2. high']>infos['pivots']['pp']: #l'avant dernière ne traverse pas mais la dernière si

        
            #analyse de l'indicateur Stochastique avec un potentiel croisement baissier ou d'un mouvement de survente suivi d'un repli qui annoncent une potentielle baisse             
            if mouvement_baissier_stoch(infos['indic_stoch'][:16]):
                trade+=2

            #analyse de l'indicateur RSI avec un potentiel croisement baissier ou une situation de surachat qui annoncent une potentielle hausse
            trade+=mouvement_baissier_RSI(infos['indic_RSI'][:16])

            #analyse des bandes de bollinger pour chercher un potentiel écartement des bandes synonyme d'un potentiel mouvement 
            trade+=mouvement_bollinger(infos['indic_bolling'])
            
            #analyse d'un potentiel rebond sur la bande inférieur de bollinger
            if float(last_ohlc['2. high'])<infos['indic_bolling']["bande_superieure"]:
                trade+=1

        #si le score dépasse 5 on évalue un potentiel mouvement baissier 
        if trade>=5:
            #on annonce des niveaux de TP et SL en s'appuyant sur les points pivots et l'ATR, en attendant une confirmation mais en annonçant le type de trade qui serait alors réalisé
            return {'stopLoss':(infos['pivots']['pp']+2*infos['indic_ATR']), 'takeProfit': infos['pivots']['s1'], 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"retournement_baissier"}
        
        else:
            trade=0  


    #renvoie d'une situation neutre, sans position, si aucune stratégie ne correspond à la situation
    else:
        return {'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None,'type_trade':None}  



#fonctions d'analyse de positions

def mouvement_haussier_stoch(stoch):
    
    #on suppose aucune indication de l'oscillateur stochastique
    bool=False

    #Partie sur la stratégie de surachat suivi d'un repli 

    #Parcours des données stochastiques dans l'ordre décroissant (de la plus ancienne à la plus récente)
    for i in range(15, -1, -1):
        #on cherche une zone de surachat
        if stoch[i]['K%']>=80:  
            #parcours des données suivant ce surachat
            for j in range(i, -1, -1):
                #on cherche un repli qui suit chronologiquement le surachat
                if stoch[j]['K%']<60: #repli
                    #on analyse s'il y a regain suivant le repli
                    if stoch[0]['K%']>70: 
                        #on considère alors une position hausière
                        bool=True
                        return bool
                    
    #Partie sur la stratégie de croisement haussier

    #Parcours des données stochastiques dans l'ordre décroissant (de la plus ancienne à la plus récente)
    for i in range(15, -1, -1):
        #on cherche une position en attente de croisement haussier
        if stoch[i]['K%']<stoch[i]['D%']:  
            #on itère sur les valeurs suivantes
            for j in range(i, 2, -1):
                #on observe un croisement, K% a dépassé D%
                if stoch[j]['K%']>stoch[j]['D%']:
                    #on valide le croisement
                    bool=True

                    #on vérifie sur les valeurs les plus récentes si ce croisement n'a pas été annulé
                    for y in range(j, -1, -1):
                        if stoch[y]['K%']<stoch[y]['D%']:
                            bool=False
                    return bool
                
    #si rien n'a été considéré, on renvoie False
    return bool

def mouvement_baissier_stoch(stoch):
    #on suppose aucune indication de l'oscillateur stochastique
    bool=False

    #Partie sur la stratégie de survente suivi d'un repli 

    #Parcours des données stochastiques dans l'ordre décroissant (de la plus ancienne à la plus récente)
    for i in range(15, -1, -1):
        #on cherche une zone de survente
        if stoch[i]['K%']<=20:  
            #parcours des données suivant cette survente
            for j in range(i, -1, -1):
                #on cherche un repli qui suit chronologiquement la survente
                if stoch[j]['K%']>40:
                    #on analyse s'il y a perte suivant le repli
                    if stoch[0]['K%']<30: 
                        #on considère alors une position baissière
                        bool=True
                        return bool
                
    #Partie sur la stratégie de croisement haussier

    #Parcours des données stochastiques dans l'ordre décroissant (de la plus ancienne à la plus récente)
    for i in range(15, -1, -1):
        #on cherche une position en attente de croisement baissier
        if stoch[i]['K%']>stoch[i]['D%']:  
            #on itère sur les valeurs suivantes
            for j in range(i, 2, -1):
                #on observe un croisement, D% a dépassé K%
                if stoch[j]['K%']<stoch[j]['D%']:
                    #on valide le croisement
                    bool=True

                    #on vérifie sur les valeurs les plus récentes si ce croisement n'a pas été annulé
                    for y in range(j, -1, -1):
                        if stoch[y]['K%']>stoch[y]['D%']:
                            bool=False
                    return bool
                
    #si rien n'a été considéré, on renvoie False            
    return bool

def mouvement_haussier_RSI(RSI):
    #compteur renvoyé à l'issue pour évaluer l'évidence du mouvement haussier
    return_value=0
    
    #situation de survente (potentiel retournement)
    if RSI[0]<30:
        return_value+=1

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
                    return_value+=1

                    #on vérifie sur les valeurs les plus récentes si ce croisement n'a pas été annulé
                    for y in range(j, -1, -1):
                        if RSI[y]<50:
                            #dans ce cas on invalide en enlevant 1
                            return_value-=1
                            
                    return return_value
    #aucun situation n'a été observée on renvoie 0
    return return_value

def mouvement_baissier_RSI(RSI):

    #compteur renvoyé à l'issue pour évaluer l'évidence du mouvement haussier
    return_value=0

    #situation de survente (potentiel retournement)
    if RSI[0]>70:
        return_value+=1

    #Croisement baissier
    #Parcours des données stochastiques dans l'ordre décroissant (de la plus ancienne à la plus récente)
    for i in range(15, -1, -1):

        #on cherche une situation au dessus de la moyenne (avant un croisement)
        if RSI[i]<50:  
           
           #on itère sur les valeurs suivantes
            for j in range(i, 2, -1):

                #on observe un croisement: le RSI est passé sous la moyenne
                if RSI[j]<50:
                    return_value+=1
                     
                    #on vérifie sur les valeurs les plus récentes si ce croisement n'a pas été annulé
                    for y in range(j, -1, -1):
                        if RSI[y]>50:
                            #dans ce cas on invalide en enlevant 1
                            return_value-=1
                
    #aucun situation n'a été observée on renvoie 0
    return return_value

def mouvement_bollinger(bandes):
    
    #on initialise une valeur correspondant à l'écart des bandes 
    diff=0
    #et une valeur à renvoyer
    return_value=1

    #Parcours des 10 dernières coordonées des bandes de la plus ancienne à la plus récente
    for values in reversed(bandes):
        #si il y a un resserement des bandes on annule l'hypothèse d'un écartement
        if values["bande_superieure"]-values["bande_inférieure"]<diff:
            return_value=0
        diff=values["bande_superieure"]-values["bande_inférieure"]
    return return_value



 
#Fonction de confirmation de prise de position
#Prend en arguments la dernière bougie, la position que l'on veut confirmer, les points pivots et les 100 dernières bougies   
def strat_confirmation(candlestick, positions, level, last_ohlc):

    #confirmation d'une position de sortie de phase de consolidation haussière
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

    #confirmation d'une position de sortie de phase de consolidation haussière
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

    #confirmation d'une position de sortie de phase de consolidation haussière   
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

    #confirmation d'une position de sortie de phase de consolidation haussière
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






