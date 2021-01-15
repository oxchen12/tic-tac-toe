from pyfiglet import Figlet

import numpy as np
import os
import re

board = np.array(
    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]
     ]
)
turn = 1


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


def winner():
    # check horizontals
    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]
    # check verticals
    for col in board.T:
        if col[0] == col[1] == col[2]:
            return col[0]
    # check \ diagonal
    if board[0][0] == board[1][1] == board[2][2] or board[2][0] == board[1][1] == board[0][2]:
        return board[1][1]
    return 0


def main():
    global turn
    while not(win := winner()):
        clear()
        printboard()
        usr_in = input(
            f"Player {turn}, enter row (t/m/b) and column (l/c/r) with no spaces\n>>> ").lower().strip()
        if re.match("[lcr][tmb]", usr_in):
            usr_in = usr_in[1] + usr_in[0]
        if re.match("[tmb][lcr]", usr_in):
            rows = {
                't': 0,
                'm': 1,
                'b': 2
            }
            cols = {
                'l': 0,
                'c': 1,
                'r': 2
            }
            row = rows[usr_in[0]]
            col = cols[usr_in[1]]
            if board[row][col] == 0:
                board[row][col] = turn
                turn = 2 if turn == 1 else 1
            else:
                pass
        else:
            pass


if __name__ == "__main__":
    main()
