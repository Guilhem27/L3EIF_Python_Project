import numpy as np
import pandas as pd

def RSI(last_OCLH):
    # Initialisation des variables
    delta = np.diff(np.array([float(d['4. close']) for d in last_OCLH]))
    gain = np.where(delta >= 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    # Calcul des moyennes mobiles des gains et des pertes sur la période spécifiée
    avg_gain = np.mean(gain)
    avg_loss = np.mean(loss)

    rs = avg_gain / avg_loss if avg_loss != 0 else np.inf
    rsi = 100 - (100 / (1 + rs))

    return rsi

def ATR(last_OCLH):
    tr_values = []

    # Calcul des True Range (TR) pour chaque période
    for i in range(1, len(last_OCLH)):
        high = float(last_OCLH[i]['2. high'])
        low = float(last_OCLH[i]['3. low'])
        close_prev = float(last_OCLH[i - 1]['4. close'])
        tr = max(high - low, abs(high - close_prev), abs(low - close_prev))
        tr_values.append(tr)

    # Initialisation de l'ATR
    atr = sum(tr_values) /len(last_OCLH)

    # Calcul de l'ATR pour les données restantes
    for i in range(len(tr_values)):
        atr = ((len(tr_values) - 1) * atr + tr_values[i]) / len(tr_values)
    return atr


def stochastic_oscillator(last_OCLH):
    # Extrayez les prix de clôture de la liste des données OHLC
    closes = [float(data['4. close']) for data in last_OCLH]

    # Calcul du plus haut et du plus bas sur les 14 dernières périodes
    high14 = max([float(d['2. high']) for d in last_OCLH])
    low14 = min([float(d['3. low']) for d in last_OCLH])

    # Dernier prix de clôture
    close = closes[0]

    # Calcul de la ligne %K
    k = ((close - low14) / (high14 - low14)) * 100

    # Calcul de la moyenne mobile de la ligne %K (ligne %D)
    d = sum(closes[-3:]) / 3

    return {'%K': k, '%D': d}


def pivots(high, low, closing):
    pp=high+low+closing
    s1= (2*pp)-high
    s2=pp-(high-low)
    s3 = low-2* (high-pp)
    r1=(2*pp)-low
    r2=pp+(high-low)
    r3 = high+2*(high-pp)
    pivots={'pp':pp, 's1': s1, 's2':s2, 's3':s3, 'r1': r1, 'r2':r2, 'r3': r3}
    return pivots



def trend(data):
    # Extraction des prix de clôture
    closes = np.array([float(d['1. close']) for d in data])

    # Calcul de la moyenne mobile simple sur 100 valeurs
    sma_100 = pd.Series(closes).rolling(window=100).mean()

    # Calcul de la moyenne mobile exponentielle sur 20 valeurs
    ema_20 = pd.Series(closes).ewm(span=20, adjust=False).mean()

    # Calcul du pourcentage de différence entre les deux moyennes mobiles
    diff_percentage = ((sma_100 - ema_20) / closes[0]) * 100

    # Calcul du taux de croissance des 100 valeurs
    growth_rate = ((closes[0] - closes[-1]) / closes[-1]) * 100

    # Renvoyer le pourcentage de différence et le taux de croissance
    return {'long_trend':sma_100, 'recent_trend': ema_20, 'diff': diff_percentage, 'growth_rate': growth_rate}





def movement(candlestick, movement):

    last_close=float(candlestick['4. close'])
    last_open=float(candlestick['1. open'])
    if movement['move']*(last_close-last_open)>=0:
        movement['length']+=1
        movement['move']+=(last_close-last_open)/last_open
    else:
        if len(movement['last_trends'])>=10:
            movement['last_trends'].pop()
            movement['last_trends'].insert(0,movement['length'])
            movement['length']=1
            movement['move']=(last_close-last_open)/last_open
    return movement


#manque bandes de bollinger

import numpy as np

def bollinger(last_OCLH, nb_ecarts_types=2):
    # Calcul de la moyenne mobile
    moyenne_mobile = np.mean([float(d['1. close']) for d in last_OCLH])
    
    # Calcul de l'écart-type
    ecart_type = np.std([float(d['1. close']) for d in last_OCLH])
    
    # Calcul des bandes de Bollinger
    bande_superieure = moyenne_mobile + nb_ecarts_types * ecart_type
    bande_inferieure = moyenne_mobile - nb_ecarts_types * ecart_type
    
    return {
        "bande_superieure": bande_superieure,
        "moyenne_mobile": moyenne_mobile,
        "bande_inferieure": bande_inferieure
    }
