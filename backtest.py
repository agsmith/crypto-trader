#!/usr/bin/env python
# -*- coding: utf-8 -*-

import appconfig as cfg
import ccxt
import json
import csv

# from book.business import *
from patterns.bullish import *
from patterns.bearish import *
from patterns.continuing import *
from training.structures import *
from patterns.commons import *
from pricing.model import *
from visualization.ingest import pricing_ingest, trade_ingest

# exchange_id = 'binanceus'
# exchange_class = getattr(ccxt, exchange_id)
# exchange = exchange_class({
#     'apiKey': cfg.binanceus["api_key"],
#     'secret': cfg.binanceus["api_secret"],
#     'timeout': 30000,
#     'enableRateLimit': True,
# })
#
# print(json.dumps(exchange.fetch_balance(), indent=4, sort_keys=True))
# filename = "/Users/asmith986/work/development/crypto-trader/training/Binance_BTCUSDT_1h.csv"


def create_candle_list(data):
    candle_list = []
    for datum in data:
        candle3 = None  # twodays ago
        candle2 = None  # yesterday
        with open(datum.filename, 'r') as csvfile:
            csvfile.__next__() # skip first line of csv file
            reader = csv.DictReader(csvfile)
            for candle in reader:
                candle1 = Candle(datum.symbol, float(candle['open']), float(candle['close']), float(candle['high']), float(candle['low']), candle['date'], candle['unix'])
                if candle2 is None:
                    candle2 = candle1
                elif candle3 is None:
                    candle3 = candle2
                    candle2 = candle1
                else:
                    candle_list.append(ThreeCandles(candle1, candle2, candle3))
                    candle3 = candle2
                    candle2 = candle1

    candle_list.sort(key=lambda x: x.candle1.u, reverse=False)

    return candle_list


def execute_pattern_analysis(book, candle_list, pricing_model):
    for candle in candle_list:
        book.current_value = calculate_current_value(candle.candle1.dt, book, pricing_model)
        book = identify_bullish_patterns(book, candle, pricing_model) #bulls
        book = identify_bearish_patterns(book, candle, pricing_model) # bears
    return book


def go():
    # init book of business so that all symbols are in bear pattern
    book = BookOfBusiness(bulls=[], bears=Structures.symbols, current_value=0.00, high_value=0.0, low_value=10000.0, portfolio=Structures.portfolio, transaction_ledger=list())

    candle_list = create_candle_list(Structures.h_data)
    # candle_list = create_candle_list(Structures.m_data)
    # candle_list = create_candle_list(Structures.d_data)

    pricing_model = generate_pricing_model(candle_list)
    book = execute_pattern_analysis(book, candle_list, pricing_model)
    # pricing_ingest(pricing_model)
    trade_ingest(book)
    print("Current Value:" + str(book.current_value))
    print("High Value:" + str(book.high_value))
    print("Low_Value:" + str(book.low_value))

go()


