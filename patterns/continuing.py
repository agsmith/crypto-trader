#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.commons import *


def identify_continuing_patterns(compound):
    identify_doji(compound.candle1)


def identify_doji(candle):
    if green(candle):
        if upper_wick(True, candle) == lower_wick(True, candle):
            if body_size(True, candle) >= (candle.o * 0.001):
                print("Doji at " + candle.dt)