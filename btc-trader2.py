#!/usr/bin/env python
# -*- coding: utf-8 -*-

import appconfig as cfg
import ccxt
import json
import csv

from patterns.bullish import *
from patterns.bearish import *
from patterns.continuing import *


def identify_patterns_in_file(filename):
    data_list = []

    day3=None # twodays ago
    day2=None # yesterday
    day1=None # current day
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            current_day = HistoricalData(float(row['open']), float(row['close']), float(row['high']), float(row['low']), row['date'])
            if day2 is None:
                day2 = current_day
            elif day3 is None:
                day3 = day2
                day2 = current_day
            else:
                data_list.append(ThreeDayHistoricalData(current_day, day2, day3))
                day3 = day2
                day2 = current_day

    for data in data_list:
        identify_bullish_patterns(data) #bulls
        identify_continuing_patterns(data) # uncertain
        identify_bearish_patterns(data) # bears


def go():
    h_filename = "training-data/Binance_BTCUSDT_1h.csv"
    d_filename = "training-data/Binance_BTCUSDT_d.csv"
    min_filename = "training-data/Binance_BTCUSDT_minute.csv"
    print("----- MINS ------------------------")
    identify_patterns_in_file(min_filename)
    print("----- HOUR ------------------------")
    identify_patterns_in_file(h_filename)
    print("----- DAYS ------------------------")
    identify_patterns_in_file(d_filename)

go()

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
# filename = "/Users/asmith986/work/development/crypto-trader/training-data/Binance_BTCUSDT_1h.csv"

