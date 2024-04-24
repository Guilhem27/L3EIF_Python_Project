from indicators import bollinger, movement, trend, pivots, stochastic_oscillator, RSI, ATR
from trading_strategy import strat, strat_confirmation



def cash_invest(available_cash, purchase_price, potential_loss):
    while cash_invested*potential_loss/purchase_price <= available_cash*0.02:   #max_risk_capital à créer
        cash_invested+=0.5
    return cash_invested/100


def daily_trade(risk_reward_ratio, raw_data, last_infos):
    trade_infos=[]

    initial_cash=last_infos['cash']
    if last_infos['cash']<=0:
        return 'fail'

    positions={'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None ,'type_trade':None}
    buy=None
    sell=None
    last_infos['pivots']=pivots(last_infos['max'], last_infos['min'], last_infos['closing'])
    last_ohlc=last_infos['last_ohlc']
    waiting_confirmation=0
    for time, ohlc in raw_data.items():

        ohlc['1. open'] = float(ohlc['1. open'])
        ohlc['2. high'] = float(ohlc['2. high'])
        ohlc['3. low'] = float(ohlc['3. low'])
        ohlc['4. close'] = float(ohlc['4. close'])

        #pour le calcul quotidien des points pivots
        if ohlc['2. high']>last_infos['max']:
            last_infos['max']=ohlc['2. high']
        if ohlc['3. low']>last_infos['min']:
            last_infos['min']=ohlc['3. low']
        last_infos['closing']=ohlc['4. close']

        #fermeture de position selon certains critères (si on est déclaré en position de trade)
        if positions['buy']==True:

            for price in ohlc.values(): 
                    
            #fermeture de position
                if (price>=positions['takeProfit'] and positions['type_trade']=='buy') or (price<=positions['takeProfit'] and positions['type_trade']=='sell'):
                    sell=buy['units']*positions['takeProfit']

                elif (price<=positions['stopLoss'] and positions['type_trade']=='buy') or (price<=positions['takeProfit'] and positions['type_trade']=='sell'):
                    sell=buy['units']*positions['stopLoss']  
                
                elif time=='19:30:00':
                    sell=buy['units']*ohlc['4. close']

                if sell!=None:
                    
                    last_cash=last_infos['cash']

                    if positions['type_position']=="sell":
                        last_infos['cash']-=sell-buy['units']*buy['price']
                    else:  
                        last_infos['cash']+=sell-buy['units']*buy['price']
                    
                    trade_infos.append({'gains':last_infos['cash']/last_cash, 'trade': positions['type_trade']})

                    positions={'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None,'type_trade':None}
                    
                    sell=None
                    buy=None

        else:
            if len(last_ohlc)>=100:   #pour ne pas commencer le trade et les calculs sans valeurs

            #calcul des indicateurs   
                last_ohlc.pop()
                last_ohlc.insert(0,ohlc)

                last_infos['indic_bolling'].insert(0, bollinger(last_ohlc[:20]))
                last_infos['indic_ATR']=ATR(last_ohlc[:14])
                last_infos['indic_RSI'].insert(RSI(last_ohlc[:14]))
                last_infos['indic_stoch'].insert(0, stochastic_oscillator(last_ohlc[:14]))
                last_infos['trend']=trend(last_ohlc)
                last_infos['movement']=movement(ohlc, last_infos['movement'])

            #prise de décision
                #recherche de position interessante en fonction du prix si pas de position existante
                if positions=={'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False,'type_position': None, 'type_trade':None}:
                    positions=strat(ohlc, last_infos, risk_reward_ratio)
                
                #attente de confirmation avec un délai de 5 candlestick, sinon on cherche une nouvelle position
                else:
                    positions=strat_confirmation(ohlc, positions, last_infos['pivots'], last_ohlc)
                    waiting_confirmation+=1

                #annulation de la position
                if waiting_confirmation==5:
                    positions=={'stopLoss': None, 'takeProfit':None,'confirmation':0, 'buy':False, 'type_position': None, 'type_trade':None}
                
                #confirmation et prise de position
                if positions['confirmation']==1:

                    #if (positions['takeProfit']-ohlc['1. open'])/(ohlc['1. open']-positions['stopLoss'])< risk_reward_ratio:  #ajustement au cas où le ratio risk reward n'est pas respecté
                    #    positions['stopLoss']+=last_infos['indic_ATR']

                    #if (positions['takeProfit']-ohlc['1. open'])/(ohlc['1. open']-positions['stopLoss'])>=risk_reward_ratio:  #si  respecté on achète
                        buy={'price':ohlc['1. open'], 'units': cash_invest(last_infos['cash'],ohlc['1. open'], abs(ohlc['1. open']-positions['stopLoss']))/ohlc['1. open']}
                        positions['buy']=True

                if positions['confirmation']==2:
                    if positions['type_position']=='buy':
                        positions['takeProfit']+=2*last_infos['indic_ATR']
                    else:
                        positions['takeProfit']-=2*last_infos['indic_ATR']

                    buy={'price':ohlc['1. open'], 'units': cash_invest(last_infos['cash'],ohlc['1. open'], abs(ohlc['1. open']-positions['stopLoss']))/ohlc['1. open']}
                    positions['buy']=True




    return  {'last_infos': last_infos, 'yield':last_infos['cash']/initial_cash, 'trade_infos':trade_infos}

