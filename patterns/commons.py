#!/usr/bin/env python
# -*- coding: utf-8 -*-

class HistoricalData:
    def __init__(self, o: float, c: float, h: float, l: float, dt: str):
        self.o = o
        self.c = c
        self.h = h
        self.l = l
        self.dt = dt


class TwoDayHistoricalData:
    def __init__(self, day1: HistoricalData, day2: HistoricalData):
        self.day1 = day1
        self.day2 = day2


class ThreeDayHistoricalData:
    def __init__(self, day1: HistoricalData, day2: HistoricalData, day3: HistoricalData):
        self.day1 = day1
        self.day2 = day2
        self.day3 = day3


def green(row):
    return (row.c >= row.o)

def red(row):
    return (row.o > row.c)

def lower_wick(green, row):
    if green:
        return row.o - row.l
    else:
        return row.c - row.l

def upper_wick(green, row):
    if green:
        return row.h-row.c
    else:
        return row.h-row.o


def body_size(green, row):
    if green:
        return row.c - row.o
    else:
        return row.o -row.c

