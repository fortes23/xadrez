#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import chess

from util import debug, minimax


class Fish():
    def __init__(self, depth=3, start_msg='Bot starting\n'):
        debug(start_msg)
        self.depth = depth

    def debug(self, msg):
        debug(msg)

    def eval_fn(self, board):
        return (0, 0)

    def cycle(self):
        fen = input()
        board = chess.Board(fen=fen)

        debug("fen: " + board.fen())

        # Get best movement
        (best, m) = minimax(board, board.turn, -99999999, 99999999, self.depth, self.eval_fn)
        debug(f"Best played {best}")

        print(m)
