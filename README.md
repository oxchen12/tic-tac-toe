# tic-tac-toe
A simple CLI tic tac toe game with multiple game modes.

## Strategy
Using this <a href="https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy">strategy</a> (credited to Newell and Simon's 1972 tic-tac-toe program), a player can guarantee at least a draw. The AI modes use this strategy to varying degrees.

## Mode 1: Player vs. AI (easy)
This AI selects a random unoccupied position to move to.

## Mode 2: Player vs. AI (medium)
This AI uses the **Win**, **Block**, **Center**, and **Empty Side** strategies. If none of these strategies work, it selects a random unoccupied position to move to.

## Mode 3: Player vs. AI (hard)
This AI uses the **Win**, **Block**, **Center**, **Opposite Corner**, **Empty Corner**, and **Empty Side** strategies. If none of these strategies work, it selects a random unoccupied position to move to.

## Mode 4: Player vs. AI (insane)
This AI uses all of the strategies, guaranteeing at least a draw.

## Mode 5: Player vs. Player
Two players each take control of "X" and "O" and take turns against each other.

## Other Notes
* Title text was generated using the `pyfiglet` package