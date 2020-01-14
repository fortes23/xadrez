#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random

import chess


def debug(msg):
    print(msg, file=sys.stderr)


debug("BF bot starting!\n")


weight_pieces = {
    'p': 1,
    'n': 3,
    'b': 3,
    'r': 5,
    'q': 9,
    'k': 90
}


def get_piece_val(board, sq):
    p = board.piece_at(sq)
    if p:
        if p.color:
            return weight_pieces[str(p).lower()]
        else:
            return -weight_pieces[str(p).lower()]
    return 0


def eval_fn(board):
    res = 0
    for sq in chess.SQUARES:
        res += get_piece_val(board, sq)
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
