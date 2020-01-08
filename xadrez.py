#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chess

board = chess.Board()

print("Starting to work...\n")

while not board.is_checkmate():
    found = False
    print(board)
    while not found:
        turn = 'WHITE' if board.turn == chess.WHITE else 'BLACK'
        a = input(f"\nInput code ({turn})\n")
        if a[0:2] not in chess.SQUARE_NAMES or a[2:4] not in chess.SQUARE_NAMES:
            print('Invalid uci code')
            continue

        if chess.Move.from_uci(a) in list(board.legal_moves):
            board.push_uci(a)
            found = True
        else:
            print('Invalid code movement')
