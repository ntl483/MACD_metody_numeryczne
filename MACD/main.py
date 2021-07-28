# data format:
# Data,Otwarcie,Najwyzszy,Najnizszy,Zamkniecie,Wolumen
# yyyy-mm-dd,float,float,float,float,int

# EMAN = (p0 + (1-alpha)^1p1 + (1-alpha)^2p2 + ... + (1-alpha)^NpN)/(1+(1-alpha)+(1-alpha)^2+...+(1-alpha)^N)


import pandas
import matplotlib.pyplot as plt

def findBuySell(macd, signal, buy, buyY, sell, sellY):
    #znajduje momenty, ktore powinny generowac sygnal kupna/sprzedaz, sprawdzajac czy oraz jak SIGNAL przecina MACD
    for j in range(1, len(signal)):
        if macd[j - 1] > signal[j - 1] and macd[j] < signal[j]:
            buyY.append(signal[j])
            buy.append(j)
        elif macd[j - 1] < signal[j - 1] and macd[j] > signal[j] and len(buy) > 0:
            sellY.append(signal[j])
            sell.append(j)

def countRevenue(sellTime, buyTime):
    #liczy zarobek, przy poczatkowym kapitale 1000 akcji w cenie z pierwszego dnia oraz zakladajac, ze mozna kupowac czesci akcji
    revenue = 1000*data["Zamkniecie"][buyTime[0]]
    for k in range(len(sellTime)):
        available = revenue/data["Zamkniecie"][buyTime[k]]     #we can buy available amount of shares
        revenue -= data["Zamkniecie"][buyTime[k]] * available
        #print(available)
        #print(revenue)
        revenue += data["Zamkniecie"][sellTime[k]]*available
        #print(revenue)

    return revenue

def countMacd(macd, signal, data):
    #wyznacza punkty wykresu macd (linie signal oraz macd)
    size = len(data)
    for current in range(26, size):
        divisor = 0
        divident = 0
        alpha = 1 - (2/(12+1))
        x = 1
        for i in range(current, current-12, -1):
            divident += x*data["Zamkniecie"][i]
            divisor += x
            x *= alpha
        ema12 = divident/divisor

        divisor = 0
        divident = 0
        alpha = 1 - (2/(26+1))
        x = 1
        for i in range(current, current-26, -1):
            divident += x * data["Zamkniecie"][i]
            divisor += x
            x *= alpha
        ema26 = divident / divisor
        macd.append(ema12 - ema26)

        macdSize = len(macd)
        thisSignal = 0
        if macdSize >= 9:
            divisor = 0
            divident = 0
            alpha = 1 - (2 / (9 + 1))
            x = 1
            for i in range(macdSize-1, macdSize-10, -1):
                divident += x * macd[i]
                divisor += x
                x *= alpha
            thisSignal = divident / divisor
        signal.append(thisSignal)


data = pandas.read_csv("csvs\\eurpln_0812.csv")
macd = [0]*26
signal = [0]*26
buy = []
sell = []
buyY = []
sellY = []

countMacd(macd, signal, data)
findBuySell(macd, signal, buy, buyY, sell, sellY)
rev = countRevenue(sell, buy)
base = 1000*data["Zamkniecie"][buy[0]]
print("kapital pocatkowy: ", base)
print("kapital koncowy: ", rev)
print("zarobek (w %): ", (rev/base-1)*100)
plot1 = plt.figure(1, dpi=150, figsize=(10, 4))
plt.plot(macd, label="MACD")
plt.plot(signal, label="SIGNAL")
plt.plot(buy, buyY, 'ro', label="zakup")
plt.plot(sell, sellY, 'bo', label="sprzedaz")
plt.grid(True)
plt.legend()
plt.title("wskaznik MACD dla EUR-PLN")

mainBuyY = []
mainSellY = []
for i in range(len(buyY)):
    mainBuyY.append(data["Zamkniecie"][buy[i]])
for j in range(len(sellY)):
    mainSellY.append(data["Zamkniecie"][sell[j]])

plot2 = plt.figure(2, dpi=150, figsize=(10, 4))
plt.plot(data["Zamkniecie"], label="EUR-PLN")
plt.plot(buy, mainBuyY, 'ro', label="zakup")
plt.plot(sell, mainSellY, 'bo', label="sprzedaz")
plt.grid(True)
plt.title("kurs EUR-PLN")
plt.legend()

plt.show()
