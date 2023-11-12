import itertools
import os

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
                        grid_line.append(char)
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
    expanded_grid = [['0' for i in range(expanded_width)] for i in range(expanded_height)]

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
    def __init__(self, block_type, position):
        """
        Initializes a new instance of the Block class.

        Parameters:
        block_type : str
            The type of the block, which can be 'A' for reflect block,
            'B' for opaque block, or 'C' for refract block.
        position : tuple of int
            The (x, y) coordinates of the block on the grid.
        """
        self.block_type = block_type # 'A' for reflect, 'B' for opaque, 'C' for refract
        self.position = position

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

def meet_block(grid, lazor, blocks_dict):
    """
    Check if the Lazor interacts with a block by checking both horizontally and vertically adjacent points.
    """
    x, y = lazor.position
    dx, dy = lazor.direction
    new_Lazors = []

    # Check both adjacent points
    adjacent_positions = [(x + dx, y), (x, y + dy)]
    for position in adjacent_positions:
        if position in blocks_dict:
            block = blocks_dict[position]
            print(block.block_type)
            interaction_result = block.interact_with_Lazor(lazor.position, lazor.direction)
            if interaction_result is None:
                # Return a Lazor with no direction change (stopped)
                return []
            
            if interaction_result:
                if isinstance(interaction_result, list):
                    # If the block is refractive, it creates multiple new Lazors
                    for new_direction in interaction_result:
                        new_Lazors.append(Lazor(lazor.position, new_direction))
                else:
                    # For a reflective block, change the direction
                    new_Lazors.append(Lazor(lazor.position, interaction_result))
                break  # If we interact with a block, we don't check the other point

    if not new_Lazors:
        # If no block interaction, the Lazor continues in the same direction
        new_Lazors.append(Lazor(lazor.position, lazor.direction))

    return new_Lazors

def generate_possible_grids(initial_grid, block_dict):
    empty_positions = [(x, y) for y in range(len(initial_grid)) 
                             for x in range(len(initial_grid[0])) 
                             if initial_grid[y][x] == 'o']

    block_types = sorted([b for b, count in block_dict.items() for i in range(count)])
    total_blocks = len(block_types)

    result_grids = []
    for positions in itertools.combinations(empty_positions, total_blocks):
        for block_order in set(itertools.permutations(block_types, total_blocks)):
            new_grid = [row[:] for row in initial_grid]
            for position, block_type in zip(positions, block_order):
                x, y = position
                new_grid[y][x] = block_type
            result_grids.append(new_grid)

    return result_grids


def pos_chk(grid, Lazor):
    '''
    This function is used to check if the lazor is inside the grid

    **Parameters:**

        grid:*list,list,string*
            The grid contains a list of lists that can represent the grid

    **Returns**

        True if the lazer is out of the grid
    '''

    grid_size = (len(grid[0]), len(grid))

    return (Lazor.position[0] < 0 or Lazor.position[0] >= grid_size[0] or
            Lazor.position[1] < 0 or Lazor.position[1] >= grid_size[1])
def simulate(grid, Lazors, blocks):

    # Store the original state of each Lazor
    original_states = [(lazor.position, lazor.direction) for lazor in Lazors]

    # Function to reset Lazors to their original states
    def reset_Lazors():
        for i, lazor in enumerate(Lazors):
            orig_pos, orig_dir = original_states[i]
            lazor.position = orig_pos
            lazor.direction = orig_dir

    # 将方块转换为字典，以方便检索
    blocks_dict = {block.position: block for block in blocks}

    # 存储活跃的激光
    active_Lazors = Lazors.copy()

    # Initialize the set for storing Lazor positions that hit targets
    hit_targets = set()

        # Initial block interaction check for each Lazor at starting position
    new_Lazors = []
    for lazor in active_Lazors:
        interaction_results = meet_block(grid, lazor, blocks_dict)
        for result in interaction_results:
            if not pos_chk(grid, result):
                new_Lazors.append(result)
    active_Lazors = new_Lazors

    while active_Lazors:
        new_Lazors = []  # To store Lazors for the next iteration

        for lazor in active_Lazors:
            # Move the Lazor
            lazor.move()

            # Check if Lazor is out of the grid
            if pos_chk(grid, lazor):
                continue  # Skip to the next Lazor

            # Block interaction check after moving
            interaction_results = meet_block(grid, lazor, blocks_dict)
            for result in interaction_results:
                if not pos_chk(grid, result):
                    new_Lazors.append(result)

                    # Check if Lazor hits a target
                    if grid[result.position[1]][result.position[0]] == 't':  
                        hit_targets.add(result.position)

        active_Lazors = new_Lazors

    # After simulation, reset Lazors to their original states
    reset_Lazors()

    if hit_targets:
        print('*',hit_targets)

    return hit_targets

def solve(grids, lazors, targets, blocks, name):
    for grid in grids:
        expanded_grid = expand_grid(grid, targets)
        blocks_list = []
        for y, row in enumerate(expanded_grid):
            for x, value in enumerate(row):
                if value in 'ABC':
                # If it belongs to one of A、B、C ，we new one Block bject
                    block = Block(value, (x, y))
                    blocks_list.append(block)
        # print(blocks_list)
        passed_targets = simulate(expanded_grid, lazors, blocks_list)
        if targets == passed_targets:
            save_grid_as_text(grid, name)
            break

def save_grid_as_text(grid, filename):
    with open(filename, 'w') as file:
        for row in grid:
            file.write(' '.join(row) + '\n')

if __name__ == "__main__":                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    bff_file = "./Lazors/Lazor data/tiny_5.bff"  # replace with .bff file name
    name = os.path.basename(bff_file[:-4])
    grid, lazors, targets, blocks = read_bff_file(bff_file)
    grids = generate_possible_grids(grid, blocks)
    solve(grids, lazors, targets, blocks, name)