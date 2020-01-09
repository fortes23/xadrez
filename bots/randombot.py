#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random

import chess
#from ..xadrez.util import debug, move

# this must be moved to util.py
def debug(msg):
    print(msg, file=sys.stderr)

def move(mov):
    if len(mov) !=4 or mov[0:2] not in chess.SQUARE_NAMES or mov[2:4] not in chess.SQUARE_NAMES:
        debug('Invalid uci move')
    else:
        print(mov)
###

debug("Random bot starting!\n")

while True:
    fen = input()
    board = chess.Board(fen=fen)
    debug("fen: " + board.fen())
    moves = list(board.legal_moves)
    r = random.randint(0, len(moves)-1)
    move(moves[r].uci())
