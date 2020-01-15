#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import subprocess


import chess


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--board', help='Show board', action='store_true')
    parser.add_argument('-d', '--debug', help='Show debug messages', action='store_true')
    _required = parser.add_argument_group('Required args')
    _required.add_argument('-b1', '--bot1', help='Executable bot 1',
                           action='store', required=True)
    _required.add_argument('-b2', '--bot2', help='Executable bot 2',
                           action='store', required=True)
    args = parser.parse_args()
    return args


def main():
    print("Starting to work...\n")
    args = parser_args()

    proc1 = subprocess.Popen([args.bot1],
                             stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    proc2 = subprocess.Popen([args.bot2],
                             stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    board = chess.Board()

    while not board.is_game_over():
        fen = board.fen() + '\n'

        if board.turn:
            proc = proc1
        else:
            proc = proc2

        os.write(proc.stdin.fileno(), fen.encode())
        outs = os.read(proc.stdout.fileno(), 4096)

        move = outs.decode('utf-8').replace('\n', '')
        print(move)
        board.push_uci(move)

        if args.debug:
            errs = os.read(proc.stderr.fileno(), 4096)
            print(errs)

        if args.board:
            print(board.unicode(invert_color=True))

    print(board.result())


if __name__ == '__main__':
    main()
