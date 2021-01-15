import numpy as np
import os
import random
import re
import time

board = np.array(
    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]
     ]
)
win = 0


def print_title():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print('  _______         ______              ______         \n /_  __(_)____   /_  __/___ ______   /_  __/___  ___ \n  / / / / ___/    / / / __ `/ ___/    / / / __ \\/ _ \\\n / / / / /__     / / / /_/ / /__     / / / /_/ /  __/\n/_/ /_/\\___/    /_/  \\__,_/\\___/    /_/  \\____/\\___/ \n                                                     \n')


def print_board():
    print_title()
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


def check_win():
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


def potential_win():
    for i in range(3):
        row = board[i]
        col = board[:, i]
        for j in range(3):
            # check for horizontal
            if row[j] == row[j-1] != 0:
                return [i, j+1 if j != 2 else 0]
            # check for vertical
            if col[j] == col[j-1] != 0:
                return [j+1 if j != 2 else 0, i]
    for i in range(3):
        # check for \ diagonal
        if board[i][i] == board[i-1][i-1] != 0:
            pos = i+1 if i != 2 else 0
            return [pos, pos]
        # check for / diagonal
        if board[0][2] == board[2][0] != 0:
            return [1, 1]
        elif board[1][1] == board[0][2] != 0:
            return [2, 0]
        elif board[1][1] == board[2][0] != 0:
            return [0, 2]
    return [-1, -1]


def main():
    mode = 0
    print_title()
    while not(mode in (1, 2, 3)):
        try:
            mode = int(input(
                "Choose a mode to play\n1. Player vs. AI (easy)\n2. Player vs. AI (unbeatable)\n3. Player vs. Player\n\n> "))
        except ValueError as e:
            input("Please enter 1/2/3")
    turn = 1
    while not(win := check_win()):
        print_board()
        if turn == 1:
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
        else:
            print("O (AI) is thinking...")
            if mode == 1:
                while turn == 2:
                    ai_row, ai_col = random.randint(0, 2), random.randint(0, 2)
                    if board[ai_row][ai_col] == 0:
                        board[ai_row][ai_col] = 2
                        turn = 1
            else:
                # 1. Win: If the player has two in a row, they can place a third to get three in a row.
                # 2. Block: If the opponent has two in a row, the player must play the third themselves to block the opponent.
                pot_win = potential_win()
                if pot_win != [-1, -1]:
                    board[pot_win[0]][pot_win[1]] = 2
                # 3. Fork: Create an opportunity where the player has two ways to win (two non-blocked lines of 2).
                # 4. Blocking an opponent's fork: If there is only one possible fork for the opponent, the player should block it. Otherwise, the player should block all forks in any way that simultaneously allows them to create two in a row. Otherwise, the player should create a two in a row to force the opponent into defending, as long as it doesn't result in them creating a fork. For example, if "X" has two opposite corners and "O" has the center, "O" must not play a corner move in order to win. (Playing a corner move in this scenario creates a fork for "X" to win.)
                # elif potential_fork() != [-1, -1]:
                #     pass
                # 5. Center: A player marks the center. (If it is the first move of the game, playing a corner move gives the second player more opportunities to make a mistake and may therefore be the better choice; however, it makes no difference between perfect players.)
                elif board[1][1] == 0:
                    board[1][1] = 2
                # 6. Opposite corner: If the opponent is in the corner, the player plays the opposite corner.
                # elif opposite_corner():
                #     pass
                # 7. Empty corner: The player plays in a corner square.

                # 8. Empty side: The player plays in a middle square on any of the 4 sides.
                turn = 1
            time.sleep(2)
    print_title()
    print_board()
    if win > 0:
        print(f"{' XO'[win]} wins!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
