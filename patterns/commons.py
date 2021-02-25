#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def print_pattern(pattern, candle):
    print(pattern + " for " + candle.s + " on " + candle.dt)


def green(candle):
    return candle.c >= candle.o


def red(candle):
    return candle.o > candle.c


def lower_wick(green, candle):
    if green:
        return candle.o - candle.l
    else:
        return candle.c - candle.l


def upper_wick(green, candle):
    if green:
        return candle.h - candle.c
    else:
        return candle.h - candle.o


def body_size(green, candle):
    if green:
        return candle.c - candle.o
    else:
        return candle.o - candle.c
