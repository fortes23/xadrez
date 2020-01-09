import sys

import chess

def debug(msg):
    print(msg, file=sys.stderr)

def move(mov):
    if len(mov) !=4 or mov[0:2] not in chess.SQUARE_NAMES or mov[2:4] not in chess.SQUARE_NAMES:
        debug('Invalid uci move')
    else:
        print(mov)
