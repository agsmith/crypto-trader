#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.commons import red, green, lower_wick, upper_wick, print_pattern, body_size
from book.business import *


def hanging_man(book, candle):
    if red(candle): # Red
        if lower_wick(False, candle) >= (body_size(False, candle) * 2): # big lower wick
            if upper_wick(False, candle) <= (body_size(False, candle) * .5): # small upper wick
                print_pattern("[BEAR] Hanging Man", candle)
                return bull_to_bear(candle, book)
            else: return book
        else: return book
    else: return book


def shooting_star(book, candle):
    if red(candle):
        if upper_wick(False, candle) >= (body_size(False, candle) * 2): # big upper wick
            if lower_wick(False, candle) <= (body_size(False, candle) * .5):  # small lower wick
                print_pattern("[BEAR] Shooting Star", candle)
                return bull_to_bear(candle, book)
            else: return book
        else: return book
    else: return book


def black_crows(book, compound):
    if red(compound.candle1):
        if red(compound.candle2):
            if red(compound.candle3):
                if compound.candle1.o < compound.candle2.o:
                    if compound.candle2.o < compound.candle3.o:
                        if compound.candle1.c < compound.candle2.c:
                            if compound.candle2.c < compound.candle3.c:
                                print_pattern("[BEAR] Black Crows", compound.candle1)
                                return bull_to_bear(compound.candle1, book)
                            else: return book
                        else: return book
                    else: return book
                else: return book
            else: return book
        else: return book
    else: return book


def bearish_harami(book, compound):
    if red(compound.candle1):
        if green(compound.candle2):
            if compound.candle1.o < compound.candle2.c:
                if compound.candle1.c > compound.candle2.o:
                    print_pattern("[BEAR] Bearish Harami", compound.candle1)
                    return bull_to_bear(compound.candle1, book)
                else: return book
            else: return book
        else: return book
    else: return book


def identify_bearish_patterns(book, compound):
    book = hanging_man(book, compound.candle1)
    book = shooting_star(book, compound.candle1)
    book = black_crows(book, compound)
    book = bearish_harami(book, compound)
    return book