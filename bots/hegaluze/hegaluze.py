#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import json

import chess


def debug(msg):
    print(msg, file=sys.stderr)


debug("Hegaluze bot starting!\n")

with open("bots/hegaluze/hegaluze.json", "r") as f:
    jsf = json.load(f)
    for k in jsf:
        debug("key: " + k)
    debug("pop name: {name}, ver: {version}, gen: {generation}".format_map(jsf))
    bot = jsf["population"][0]



def get_weigth_piece(name, pos):
    return bot["weight"][name][pos]


def eval_fn(board):
    res = 0
    for p in chess.PIECE_TYPES:
        for wp in board.pieces(p, chess.WHITE):
            res += get_weigth_piece(chess.piece_symbol(p), wp)
        for bp in board.pieces(p, chess.BLACK):
            res -= get_weigth_piece(chess.piece_symbol(p), chess.square_mirror(bp))

    return res


def minimax(board, depth, _maximize, alpha, beta):

    if board.is_checkmate():
        return ((-1)**_maximize * 10000, None)
    elif board.is_stalemate() or board.is_insufficient_material():
        return(0, None)

    if not depth:
        return (eval_fn(board), None)

    best_score = (-1)**_maximize * 9999999

    res = None
    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)
    for m in legal_moves:
        aux_b = board.copy()
        aux_b.push_uci(m.uci())
        sub_score = minimax(aux_b, depth-1, not _maximize, alpha, beta)[0]
        if _maximize:
            alpha = max(alpha, sub_score)
            sb = sub_score - best_score
        else:
            beta = min(beta, sub_score)
            sb = best_score - sub_score

        if sb > 0:
            best_score = sub_score
            res = m.uci()

        if alpha >= beta:
            break

    return (best_score, res)


while True:
    fen = input()
    board = chess.Board(fen=fen)

    debug("fen: " + board.fen())
    moves = list(board.legal_moves)

    # Get best movement
    (best, m) = minimax(board, 3, board.turn, -99999999, 99999999)
    debug(f"Best played {best}")

    print(m)
