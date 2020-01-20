#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

import chess

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../xadrez')

from fish import Fish  # noqa: E402


pawn_weight_pos = [0, 0, 0, 0, 0, 0, 0, 0,
                   5, 10, 10, -20, -20, 10, 10, 5,
                   5, -5, -10, 0, 0, -10, -5, 5,
                   0, 0, 0, 20, 20, 0, 0, 0,
                   5, 5, 10, 25, 25, 10, 5, 5,
                   10, 10, 20, 30, 30, 20, 10, 10,
                   50, 50, 50, 50, 50, 50, 50, 50,
                   0, 0, 0, 0, 0, 0, 0, 0]

knights_weight_pos = [-50, -40, -30, -30, -30, -30, -40, -50,
                      -40, -20, 0, 5, 5, 0, -20, -40,
                      -30, 5, 10, 15, 15, 10, 5, -30,
                      -30, 0, 15, 20, 20, 15, 0, -30,
                      -30, 5, 15, 20, 20, 15, 5, -30,
                      -30, 0, 10, 15, 15, 10, 0, -30,
                      -40, -20, 0, 0, 0, 0, -20, -40,
                      -50, -40, -30, -30, -30, -30, -40, -50]

bishops_weight_pos = [-20, -10, -10, -10, -10, -10, -10, -20,
                      -10, 5, 0, 0, 0, 0, 5, -10,
                      -10, 10, 10, 10, 10, 10, 10, -10,
                      -10, 0, 10, 10, 10, 10, 0, -10,
                      -10, 5, 5, 10, 10, 5, 5, -10,
                      -10, 0, 5, 10, 10, 5, 0, -10,
                      -10, 0, 0, 0, 0, 0, 0, -10,
                      -20, -10, -10, -10, -10, -10, -10, -20]

rooks_weight_pos = [0, 0, 0, 5, 5, 0, 0, 0,
                    -5, 0, 0, 0, 0, 0, 0, -5,
                    -5, 0, 0, 0, 0, 0, 0, -5,
                    -5, 0, 0, 0, 0, 0, 0, -5,
                    -5, 0, 0, 0, 0, 0, 0, -5,
                    -5, 0, 0, 0, 0, 0, 0, -5,
                    5, 10, 10, 10, 10, 10, 10, 5,
                    0, 0, 0, 0, 0, 0, 0, 0]

queens_weight_pos = [-20, -10, -10, -5, -5, -10, -10, -20,
                     -10, 0, 0, 0, 0, 0, 0, -10,
                     -10, 5, 5, 5, 5, 5, 0, -10,
                     0, 0, 5, 5, 5, 5, 0, -5,
                     -5, 0, 5, 5, 5, 5, 0, -5,
                     -10, 0, 5, 5, 5, 5, 0, -10,
                     -10, 0, 0, 0, 0, 0, 0, -10,
                     -20, -10, -10, -5, -5, -10, -10, -20]

kings_weight_pos = [20, 30, 10, 0, 0, 10, 30, 20,
                    20, 20, 0, 0, 0, 0, 20, 20,
                    -10, -20, -20, -20, -20, -20, -20, -10,
                    -20, -30, -30, -40, -40, -30, -30, -20,
                    -30, -40, -40, -50, -50, -40, -40, -30,
                    -30, -40, -40, -50, -50, -40, -40, -30,
                    -30, -40, -40, -50, -50, -40, -40, -30,
                    -30, -40, -40, -50, -50, -40, -40, -30]


class Xouba(Fish):
    def __init__(self, depth):
        super().__init__(depth, "Starting xouba!")

        self.weight_pieces = {
            'p': {"mat": 10, "pos": pawn_weight_pos},
            'n': {"mat": 30, "pos": knights_weight_pos},
            'b': {"mat": 30, "pos": bishops_weight_pos},
            'r': {"mat": 50, "pos": rooks_weight_pos},
            'q': {"mat": 90, "pos": queens_weight_pos},
            'k': {"mat": 900, "pos": kings_weight_pos}
        }

    def get_weigth_piece(self, name, pos):
        return self.weight_pieces[name]['mat'] + self.weight_pieces[name]['pos'][pos]

    def eval_fn(self, board):
        res = 0
        for p in chess.PIECE_TYPES:
            for wp in board.pieces(p, chess.WHITE):
                res += self.get_weigth_piece(chess.piece_symbol(p), wp)
            for bp in board.pieces(p, chess.BLACK):
                res -= self.get_weigth_piece(chess.piece_symbol(p), chess.square_mirror(bp))

        return res


x = Xouba(3)
while True:
    x.cycle()
