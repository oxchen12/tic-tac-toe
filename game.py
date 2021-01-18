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
    """Clears the terminal screen and prints the stylied title."""
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


def check_win(brd, all=False):
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
    if (brd[0][0] == brd[1][1] == brd[2][2] or brd[2][0] == brd[1][1] == brd[0][2]) and brd[1][1] != 0:
        return brd[1][1]
    # if the brd is filled, the result is a draw
    return 0 if 0 in brd else -1


def potential_win(brd, p_range=[2, 1], all=False):
    """Checks the board for a potential win on the next turn. 

    Args:
        brd (numpy.array): A 3x3 numpy array containing the board data.
        p_range (list, optional): The range and order of corresponding players to check over. Defaults to [2, 1].
        all (bool, optional): Whether to return all solutions or just one. Defaults to False.

    Returns:
        [type]: [description]
    """
    solutions = []
    for p in p_range:
        for i in range(3):
            row = brd[i]
            col = brd[:, i]
            for j in range(3):
                # check for horizontal
                if row[j] == row[j-1] == p != 0:
                    solutions.append([i, j+1 if j != 2 else 0])
                # check for vertical
                if col[j] == col[j-1] == p != 0:
                    solutions.append([j+1 if j != 2 else 0, i])
        for i in range(3):
            # check for \ diagonal
            if brd[i][i] == brd[i-1][i-1] == p != 0:
                pos = i+1 if i != 2 else 0
                solutions.append([pos, pos])
            # check for / diagonal
            if brd[0][2] == brd[2][0] == p != 0:
                solutions.append([1, 1])
            elif brd[1][1] == brd[0][2] == p != 0:
                solutions.append([2, 0])
            elif brd[1][1] == brd[2][0] == p != 0:
                solutions.append([0, 2])
    return solutions if all else solutions[0]


def potential_fork(brd):
    """Checks the board for a potential fork on the next turn first for the AI and then for the player.

    Args:
        board (numpy.array): A 3x3 numpy array containing the board data.

    Returns:
        A list containing the board index corresponding to the ideal move for the AI to either create a fork for itself or block the player's fork. Returns an empty list if no such move exists.
    """
    for p in (2, 1):
        win_in_two = []
        for i in range(3):
            for j in range(3):
                test_board = brd.copy()
                if test_board[i][j] == 0:
                    test_board[i][j] = p
                    if potential_win(test_board, p_range=[p], all=True) != []:
                        win_in_two.append([i, j])
        if len(win_in_two) >= 2:
            return win_in_two[0]
    return []


def main():
    mode = 0
    while not(mode in (1, 2, 3)):
        print_title()
        try:
            mode = int(input(
                "Choose a mode to play\n1. Player vs. AI (easy)\n2. Player vs. AI (unbeatable)\n3. Player vs. Player\n\n> "))
        except ValueError:
            input("Please enter 1/2/3/4")
    turn = 1
    while not(win := check_win()):
        print_board()
        if turn == 1 or mode == 3:
            # usr_in = input(
            #     f"{' XO'[turn]}, enter row (t/m/b) and column (l/c/r) with no spaces\n> ").lower().strip()
            # if re.match("[lcr][tmb]", usr_in):
            #     usr_in = usr_in[1] + usr_in[0]
            # if re.match("[tmb][lcr]", usr_in):
            #     rows = {
            #         't': 0,
            #         'm': 1,
            #         'b': 2
            #     }
            #     cols = {
            #         'l': 0,
            #         'c': 1,
            #         'r': 2
            #     }
            #     row = rows[usr_in[0]]
            #     col = cols[usr_in[1]]
            #     if board[row][col] == 0:
            #         board[row][col] = turn
            #         turn = 2 if turn == 1 else 1
            try:
                usr_in = int(
                    input(f"{' XO'[turn]}, enter 1-9 to move\n\n> ")) - 1
                if 0 <= usr_in < 9:
                    row = int(usr_in / 3)
                    col = usr_in % 3
                    if board[row][col] == 0:
                        board[row][col] = turn
                        turn = 2 if turn == 1 else 1
            except ValueError:
                print("Invalid move")
                time.sleep(2)
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
                pot_win = potential_win(board)
                pot_fork = potential_fork(board)
                if pot_win:
                    board[pot_win[0]][pot_win[1]] = 2
                # 3. Fork: Create an opportunity where the player has two ways to win (two non-blocked lines of 2).
                # 4. Blocking an opponent's fork: If there is only one possible fork for the opponent, the player should block it. Otherwise, the player should block all forks in any way that simultaneously allows them to create two in a row. Otherwise, the player should create a two in a row to force the opponent into defending, as long as it doesn't result in them creating a fork. For example, if "X" has two opposite corners and "O" has the center, "O" must not play a corner move in order to win. (Playing a corner move in this scenario creates a fork for "X" to win.)
                elif pot_fork:
                    board[pot_fork[0]][pot_fork[1]] = 2
                # 5. Center: A player marks the center. (If it is the first move of the game, playing a corner move gives the second player more opportunities to make a mistake and may therefore be the better choice; however, it makes no difference between perfect players.)
                elif board[1][1] == 0:
                    board[1][1] = 2
                # 6. Opposite corner: If the opponent is in the corner, the player plays the opposite corner.
                # 7. Empty corner: The player plays in a corner square.
                elif not(board[0][0] and board[0][2] and board[2][0] and board[2][2]):
                    pass
                # 8. Empty side: The player plays in a middle square on any of the 4 sides.
                else:
                    if board[0][1] == 0:
                        board[0][1] = 2
                    elif board[1][0] == 0:
                        board[1][0] = 2
                    elif board[1][2] == 0:
                        board[1][2] = 2
                    else:
                        board[2][1] = 2
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
