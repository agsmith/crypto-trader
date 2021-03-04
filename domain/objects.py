class Candle:
    def __init__(self, s: str, o: float, c: float, h: float, l: float, dt: str, u: str):
        self.s = s
        self.o = o
        self.c = c
        self.h = h
        self.l = l
        self.dt = dt
        self.u = u


class TwoCandles:
    def __init__(self, candle1: Candle, candle2: Candle):
        self.candle1 = candle1
        self.candle2 = candle2


class ThreeCandles:
    def __init__(self, candle1: Candle, candle2: Candle, candle3: Candle):
        self.candle1 = candle1
        self.candle2 = candle2
        self.candle3 = candle3


class SymbolPrice:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price


class Trade:
    def __init__(self, date: str, this_symbol: str, this_price: float, that_symbol: str, that_price: float):
        self.date = date
        self.this_symbol = this_symbol
        self.this_price = this_price
        self.that_symbol = that_symbol
        self.that_price = that_price


class CurrValTrade:
    def __init__(self, current_value: float, trade: Trade):
        self.current_value = current_value
        self.trade = trade


class BookOfBusiness:
    def __init__(self, bulls: list[str], bears: list[str], portfolio: dict, current_value: float, high_value: float,
                 low_value: float, transaction_ledger: list[CurrValTrade]):
        self.bulls = bulls
        self.bears = bears
        self.portfolio = portfolio
        self.current_value = current_value
        self.high_value = high_value
        self.low_value = low_value
        self.transaction_ledger = transaction_ledger