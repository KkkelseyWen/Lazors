# Lazors Project

This repository contains the Lazor project developed for EN.540.635 Software Carpentry FA2023.

## Collaborators
- Wen Zhang (KkkelseyWen): wzhan156@jh.edu
- Xinglin Chen (WalkingWithClouds): xchen255@jh.edu
- Ziyi Wang (sweetziyi): zwang412@jh.edu

## Background
&ensp;&ensp;Lazors is a puzzle game of lasers and mirrors in which players need to arrange blocks wisely to hit all
the targets. It offers more than a hundred levels, ranging from easy distractions to hard challenges.
   
&ensp;&ensp;This game is available on [Steam](https://steamcommunity.com/app/341290), 
[Google Play](https://play.google.com/store/apps/details?id=net.pyrosphere.lazors&hl=en&pli=1) 
and [Apple Store](https://apps.apple.com/us/app/lazors/id386458926).

## Project Overview

&ensp;&ensp;The Lazors project aims find solutions to specified lazor puzzles.

### How to use it?
&ensp;&ensp;Get the .bff file which represents the puzzle and put it into the program to generate a solution.
A standard .bff file contains the following information:
```
GRID START
o   o   o   o
o   o   o   o
o   o   o   o
o   o   o   o
GRID STOP

A 2
C 1

L 2 7 1 -1

P 3 0
P 4 3
P 2 5
P 4 7
```
- For the **GRID START** and **GRID STOP** part:    

&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;x = no block allowed   
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;o = blocks allowed   
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;A = fixed reflect block   
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;B= fixed opaque block   
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;C = fixed refract block  

- For the **Block** part:    

&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;A, B, C and their corresponding number represents 
the block types and numbers the players have to play with

- For the **Lazor** part:   
&ensp;&ensp;L 2 7 1 -1   
&ensp;&ensp;Each L stands for a lazor point    
&ensp;&ensp;The first 2 numbers symbolize the coordinates of lazor   
&ensp;&ensp;The last 2 numbers symbolize the directions    
&ensp;&ensp;Define direction 1:right/up;  -1:left/down


- For the **Target** part:
&ensp;&ensp;** To note**: They are marked as '?' in **Version2**.    
&ensp;&ensp;Each P stands for a target point    
&ensp;&ensp;The following numbers represent its coordinate    

The output txt in **Version1** looks as below:
```
A B A
o o o
A C o
```

The output txt in **Version2** looks as below:
```
Solution found for ./Lazor data/tiny_5.bff:
+-+-+-+
|A|B|A|
+?+-+-+
|o|o|o?
+-+-+-+
|A|C|o|
+-+-+-+
```
&ensp;&ensp;According to the solution file the program outputs, put you blocks as instructed,
then Bang! Problem Solved!

## Solutions
### Version 1

#### Algorithm
The core algorithm iterates through all possible block position combinations in the grid to identify the correct solution.

#### Input
- Reads `.bff` files and converts them into variables for processing.
- In the expanded grid:
  - (2k+1, 2m+1) points indicate block positions.
  - (2k, 2m+1) and (2m+1, 2k) points denote where the laser starts, ends, or interacts with blocks.

#### Process
- Calculates all possible block positions and orders based on the input grid and available blocks, storing results for iteration.
- For each block combination, the algorithm places blocks in the grid, simulates the laser path, and checks if all targets are hit.
- If all targets are hit, the solution is returned; otherwise, the next block combination is tried.

#### Output
- Generates a `.txt` file that displays the input grid with the solution for block positions.

#### Testing Results
- Iterative approach successfully solves all puzzles, typically in under a minute.
- Notably, the 'yarn_5' puzzle takes over 3 minutes due to complex block combinations and the subsequent intricate simulation process.


### Version 2
#### Algorithm
- The core algorithm is Depth-First Search (DFS) for exploring possible block placements. 
- Multi-threading is utilized in execution, allowing parallel processing of different puzzle configurations or simultaneous handling of multiple puzzles.

#### Input
- The same as the previous version of the puzzle, which includes a grid layout, available blocks, lasers, and required target points.

#### Process
- **Initialization**: The grid is initialized with positions marked as 'o', where blocks can be placed. Blocks ('A', 'B', 'C') are available in specified quantities.

- **Block Placement**:
  - The `Solver` class's solve method orchestrates the placement of blocks on the grid.  It uses a recursive approach to iteratively place blocks in empty positions and backtrack if necessary.
  - The `recursive_solve` method within the `Solver` class is the key to understanding the placement process.  It iterates through each empty position on the grid and tries placing different block types (or leaving it empty denoted by 'o').
  - The order in which blocks are placed is determined by the iteration over the block types in the line for block_type in 'ABCo':.  This means the algorithm tries placing an 'A' block first, then 'B', 'C', and finally considers leaving the position empty.
  - If a block type is chosen, the method updates the grid and the available block count, then recursively calls itself for the next position.
  - If no solution is found for a particular placement, the algorithm backtracks, which involves undoing the last placement and trying the next block type in the sequence.
  - The condition for a successful solution is when all lasers hit the required targets.

- **Laser Simulation**: After each block placement, the paths of lasers are simulated to check if they intersect with all target points.

- **Backtracking**: If a configuration fails (i.e., not all targets are hit), the algorithm backtracks by removing the last placed block and trying a different configuration.

- **Multi-threading Implementation**: The puzzle solver employs multi-threading to potentially solve multiple puzzles in parallel. This is useful for complex grids or multiple puzzle instances, improving performance and efficiency.
  
- **Recursive Solution Finding**: The solver uses a recursive method to navigate through the possible configurations, constantly checking against the laser path simulation to find a valid solution.

#### Output
- A list of tuples representing the placed blocks' types and positions, or None if no solution is found.
- Generates a `.txt` file that displays the input grid with the solution for block positions.

#### Test Results
- Successfully solve all puzzles, typically in under a minute.

### Runtime
| Runtime       |                 |                 |
| ------------- | --------------- | --------------- |
| **Level**        | **Version_1**       | **Version_2**       |
| dark_1        | < 15 sec | < 15 sec  |
| mad_1         | < 15 sec  | < 15 sec |
| mad_4         | < 15 sec  | < 15 sec  |
| mad_7         | around 1 min    | < 15 sec  |
| numbered_6    | < 15 sec  | < 15 sec  |
| showstopper_4 | < 15 sec  | < 15 sec  |
| tiny_5        | < 15 sec  | < 15 sec  |
| yarn_5        | 7-8 min         | < 15 sec  |


