import requests
import csv

maxs =[]
mins =[]

# def loadData(f_name):
#     data  = f_name.read().split("\n")
#     data = data[:len(data)-1]
#     label = []

#     with open(f_name, 'r') as file:
#         reader = csv.reader(file)
#         # Pular o cabeçalho
#         next(reader)  # Isso pula a primeira linha (cabeçalho)

#         for row in reader:
#             try:
#                 # Certifique-se de que cada valor possa ser convertido em float
#                 data.append([float(x) for x in row[:-1]])  # Assumindo que os dados estão nas colunas, exceto a última
#                 label.append(float(row[-1]))  # Assumindo que a última coluna é o label
#             except ValueError:
#                 # Se houver erro ao converter, ignore a linha ou faça outro tratamento
#                 print(f"Skipping row due to error: {row}")
#                 continue

#     for i in range(len(data)):
#         data[i] = data[i].split(",")
#         data[i] = [float(x) for x in data[i]]
#         label.append(data[i][len(data[i])-1])
#         data[i] = data[i][0:len(data[i])-1]
#     return data[:-2],label[2:]  #Removing first two and last two so each X[i] tries to predict Y[i+2] (i've used i+2 and not to i+1 to force it to predict the future (O) )

def loadData(file_name):
    data = []
    labels = []
    
    # Assegure-se de que file_name é uma string com o caminho correto do arquivo
    with open(file_name, 'r') as file:  # Aqui passamos o caminho corretamente
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho

        for i, row in enumerate(reader, start=1):
            if len(row) == 7:  # Ajuste conforme necessário
                try:
                    # Faça o pré-processamento da linha aqui
                    data.append(row)
                except Exception as e:
                    print(f"Erro ao processar a linha {i}: {e}")
            else:
                print(f"Erro no formato da linha {i}: {row}")
        
        for row in reader:
            try:
                # Processa as linhas, convertendo os dados em floats
                data.append([float(x) for x in row[:-1]])  # Colunas, exceto a última
                labels.append(float(row[-1]))  # Última coluna como label
            except ValueError:
                # Caso haja erro na conversão
                print(f"Erro na linha: {row}")
                continue

        print(f"Total de linhas válidas: {len(data)}")
                
    return data, labels

def reduceVector(vec,getVal=False):
    vect = []
    mx,mn = max(vec),min(vec)
    mx = mx+mn
    mn = mn-((mx-mn)*0.4)
    for x in vec:
        vect.append((x-mn)/(mx-mn))
    if not getVal:return vect
    else:return vect,mx,mn

def reduceValue(x,mx,mn):
    return (x-mn)/(mx-mn)

def augmentValue(x,mx,mn):
    return (mx-mn)*x+mn

def reduceMatRows(data):
    l = len(data[0])
    for i in range(l):
        v = []
        for t in range(len(data)):
            v.append(data[t][i])
        v,mx,mn = reduceVector(v,getVal=True)
        maxs.append(mx)
        mins.append(mn)
        for t in range(len(data)):
            data[t][i] = v[t]

    return data
def reduceCurrent(data):
    for i in range(len(data)):
        data[i] = reduceValue(data[i],maxs[i],mins[i])
    return data

def getCurrentData(label=False):

  keys = ["price_usd","24h_volume_usd","market_cap_usd","available_supply","total_supply","percent_change_1h","percent_change_24h","percent_change_7d"]
  vect = []
  data = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/").json()[0]
  bstamp = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/").json()
  bkc = requests.get("https://blockchain.info/ticker").json()
  '''
  for i in data.keys():
    if i in keys:
      vect.append(float(data[i]))
  '''
  for k in keys:
    for d in data.keys():
        if k == d:
            vect.append(float(data[d]))
    
  vect.append(float(bstamp["volume"]))
  vect.append(float(bstamp["vwap"]))
  vect.append(float(bkc["USD"]["sell"]))
  vect.append(float(bkc["USD"]["buy"]))

  #print("blockchain.info ",float(bkc["USD"]["15m"]))
  if label:
    return vect,float(bkc["USD"]["15m"])
  return vect

def getCEXData():
   data = requests.get("https://cex.io/api/ticker/BTC/USD").json()
   #print("CEX ",data)
   return data 