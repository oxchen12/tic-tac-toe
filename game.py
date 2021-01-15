from pyfiglet import Figlet

import numpy as np
import os
import re

board = np.array(
    [[1, 0, 0],
     [0, 2, 0],
     [0, 0, 1]
     ]
)
turn = 1
win = 0


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def printboard():
    title = Figlet(font="slant").renderText("Tic Tac Toe")
    print(title)
    clear()
    board_str = "+---+---+---+\n"
    for row in board:
        for i in range(3):
            board_str += "| "
            if row[i] == 1:
                board_str += "X "
            elif row[i] == 2:
                board_str += "O "
            else:
                board_str += "  "
        board_str += "|\n+---+---+---+\n"
    print(board_str)


def main():
    while not(win):
        clear()
        printboard()
        usr_in = input(
            f"Player {turn}, enter row (t/m/b) and column (l/c/r) with no spaces\n>>> ").lower().strip()
        if re.match("[lcr][tmb]", usr_in):
            usr_in = usr_in[1] + usr_in[0]
        if re.match("[tmb][lcr]", usr_in):
            pass
        else:
            pass


if __name__ == "__main__":
    main()
