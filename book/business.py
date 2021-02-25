#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Trade {
#     this-sym
#     this-price
#     that-sym
#     that-price
# }
#
# Portfolio {
#     current_value
#     PortfolioItems: Dict(symbol -> PortfolioItem)
# }
# PortfolioItem {
#     symbol
#     amount
#     purchase_price
#     current_value
# }
# BookOfBusiness{
#     transaction-ledger = List(Trade)
#     bulls(List(symbols))
#     bears(List(symbols))
#     portfolio(List(PortfolioItem))
#
# }
from _ast import List
from training.structures import *
from patterns.commons import *
from pricing.model import *

class Trade:
    def __init__(self, date: str, this_symbol: str, this_price: float, that_symbol: str, that_price: float):
        self.date = date
        self.this_symbol = this_symbol
        self.this_price = this_price
        self.that_symbol = that_symbol
        self.that_price = that_price

class BookOfBusiness:
    def __init__(self, bulls: list[str], bears: list[str], portfolio: dict, current_value: float, transaction_ledger: list[Trade]=(), ):
        self.bulls = bulls
        self.bears = bears
        self.portfolio = portfolio
        self.current_value =current_value
        self.transaction_ledger = transaction_ledger


def calculate_current_value(date, book, pricing_model):
    current_value = 0
    for key in book.portfolio.keys():
        value = book.portfolio[key]
        if value > 0:
            current_price = get_current_price(key, date, pricing_model)
            current_value += current_price * value
    return current_value



def update_portfolio(trade: Trade, book: BookOfBusiness, pricing_model: dict):
    portfolio = book.portfolio
    portfolio[trade.this_symbol] = 0
    portfolio[trade.that_symbol] = trade.this_price/trade.that_price
    book.portfolio = portfolio
    book.current_value = calculate_current_value(trade.date, book, pricing_model)
    return book


def add_trade_to_ledger(trade: Trade, book: BookOfBusiness):
    ledger = book.transaction_ledger
    ledger.append(trade)
    return book


def execute_buy_trade(candle, book, pricing_model):
    for bear in book.bears:
        if book.portfolio[bear] > 0:
            trade = Trade(candle.dt, bear, get_current_price(bear,candle.dt, pricing_model), candle.s, get_current_price(candle.s,candle.dt, pricing_model))
            book = update_portfolio(trade, book, pricing_model)
    return book


def execute_sell_trade(candle, book, pricing_model):
    for bull in book.bulls:
        price_to_split=candle.c
        num_bulls=len(book.bulls)
        price_per_bull=price_to_split/num_bulls
        this_symbol = candle.s
        this_price = price_per_bull
        that_symbol = bull
        that_price = get_current_price(that_symbol, candle.dt, pricing_model)
        trade = Trade(candle.dt, this_symbol, this_price, that_symbol, that_price)
        # book = add_trade_to_ledger(trade, book)
        book = update_portfolio(trade, book, pricing_model)
    return book

def print_bulls_bears(book):
    print("_____bulls_______")
    print(*book.bulls, sep=", ")
    print("_____bears_______")
    print(*book.bears, sep = ", ")


def create_trade(candle: Candle, book: BookOfBusiness, pricing_model):
    this_symbol = candle.s
    this_price = candle.c
    that_symbol = book.bulls[0]
    that_price = get_current_price(that_symbol, candle.dt, pricing_model)
    return Trade(candle.dt, this_symbol, this_price, that_symbol, that_price)


def bull_to_bear(candle: Candle, book: BookOfBusiness, pricing_model):
    if candle.s in book.bulls:
        book.bulls.remove(candle.s)
    if candle.s not in book.bears:
        book.bears.append(candle.s)
        # if this is an owned asset, execute a trade
        if book.portfolio[candle.s] > 0:
            if len(book.bulls) > 0:
                book = execute_sell_trade(candle, book, pricing_model)
    print_bulls_bears(book)
    return book


def bear_to_bull(candle: Candle, book: BookOfBusiness, pricing_model):
    if candle.s in book.bears:
        book.bears.remove(candle.s)
    if candle.s not in book.bulls:
        book.bulls.append(candle.s)
        # if book.portfolio[candle.s] > 0: # if this is an owned asset, execute a trade
        if len(book.bears) > 0:
            book = execute_buy_trade(candle, book, pricing_model)
    print_bulls_bears(book)
    return book
