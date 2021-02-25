#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.commons import *
from book.business import *


def identify_bullish_patterns(book, compound, pricing_model):
    book = hammer(book, compound.candle1, pricing_model)
    book = inverted_hammer(book, compound.candle1, pricing_model)
    book = white_soldiers(book, compound, pricing_model)
    book = bullish_harami(book, compound, pricing_model)
    return book


def inverted_hammer(book, candle, pricing_model):
    if green(candle):
        if upper_wick(True, candle) >= (body_size(True, candle) * 2):
            if lower_wick(True, candle) <=(body_size(True, candle) * .5):
                print_pattern("[BULL] Inverted Hammer", candle)
                return bear_to_bull(candle, book, pricing_model)
            else: return book
        else: return book
    else: return book


def hammer(book, candle, pricing_model):
    if green(candle):
        if lower_wick(True, candle) >= (body_size(True, candle) * 2):
            if upper_wick(True, candle) <=(body_size(True, candle) * .5):
                print_pattern("[BULL] Hammer", candle)
                return bear_to_bull(candle, book, pricing_model)
            else: return book
        else: return book
    else: return book


def white_soldiers(book, compound, pricing_model):
    if(green(compound.candle1)):
        if(green(compound.candle2)):
            if(green(compound.candle3)):
                if compound.candle1.o > compound.candle2.o:
                    if compound.candle2.o > compound.candle3.o:
                        if compound.candle1.c > compound.candle2.c:
                            if compound.candle2.c > compound.candle3.c:
                                print_pattern("[BULL] White Soldiers", compound.candle1)
                                return bear_to_bull(compound.candle1, book, pricing_model)
                            else: return book
                        else: return book
                    else: return book
                else: return book
            else: return book
        else: return book
    else: return book

def bullish_harami(book, compound, pricing_model):
    if(green(compound.candle1)):
        if(red(compound.candle2)):
            if(compound.candle1.o > compound.candle2.c):
                if(compound.candle1.c < compound.candle2.o):
                    print_pattern("[BULL] Bullish Harami", compound.candle1)
                    return bear_to_bull(compound.candle1, book, pricing_model)
                else: return book
            else: return book
        else: return book
    else: return book

