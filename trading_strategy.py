#fonction de prise de position principale
#prend comme arguments la bougie actuelle et les informations précédentes (bougies et indicateurs)
#compare la situation réelle avec des stratégies de prise de position précises
def strat(candlestick, infos, last_ohlc, rsi1, rsi2, rate1, rate2):



    if infos['indic_RSI'][0]>rsi1 and infos['trend']['value_growth']>rate1:
                

        return {'stopLoss':None, 'takeProfit': None, 'confirmation':False, 'buy':False, 'type_position': 'buy', 'type_trade':"long"}


   
   
    #if infos['indic_RSI'][0]<rsi2  and infos['trend']['value_growth']<rate2:
                
            #return {'stopLoss':None, 'takeProfit': None, 'confirmation':False, 'buy':False, 'type_position': 'sell', 'type_trade':"short"}
        

    #renvoie d'une situation neutre, sans position, si aucune stratégie ne correspond à la situation
    return {'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None,'type_trade':None}  


 
#Fonction de confirmation de prise de position
#Prend en arguments la dernière bougie, la position que l'on veut confirmer, les points pivots et les 100 dernières bougies   
def strat_confirmation(candlestick, positions, infos, last_ohlc, trend,vol1, vol2, sl1, sl2, tp1, tp2):

    #confirmation d'une position de sortie de phase de consolidation haussière
    if positions['type_trade']=="long":
            
            
        if positions['confirmation']==0:
            if (float(last_ohlc[0]['5. volume'])+float(last_ohlc[1]['5. volume']))/2>vol1*trend['volume_mean']:
                positions={'stopLoss':(float(candlestick['4. close'])-sl1*infos['indic_ATR']), 'takeProfit': (float(candlestick['4. close'])+tp1*infos['indic_ATR']), 'confirmation':2, 'buy':False, 'type_position': 'buy', 'type_trade':"long", 'ecart':sl1*infos['indic_ATR']}
                
                print({'stopLoss':(float(candlestick['4. close'])-sl1*infos['indic_ATR']), 'takeProfit': (float(candlestick['4. close'])+tp1*infos['indic_ATR']), 'confirmation':2, 'buy':False, 'type_position': 'buy', 'type_trade':"long"})
                print(candlestick)
                print(' ')

    #confirmation d'une position de sortie de phase de consolidation baissière
    if positions['type_trade']=="short":
        
        if positions['confirmation']==0:
            for type, price in candlestick.items():
                if float(price)<infos['pivots']['r1'] and type!='5. volume':
                    positions['confirmation']=1
                    
                    

        elif positions['confirmation']==1:
            if (float(last_ohlc[0]['5. volume'])+float(last_ohlc[1]['5. volume']))/2>vol2*(trend['volume_mean']):
                positions={'stopLoss':(float(candlestick['4. close'])+sl2*infos['indic_ATR']), 'takeProfit': (float(candlestick['4. close'])-tp2*infos['indic_ATR']), 'confirmation':2, 'buy':False, 'type_position': 'sell', 'type_trade':"short", 'ecart':sl2*infos['indic_ATR']}
                
                print({'stopLoss':(float(candlestick['4. close'])+sl2*infos['indic_ATR']), 'takeProfit': (float(candlestick['4. close'])-tp2*infos['indic_ATR']), 'confirmation':2, 'buy':False, 'type_position': 'sell', 'type_trade':"short"})
                print(candlestick)
                print(' ')
 

    return positions
    




