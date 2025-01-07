## run the code for about 2/3 days

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