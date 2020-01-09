#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random

import chess


def debug(msg):
    print(msg, file=sys.stderr)


debug("Random bot starting!\n")


while True:
    fen = input()
    board = chess.Board(fen=fen)
    debug("fen: " + board.fen())
    moves = list(board.legal_moves)
    r = random.randint(0, len(moves)-1)
    print(moves[r].uci())
