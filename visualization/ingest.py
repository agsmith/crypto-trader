from ctypes import Union
from datetime import datetime

from influxdb_client import InfluxDBClient, WritePrecision, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
from book.business import BookOfBusiness

token = "ovqvP50lEKpRx51v9_BFxNzpd6SozAJbk26Wfv_HjzLFVzybeXnbyJoznct3sCnQTNRcuP-voQ-gjrKY3kAV1w=="
org = "quantegy"
pricing_bucket = "pricing-data"
trade_bucket = "trade-data"

client = InfluxDBClient(url="http://127.0.0.1:55000", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

# data = "mem,host=host1 used_percent=23.43234543"
# write_api.write(bucket, org, data)


def pricing_ingest(pricing_model):
    for key in pricing_model.keys():
        prisyms = pricing_model[key]
    for prisym in prisyms:
        symbol = prisym.symbol
        price = prisym.price
        date = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
        point = Point("PriceEvent").\
            tag("symbol", symbol).\
            field("price", price).\
            time(date, WritePrecision.NS)
        print("Writing " + symbol + ": " + str(price) + " to influxDB")
        write_api.write(pricing_bucket, org, point)


def trade_ingest(book):
    for transaction in book.transaction_ledger:
        date = datetime.strptime(transaction.trade.date, '%Y-%m-%d %H:%M:%S')
        if not isinstance(transaction.current_value, float):
            print("not_float")
            transaction.current_value = float(transaction.current_value)
        trade_str = transaction.trade.this_symbol + "/" + transaction.trade.that_symbol
        point = Point("TradeEvent").\
            tag("trade", "trade").\
            field("trade-symbols", trade_str).\
            field("book_value", transaction.current_value).\
            time(date, WritePrecision.NS)
        print("Writing Trade " + trade_str + " to influxDB")
        write_api.write(trade_bucket, org, point)




