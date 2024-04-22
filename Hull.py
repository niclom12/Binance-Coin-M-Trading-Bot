import numpy as np
from math import sqrt


def wma(data, period):
    norm = 0.0
    sum = 0.0
    for i in range(period):
        weight = (period - i) * period
        norm += weight
        sum += data[i] * weight
    return sum / norm

def Hulls(data, period):
    wma_55 = [None] * 55
    wma_2 = [None] * 55

    # Calculate WMA
    for i in range(55):
        if i + 55 <= len(data):  # Ensure there is enough data to calculate WMA
            wma_55[i] = wma(data[i:i+55], 55)
        if i + 27 <= len(data):  # Ensure there is enough data to calculate WMA for half of 55
            wma_2[i] = wma(data[i:i+27], 27)  # Use 27 as the period, rounded down from 27.5

    hma_raw = [None] * 20
    for i in range(20):
        hma_raw[i] = (2 * wma_2[i]) - wma_55[i]
        
    hull = [None] * 4
    for i in range(4):
        hull[i] = wma(hma_raw[i:], round(sqrt(55)))
        
    return hull

def logic(data):
    hull = Hulls(data, 55)
    print(hull)
    hul1 = hull[0] - hull[2]
    hul2 = hull[1] - hull[3]
    if ((hul1 >= 0) and (hul2 < 0)):
        print("Buy")
        return "Buy"
    elif ((hul1 < 0) and (hul2 >= 0)):
        print("Sell")
        return "Sell"
    elif(hul1 >= 0):
        print("Bullish")
        return
    else:
        print("Bearish")
        return


