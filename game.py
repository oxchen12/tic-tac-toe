import numpy as np
import os
import re

board = np.array(
    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]
     ]
)
win = 0


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def printtitle():
    print('  _______         ______              ______         \n /_  __(_)____   /_  __/___ ______   /_  __/___  ___ \n  / / / / ___/    / / / __ `/ ___/    / / / __ \\/ _ \\\n / / / / /__     / / / /_/ / /__     / / / /_/ /  __/\n/_/ /_/\\___/    /_/  \\__,_/\\___/    /_/  \\____/\\___/ \n                                                     \n')


def printboard():
    clear()
    printtitle()
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
        if row[0] == row[1] == row[2] and row[0] != 0:
            return row[0]
    # check verticals
    for col in board.T:
        if col[0] == col[1] == col[2] and col[0] != 0:
            return col[0]
    # check \ diagonal
    if (board[0][0] == board[1][1] == board[2][2] or board[2][0] == board[1][1] == board[0][2]) and board[1][1] != 0:
        return board[1][1]
    return 0 if 0 in board else -1


def main():
    printtitle()
    while usr_mode_in := input("Choose a mode to play\n1. Player vs. AI (easy)\n2. Player vs. AI (unbeatable)\n3. Player vs. Player"):
        pass
    turn = 1
    while not(win := winner()):
        clear()
        printboard()
        if multiplayer:
            pass
        usr_in = input(
            f"{' XO'[turn]}, enter row (t/m/b) and column (l/c/r) with no spaces\n> ").lower().strip()
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
    if win > 0:
        print(f"{' XO'[win]} wins!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
