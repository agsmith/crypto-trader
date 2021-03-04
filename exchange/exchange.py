#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ccxt
import appconfig as cfg

exchange = None


def init_exchange():
    exchange_id = cfg.exchange["id"]
    exchange_class = getattr(ccxt, exchange_id)
    return exchange_class({
        'apiKey': cfg.exchange["api_key"],
        'secret': cfg.exchange["api_secret"],
        'timeout': 30000,
        'enableRateLimit': True,
    })


def refresh_exchange():
    global exchange
    exchange = init_exchange()
    return exchange


def get_exchange():
    global exchange
    if exchange is None:
        exchange = refresh_exchange()
    return exchange

