#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random

from stockfish import Stockfish


def debug(msg):
    print(msg, file=sys.stderr)


debug("Stockfish bot starting!\n")

s = Stockfish('./bin/stockfish')
s.set_skill_level(2)

while True:
    fen = input()
    debug(fen)
    s.set_fen_position(fen)
    print(s.get_best_move())