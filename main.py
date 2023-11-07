#import libraries here

def read_bff_file(filename):
    '''
    Reads a '.bff' file and extracts the grid layout, available blocks, lasers, and required points for the Lazor game.

    The '.bff' file format is assumed to be as follows:
    - Grid definition starts with 'GRID START' and ends with 'GRID STOP'.
    - Each row in the grid is represented by a line of characters between 'GRID START' and 'GRID STOP'.
      'o' represents an empty space where blocks can be placed.
      'A', 'B', 'C' represent fixed reflect, opaque, and refract blocks respectively.
      'x' represents a space where no blocks can be placed.
    - After the grid definition, available movable blocks are specified by lines starting with 'A', 'B', or 'C' followed by the quantity.
    - Lasers are defined by lines starting with 'L' followed by their position and direction vectors.
    - Points that lasers need to intersect are defined by lines starting with 'P' followed by the coordinates.

    Parameters:
    filename : str
        The path to the '.bff' file to be read.

    Returns:
    grid : list of list of str
        A 2D list representing the game grid where each position can be:
        - 'o': Empty space where blocks can be placed.
        - 'A': Fixed reflect block.
        - 'B': Fixed opaque block.
        - 'C': Fixed refract block.
        - 'x': Space where no blocks can be placed.
    blocks : dict
        A dictionary with keys 'A', 'B', and 'C' corresponding to the available reflect, opaque, and refract blocks and their quantities.
    lasers : list of tuples
        A list where each tuple contains the position (x, y) and the direction vector (dx, dy) for each laser.
    points : list of tuples
        A list of tuples where each tuple represents the coordinates (x, y) of the points that the lasers need to intersect.

    '''
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
                        grid_line.append(None)
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
                lasers.append((position, direction))
            elif line.startswith('P '):
                parts = line.split()
                position = (int(parts[1]), int(parts[2]))
                targets.append(position)

    # Processing grid to include fixed blocks
    # processed_grid = []
    # for y, row in enumerate(grid):
    #     processed_row = []
    #     for x, cell in enumerate(row):
    #         if cell == 'o':
    #             processed_row.append(None)
    #         elif cell in blocks:
    #             processed_row.append(Block(cell, fixed=True))
    #     processed_grid.append(processed_row)

    return grid, lasers, targets, blocks


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

def main(bff_file):
    board, lasers, targets, blocks = read_bff_file(bff_file)

    solution = solve(board, lasers, targets, blocks)

    if solution:
        output_solution(solution, output_type="txt")
        print("Solution saved to solution.txt")
    else:
        print("No solution found.")

if __name__ == "__main__":                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    bff_file = "./Lazors/Lazor data/tiny_5.bff"  # replace with your .bff file name
    print(read_bff_file(bff_file))
    # main(bff_file)
