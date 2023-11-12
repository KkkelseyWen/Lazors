# Lazors
&ensp;&ensp;This is the Lazor project for EN.540.635 Software Farpentry FA2023 <br>
&ensp;&ensp;Collaborators: Wen Zhang; Xinglin Chen; Ziyi Wang

## Idea of Solution
### Algorithm
&ensp;&ensp;Iterate every possible combination of blocks to find the solution.   


### Input
&ensp;&ensp;read the bff file and convert it into variables for further calculation.<br>

&ensp;&ensp;(2k+1, 2m+1) points represent the position of blocks.<br>
&ensp;&ensp;(2k, 2m+1) and (2m+1, 2k) represent the points where the lazor starts, ends or interacts with the blocks. <br>

### Process
&ensp;&ensp;According to the input gird and blocks,calculate all the possible positions and order to place blocks.<br>
&ensp;&ensp;For each combination, calculate the lazor path and check whether all the targets have been hit.

### Output
&ensp;&ensp;A txt file which resembles the input grid but contains the position of all the blocks.


