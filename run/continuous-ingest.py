#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import appconfig as cfg
import ccxt
import json
from visualization.ingest import live_ingest


def continuous_ingest():
    exchange_id = 'binanceus'
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': cfg.binanceus["api_key"],
        'secret': cfg.binanceus["api_secret"],
        'timeout': 30000,
        'enableRateLimit': True,
    })
    while True:
        # Code executed here
        live_ingest(json.dumps(exchange.fetchTickers(), indent=4, sort_keys=True))
        time.sleep(60)


continuous_ingest()
