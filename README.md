# tic-tac-toe
A simple CLI tic tac toe game with multiple game modes.

## Strategy
Using this <a href="https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy">strategy</a> (credited to Newell and Simon's 1972 tic-tac-toe program), a player can guarantee at least a draw. The AI modes use this strategy to varying degrees. The strategy is executed by consistently choosing the first available of 8 substrategies:

1. **Win**: If the player has two in a row, they can place a third to get three in a row.
2. **Block**: If the opponent has two in a row, the player must play the third themselves to block the opponent.
3. **Fork**: Create an opportunity where the player has two ways to win (two non-blocked lines of 2).
4. **Blocking an opponent's fork**: If there is only one possible fork for the opponent, the player should block it. Otherwise, the player should block all forks in any way that simultaneously allows them to create two in a row. 
5. **Center**: A player marks the center.
6. **Opposite Corner**: If the opponent is in the corner, the player plays the opposite corner.
7. **Empty Corner**: The player plays in a corner square.
8. **Empty Side**: The player plays in a middle square on any of the 4 sides.

## Mode 1: Player vs. AI (easy)
This AI selects a random unoccupied position to move to.

## Mode 2: Player vs. AI (medium)
This AI uses the **Win**, **Block**, **Center**, and **Empty Side** substrategies. If none of these strategies work, it selects a random unoccupied position to move to.

## Mode 3: Player vs. AI (hard)
This AI uses the **Win**, **Block**, **Center**, **Opposite Corner**, **Empty Corner**, and **Empty Side** substrategies. If none of these strategies work, it selects a random unoccupied position to move to.

## Mode 4: Player vs. AI (insane)
This AI uses all of the strategies, guaranteeing at least a draw.

## Mode 5: Player vs. Player
Two players each take control of "X" and "O" and take turns against each other.

## Other Notes
* Title text was generated using the `pyfiglet` package