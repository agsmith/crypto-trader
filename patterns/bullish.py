#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.commons import *


def identify_bullish_patterns(compound):
    hammer(compound.day1)
    inverted_hammer(compound.day1)
    white_soldiers(compound)
    bullish_harami(compound)


def inverted_hammer(row):
    if green(row):
        if upper_wick(True, row) >= (body_size(True, row) * 2):
            if lower_wick(True, row) <=(body_size(True, row) * .5):
                print("Inverted Hammer at " + row.dt)


def hammer(row):
    if green(row):
        if lower_wick(True, row) >= (body_size(True, row) * 2):
            if upper_wick(True, row) <=(body_size(True, row) * .5):
                print("Hammer at " + row.dt)


def white_soldiers(compound):
    if(green(compound.day1)):
        if(green(compound.day2)):
            if(green(compound.day3)):
                if compound.day1.o > compound.day2.o:
                    if compound.day2.o > compound.day3.o:
                        if compound.day1.c > compound.day2.c:
                            if compound.day2.c > compound.day3.c:
                                print("White Soldiers on " + compound.day1.dt)

def bullish_harami(compound):
    if(green(compound.day1)):
        if(red(compound.day2)):
            if(compound.day1.o > compound.day2.c):
                if(compound.day1.c < compound.day2.o):
                    print("Bullish Harami on " + compound.day1.dt)

