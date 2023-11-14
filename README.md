# Lazors Project

This repository contains the Lazor project developed for EN.540.635 Software Carpentry FA2023.

## Collaborators
- Wen Zhang: wzhan156@jh.edu
- Xinglin Chen: xchen255@jh.edu
- Ziyi Wang: zwang412@jh.edu

## Background
Lazors is a puzzle game of lasers and mirrors in which players need to arrange blocks wisely to hit all
the targets. It offers more than a hundred levels, ranging from easy distractions to hard challenges.
   
This game is available on [Steam](https://steamcommunity.com/app/341290), 
[Google Play](https://play.google.com/store/apps/details?id=net.pyrosphere.lazors&hl=en&pli=1) 
and [Apple Store](https://apps.apple.com/us/app/lazors/id386458926).

## Project Overview

The Lazors project aims find solutions to specified lazor puzzles.

### How to use it?
Get the .bff file which represents the puzzle and put it into the program to generate a solution.
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
For the **GRID START** and **GRID STOP** part:  

x = no block allowed   
o = blocks allowed   
A = fixed reflect block   
B = fixed opaque block   
C = fixed refract block  

For the **Block** part:    

A, B, C and their corresponding number represents 
the block types and numbers the players have to play with

For the **Lazor** part:   
L 2 7 1 -1   
Each L stands for a lazor point    
The first 2 numbers symbolize the coordinates of lazor   
The last 2 numbers symbolize the directions    
Define direction 1:right/up;  -1:left/down

For the **Target** part:    
Each P stands for a target point  
The following numbers represent its coordinate

The output txt looks as below:
```
A B A
o o o
A C o
```
According to the solution file the program outputs, put you blocks as instructed,
then Bang! Problem Solved!

## Solutions
### Version 1

#### Algorithm
The core algorithm iterates through all possible block combinations to identify the correct solution.

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
&ensp;&ensp;Deep Search First   

#### Input
&ensp;&ensp;Same as the previous version.
#### Process

#### Output

#### Test Results



