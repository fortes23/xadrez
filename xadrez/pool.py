import os
import subprocess


import chess


class Pool():
    def __init__(self, bot1, bot2, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                 debug=False, print_board=False):
        self.RESULT_UNKNOWN = -1
        self.RESULT_DRAW = 0
        self.RESULT_WIN_WHITE = 1
        self.RESULT_WIN_BLACK = 2

        self.proc1 = subprocess.Popen(bot1,
                                      stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        self.proc2 = subprocess.Popen(bot2,
                                      stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        self.init_fen = fen
        self.board = chess.Board(fen)
        self.debug = debug
        self.print_board = print_board
        self.last_result = self.RESULT_UNKNOWN

    def __del__(self):
        self.proc1.kill()
        self.proc2.kill()

    def reset_chess_board(self, new_fen=None):
        if new_fen:
            self.board = chess.Board(new_fen)
        else:
            self.board = chess.Board(self.init_fen)

    def match(self):
        self.result = self.RESULT_UNKNOWN

        while not self.board.is_game_over():
            fen = self.board.fen() + '\n'

            if self.board.turn:
                proc = self.proc1
            else:
                proc = self.proc2

            os.write(proc.stdin.fileno(), fen.encode())
            outs = os.read(proc.stdout.fileno(), 4096)

            move = outs.decode('utf-8').replace('\n', '')
            print(move)

            if self.debug:
                errs = os.read(proc.stderr.fileno(), 4096)
                print(errs)

            self.board.push_uci(move)

            if self.print_board:
                print(self.board.unicode(invert_color=True))

        res = self.board.result()

        if res == "0-1":
            self.last_result = self.RESULT_WIN_BLACK
        elif res == "1-0":
            self.last_result = self.RESULT_WIN_WHITE
        elif res == "1/2-1/2":
            self.last_result = self.RESULT_DRAW

        print(res)
