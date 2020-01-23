#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from xadrez.pool import Pool


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--board', help='Show board', action='store_true')
    parser.add_argument('-d', '--debug', help='Enable debugging messages', action='store_true')
    parser.add_argument('-f', '--fen', help='Start from given position', action='store',
                        default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
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

    p = Pool(bot1=args.bot1, bot2=args.bot2, fen=args.fen,
             debug=args.debug, print_board=args.board)
    p.match()


if __name__ == '__main__':
    main()
