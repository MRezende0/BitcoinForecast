#!/usr/bin/python3

##
## run the code for about 2/3 days
##

# import requests
# import time

# f_name = input("dataset name:")
# f = open(f_name,"a")
# keys = ["price_usd","24h_volume_usd","market_cap_usd","available_supply","total_supply","percent_change_1h","percent_change_24h","percent_change_7d"]
# vals = [0]*len(keys)

# while True:
#   data = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT").json()
#   bstamp = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/").json() 
#   bkc = requests.get("https://blockchain.info/ticker").json()
  
#   for d in data.keys():
#      if d in keys:
#        indx = keys.index(d)
#        vals[indx] = data[d]
#   for val in vals:
#        f.write(val+",")
      
#   f.write("{},{},".format(bstamp["volume"],bstamp["vwap"]))
#   f.write("{},{},{}".format(bkc["USD"]["sell"],bkc["USD"]["buy"],bkc["USD"]["15m"]))
#   f.write("\n")
#   f.flush()
#   time.sleep(9*60)

import requests
import time
import csv
from datetime import datetime

# Nome do arquivo CSV
f_name = input("Nome do arquivo CSV (ex: dataset.csv): ")

# Abrir o arquivo em modo de acréscimo e configurar o cabeçalho
with open(f_name, "a", newline="") as f:
    writer = csv.writer(f)
    
    # Escrever cabeçalho apenas se o arquivo estiver vazio
    if f.tell() == 0:
        writer.writerow(["timestamp", "binance_last_price", "binance_volume",
                         "bitstamp_volume", "bitstamp_vwap",
                         "blockchain_sell", "blockchain_buy", "blockchain_15m"])
    
    while True:
        try:
            # Coleta de dados
            binance_data = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT").json()
            bitstamp_data = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/").json()
            blockchain_data = requests.get("https://blockchain.info/ticker").json()
            
            # Extração de informações
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            binance_last_price = binance_data["lastPrice"]
            binance_volume = binance_data["volume"]
            bitstamp_volume = bitstamp_data["volume"]
            bitstamp_vwap = bitstamp_data["vwap"]
            blockchain_sell = blockchain_data["USD"]["sell"]
            blockchain_buy = blockchain_data["USD"]["buy"]
            blockchain_15m = blockchain_data["USD"]["15m"]
            
            # Escrever os dados no CSV
            writer.writerow([timestamp, binance_last_price, binance_volume,
                             bitstamp_volume, bitstamp_vwap,
                             blockchain_sell, blockchain_buy, blockchain_15m])
            
            # Garantir que os dados sejam salvos imediatamente
            f.flush()
            print(f"{timestamp} - Dados salvos no arquivo.")
        
        except Exception as e:
            print(f"Erro: {e}")
        
        # Coleta dados a cada 1 minuto
        time.sleep(1 * 60)