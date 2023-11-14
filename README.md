# Lazors
&ensp;&ensp;This is the Lazor project for EN.540.635 Software Farpentry FA2023 <br>
&ensp;&ensp;Collaborators: Wen Zhang; Xinglin Chen; Ziyi Wang

## Idea of Solution
### Version 1
#### Algorithm
&ensp;&ensp;Iterate every possible combination of blocks to find the solution.

#### Input
&ensp;&ensp;read the bff file and convert it into variables for further calculation.<br>
&ensp;&ensp;In the expanded grid:   
&ensp;&ensp;&ensp;&ensp;(2k+1, 2m+1) points represent the position of blocks.<br>
&ensp;&ensp;&ensp;&ensp;(2k, 2m+1) and (2m+1, 2k) represent the points where the lazor starts, ends or interacts with the blocks. <br>

#### Process
&ensp;&ensp;According to the input gird and blocks, we calculate all the possible positions and order to place blocks. 
Then store the results for further interation.<br>
&ensp;&ensp;For each combination, we put blocks into the grid, then simulate the lazor path and check whether all the targets have been hit.    
&ensp;&ensp;If we hit all the targets, return the result; otherwise try the next combination of blocks.

#### Output
&ensp;&ensp;A txt file which resembles the input grid but contains the solution of positions of blocks.

#### Test Results
&ensp;&ensp;Using iteration, we can solve all the questions correctly. Most of the questions can be solve in less than 1min. 
However, in the yarn_5 question, this program takes more than 3min to find the right solution. 
This is probably results from the complex of block combination with following complicated simulation process.

### Version 2
#### Algorithm
&ensp;&ensp;Deep Search First   

#### Input
&ensp;&ensp;Same as the previous version.
#### Process

#### Output

#### Test Results



