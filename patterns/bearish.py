#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.commons import *


def identify_bearish_patterns(compound):
    hanging_man(compound.day1)
    shooting_star(compound.day1)
    black_crows(compound)
    bearish_harami(compound)


def hanging_man(row):
    if red(row): # Red
        if lower_wick(False, row) >= (body_size(False, row) * 2): # big lower wick
            if upper_wick(False, row) <= (body_size(False, row) * .5): # small upper wick
                print("Hanging Man at " + row.dt)


def shooting_star(row):
    if red(row):
        if upper_wick(False, row) >= (body_size(False, row) * 2): # big upper wick
            if lower_wick(False, row) <= (body_size(False, row) * .5):  # small lower wick
                print("Shooting Star at " + row.dt)


def black_crows(compound):
    if(red(compound.day1)):
        if(red(compound.day2)):
            if(red(compound.day3)):
                if compound.day1.o < compound.day2.o:
                    if compound.day2.o < compound.day3.o:
                        if compound.day1.c < compound.day2.c:
                            if compound.day2.c < compound.day3.c:
                                print("Black Crows on " + compound.day1.dt)


def bearish_harami(compound):
    if(red(compound.day1)):
        if(green(compound.day2)):
            if(compound.day1.o < compound.day2.c):
                if(compound.day1.c > compound.day2.o):
                    print("Bearish Harami on " + compound.day1.dt)