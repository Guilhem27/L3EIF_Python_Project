import numpy as np

#Calcule l'indice de force relative (RSI) pour une série de prix de clôture, utile pour repérer des situations de surachat/survente
def RSI(last_OCLH):

    # Extraction des variations de prix (delta)
    delta = np.diff(np.array([float(d['4. close']) for d in last_OCLH]))

    # Séparation des variations en gains et pertes
    gain = np.where(delta >= 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    # Calcul des moyennes mobiles des gains et des pertes sur la période spécifiée
    avg_gain = np.mean(gain)
    avg_loss = np.mean(loss)

    # Calcul du rapport de force (RS)
    rs = avg_gain / avg_loss if avg_loss != 0 else np.inf

    # Calcul de l'indice de force relative (RSI)
    rsi = 100 - (100 / (1 + rs))

    return round(rsi, 5)


#'ATR' mesure la volatilité des prix sur une période donnée (les 14 dernières valeurs)
def ATR(last_OCLH):
    
    # Liste pour stocker les valeurs des True Range (TR), maximum entre:
    #-la différence entre le prix le plus haut et le prix le plus bas
    #-la différence absolue entre le prix le plus haut et le prix de clôture de la période précédente
    #-la différence absolue entre le prix le plus bas et le prix de clôture de la période précédente
    tr_values = []

    # Calcul des True Range pour chaque période
    for i in range(1, len(last_OCLH)):

        # Extraction des prix High, Low et Close
        high = float(last_OCLH[i]['2. high'])
        low = float(last_OCLH[i]['3. low'])
        close_prev = float(last_OCLH[i - 1]['4. close'])

         # Calcul du True Range (TR) pour la période actuelle
        tr = max(high - low, abs(high - close_prev), abs(low - close_prev))
        tr_values.append(tr)

    # Initialisation de l'ATR
    atr = sum(tr_values) /len(last_OCLH)

    # Calcul de l'ATR pour les données restantes afin d'en calculer une moyenne
    for i in range(len(tr_values)):
        atr = ((len(tr_values) - 1) * atr + tr_values[i]) / len(tr_values)

    return round(atr,5)



def pivots(high, low, closing):


    # Calcul du point pivot (PP)
    pp=round(((high+low+closing)/3),5)

    # Calcul des niveaux de support (S1, S2, S3)
    s1= round(((2*pp)-high),5)
    s2=round((pp-(high-low)),5)

    # Calcul des niveaux de résistance (R1, R2, R3)
    r1=round(((2*pp)-low),5)
    r2=round((pp+(high-low)),5)

    # Création d'un dictionnaire contenant les points pivots et leurs niveaux associés
    pivots={'pp':pp, 's1': s1, 's2':s2, 'r1': r1, 'r2':r2}
    return pivots



#rend compte de la direction, de la longueur et de la force du mouvement en cours
def movement(candlestick, movement):

     # Extraction du prix de clôture et du prix d'ouverture de la bougie
    last_close=float(candlestick['4. close'])
    last_open=float(candlestick['1. open'])

    # Vérification du mouvement de la bougie par rapport au mouvement précédent
    if movement['move']*(last_close-last_open)>=0:
        # Si le mouvement est dans la même direction que le mouvement précédent
        # Incrémentation de la longueur du mouvement et ajustement du mouvement total
        movement['length']+=1
        movement['move']+=(last_close-last_open)/last_open

    else:
        # Si le mouvement est dans une direction opposée au mouvement précédent
        # Réinitialisation de la longueur du mouvement et remplacement du mouvement total
        movement['length']=1
        movement['move']=(last_close-last_open)/last_open

    return movement


# calcul un taux de croissance des prix sur les 100 dernières valeurs
def trend(data):
    # Extraction des prix de clôture
    closes = np.array([float(d['4. close']) for d in data])
    volumes = np.array([float(d['4. close']) for d in data])
    # Calcul du taux de croissance des 100 valeurs
    value_growth = ((closes[0] - closes[-1]) / closes[-1]) * 100
    volume_mean= sum(volumes)/len(volumes)
    # Renvoyer le pourcentage de différence et le taux de croissance
    return {'value_growth': round(value_growth,5), 'volume_mean':round(volume_mean)}
