import json
import time
from datetime import datetime
import appconfig as cfg

from influxdb_client import InfluxDBClient, WritePrecision, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
from domain.objects import Candle, SymbolPrice, Trade

from exchange.exchange import get_exchange
from pricing.model import get_price_from_model

org = "quantegy"
backtest_bucket = "backtest-data"
pricing_bucket = "pricing-data"
trade_bucket = "trade-data"
portfolio_bucket = "portfolio-data"

client = InfluxDBClient(url=cfg.influxdb["url"], token=cfg.influxdb["token"])

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
delete_api = client.delete_api()


def purge_backtest_dashboard():
    start = "1970-01-01T00:00:00Z"
    stop = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    delete_api.delete(start, stop, '_measurement="PortfolioEvent"', backtest_bucket, org)
    delete_api.delete(start, stop, '_measurement="PriceEvent"', backtest_bucket, org)
    delete_api.delete(start, stop, '_measurement="TradeEvent"', backtest_bucket, org)



def backtest_portfolio_ingest(portfolio: dict, date: str, pricing_model: dict):
    start = "1970-01-01T00:00:00Z"
    stop = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    delete_api.delete(start, stop, '_measurement="PortfolioEvent"', backtest_bucket, org)
    for key in portfolio.keys():
        if portfolio[key] > 0:
            share_price = get_price_from_model(key, date, pricing_model)
            shares = portfolio[key]
            holding_price = share_price * shares
            point = Point("PortfolioEvent"). \
                tag("symbol", key). \
                field("shares", shares). \
                field("share_price", share_price). \
                field("holding_price", holding_price). \
                time(stop, WritePrecision.NS)
            print("Writing " + key + " to portfolio bucket")
            write_api.write(backtest_bucket, org, point)


def portfolio_ingest(portfolio: dict):
    start = "1970-01-01T00:00:00Z"
    stop = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    delete_api.delete(start, stop, '_measurement="PortfolioEvent"', portfolio_bucket, org)
    for key in portfolio.keys():
        if portfolio[key] > 0:
            share_price = get_price_for_symbol(key)
            shares = portfolio[key]
            holding_price = share_price * shares

            point = Point("PortfolioEvent"). \
                tag("symbol", key). \
                field("shares", shares). \
                field("share_price", share_price). \
                field("holding_price", holding_price). \
                time(stop, WritePrecision.NS)
            print("Writing " + key + " to portfolio bucket")
            write_api.write(portfolio_bucket, org, point)


def backtest_pricing_ingest(pricing_model):
    for key in pricing_model.keys():
        prisyms = pricing_model[key]
        for prisym in prisyms:
            symbol = prisym.symbol
            price = float(prisym.price)
            date = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
            point = Point("PriceEvent"). \
                tag("symbol", symbol). \
                field("price", price). \
                time(date, WritePrecision.NS)
            print("Writing " + symbol + ": " + str(price) + " to influxDB")
            write_api.write(backtest_bucket, org, point)


def initial_value_ingest(current_value):
    now = datetime.utcnow()
    date = now.strftime('%Y-%m-%dT%H:%M')
    point = Point("TradeEvent"). \
        tag("initVal", "initVal"). \
        field("init_value", float(current_value)). \
        time(date, WritePrecision.NS)
    write_api.write(trade_bucket, org, point)
    print("Graphed initial value at " + str(current_value))


def low_value_ingest(current_value):
    now = datetime.utcnow()
    date = now.strftime('%Y-%m-%dT%H:%M')
    point = Point("TradeEvent"). \
        tag("lowVal", "lowVal"). \
        field("low_value", float(current_value)). \
        time(date, WritePrecision.NS)
    write_api.write(trade_bucket, org, point)
    print("Graphed low value at " + str(current_value))


def high_value_ingest(current_value):
    now = datetime.utcnow()
    date = now.strftime('%Y-%m-%dT%H:%M')
    point = Point("TradeEvent"). \
        tag("highVal", "highVal"). \
        field("high_value", float(current_value)). \
        time(date, WritePrecision.NS)
    write_api.write(trade_bucket, org, point)
    print("Graphed high value at " + str(current_value))


def backtest_current_value_ingest(date: str, current_value):
    point = Point("TradeEvent"). \
        tag("currVal", "currVal"). \
        field("book_value", float(current_value)). \
        time(date, WritePrecision.NS)
    write_api.write(backtest_bucket, org, point)
    print("Graphed current value at " + str(current_value))


def backtest_btc_price_ingest(date, value):
    point = Point("TradeEvent"). \
        tag("btcVal", "btcVal"). \
        field("btc_value", float(value)). \
        time(date, WritePrecision.NS)
    write_api.write(backtest_bucket, org, point)

def current_value_ingest(current_value):
    now = datetime.utcnow()
    date = now.strftime('%Y-%m-%dT%H:%M')
    point = Point("TradeEvent"). \
        tag("currVal", "currVal"). \
        field("book_value", float(current_value)). \
        time(date, WritePrecision.NS)
    write_api.write(trade_bucket, org, point)
    print("Graphed current value at " + str(current_value))


def trade_ingest(trade: Trade, current_value: float):
    date = datetime.strptime(trade.date, '%Y-%m-%dT%H:%M')
    if not isinstance(current_value, float):
        print("not_float")
        current_value = float(current_value)

    trade_str = trade.this_symbol + "/" + trade.that_symbol
    point = Point("TradeEvent"). \
        tag("trade", trade_str). \
        field("book_value", current_value). \
        time(date, WritePrecision.NS)
    write_api.write(trade_bucket, org, point)


def ledger_ingest(book):
    for transaction in book.transaction_ledger:
        date = datetime.strptime(transaction.trade.date, '%Y-%m-%d %H:%M:%S')
        if not isinstance(transaction.current_value, float):
            print("not_float")
            transaction.current_value = float(transaction.current_value)
        trade_str = transaction.trade.this_symbol + "/" + transaction.trade.that_symbol
        point = Point("TradeEvent"). \
            tag("trade", "trade"). \
            field("trade-symbols", trade_str). \
            field("book_value", transaction.current_value). \
            time(date, WritePrecision.NS)
        print("Writing Trade " + trade_str + " to influxDB")
        write_api.write(trade_bucket, org, point)


def live_ingest_single_symbol(raw: str):
    o: str = ""
    c: str = ""
    h: str = ""
    l: str = ""
    s: str = ""
    sym: str = ""
    dt: str = ""
    u: str = ""

    json_object = json.loads(raw)
    for k in json_object.keys():
        if k == "symbol":
            s = json_object[k]
        if k == "open":
            o = json_object[k]
        if k == "close":
            c = json_object[k]
        if k == "high":
            h = json_object[k]
        if k == "low":
            l = json_object[k]
        if k == "datetime":
            d = json_object[k]
            date = datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%fZ')
            dt = d[:-8]
            unix = time.mktime(date.timetuple())
            u = str(unix)
    last_chars = s[-4:]
    if last_chars == "/USD":
        sym = s[:-4]
        point = Point("PriceEvent"). \
            tag("symbol", sym). \
            field("price", c). \
            time(date, WritePrecision.NS)
        write_api.write(pricing_bucket, org, point)
    return Candle(sym, o, c, h, l, dt, u)


def live_ingest(raw: str):
    print("Ingesting Data...")
    candle_list = []
    json_object = json.loads(raw)
    for key in json_object.keys():
        symbol_data = json.dumps(json_object[key])
        candle = live_ingest_single_symbol(symbol_data)
        if candle.s != "":
            candle_list.append(candle)
    return candle_list


def get_price_and_symbol(symbol: str):
    return SymbolPrice(symbol, get_price_for_symbol(symbol))


def get_price_for_symbol(symbol: str):
    # query = f' from(bucket: "pricing-data")\
    #     |> range(start: -10m)\
    #     |> filter(fn: (r) => r["_measurement"] == "PriceEvent")\
    #     |> filter(fn: (r) => r["_field"] == "price")\
    #     |> filter(fn: (r) => r["symbol"] == "{symbol}")\
    #     |> yield(name: "mean")'
    # get_price_for_symbol
    # result = client.query_api().query(org=org, query=query)
    # results = []
    # for table in result:
    #     for record in table.records:
    #         results.append((record.get_field(), record.get_value()))
    #
    # if len(results) == 0:
    exchange = get_exchange()
    candle = live_ingest_single_symbol(json.dumps(exchange.fetchTicker(symbol + "/USD"), indent=4, sort_keys=True))
    return candle.c
    # else:
    #     result_tuple = results[0]
    #     price = result_tuple[1]
    #     sympri = (SymbolPrice(symbol, price))
    #     return sympri.price


def get_all_symbols():
    query = ' from(bucket: "pricing-data")\
        |> range(start: -1m)\
        |> filter(fn: (r) => r["_measurement"] == "PriceEvent")\
        |> filter(fn: (r) => r["_field"] == "price")\
        |> yield(name: "mean")'

    result = client.query_api().query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(("symbol", record.values["symbol"]))

    return results
