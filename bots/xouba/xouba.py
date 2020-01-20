#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

import chess

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../xadrez')

from fish import Fish  # noqa: E402


class Xouba(Fish):
    def __init__(self, json_file, depth):
        super().__init__(depth, "Starting xouba!")

        with open(json_file, "r") as f:
            jsf = json.load(f)
            self.weight_pieces = jsf

    def get_weigth_piece(self, name, pos):
        return self.weight_pieces[name]['wmat'] + self.weight_pieces[name]['wpos'][pos]

    def eval_fn(self, board):
        res = 0
        for p in chess.PIECE_TYPES:
            for wp in board.pieces(p, chess.WHITE):
                res += self.get_weigth_piece(chess.piece_symbol(p), wp)
            for bp in board.pieces(p, chess.BLACK):
                res -= self.get_weigth_piece(chess.piece_symbol(p), chess.square_mirror(bp))

        return res


x = Xouba(os.path.dirname(os.path.realpath(__file__)) + '/xouba.json', 3)
while True:
    x.cycle()
