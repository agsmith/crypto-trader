#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

from book.business import calculate_current_value, zero_portfolio, execute_bull_trade, \
    calculate_current_value_from_model
from domain.objects import Candle, ThreeCandles, BookOfBusiness
from visualization.ingest import get_price_for_symbol, portfolio_ingest, backtest_portfolio_ingest
from pricing.model import get_price_from_model


def balance_backtest_portfolio(book: BookOfBusiness, ccc: ThreeCandles, pricing_model: dict) -> BookOfBusiness:
    if len(book.bulls) > 0:
        current_value = calculate_current_value_from_model(book, ccc.candle1.dt, pricing_model)
        book = zero_portfolio(book)
        amount_of_splits = current_value / len(book.bulls)
        for bull in book.bulls:
            bull_price = get_price_from_model(bull, ccc.candle1.dt, pricing_model)
            bull_shares = amount_of_splits / bull_price
            book.portfolio[bull] = bull_shares
        book.current_value = calculate_current_value_from_model(book, ccc.candle1.dt, pricing_model)
    # backtest_portfolio_ingest(book.portfolio, ccc.candle1.dt, pricing_model)
    if book.high_value < book.current_value:
        book.high_value = book.current_value
    if book.low_value > book.current_value:
        book.low_value = book.current_value
    return book


def balance_portfolio(book: BookOfBusiness) -> BookOfBusiness:

    if len(book.bulls) > 0:
        current_value = calculate_current_value(book)
        book = zero_portfolio(book)
        amount_of_splits = current_value/len(book.bulls)
        for bull in book.bulls:
            bull_price = get_price_for_symbol(bull)
            bull_shares = amount_of_splits/bull_price
            book.portfolio[bull] = bull_shares
        book.current_value = calculate_current_value(book)
    portfolio_ingest(book.portfolio)
    if book.high_value < book.current_value:
        book.high_value = book.current_value
    if book.low_value > book.current_value:
        book.low_value = book.current_value
    return book


def print_pattern(pattern, candle):
    print(pattern + " for " + candle.s + " on " + candle.dt)


def green(candle):
    return candle.c >= candle.o


def red(candle):
    return candle.o > candle.c


def lower_wick(green, candle):
    if green:
        return candle.o - candle.l
    else:
        return candle.c - candle.l


def upper_wick(green, candle):
    if green:
        return candle.h - candle.c
    else:
        return candle.h - candle.o


def body_size(green, candle):
    if green:
        return candle.c - candle.o
    else:
        return candle.o - candle.c


def create_new_three_candle(candle, ccc):
    if ccc.candle2 is None:
        ccc.candle2 = ccc.candle1
    elif ccc.candle3 is None:
        ccc.candle3 = ccc.candle2
        ccc.candle2 = ccc.candle1
    else:
        ccc.candle3 = ccc.candle2
        ccc.candle2 = ccc.candle1
        ccc.candle1 = candle
    return ccc



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


