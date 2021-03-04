#!/usr/bin/env python
# -*- coding: utf-8 -*-
from domain.objects import Candle, SymbolPrice


def refine_pricing_model(candle: Candle, model: dict) -> dict:
    sym_pri = SymbolPrice(candle.s, candle.c)
    key = candle.dt
    if key in model.keys():
        existing_price_list = model[key]
        existing_price_list.append(sym_pri)
        model[key] = existing_price_list
    else:
        model[key] = [sym_pri]
    return model


def generate_pricing_model(candle_list) -> dict:
    model = {}
    for three_candles in candle_list:
        model = refine_pricing_model(three_candles.candle1, model)
    return model


def get_price_from_model(symbol: str, dt: str, model: dict):
    syms_pris = model[dt]
    for sym_pri in syms_pris:
        if sym_pri.symbol == symbol:
            return sym_pri.price