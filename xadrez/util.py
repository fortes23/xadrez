import sys
import random


def debug(msg):
    print(msg, file=sys.stderr)


def minimax(board, _maximize, alpha, beta, depth, eval_fn):

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
        sub_score = minimax(aux_b, not _maximize, alpha, beta, depth-1, eval_fn)[0]
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
