#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random

import chess


def debug(msg):
    print(msg, file=sys.stderr)


debug("BF bot starting!\n")

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

weight_pieces = {
    'p': {"mat": 10, "pos": pawn_weight_pos},
    'n': {"mat": 30, "pos": knights_weight_pos},
    'b': {"mat": 30, "pos": bishops_weight_pos},
    'r': {"mat": 50, "pos": rooks_weight_pos},
    'q': {"mat": 90, "pos": queens_weight_pos},
    'k': {"mat": 900, "pos": kings_weight_pos}
}


def get_weigth_piece(name, pos):
    return weight_pieces[name]['mat'] + weight_pieces[name]['pos'][pos]


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
