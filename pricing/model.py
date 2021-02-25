#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.commons import *

class SymbolPrice:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price

def refine_pricing_model(candle: Candle, model: dict):
    sym_pri = SymbolPrice(candle.s, candle.c)
    if candle.dt in model.keys():
        existing_price_list = model[candle.dt]
        existing_price_list.append(sym_pri)
        model[candle.dt] = existing_price_list
    else:
        model[candle.dt] = [sym_pri]
    return model


def generate_pricing_model(candle_list):
    model = {}
    for three_candles in candle_list:
        model = refine_pricing_model(three_candles.candle1, model)
    return model


def get_current_price(symbol: str, dt: str, model):
    syms_pris = model[dt]
    for sym_pri in syms_pris:
        if sym_pri.symbol is symbol:
            return sym_pri.price