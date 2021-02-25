#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FilesAndSymbols:
    def __init__(self, symbol: str, filename: str):
        self.symbol = symbol
        self.filename = filename


class Structures:

    BTC_h = FilesAndSymbols("BTC","training/data/Binance_BTCUSDT_1h.csv")
    BTC_d = FilesAndSymbols("BTC","training/data/Binance_BTCUSDT_d.csv")
    BTC_m = FilesAndSymbols("BTC","training/data/Binance_BTCUSDT_minute.csv")
    ETH_h = FilesAndSymbols("ETH","training/data/Binance_ETHUSDT_1h.csv")
    ETH_d = FilesAndSymbols("ETH","training/data/Binance_ETHUSDT_d.csv")
    ETH_m = FilesAndSymbols("ETH","training/data/Binance_ETHUSDT_minute.csv")
    LTC_h = FilesAndSymbols("LTC","training/data/Binance_LTCUSDT_1h.csv")
    LTC_d = FilesAndSymbols("LTC","training/data/Binance_LTCUSDT_d.csv")
    LTC_m = FilesAndSymbols("LTC","training/data/Binance_LTCUSDT_minute.csv")
    NEO_h = FilesAndSymbols("NEO","training/data/Binance_NEOUSDT_1h.csv")
    NEO_d = FilesAndSymbols("NEO","training/data/Binance_NEOUSDT_d.csv")
    NEO_m = FilesAndSymbols("NEO","training/data/Binance_NEOUSDT_minute.csv")
    BNB_h = FilesAndSymbols("BNB","training/data/Binance_BNBUSDT_1h.csv")
    BNB_d = FilesAndSymbols("BNB","training/data/Binance_BNBUSDT_d.csv")
    BNB_m = FilesAndSymbols("BNB","training/data/Binance_BNBUSDT_minute.csv")
    XRP_h = FilesAndSymbols("XRP","training/data/Binance_XRPUSDT_1h.csv")
    XRP_d = FilesAndSymbols("XRP","training/data/Binance_XRPUSDT_d.csv")
    XRP_m = FilesAndSymbols("XRP","training/data/Binance_XRPUSDT_minute.csv")
    LINK_h = FilesAndSymbols("LINK","training/data/Binance_LINKUSDT_1h.csv")
    LINK_d = FilesAndSymbols("LINK","training/data/Binance_LINKUSDT_d.csv")
    LINK_m = FilesAndSymbols("LINK","training/data/Binance_LINKUSDT_minute.csv")
    EOS_h = FilesAndSymbols("EOS","training/data/Binance_EOSUSDT_1h.csv")
    EOS_d = FilesAndSymbols("EOS","training/data/Binance_EOSUSDT_d.csv")
    EOS_m = FilesAndSymbols("EOS","training/data/Binance_EOSUSDT_minute.csv")
    TRX_h = FilesAndSymbols("TRX","training/data/Binance_TRXUSDT_1h.csv")
    TRX_d = FilesAndSymbols("TRX","training/data/Binance_TRXUSDT_d.csv")
    TRX_m = FilesAndSymbols("TRX","training/data/Binance_TRXUSDT_minute.csv")
    ETC_h = FilesAndSymbols("ETC","training/data/Binance_ETCUSDT_1h.csv")
    ETC_d = FilesAndSymbols("ETC","training/data/Binance_ETCUSDT_d.csv")
    ETC_m = FilesAndSymbols("ETC","training/data/Binance_ETCUSDT_minute.csv")
    XLM_h = FilesAndSymbols("XLM","training/data/Binance_XLMUSDT_1h.csv")
    XLM_d = FilesAndSymbols("XLM","training/data/Binance_XLMUSDT_d.csv")
    XLM_m = FilesAndSymbols("XLM","training/data/Binance_XLMUSDT_minute.csv")
    ZEC_h = FilesAndSymbols("ZEC","training/data/Binance_ZECUSDT_1h.csv")
    ZEC_d = FilesAndSymbols("ZEC","training/data/Binance_ZECUSDT_d.csv")
    ZEC_m = FilesAndSymbols("ZEC","training/data/Binance_ZECUSDT_minute.csv")
    ADA_h = FilesAndSymbols("ADA","training/data/Binance_ADAUSDT_1h.csv")
    ADA_d = FilesAndSymbols("ADA","training/data/Binance_ADAUSDT_d.csv")
    ADA_m = FilesAndSymbols("ADA","training/data/Binance_ADAUSDT_minute.csv")
    QTUM_h = FilesAndSymbols("QTUM","training/data/Binance_QTUMUSDT_1h.csv")
    QTUM_d = FilesAndSymbols("QTUM","training/data/Binance_QTUMUSDT_d.csv")
    QTUM_m = FilesAndSymbols("QTUM","training/data/Binance_QTUMUSDT_minute.csv")
    DASH_h = FilesAndSymbols("DASH","training/data/Binance_DASHUSDT_1h.csv")
    DASH_d = FilesAndSymbols("DASH","training/data/Binance_DASHUSDT_d.csv")
    DASH_m = FilesAndSymbols("DASH","training/data/Binance_DASHUSDT_minute.csv")
    XMR_h = FilesAndSymbols("XMR","training/data/Binance_XMRUSDT_1h.csv")
    XMR_d = FilesAndSymbols("XMR","training/data/Binance_XMRUSDT_d.csv")
    XMR_m = FilesAndSymbols("XMR","training/data/Binance_XMRUSDT_minute.csv")
    BTT_h = FilesAndSymbols("BTT","training/data/Binance_BTTUSDT_1h.csv")
    BTT_d = FilesAndSymbols("BTT","training/data/Binance_BTTUSDT_d.csv")
    BTT_m = FilesAndSymbols("BTT","training/data/Binance_BTTUSDT_minute.csv")

    symbols = ["BTC", "ETH", "LTC", "NEO", "BNB", "XRP", "LINK", "EOS", "TRX", "ETC", "XLM", "ZEC", "ADA", "QTUM",
               "DASH", "XMR", "BTT"]

    h_data = {BTC_h,ETH_h,LTC_h,NEO_h,BNB_h,XRP_h,LINK_h,
               EOS_h,TRX_h,ETC_h,XLM_h,ZEC_h,ADA_h,QTUM_h,
               DASH_h,XMR_h,BTT_h}

    d_data = {BTC_d,ETH_d,LTC_d,NEO_d,BNB_d,XRP_d,LINK_d,
               EOS_d,TRX_d,ETC_d,XLM_d,ZEC_d,ADA_d,QTUM_d,
               DASH_d,XMR_d,BTT_d}

    m_data = {BTC_m,ETH_m,LTC_m,NEO_m,BNB_m,XRP_m,LINK_m,
               EOS_m,TRX_m,ETC_m,XLM_m,ZEC_m,ADA_m,QTUM_m,
               DASH_m,XMR_m,BTT_m}

    portfolio = {"BTC": 1.0, "ETH": 0.0, "LTC": 0.0, "NEO": 0.0, "BNB": 0.0, "XRP": 0.0, "LINK": 0.0, "EOS": 0.0, "TRX": 0.0, "ETC": 0.0, "XLM": 0.0, "ZEC": 0.0, "ADA": 0.0, "QTUM": 0.0,
               "DASH": 0.0, "XMR": 0.0, "BTT": 0.0}
