from genericpath import isfile
import binance
import csv
from datetime import datetime
import os


path = os.getcwd()
def set_tool():
    """
    create dir to save CSV
    """
    if not os.path.isdir(path+'/history'):
        os.mkdir(path+'/history')

def client(api,sec):
    """
    args:
        api:str(apikey)
        sec:str(secretkey)
    return:
        clients: object(binance.Client())
    """
    clients = binance.Client(api,sec)
    return clients

def Get_history_data_toCSV(client,symbol,invertal):
    """
    args:
        client: object binance.Client()
        symbol: str 'BNBUSDT'
        invertal: str '1d'
    return:
        BTC_list: dict ['Date','Open','High','Low','Close']
    """
    BTC_Kline = client.get_historical_klines(symbol,invertal)
    BTC_list = []
    for item in BTC_Kline:
        timestamp = item[0]
        date_time = datetime.fromtimestamp(int(timestamp)/1000)
        d = date_time.strftime("%m-%d-%Y, %H:%M")
        new_list = [d,item[1],item[2],item[3],item[4]]
        BTC_list.append(new_list)
    if isfile(path+'/history/'+symbol+'_'+invertal+'.csv'): 
        os.remove(path+'/history/'+symbol+'_'+invertal+'.csv')
    with open(path+'/history/'+symbol+'_'+invertal+'.csv','a')as f:
        writer = csv.writer(f)
        writer.writerow(['Date','Open','High','Low','Close'])
        for item in BTC_list:
            writer.writerow(item)
    return BTC_list

def get_Future_SymbolList(client):
    """
    args:
        client: object binance.Client()

    return:
        symbolList: List 
    """
    account = client.futures_account()
    SymbolList = []
    SymbolList.append('BSWBUSD')
    for item in account['positions']:	
        if 'USDT' in item['symbol']:
            SymbolList.append(item['symbol'])
    return SymbolList

def get_future_OI(symbol,client):
  '''取得當前持倉量
  args:
    symbol(str):'BTCUSDT'
  return:
    OI(float):3.43 
  '''
  account = client.futures_account()
  for i in account['positions']:
    if i['symbol'] == symbol:
      hold = i['positionAmt']
      break
  OI = float(hold)
  return OI

def get_future_mark_price(symbol,client):
    '''取得合約當前標記價格
    args:
        symbol(str):'BTCUSDT'
        client : binance.Client()
    return:
        NowPrice(float):40407.11

    '''
    marklist = client.futures_mark_price()
    for i in marklist:
        if i['symbol']== symbol:
            NowPrice = i['markPrice']
            break
    NowPrice = float(NowPrice)
    return NowPrice

def get_quantityPrecision(symbol,client):
  '''取得最小顆數單位
  args:
    symbol (str)= 'ETHUSDT'
  return:
    pricePrecision(str):'3'
  '''
  info = client.futures_exchange_info()
  for i in info['symbols']:
    if i['symbol'] == symbol:
      pricePrecision = i['quantityPrecision']
      break
  return pricePrecision	

def future_buy(symbol,quantity,client):
	'''買入
	args:
		symbol(str):'BTCUSDT'
		quantity(float): 3.24  #How many BTC you want to buy
        client : bainace.client()
    return:
        bool: successful or failed
	'''
	if quantity != 0:
		try:
			client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
			return True
		except Exception as e:
			print("{} order buy not successful".format(symbol))
			print(e)
			return False
	else:
		return False

def future_sell(symbol,quantity,client):
	'''賣出
	args:
		symbol(str):'BTCUSDT'
		quantity(float): 3.24  #How many BTC you want to sell 
        client: binance.Client()
    return:
        bool : successfil or failed
	'''
	try:
		client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)
		return True
	except Exception as e:
		print("{} order sell not successful".format(symbol))
		print(e)
		return False