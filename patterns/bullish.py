#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.commons import red, green, lower_wick, body_size, upper_wick, print_pattern
from book.business import *


def inverted_hammer(book, candle):
    if green(candle):
        if upper_wick(True, candle) >= (body_size(True, candle) * 2):
            if lower_wick(True, candle) <=(body_size(True, candle) * .5):
                print_pattern("[BULL] Inverted Hammer", candle)
                return bear_to_bull(candle, book)
            else: return book
        else: return book
    else: return book


def hammer(book, candle):
    if green(candle):
        if lower_wick(True, candle) >= (body_size(True, candle) * 2):
            if upper_wick(True, candle) <=(body_size(True, candle) * .5):
                print_pattern("[BULL] Hammer", candle)
                return bear_to_bull(candle, book)
            else: return book
        else: return book
    else: return book


def white_soldiers(book, ccc):
    if(green(ccc.candle1)):
        if(green(ccc.candle2)):
            if(green(ccc.candle3)):
                if ccc.candle1.o > ccc.candle2.o:
                    if ccc.candle2.o > ccc.candle3.o:
                        if ccc.candle1.c > ccc.candle2.c:
                            if ccc.candle2.c > ccc.candle3.c:
                                print_pattern("[BULL] White Soldiers", ccc.candle1)
                                return bear_to_bull(ccc.candle1, book)
                            else: return book
                        else: return book
                    else: return book
                else: return book
            else: return book
        else: return book
    else: return book

def bullish_harami(book, ccc):
    if(green(ccc.candle1)):
        if(red(ccc.candle2)):
            if(ccc.candle1.o > ccc.candle2.c):
                if(ccc.candle1.c < ccc.candle2.o):
                    print_pattern("[BULL] Bullish Harami", ccc.candle1)
                    return bear_to_bull(ccc.candle1, book)
                else: return book
            else: return book
        else: return book
    else: return book


def identify_bullish_patterns(book, ccc):
    book = hammer(book, ccc.candle1)
    book = inverted_hammer(book, ccc.candle1)
    book = white_soldiers(book, ccc)
    book = bullish_harami(book, ccc)
    return book