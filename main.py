#import libraries here

def read_bff_file(filename):
   
    grid = []
    blocks = {'A': 0, 'B': 0, 'C': 0}  # initialize block counts
    lasers = []
    targets = []

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
                        block = Block(char, (len(grid) - 1, x), fixed=True)
                        grid_line.append(block.block_type)
                grid.append(grid_line)
            elif line.startswith('A ') or line.startswith('B ') or line.startswith('C '):
                block_type, count = line.split()
                blocks[block_type] = int(count)
            elif line.startswith('L '):
                parts = line.split()
                position = (int(parts[1]), int(parts[2]))
                direction = (int(parts[3]), int(parts[4]))
                lasers.append(Laser(position, direction))
            elif line.startswith('P '):
                parts = line.split()
                position = (int(parts[1]), int(parts[2]))
                targets.append(position)

    return grid, lasers, targets, blocks

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
                expanded_grid[center_y][center_x] = 1
            elif value == 'x':
                expanded_grid[center_y][center_x] = 2
            elif value == 'A':
                expanded_grid[center_y][center_x] = 3
            elif value == 'B':
                expanded_grid[center_y][center_x] = 4
            elif value == 'C':
                expanded_grid[center_y][center_x] = 5
    
    for xt, yt in targets:
        expanded_grid[yt][xt] = 6

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

    def interact_with_laser(self, laser_position, laser_direction):
        # Determine which direction the laser came from
        # Based on the Grid design, we think that the center is in odd coordinates and the edge is in even coordinates
        x_in = (laser_position[0] % 2 == 0)
        y_in = (laser_position[1] % 2 == 0)

        # Interact with laser based on Block type
        if self.block_type == 'A':  # reflect
            if x_in and not y_in:
                # The laser enters from left or right
                return (-laser_direction[0], laser_direction[1])
            elif y_in and not x_in:
                # The laser comes in from above or below
                return (laser_direction[0], -laser_direction[1])
        elif self.block_type == 'C':  # refract
            # The refracted laser keeps the direction unchanged and adds a reflection direction
            if x_in and not y_in:
                return [(laser_direction[0], laser_direction[1]), (-laser_direction[0], laser_direction[1])]
            elif y_in and not x_in:
                return [(laser_direction[0], laser_direction[1]), (laser_direction[0], -laser_direction[1])]
        # For other types of blocks, or if the laser is absorbed, return None
        return None
        
class Laser:
    
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def move(self):
        # Move the laser to the next position based on its direction
        self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

def simulate(grid, lasers, blocks):
    """
    Simulate the movement of lasers through a grid with blocks.
    
    Parameters:
    grid : list of list of int
        The grid representation, where numbers indicate different entities (0 for empty, 1 for block, etc.)
    lasers : list of Laser
        The lasers present in the grid at the start of simulation.
    blocks : list of Block
        The blocks present in the grid that can interact with the lasers.
        
    Returns:
    list of tuple
        The positions of lasers that hit target points.
    """
    # Define the grid size
    grid_size = (len(grid[0]), len(grid))
    
    # Convert the list of blocks to a dictionary for easy access
    block_dict = {block.position: block for block in blocks}
    
    # Initialize the set for storing laser positions that hit targets
    hit_targets = set()
    
    # Loop until there are no more lasers to simulate
    while lasers:
        new_lasers = []
        for laser in lasers:
            # Move the laser one step
            laser.move()
            
            # Check if laser is out of bounds and skip if it is
            if not (0 <= laser.position[0] < grid_size[0] and 0 <= laser.position[1] < grid_size[1]):
                continue
            
            # Check if the laser hits a target point
            if grid[laser.position[1]][laser.position[0]] == 6:
                hit_targets.add(laser.position)
                continue  # Laser stops if it hits a target point
            
            # Check if the laser hits a block
            if laser.position in block_dict:
                block = block_dict[laser.position]
                interaction_result = block.interact_with_laser(laser.position, laser.direction)
                
                if interaction_result is None:
                    continue  # Laser stops if it hits an opaque block or if it's absorbed
                elif isinstance(interaction_result, list):
                    # If block is a refract block, keep the original direction and add the new one
                    for new_direction in interaction_result:
                        new_lasers.append(Laser(laser.position, new_direction))
                else:
                    # If block is a reflect block, change the laser direction
                    laser.direction = interaction_result
                    new_lasers.append(laser)
                    
        # Update the lasers for the next iteration
        lasers = new_lasers
    
    # Return the positions of lasers that hit target points
    return list(hit_targets)



def main(bff_file):
    board, lasers, targets, blocks = read_bff_file(bff_file)

    solution = solve(board, lasers, targets, blocks)

    if solution:
        output_solution(solution, output_type="txt")
        print("Solution saved to solution.txt")
    else:
        print("No solution found.")

if __name__ == "__main__":                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    bff_file = "./Lazor data/dark_1.bff"  # replace with your .bff file name
    print(read_bff_file(bff_file))
    grid, lasers, targets, blocks = read_bff_file(bff_file)
    print(expand_grid(grid, targets))
    expanded_grid = expand_grid(grid, targets)
    # print(simulate_laser_movement(grid, lasers[0], targets, blocks))
    # main(bff_file)
