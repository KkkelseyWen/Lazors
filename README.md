# Lazors
This is the Lazor project for EN.540.635 Software Farpentry FA2023 <br>
Collaborators: Wen Zhang; Xinglin Chen; Ziyi Wang

## Idea of Solution
Algorithm:<br>
    Using deep first search (DFS) to find the solution

Imput:<br>
    read the bff file and convert it into a list.<br>
    (2k+1, 2m+1) points represent the position of blocks.<br>
    (2k, 2m+1) and (2m+1, 2k) represent the points where the lazor starts, ends or interacts with the blocks. <br>

Process:<br>
    according to the lazor position and direction, calculate all the possible positions to place blocks.<br>
    order to place blocks: A <rightarrow> C <rightarrow> B<br>
    place a block on a certain possible position, calculate new lazor path and direction, check if the lazor hits all the targets.<br>
    if we run out of A and C but do not hit all the target, pop the last block.<br>
    if the lazor hits all the target but there still remains blocks, calculate all the blocks without lazor then place the blocks in the order of B <rightarrow> C <rightarrow>A.<br>
    if there still have blocks left, put it in every possible position and check if the lazor still hits the target.

Output:
    a dictionary contains the position of all the blocks.


