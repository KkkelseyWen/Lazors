#import libraries here

def read_bff_file(filename):
   
    grid = []
    blocks = {'A': 0, 'B': 0, 'C': 0}  # initialize block counts
    lazors = []
    targets = set()

    with open(filename, 'r') as file:
        lines = file.readlines()
        read_grid = False

        for line in lines:
            line = line.strip()
            if 'GRID START' in line:
                read_grid = True
                continue
            if 'GRID STOP' in line:
                read_grid = False
                continue

            if read_grid:
                # Use Block object or None to replace characters
                grid_line = []
                for x, char in enumerate(line):
                    if char == 'o':
                        grid_line.append('o')
                    elif char == 'x':
                        grid_line.append('x')
                    elif char in 'ABC':
                        # If it belongs to one of A、B、C ，we new one Block bject
                        block = Block(char, (2*(len(grid) - 1), 2*x+1), fixed=True)
                        grid_line.append(block.block_type)
                grid.append(grid_line)
            elif line.startswith('A ') or line.startswith('B ') or line.startswith('C '):
                block_type, count = line.split()
                blocks[block_type] = int(count)
            elif line.startswith('L '):
                parts = line.split()
                position = (int(parts[1]), int(parts[2]))
                direction = (int(parts[3]), int(parts[4]))
                lazors.append(Lazor(position, direction))
            elif line.startswith('P '):
                parts = line.split()
                position = (int(parts[1]), int(parts[2]))
                targets.add(position)

    return grid, lazors, targets, blocks

def expand_grid(raw_grid, targets):
    # 计算扩展后的网格大小
    expanded_height = len(raw_grid) * 2 + 1
    expanded_width = len(raw_grid[0]) * 2 + 1

    # 创建扩展网格，默认值为0
    expanded_grid = [[0 for i in range(expanded_width)] for i in range(expanded_height)]

    # 映射原始网格到扩展网格
    for y, row in enumerate(raw_grid):
        for x, value in enumerate(row):
            # 计算扩展网格上的中心点坐标
            center_y = 2 * y + 1
            center_x = 2 * x + 1
            
            # 根据原始网格的值填充扩展网格的中心点
            if value == 'o':
                expanded_grid[center_y][center_x] = 'o'
            elif value == 'x':
                expanded_grid[center_y][center_x] = 'x'
            elif value == 'A':
                expanded_grid[center_y][center_x] = 'A'
            elif value == 'B':
                expanded_grid[center_y][center_x] = 'B'
            elif value == 'C':
                expanded_grid[center_y][center_x] = 'C'
    
    for xt, yt in targets:
        expanded_grid[yt][xt] = 't'

    return expanded_grid

# Define the Block class
class Block:
    def __init__(self, block_type, position, fixed=False):
        """
        Initializes a new instance of the Block class.

        Parameters:
        block_type : str
            The type of the block, which can be 'A' for reflect block,
            'B' for opaque block, or 'C' for refract block.
        position : tuple of int
            The (x, y) coordinates of the block on the grid.
        fixed : boolean
            Whether the block is fixed on grid or not.
        """
        self.block_type = block_type # 'A' for reflect, 'B' for opaque, 'C' for refract
        self.position = position
        self.fixed = fixed

    def interact_with_Lazor(self, Lazor_position, Lazor_direction):
        # Determine which direction the Lazor came from
        # Based on the Grid design, we think that the center is in odd coordinates and the edge is in even coordinates
        x_in = (Lazor_position[0] % 2 == 0)
        y_in = (Lazor_position[1] % 2 == 0)

        # Interact with Lazor based on Block type
        if self.block_type == 'A':  # reflect
            if x_in and not y_in:
                # The Lazor enters from left or right
                return (-Lazor_direction[0], Lazor_direction[1])
            elif y_in and not x_in:
                # The Lazor comes in from above or below
                return (Lazor_direction[0], -Lazor_direction[1])
        elif self.block_type == 'C':  # refract
            # The refracted Lazor keeps the direction unchanged and adds a reflection direction
            if x_in and not y_in:
                return [(Lazor_direction[0], Lazor_direction[1]), (-Lazor_direction[0], Lazor_direction[1])]
            elif y_in and not x_in:
                return [(Lazor_direction[0], Lazor_direction[1]), (Lazor_direction[0], -Lazor_direction[1])]
        # For other types of blocks, or if the Lazor is absorbed, return None
        return None
        
class Lazor:
    
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def move(self):
        # Move the Lazor to the next position based on its direction
        self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

def meet_block(grid, Lazor, blocks):
    """
    Check if the Lazor interacts with a block by checking both horizontally and vertically adjacent points.
    """
    x, y = Lazor.position
    dx, dy = Lazor.direction
    new_Lazors = []

    # Check both adjacent points
    adjacent_positions = [(x + dx, y), (x, y + dy)]
    for position in adjacent_positions:
        if position in blocks:
            block = blocks[position]
            interaction_result = block.interact_with_Lazor(Lazor.position, Lazor.direction)
            
            if interaction_result:
                if isinstance(interaction_result, list):
                    # If the block is refractive, it creates multiple new Lazors
                    for new_direction in interaction_result:
                        new_Lazors.append(Lazor(Lazor.position, new_direction))
                else:
                    # For a reflective block, change the direction
                    new_Lazors.append(Lazor(Lazor.position, interaction_result))
                break  # If we interact with a block, we don't check the other point

    if not new_Lazors:
        # If no block interaction, the Lazor continues in the same direction
        new_Lazors.append(Lazor(Lazor.position, Lazor.direction))

    return new_Lazors

def pos_chk(grid, Lazor):
    '''
    This function is used to check if the lazor and its next step
    is inside the grid, if it is not, return to the last step.

    **Parameters:**

        grid:*list,list,string*
            The grid contains a list of lists that can represent the grid

    **Returns**

        True if the lazer is still in the grid
    '''

    grid_size = (len(grid[0]), len(grid))

    return 0 <= Lazor.position[0] < grid_size[0] and 0 <= Lazor.position[1] < grid_size[1]

def simulate(grid, Lazors, blocks):
    """
    Simulate the movement of Lazors through a grid with blocks.
    
    Parameters:
    grid : list of list of int
        The grid representation, where numbers indicate different entities (0 for empty, 1 for block, etc.)
    Lazors : list of Lazor
        The Lazors present in the grid at the start of simulation.
    blocks : list of Block
        The blocks present in the grid that can interact with the Lazors.
        
    Returns:
    list of tuple
        The positions of Lazors that hit target points.
    """
    # Define the grid size
    grid_size = (len(grid[0]), len(grid))
    
    # Convert the list of blocks to a dictionary for easy access
    block_dict = {block.position: block for block in blocks}
    print(block_dict)
    # Initialize the set for storing Lazor positions that hit targets
    hit_targets = set()
    
    # Loop until there are no more Lazors to simulate
    while Lazors:
        new_Lazors = []
        for Lazor in Lazors:
            # Move the Lazor one step
            Lazor.move()
            
            # Check if Lazor is out of bounds and skip if it is
            if pos_chk(grid, Lazor):
                continue
            
            # Check if the Lazor hits a target point
            if grid[Lazor.position[1]][Lazor.position[0]] == 't':
                hit_targets.add(Lazor.position)
                continue  # Lazor stops if it hits a target point
            
            # Check if the Lazor hits a block
            new_Lazors = meet_block(grid, Lazor, blocks)
                    
        # Update the Lazors for the next iteration
        Lazors = new_Lazors
    
    # Return the positions of Lazors that hit target points
    return hit_targets

'''记录一下想到的，simulate()会返回目前光路经过的目标点的集合。
现在还至少需要两个函数， 一个solve()，其中targets == hit_targests时问题解决，循环停止。
另一个函数写着写着忘了，大致应该是在solve()中涉及block怎么放的问题的。
哦还会有一个save结果的，保存类型还要商量下，现在空想一下光路不太好保存，保存grid的话应该很简单，但是也得需要block放完记录一下。
'''


if __name__ == "__main__":                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    bff_file = "./Lazors/Lazor data/tiny_5.bff"  # replace with your .bff file name
    # print(read_bff_file(bff_file))
    grid, lazors, targets, blocks = read_bff_file(bff_file)
    # print(expand_grid(grid, targets))
    print(blocks)
    print(lazors[0].position)
    print(targets)
    expanded_grid = expand_grid(grid, targets)
    # print(meet_block(expanded_grid,lazors[0],blocks)[0].position)
    # print(simulate_Lazor_movement(grid, lazors[0], targets, blocks))
    # main(bff_file)
