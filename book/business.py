#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from domain.objects import Trade, CurrValTrade, BookOfBusiness
from exchange.exchange import get_exchange
from pricing.model import *
from visualization.ingest import get_price_for_symbol, trade_ingest, get_all_symbols, get_price_and_symbol, live_ingest_single_symbol


def print_trade(trade):
    print("Trading " + trade.this_symbol + "@" + str(trade.this_price) + " for " + trade.that_symbol + "@" + str(
        trade.that_price))


def calculate_current_value_from_model(book: BookOfBusiness, date: str, pricing_model: dict) -> BookOfBusiness:
    current_value = 0
    for key in book.portfolio.keys():
        value = book.portfolio[key]
        if value > 0:
            current_price = get_price_from_model(key, date, pricing_model)
            if current_price is None:
                print(key + " price data not found")
            current_value = current_value + (current_price * value)
    return current_value


def calculate_current_value(book: BookOfBusiness):
    current_value = 0
    for key in book.portfolio.keys():
        value = book.portfolio[key]
        if value > 0:
            exchange = get_exchange()
            candle = live_ingest_single_symbol(json.dumps(exchange.fetchTicker(key+"/USD"), indent=4, sort_keys=True))
            current_price = candle.c
            current_value = current_value + (current_price * value)
    return current_value


def zero_portfolio(book: BookOfBusiness) -> BookOfBusiness:
    for item in book.portfolio.keys():
        book.portfolio[item] = 0
    return book


def update_portfolio(trade: Trade, book: BookOfBusiness, pricing_model: dict):
    portfolio = book.portfolio
    num_shares = portfolio[trade.this_symbol]
    portfolio[trade.this_symbol] = 0
    if trade.this_price is None:
        trade.this_price = get_price_for_symbol(trade.this_symbol)
    if trade.that_price is None:
        trade.that_price = get_price_for_symbol(trade.that_symbol)
    if num_shares is None:
        num_shares = 0
    portfolio[trade.that_symbol] = (trade.this_price * num_shares) / trade.that_price
    book.portfolio = portfolio
    book.current_value = calculate_current_value(book)
    if book.current_value > book.high_value:
        book.high_value = book.current_value
    if book.current_value < book.low_value:
        book.low_value = book.current_value
    return book


def add_trade_to_ledger(trade: Trade, book: BookOfBusiness):
    cvt = CurrValTrade(book.current_value, trade)
    book.transaction_ledger.append(cvt)
    return book


def execute_bull_trade(candle, book, pricing_model):
    for bear in book.bears:
        if book.portfolio[bear] > 0:
            if bear is not candle.s:
                trade = create_trade(candle.dt, bear, get_price_from_model(bear, candle.dt, pricing_model), candle.s,
                                     get_price_from_model(candle.s, candle.dt, pricing_model))
                book = add_trade_to_ledger(trade, book)
                book = update_portfolio(trade, book, pricing_model)
                trade_ingest(trade, book.current_value)
    return book


def execute_bear_trade(candle, book, pricing_model):
    for bull in book.bulls:
        price_to_split = candle.c
        num_bulls = len(book.bulls)
        price_per_bull = price_to_split / num_bulls
        this_symbol = candle.s
        this_price = price_per_bull
        that_symbol = bull
        that_price = get_price_from_model(that_symbol, candle.dt, pricing_model)
        if this_symbol is not that_symbol:
            trade = create_trade(candle.dt, this_symbol, this_price, that_symbol, that_price)
            book = add_trade_to_ledger(trade, book)
            book = update_portfolio(trade, book, pricing_model)
            trade_ingest(trade, book.current_value)
    return book


def print_bulls_bears(book):
    print("_____bulls_______")
    print(*book.bulls, sep=", ")
    print("_____bears_______")
    print(*book.bears, sep=", ")


def create_trade(date, this_symbol, this_price, that_symbol, that_price):
    trade = Trade(date, this_symbol, this_price, that_symbol, that_price)
    print_trade(trade)
    return trade


def bull_to_bear(candle: Candle, book: BookOfBusiness) -> BookOfBusiness:
    if candle.s in book.bulls:
        book.bulls.remove(candle.s)
    if candle.s not in book.bears:
        book.bears.append(candle.s)
    return book


def bear_to_bull(candle: Candle, book: BookOfBusiness) -> BookOfBusiness:
    if candle.s in book.bears:
        book.bears.remove(candle.s)
    if candle.s not in book.bulls:
        book.bulls.append(candle.s)
    return book


def get_recent_prices():
    prices = []
    symbols = get_all_symbols()
    for symbol in symbols:
        prices.append(get_price_and_symbol(symbol[1]))
    return prices
