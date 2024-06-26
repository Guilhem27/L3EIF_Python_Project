#fonction de prise de position principale
#prend comme arguments la bougie actuelle et les informations précédentes (bougies et indicateurs)
#compare la situation réelle avec des stratégies de prise de position précises
def strat(candlestick, infos, last_ohlc, strat,rsi, rate):



    if infos['indic_RSI']>rsi and infos['trend']['value_growth']>rate and strat=='long_trend' and infos['EMA']>float(candlestick['2. high']) :
                

        return {'stopLoss':None, 'takeProfit': None, 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"long"}


   
   
    if infos['indic_RSI']<rsi  and infos['trend']['value_growth']<-rate and strat=='short_trend' and infos['EMA']<float(candlestick['3. low']):
                
            return {'stopLoss':None, 'takeProfit': None, 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"short"}
        

    #renvoie d'une situation neutre, sans position, si aucune stratégie ne correspond à la situation
    return {'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None,'type_trade':None}  


 
#Fonction de confirmation de prise de position
#Prend en arguments la dernière bougie, la position que l'on veut confirmer, les points pivots et les 100 dernières bougies   
def strat_confirmation(candlestick, positions, infos, last_ohlc, trend, vol, sl, tp):

    #confirmation d'une position de sortie de phase de consolidation haussière
    if positions['type_trade']=="long":
            
            
        if positions['confirmation']==0:
            if (float(last_ohlc[0]['5. volume'])+float(last_ohlc[1]['5. volume']))/2>vol*trend['volume_mean']:
                positions={'stopLoss':(float(candlestick['4. close'])-sl*infos['indic_ATR']), 'takeProfit': (float(candlestick['4. close'])+tp*infos['indic_ATR']), 'confirmation':2, 'buy':False, 'type_position': 'buy', 'type_trade':"long", 'ecart':sl*infos['indic_ATR']}
                
                #print({'stopLoss':(float(candlestick['4. close'])-sl*infos['indic_ATR']), 'takeProfit': (float(candlestick['4. close'])+tp*infos['indic_ATR']), 'confirmation':2, 'buy':False, 'type_position': 'buy', 'type_trade':"long"})
                #print(candlestick)
                #print(' ')

    #confirmation d'une position de sortie de phase de consolidation baissière
    if positions['type_trade']=="short":
        
        if positions['confirmation']==0:
            if (float(last_ohlc[0]['5. volume'])+float(last_ohlc[1]['5. volume']))/2>vol*(trend['volume_mean']):
                positions={'stopLoss':(float(candlestick['4. close'])+sl*infos['indic_ATR']), 'takeProfit': (float(candlestick['4. close'])-tp*infos['indic_ATR']), 'confirmation':2, 'buy':False, 'type_position': 'sell', 'type_trade':"short", 'ecart':sl*infos['indic_ATR']}
                
                #print({'stopLoss':(float(candlestick['4. close'])+sl*infos['indic_ATR']), 'takeProfit': (float(candlestick['4. close'])-tp*infos['indic_ATR']), 'confirmation':2, 'buy':False, 'type_position': 'sell', 'type_trade':"short"})
                #print(candlestick)
                #print(' ')
 

    return positions
    




