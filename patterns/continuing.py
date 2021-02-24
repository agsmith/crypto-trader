#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patterns.commons import *


def identify_continuing_patterns(compound):
    identify_doji(compound.day1)


def identify_doji(row):
    if green(row):
        if upper_wick(True, row) == lower_wick(True, row):
            if body_size(True, row) >= (row.o * 0.001):
                print("Doji at " + row.dt)