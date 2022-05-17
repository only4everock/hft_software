from datetime import datetime
import requests
from tradingview_ta import *
from binance.client import Client
import sys
import time

user_key = ""
secret_key = ""
binance_client = Client(user_key, secret_key)
import bybit
import os

api = ""
secret = ""
client = bybit.bybit(test=False, api_key=api, api_secret=secret)


def restart():
    print("argv: ", sys.argv)
    print("sys executable:", sys.executable)
    print("restart now!")
    os.execv(sys.executable, ["python3"] + sys.argv)


try:
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        handler = TA_Handler(symbol='XRPUSDT', exchange='BINANCE',
                             screener='crypto', interval='1m', timeout=None)
        analysis = handler.get_analysis()
        ta1 = analysis.summary['RECOMMENDATION']
        ta2 = analysis.indicators['Recommend.All']

        # print(ta1,"TA1")
        # print(ta2,"TA2")

        handler2 = TA_Handler(symbol='XRPUSDT', exchange='BINANCE',
                              screener='crypto', interval='5m',
                              timeout=None)

        analysis2 = handler2.get_analysis()
        ta3 = analysis2.summary['RECOMMENDATION']
        ta4 = analysis2.indicators['Recommend.All']

        # print(ta3,"TA3")
        # print(ta4,"TA4")

        handler3 = TA_Handler(symbol='XRPUSDT', exchange='BINANCE',
                              screener='crypto', interval='15m',
                              timeout=None)

        analysis3 = handler3.get_analysis()
        ta5 = analysis3.summary['RECOMMENDATION']
        ta6 = analysis3.indicators['Recommend.All']

        # print(ta5, "TA5")
        # print(ta6, "TA6")

        if ta1 == 'BUY':
            summary = 1

        if ta1 == 'STRONG_BUY':
            summary = 2

        if ta1 == 'SELL':
            summary = -1

        if ta1 == 'STRONG_SELL':
            summary = -2

        if ta1 == 'NEUTRAL':
            summary = 0

        if ta3 == 'BUY':
            summary1 = 1

        if ta3 == 'SELL':
            summary1 = -1

        if ta3 == 'STRONG_BUY':
            summary1 = 2

        if ta3 == 'STRONG_SELL':
            summary1 = -2

        if ta3 == 'NEUTRAL':
            summary1 = 0

        if ta5 == 'BUY':
            summary2 = 1

        if ta5 == 'SELL':
            summary2 = -1

        if ta5 == 'STRONG_BUY':
            summary2 = 2

        if ta5 == 'STRONG_SELL':
            summary2 = -2

        if ta5 == 'NEUTRAL':
            summary2 = 0

        if ta2 > 0:
            indicators10 = 1

        if ta2 <= 0:
            indicators10 = -1

        if ta4 > 0:
            indicators11 = 1

        if ta4 <= 0:
            indicators11 = -1

        if ta6 > 0:
            indicators12 = 1

        if ta6 <= 0:
            indicators12 = -1

        total_summary = summary + summary1 + summary2

        total_indicators = indicators10 + indicators11 + indicators12

        alis = binance_client.futures_order_book(symbol="XRPUSDT")
        total_asks = 0
        total_bids = 0
        for i in range(0, 500):
            total_asks += float(alis["asks"][i][1])
            total_bids += float(alis["bids"][i][1])
        # print(total_asks, total_bids)

        orderbook = client.Market.Market_orderbook(symbol="XRPUSD").result()
        orderbook1 = orderbook[0]["result"]
        # print(orderbook1[49]["size"] )
        # print(orderbook1[48]["size"])
        # print(orderbook1[0:25])
        buy_orders = orderbook1[0]["size"] + orderbook1[1]["size"] + orderbook1[2]["size"] + orderbook1[3]["size"] + \
                     orderbook1[4]["size"] + orderbook1[5]["size"] + orderbook1[6]["size"] + orderbook1[7]["size"] + \
                     orderbook1[8]["size"] + orderbook1[9]["size"] + orderbook1[10]["size"] + orderbook1[11]["size"] + \
                     orderbook1[12]["size"] + orderbook1[13]["size"] + orderbook1[14]["size"] + orderbook1[15]["size"] + \
                     orderbook1[16]["size"] + orderbook1[17]["size"] + orderbook1[18]["size"] + orderbook1[19]["size"] + \
                     orderbook1[20]["size"] + orderbook1[21]["size"] + orderbook1[22]["size"] + orderbook1[23]["size"] + \
                     orderbook1[24]["size"]
        sell_orders = orderbook1[25]["size"] + orderbook1[26]["size"] + orderbook1[27]["size"] + orderbook1[28][
            "size"] + \
                      orderbook1[29]["size"] + orderbook1[30]["size"] + orderbook1[31]["size"] + orderbook1[32][
                          "size"] + \
                      orderbook1[33]["size"] + orderbook1[34]["size"] + orderbook1[35]["size"] + orderbook1[36][
                          "size"] + \
                      orderbook1[37]["size"] + orderbook1[38]["size"] + orderbook1[39]["size"] + orderbook1[40][
                          "size"] + \
                      orderbook1[41]["size"] + orderbook1[42]["size"] + orderbook1[43]["size"] + orderbook1[44][
                          "size"] + \
                      orderbook1[45]["size"] + orderbook1[46]["size"] + orderbook1[47]["size"] + orderbook1[48][
                          "size"] + \
                      orderbook1[49]["size"]

        if total_summary >= 3:
            total_summary_skor = 1

        if total_summary <= 3:
            total_summary_skor = -1

        if total_indicators >= 1.5:
            total_indicators_skor = 1

        if total_indicators <= 1.5:
            total_indicators_skor = -1

        if buy_orders > sell_orders:
            bybit_skor = 1
        if sell_orders > buy_orders:
            bybit_skor = -1

        if total_bids > total_asks:
            binance_skor = 1

        if total_bids < total_asks:
            binance_skor = -1


        def sell_checker():
            with open(r"sell.txt", 'r') as fp:
                for count, line in enumerate(fp):
                    pass
                print('Total Lines', count + 1)

                return count + 1


        def buy_checker():
            with open(r"buy.txt", 'r') as fp:
                for count, line in enumerate(fp):
                    pass
                print('Total Lines', count + 1)

                return count + 1


        if buy_checker() > sell_checker():
            maker_skor = 1
        else:
            maker_skor = -1

        total_skor = bybit_skor + binance_skor + total_summary_skor + total_indicators_skor + maker_skor

        ali = client.Positions.Positions_myPosition(symbol="XRPUSD").result()

        mehmet = ali[0]['result']

        # print(mehmet["side"])
        # print(mehmet["size"])
        market_price = float([x['last_price'] for x in
                              requests.get('https://api.bybit.com/v2/public/tickers?symbol=XRPUSD').json()[
                                  'result']][0])

        print(total_skor, "TOTAL SKOR 5 UZERINDEN", current_time)

        f = open("total_skor.txt", "a")
        f.write(f"{total_skor} , {market_price},{current_time}\n")
        f.close()

        entry = round(float(mehmet["entry_price"]), 4)
        # print(entry)
        last_price = round(market_price, 4)


        # print(last_price)

        def price_difference_calculator(current, previous):
            if current == previous:
                return 0
            try:
                return (abs(current - previous) / previous) * 100.0
            except ZeroDivisionError:
                return 0


        if price_difference_calculator(float(mehmet["entry_price"]), market_price) == "None":
            uzaklik = 0.1
        # print(price_difference_calculator(float(mehmet["entry_price"]), market_price), "BU KADAR UZAKTASIN")

        uzaklik = price_difference_calculator(float(mehmet["entry_price"]), market_price)

        ######### EMİR GÖNDERİMLERİ###################





        if mehmet["size"] >= 2000:
            time.sleep(300)

        if mehmet["side"] == "Buy" and mehmet["unrealised_pnl"] <= 0 and total_skor > 0:

            if uzaklik > 0.1 and uzaklik < 0.2 and mehmet["size"] < 300 :
                client.Order.Order_new(side="Buy", symbol="XRPUSD", order_type="Limit", qty=160,
                                       price=market_price - 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 0.2 and uzaklik < 0.4 and mehmet["size"] < 750 and mehmet["size"] > 300:
                client.Order.Order_new(side="Buy", symbol="XRPUSD", order_type="Limit", qty=320,
                                       price=market_price - 0.0003,
                                       time_in_force="PostOnly").result()

            if uzaklik > 0.4 and uzaklik < 0.8 and mehmet["size"] > 750 and mehmet["size"] < 1000:
                client.Order.Order_new(side="Buy", symbol="XRPUSD", order_type="Limit", qty=480,
                                       price=market_price - 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 1 and uzaklik < 2 and mehmet["size"] > 1000 and mehmet["size"] < 1250:
                client.Order.Order_new(side="Buy", symbol="XRPUSD", order_type="Limit", qty=640,
                                       price=market_price - 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 2 and uzaklik < 4 and mehmet["size"] > 1250 and mehmet["size"] < 1500:
                client.Order.Order_new(side="Buy", symbol="XRPUSD", order_type="Limit", qty=800,
                                       price=market_price - 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 4 and mehmet["size"] > 1500 and mehmet["size"] < 1750:
                client.Order.Order_new(side="Buy", symbol="XRPUSD", order_type="Limit", qty=960,
                                       price=market_price - 0.0001,
                                       time_in_force="PostOnly").result()

        if total_skor > 0 and mehmet["side"] == "None":
            client.Order.Order_new(side="Buy", symbol="XRPUSD", order_type="Limit", qty=80, price=market_price - 0.0001,
                                   time_in_force="PostOnly").result()

        if total_skor < 0 and mehmet["side"] == "None":
            client.Order.Order_new(side="Sell", symbol="XRPUSD", order_type="Limit", qty=80,
                                   price=market_price + 0.0001,
                                   time_in_force="PostOnly").result()

        if mehmet["side"] == "Sell" and mehmet["unrealised_pnl"] <= 0 and total_skor < 0:

            if uzaklik > 0.1 and uzaklik < 0.2 and mehmet["size"] < 300:
                client.Order.Order_new(side="Sell", symbol="XRPUSD", order_type="Limit", qty=160,
                                       price=market_price + 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 0.2 and uzaklik < 0.4 and mehmet["size"] < 750 and mehmet["size"] > 300:
                client.Order.Order_new(side="Sell", symbol="XRPUSD", order_type="Limit", qty=320,
                                       price=market_price + 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 0.4 and uzaklik < 0.8 and mehmet["size"] > 750 and mehmet["size"] < 1000:
                client.Order.Order_new(side="Sell", symbol="XRPUSD", order_type="Limit", qty=480,
                                       price=market_price + 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 1 and uzaklik < 2 and mehmet["size"] > 1000 and mehmet["size"] < 1250:
                client.Order.Order_new(side="Sell", symbol="XRPUSD", order_type="Limit", qty=640,
                                       price=market_price + 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 2 and uzaklik < 4 and mehmet["size"] > 1250 and mehmet["size"] < 1500:
                client.Order.Order_new(side="Sell", symbol="XRPUSD", order_type="Limit", qty=800,
                                       price=market_price + 0.0001,
                                       time_in_force="PostOnly").result()

            if uzaklik > 4 and mehmet["size"] > 1500 and mehmet["size"] < 1750:
                client.Order.Order_new(side="Sell", symbol="XRPUSD", order_type="Limit", qty=960,
                                       price=market_price + 0.0001,
                                       time_in_force="PostOnly").result()
except:
    restart()
