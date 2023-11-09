# Lazors
&ensp;&ensp;This is the Lazor project for EN.540.635 Software Farpentry FA2023 <br>
&ensp;&ensp;Collaborators: Wen Zhang; Xinglin Chen; Ziyi Wang

## Idea of Solution
**Algorithm**:<br>
&ensp;&ensp;Using deep first search (DFS) to find the solution

**Imput**:<br>
&ensp;&ensp;read the bff file and convert it into a list.<br>
&ensp;&ensp;(2k+1, 2m+1) points represent the position of blocks.<br>
&ensp;&ensp;(2k, 2m+1) and (2m+1, 2k) represent the points where the lazor starts, ends or interacts with the blocks. <br>

**Process**:<br>
&ensp;&ensp;according to the lazor position and direction, calculate all the possible positions to place blocks.<br>
&ensp;&ensp;order to place blocks: A $\rightarrow$ C $\rightarrow$ B<br>
&ensp;&ensp;place a block on a certain possible position, calculate new lazor path and direction, check if the lazor hits all the targets.<br>
&ensp;&ensp;if we run out of A and C but do not hit all the target, pop the last block.<br>
&ensp;&ensp;if the lazor hits all the target but there still remains blocks, calculate all the blocks without lazor then place the blocks in the order of B $\rightarrow$ C $\rightarrow$ A.<br>
&ensp;&ensp;if there still have blocks left, put it in every possible position and check if the lazor still hits the target.

**Output**:<br>
&ensp;&ensp;a dictionary contains the position of all the blocks.


