import numpy as np
import os
import random
import time

board = np.array(
    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]
     ]
)
win = 0


def print_title():
    """Clears the terminal screen and prints the stylized title."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print('  _______         ______              ______         \n /_  __(_)____   /_  __/___ ______   /_  __/___  ___ \n  / / / / ___/    / / / __ `/ ___/    / / / __ \\/ _ \\\n / / / / /__     / / / /_/ / /__     / / / /_/ /  __/\n/_/ /_/\\___/    /_/  \\__,_/\\___/    /_/  \\____/\\___/ \n                                                     \n')


def print_board():
    """Prints the current state of the board using X's and O's."""
    print_title()
    board_str = "+---+---+---+\n"
    for row in board:
        for i in range(3):
            board_str += f"| {' XO'[row[i]]} "
        board_str += "|\n+---+---+---+\n"
    print(board_str)


def check_win(brd):
    """Checks the board for a winning state.

    Args:
        brd (numpy.array): A 3x3 numpy array containing the board data.

    Returns:
        An int describing the state of the board. A return value of 1 or 2 indicates a win for the corresponding player; -1 indicates a draw; 0 indicates no win or draw.
    """
    for i in range(3):
        row = brd[i]
        col = brd[:, i]
        # check horizontals
        if row[0] == row[1] == row[2] and row[0] != 0:
            return row[0]
        # check verticals
        if col[0] == col[1] == col[2] and col[0] != 0:
            return col[0]
    # check diagonals
    if (brd[0, 0] == brd[1, 1] == brd[2, 2] or brd[2, 0] == brd[1, 1] == brd[0, 2]) and brd[1, 1] != 0:
        return brd[1, 1]
    # if the brd is filled, the result is a draw
    return 0 if 0 in brd else -1


def pot_win(brd, p_range=[2, 1]):
    """Checks the board for a potential win on the next turn. 

    Args:
        brd (numpy.array): A 3x3 numpy array containing the board data.
        p_range (list, optional): The range and order of corresponding players to check over. Defaults to [2, 1].

    Returns:
        A set of tuples, each of which is a 2d array index for a win solution.
    """
    pot_solutions = set()
    for p in p_range:
        for i in range(3):
            row = brd[i]
            col = brd[:, i]
            for j in range(3):
                # check for horizontal
                if (row[j] == row[j-1]) and (row[j] == p) and (col[j] != 0):
                    pot_solutions.add((i, (j+1) % 3))
                # check for vertical
                if (col[j] == col[j-1]) and (col[j] == p) and (col[j] != 0):
                    pot_solutions.add(((j+1) % 3, i))
        for i in range(3):
            # check for \ diagonal
            if (brd[i, i] == brd[i-1, i-1]) and (brd[i, i] == p) and (brd[i, i] != 0):
                pot_solutions.add(((i+1) % 3, (i+1) % 3))
            # check for / diagonal
            if (brd[0, 2] == brd[2, 0]) and (brd[0, 2] == p) and (brd[0, 2] != 0):
                pot_solutions.add((1, 1))
            elif (brd[1, 1] == brd[0, 2]) and (brd[1, 1] == p) and (brd[1, 1] != 0):
                pot_solutions.add((2, 0))
            elif (brd[1, 1] == brd[2, 0]) and (brd[1, 1] == p) and (brd[1, 1] != 0):
                pot_solutions.add((0, 2))
    solutions = set()
    for s in pot_solutions:
        if board[s] == 0:
            solutions.add(s)
    return solutions


def pot_fork(brd):
    """Checks the board for a potential fork on the next turn first for the AI and then for the player.

    Args:
        board (numpy.array): A 3x3 numpy array containing the board data.

    Returns:
        A tuple containing a 2d array index corresponding to the ideal move for the AI to either create a fork for itself or block the player's fork. Returns an empty tuple if no such move exists.
    """
    for p in (2, 1):
        for i in range(3):
            for j in range(3):
                test_board = brd.copy()
                if test_board[i, j] == 0:
                    test_board[i, j] = p
                    if len(pot_win(test_board, p_range=[p])) >= 2:
                        return (i, j)
    return ()


def pot_corner(brd):
    """Checks the board for an empty corner to move into, checking for opposite corners and then defaulting to any empty corner.

    Args:
        brd (numpy.array): A 3x3 numpy array containing the board data.

    Returns:
        A tuple containing a 2d array index corresponding to the selected corner for the AI to move to. Returns an empty tuple if no such move exists.
    """
    corners = ((0, 0), (0, 2), (2, 2), (2, 0))
    empty_corners = []
    for c in corners:
        if brd[c] == 0:
            empty_corners.append(c)
    if empty_corners:
        # check for opposite corner
        for e in empty_corners:
            if board[corners[corners.index(e) - 2]] == 1:
                return e
        # check for empty corner
        return empty_corners[0]
    return ()


def pot_side(brd):
    """Checks the board for an empty side to move into.

    Args:
        brd (numpy.array): A 3x3 numpy array containing the board data.

    Returns:
        A tuple containing a 2d array index corresponding to the selected side to move into. Returns an empty tuple if no such move exists.
    """
    for s in ((0, 1), (1, 0), (1, 2), (2, 1)):
        if brd[s] == 0:
            return s
    return ()


def rand_move(brd):
    while True:
        ai_row, ai_col = random.randint(0, 2), random.randint(0, 2)
        if brd[ai_row, ai_col] == 0:
            return (ai_row, ai_col)


def main():
    mode = 0
    while not(mode in (1, 2, 3, 4)):
        print_title()
        try:
            mode = int(input(
                "Choose a mode to play\n1. Player vs. AI (easy)\n2. Player vs. AI (medium)\n3. Player vs. AI (hard)\n4. Player vs. AI (insane) \n5. Player vs. Player\n\n> "))
        except ValueError:
            input("Please enter 1/2/3/4")
    turn = 1
    while not(win := check_win(board)):
        print_board()
        if turn == 1 or mode == 5:
            try:
                usr_in = int(
                    input(f"{' XO'[turn]}, enter 1-9 to move\n\n> ")) - 1
                if 0 <= usr_in < 9:
                    row = int(usr_in / 3)
                    col = usr_in % 3
                    if board[row, col] == 0:
                        board[row, col] = turn
                        turn = 2 if turn == 1 else 1
            except ValueError:
                print("Invalid move")
                time.sleep(2)
        else:
            print("O (AI) is thinking...")
            pw = pot_win(board)
            pf = pot_fork(board)
            pc = pot_corner(board)
            ps = pot_side(board)
            if mode == 1:
                board[rand_move] = 2
            else:
                if pw:
                    board[pw[0]] = 2
                elif pf and mode == 4:
                    board[pf] = 2
                elif board[1, 1] == 0:
                    board[1, 1] = 2
                elif pc and mode == 3:
                    board[pc] = 2
                elif ps:
                    board[ps] = 2
                else:
                    board[rand_move] = 2
            turn = 1
            time.sleep(0.5)
    print_title()
    print_board()
    if win > 0:
        print(f"{' XO'[win]} wins!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
