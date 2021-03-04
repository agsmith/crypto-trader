#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
import json


from domain.objects import ThreeCandles, BookOfBusiness
from patterns.bearish import identify_bearish_patterns
from patterns.bullish import identify_bullish_patterns
from patterns.commons import create_new_three_candle, calculate_current_value, balance_portfolio
from pricing.model import generate_pricing_model
from visualization.ingest import live_ingest, get_all_symbols, current_value_ingest, portfolio_ingest, \
    high_value_ingest, low_value_ingest, initial_value_ingest
from exchange.exchange import get_exchange, refresh_exchange


def soak():
    candle_dict = {}
    portfolio = {"BTC": 1.0}
    symbols = ["BTC"]
    exchange = get_exchange()
    exchange_counter = 0
    live_ingest(json.dumps(exchange.fetchTickers(), indent=4, sort_keys=True))
    symbol_tuples = get_all_symbols()
    for symbol_tuple in symbol_tuples:
        symbol = symbol_tuple[1]
        if symbol not in symbols:
            symbols.append(symbol)
            if symbol == "BTC":
                portfolio[symbol] = 1.0
            else:
                portfolio[symbol] = 0.0

    portfolio_ingest(portfolio)
    book = BookOfBusiness(bulls=[], bears=symbols, current_value=0.00, high_value=0.0, low_value=5000000.0,
                          portfolio=portfolio, transaction_ledger=list())

    book.current_value = calculate_current_value(book)
    initial_value = book.current_value
    initial_value_ingest(initial_value)

    while True:
        exchange_counter = exchange_counter +1
        if exchange_counter > 30:
            exchange = refresh_exchange()

        new_candle_list = live_ingest(json.dumps(exchange.fetchTickers(), indent=4, sort_keys=True))
        for candle in new_candle_list:
            try:
                existing_three_candle = candle_dict[candle.s]
                new_three_candle = create_new_three_candle(candle, existing_three_candle)
                candle_dict[candle.s] = new_three_candle
            except:
                existing_three_candle = ThreeCandles(candle1=candle, candle2=None, candle3=None)
                candle_dict[candle.s] = existing_three_candle

        ccc_list = []
        for key in candle_dict.keys():
            ccc_list.append(candle_dict[key])

        if ccc_list[0].candle3 is not None:
            for ccc in ccc_list:
                book = identify_bullish_patterns(book, ccc)  # bulls
                book = identify_bearish_patterns(book, ccc)  # bears
            book = balance_portfolio(book)
            current_value_ingest(book.current_value)
            high_value_ingest(book.high_value)
            low_value_ingest(book.low_value)
            initial_value_ingest(initial_value)
        now = datetime.now()
        nowdate = now.strftime('%Y-%m-%dT%H:%M')
        print("Sleeping..." + nowdate)
        time.sleep(60)


soak()
