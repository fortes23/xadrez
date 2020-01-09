#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess


import chess

board = chess.Board()

print("Starting to work...\n")

proc1 = subprocess.Popen(['python3', './bots/randombot.py'],
                         stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)

proc2 = subprocess.Popen(['python3', './bots/randombot.py'],
                         stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)

while not board.is_game_over():
    print(board)
    fen = board.fen() + '\n'

    if board.turn:
        proc = proc1
    else:
        proc = proc2

    os.write(proc.stdin.fileno(), fen.encode())
    outs = os.read(proc.stdout.fileno(), 4096)
    errs = os.read(proc.stderr.fileno(), 4096)

    move = outs.decode('utf-8').replace('\n', '')

    print(move)
    print(errs)
    board.push_uci(move)
