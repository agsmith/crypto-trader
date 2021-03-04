#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.bearish import *
from patterns.bullish import identify_bullish_patterns
from patterns.commons import create_candle_list, balance_backtest_portfolio
from training.structures import *
from pricing.model import *
from visualization.ingest import backtest_pricing_ingest, ledger_ingest, backtest_current_value_ingest, \
    backtest_btc_price_ingest, purge_backtest_dashboard, backtest_portfolio_ingest


def backtest():
    book = BookOfBusiness(bulls=[], bears=Structures.symbols, current_value=0.00, high_value=0.0, low_value=10000.0, portfolio=Structures.portfolio, transaction_ledger=list())

    purge_backtest_dashboard()

    candle_list = create_candle_list(Structures.h_data)
    # candle_list = create_candle_list(Structures.m_data)
    # candle_list = create_candle_list(Structures.d_data)

    pricing_model = generate_pricing_model(candle_list)
    backtest_pricing_ingest(pricing_model)
    for ccc in candle_list:
        book = identify_bullish_patterns(book, ccc)  # bulls
        book = identify_bearish_patterns(book, ccc)  # bears
        book = balance_backtest_portfolio(book, ccc, pricing_model)
        backtest_current_value_ingest(ccc.candle1.dt, book.current_value)
        btc_price = get_price_from_model("BTC", ccc.candle1.dt, pricing_model)
        backtest_btc_price_ingest(ccc.candle1.dt, btc_price)
        backtest_portfolio_ingest(book.portfolio, ccc.candle1.dt, pricing_model)
    print("Current Value:" + str(book.current_value))
    print("High Value:" + str(book.high_value))
    print("Low_Value:" + str(book.low_value))


backtest()
