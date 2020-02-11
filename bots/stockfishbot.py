#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse

from stockfish import Stockfish


def debug(msg):
    print(msg, file=sys.stderr)


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', help='Show board', type=int,
                        action='store', default=1)
    args = parser.parse_args()
    return args


debug("Stockfish bot starting!\n")

args = parser_args()
s = Stockfish('./bin/stockfish')
s.set_skill_level(args.level)

while True:
    fen = input()
    debug(fen)
    s.set_fen_position(fen)
    print(s.get_best_move())
