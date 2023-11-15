import threading
import os


# Define the Block class
class Block:

    def __init__(self, block_type, position, fixed=False):
        """
        Initializes a new instance of the Block class.

        Parameters:
        block_type : str
            The type of the block,
            which can be 'A' for reflect block,
            'B' for opaque block,
            and 'C' for refract block.
        position : tuple of int
            The (x, y) coordinates of the block on the grid.
        fixed : boolean
            Whether the block is fixed on grid or not.
        """
        # 'A' for reflect, 'B' for opaque, 'C' for refract
        self.block_type = block_type
        self.position = position
        self.fixed = fixed

    def interact_with_Lasers(self, Laser_position, Laser_direction):
        """
        Calculates the interaction between a laser and a block.

        Parameters:
        Laser_position : tuple of int
            The (x, y) coordinates of the laser's position.
        Laser_direction : tuple of int
            The (dx, dy) direction vector of the laser.

        Returns:
        list or None
            If the block interacts with the laser,
            it returns a list of new laser directions.
            If the block does not interact with the laser,
            it returns None.
        """

        # Determine the direction laser came from
        # center:(2k+1, 2k+1)
        # interaction point:(2k+1, 2k) or (2k, 2k+1)

        x_in = (Laser_position[0] % 2 == 0)  # interaction on left or right
        y_in = (Laser_position[1] % 2 == 0)  # interaction on top or bottom

        # Interact with Laser based on Block type
        if self.block_type == 'A':  # reflect

            if x_in and not y_in:
                # left or right, change x
                return -Laser_direction[0], Laser_direction[1]

            elif y_in and not x_in:
                # top or bottom, change y
                return Laser_direction[0], -Laser_direction[1]

        elif self.block_type == 'C':  # refract
            # one laser direction unchanged
            # adds a reflection direction

            if x_in and not y_in:
                return [(Laser_direction[0], Laser_direction[1]),
                        (-Laser_direction[0], Laser_direction[1])]
            elif y_in and not x_in:
                return [(Laser_direction[0], Laser_direction[1]),
                        (Laser_direction[0], -Laser_direction[1])]

        # other types of blocks or does not interact
        return None


# Define the Laser class.
class Laser:

    def __init__(self, position, direction, active=True):
        """
        Initializes a new Laser instance.

        Parameters:
        - position: A tuple (x, y) for the laser's starting position.
        - direction: A tuple (dx, dy) representing
                     the laser's movement direction.
        - active: A boolean indicating if the laser is currently active.
        """
        self.position = position
        self.direction = direction
        self.active = active

    def move(self, grid):
        """
        Move the laser to the next position based on its direction.

        Parameters:
        - grid: The grid in which the laser is moving.
        """
        self.position = (self.position[0] + self.direction[0],
                         self.position[1] + self.direction[1])
        # Check if the new position is out of the grid and update active status
        if not self.is_inside(grid):
            self.active = False

    def is_inside(self, grid):
        """
        Check if the laser is inside the grid.

        Parameters:
        - grid: The grid to check against.
        """
        grid_size = (len(grid.expanded_grid[0]), len(grid.expanded_grid))
        return (0 <= self.position[0] < grid_size[0]
                and 0 <= self.position[1] < grid_size[1])


# Define the Grid class.
class Grid:

    def __init__(self, raw_grid, targets):
        """
        Initializes a new instance of the Grid class.

        Parameters:
        raw_grid : list of list of str
            The raw grid data representing the game board.
        targets : list of tuple of int
            A list of target points' coordinates (x, y) on the grid.
            """
        # Directly call expand_grid with self
        self.expanded_grid = self.expand_grid(raw_grid, targets)
        self.targets = {tuple(t): False for t in targets}

    def expand_grid(self, raw_grid, targets):
        """
        Expands the raw grid into an expanded grid with additional symbols.

        Parameters:
        raw_grid : list of list of str
            The raw grid data representing the game board.
        targets : list of tuple of int
            A list of target points' coordinates (x, y) on the grid.

        Returns:
        list of list of str
            The expanded grid with additional symbols.
        """
        # Calculate the size of the expanded grid
        expanded_height = len(raw_grid) * 2 + 1
        expanded_width = len(raw_grid[0]) * 2 + 1

        # Create the expanded grid with a default value of '0'

        expanded_grid = [['0' for _ in range(expanded_width)]
                         for _ in range(expanded_height)]

        for i in range(expanded_width):
            for j in range(expanded_height):
                if i % 2 == 0 and j % 2 == 0:
                    expanded_grid[j][i] = '+'
                if i % 2 != 0 and j % 2 != 0:
                    expanded_grid[j][i] = 'o'
                if i % 2 != 0 and j % 2 == 0:
                    expanded_grid[j][i] = '-'
                if i % 2 == 0 and j % 2 != 0:
                    expanded_grid[j][i] = '|'

        # Map the original grid to the expanded grid
        for y, row in enumerate(raw_grid):
            for x, value in enumerate(row):
                # Calculate the coordinates of the center point
                # on the expanded grid
                center_y = 2 * y + 1
                center_x = 2 * x + 1

                # Fill in the center point of the expanded grid
                # based on the value from the original grid.
                # Open space where blocks can be placed
                if value == 'o':
                    expanded_grid[center_y][center_x] = 'o'
                # Space where no blocks can be placed
                elif value == 'x':
                    expanded_grid[center_y][center_x] = 'x'
                # Fixed reflect block
                elif value == 'A':
                    expanded_grid[center_y][center_x] = 'A'
                # Fixed opaque block
                elif value == 'B':
                    expanded_grid[center_y][center_x] = 'B'
                # Fixed refract block
                elif value == 'C':
                    expanded_grid[center_y][center_x] = 'C'

        # Mark the target points in the expanded grid
        for target in targets:
            xt, yt = target
            expanded_grid[yt][xt] = '?'

        return expanded_grid

    def is_inside(self, position):
        x, y = position
        return (0 <= x < len(self.expanded_grid[0])
                and 0 <= y < len(self.expanded_grid))

    def can_place_block(self, position, block):
        x, y = position
        return self.is_inside(position) and self.expanded_grid[y][x] == 'o'

    def get_all_empty_positions(self):
        """
        Get all positions in the grid where a block can be placed.

        Returns:
            List[Tuple[int, int]]: A list of tuples
            representing the coordinates of empty positions.
        """
        empty_positions = []
        for y, row in enumerate(self.expanded_grid):
            for x, value in enumerate(row):
                if value == 'o':
                    empty_positions.append((x, y))
        return empty_positions

    def place_block(self, position, block_type):
        x, y = position
        if self.can_place_block(position, block_type):
            self.expanded_grid[y][x] = block_type
            return True
        return False

    def remove_block(self, position):
        x, y = position
        if self.is_inside(position) and self.expanded_grid[y][x] != 'x':
            self.expanded_grid[y][x] = 'o'


def read_bff_file(filename):
    """
    Reads a '.bff' file and extracts the grid layout,
    available blocks, lasers, and required points
    for the lazor game.

    The '.bff' file format is assumed to be as follows:
    - Grid definition starts with 'GRID START'
      and ends with 'GRID STOP'.
    - Each row in the grid is represented by a line of
       characters between 'GRID START' and 'GRID STOP'.
      'o' represents an empty space where blocks can be placed.
      'A', 'B', 'C' represent fixed reflect, opaque,
      and refract blocks respectively.
      'x' represents a space where no blocks can be placed.
    - After the grid definition, available movable blocks
      are specified by lines starting with
      'A', 'B', or 'C' followed by the quantity.
    - Lasers are defined by lines starting with 'L'
       followed by their position and direction vectors.
    - Points that lasers need to intersect are defined
       by lines starting with 'P' followed by the coordinates.

    Parameters:
    filename : str
        The path to the '.bff' file to be read.

    Returns:
    grid : list of str
        A 2D list representing the game grid
        where each position can be:
        - 'o': Empty space where blocks can be placed.
        - 'A': Fixed reflect block.
        - 'B': Fixed opaque block.
        - 'C': Fixed refract block.
        - 'x': Space where no blocks can be placed.
    blocks : dict
        A dictionary with keys 'A', 'B', and 'C'
        corresponding to the available reflection,
        opaque, and refract blocks and their quantities.
    lasers : list of tuples
        A list where each tuple contains the position (x, y)
        and the direction vector (dx, dy) for each laser.
    points : list of tuples
        A list of tuples where each tuple represents
        the coordinates (x, y) of the points
        that the lasers need to intersect.
    """

    grid = []
    # initialize block counts
    blocks = {'A': 0, 'B': 0, 'C': 0}
    lasers = []
    targets = []

    try:
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
                elif line.startswith('A ') or line.startswith('B ')\
                        or line.startswith('C '):
                    block_type, count = line.split()
                    blocks[block_type] = int(count)
                elif line.startswith('L '):
                    parts = line.split()
                    position = (int(parts[1]), int(parts[2]))
                    direction = (int(parts[3]), int(parts[4]))
                    # Create a Laser object
                    lasers.append(Laser(position, direction))
                elif line.startswith('P '):
                    parts = line.split()
                    # Ensure that positions are added as tuples of two integers
                    position = (int(parts[1]), int(parts[2]))
                    targets.append(position)

        # Check that the file was read properly
        if not grid or not blocks or not lasers or not targets:
            raise ValueError("File contents are incomplete "
                             "or in an incorrect format.")

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        # Handle exceptions or re-raise them
        raise

    return grid, lasers, targets, blocks


def simulate(grid, Lasers, blocks):
    """
    This function simulates the laser path
    and finds all the passed target points

    Parameters:
        grid: *list*
            expanded grid
        Lasers: *list*
            position and direction of all the lasers
        blocks: *list*
            all the blocks objects

    Returns:
        hit_targets: *set*
            all the positions of passed targets

    """
    # original state of each Laser
    original_states = [(laser.position, laser.direction) for laser in Lasers]

    def reset_Lasers():
        """ Reset Lasers to their original states. """
        for i, laser in enumerate(Lasers):
            orig_pos, orig_dir = original_states[i]
            laser.position = orig_pos
            laser.direction = orig_dir

    blocks_dict = {block.position: block for block in blocks}

    # initialize
    active_Lasers = Lasers.copy()

    # store Laser positions that hit targets
    hit_targets = set()

    # Initial block interaction check for each Laser at starting position
    new_Lasers = []

    for laser in active_Lasers:
        interaction_results = meet_block(laser, blocks_dict)
        new_Lasers.extend(interaction_results)

    active_Lasers = new_Lasers

    while active_Lasers:
        new_Lasers = []

        for laser in active_Lasers:
            if laser.active:
                # Move the Laser
                laser.move(grid)

                # Check if Laser is within grid bounds
                if not laser.is_inside(grid):
                    continue

                # Block interaction check after moving
                interaction_results = meet_block(laser, blocks_dict)
                new_Lasers.extend(interaction_results)

                # Check if Laser hits a target
                target_cell \
                    = grid.expanded_grid[laser.position[1]][laser.position[0]]
                if (laser.position[1] < len(grid.expanded_grid) and
                        laser.position[0] < len(grid.expanded_grid[0])):
                    if (target_cell == '?'):
                        hit_targets.add(laser.position)

        active_Lasers = new_Lasers

    # After simulation, reset Lasers to their original states
    reset_Lasers()

    return hit_targets


def meet_block(laser, blocks_dict):
    """
    This function checks if the lazor interacts with a block

    Parameters:
        laser: *list*
            2 tuples represent lazor position and direction

        blocks_dict: *dict*
           number and types of all  blocks

    Returns:
        new_Lasers: *object*
            new lazor positions and directions after interaction

    """
    x, y = laser.position
    dx, dy = laser.direction
    new_Lasers = []

    # Check both adjacent points
    adjacent_positions = [(x + dx, y), (x, y + dy)]

    for position in adjacent_positions:

        if position in blocks_dict:

            block = blocks_dict[position]

            interaction_result = block.interact_with_Lasers(laser.position,
                                                            laser.direction)

            if interaction_result is None:
                # Return a Laser with no direction change (stopped)
                return []

            if interaction_result and isinstance(interaction_result, list):
                # refractive block generates multiple new Lasers
                for new_direction in interaction_result:
                    new_Lasers.append(Laser(laser.position, new_direction))
            else:
                # reflective block, change the direction
                new_Lasers.append(Laser(laser.position, interaction_result))

            # If interaction, do not check other points
            break

    if not new_Lasers:
        # If no interaction, the Laser continues in the same direction
        new_Lasers.append(Laser(laser.position, laser.direction))

    return new_Lasers


# Define the Solver class.
class Solver:
    def __init__(self, grid, blocks, lasers, targets):
        """
        Initializes a new instance of the Solver class.

        Parameters:
        grid : Grid
            The game grid containing the layout of blocks and targets.
        blocks : dict
            A dictionary containing the available block types
            ('A', 'B', 'C') and their quantities.
        lasers : list of Laser
            A list of Laser objects representing the lasers in the puzzle.
        targets : list of tuple
            A list of tuples representing the target points'
            coordinates (x, y) on the grid.
        """
        self.grid = grid
        self.blocks = blocks
        self.lasers = lasers
        self.targets = targets

    def solve(self):
        """
        Solve the lazor puzzle and find a valid solution.

        Returns:
        list of tuple or None
            A list of tuples representing the placed blocks'
            types and positions (block_type, (x, y)).
            Returns None if no valid solution is found.
        """
        # Generate a list of all empty positions in the grid
        empty_positions = self.grid.get_all_empty_positions()
        return self.recursive_solve(0, empty_positions, [], self.blocks.copy())

    def recursive_solve(self, index, empty_positions,
                        placed_blocks, available_blocks):
        """
        Recursively solve the laser puzzle by
        trying different block placements.

        Parameters:
        index : int
            The current index of the empty positions list.
        empty_positions : list of tuple
            A list of tuples representing the coordinates
            (x, y) of empty positions on the grid.
        placed_blocks : list of tuple
            A list of tuples representing the placed blocks'
            types and positions (block_type, (x, y)).
        available_blocks : dict
            A dictionary containing the remaining
            quantities of available block types.

        Returns:
        list of tuple or None
            A list of tuples representing the placed blocks'
            types and positions (block_type, (x, y)).
        Returns None if no valid solution is found.
        """
        if index == len(empty_positions):
            # Check if all types of blocks are exhausted
            if all(count == 0 for count in available_blocks.values()):
                # Convert placed_blocks tuples to Block objects
                block_objects = [Block(block_type, position)
                                 for block_type, position in placed_blocks]
                hit_targets = simulate(self.grid, self.lasers, block_objects)

                # Check if all targets are hit
                if all(target in hit_targets for target in self.targets):
                    return placed_blocks
            return None

        current_position = empty_positions[index]

        for block_type in 'ABCo':
            if block_type == 'o' or available_blocks[block_type] > 0:
                # Place block and update remaining blocks count
                if block_type != 'o':
                    self.grid.place_block(current_position, block_type)
                    available_blocks[block_type] -= 1
                    placed_blocks.append((block_type, current_position))

                # Recursively solve for the next position
                result = self.recursive_solve(index + 1, empty_positions,
                                              placed_blocks, available_blocks)
                if result is not None:
                    return result  # Solution found

                # Backtrack: Remove block and restore remaining blocks count
                if block_type != 'o':
                    self.grid.remove_block(current_position)
                    available_blocks[block_type] += 1
                    placed_blocks.pop()

        return None


# A thread lock used to synchronize access to
# the output when printing solutions or failure messages.
output_lock = threading.Lock()


def solve_puzzle(file_path):
    """
    Solve a laser puzzle from a given BFF file and
    print the solution or a failure message.

    Parameters:
    file_path : str
        The path to the BFF file containing the lazor puzzle data.

    Returns:
    None
    """
    # Read the puzzle data from the BFF file
    grid_data, lasers, targets, blocks = read_bff_file(file_path)

    # Create a grid object
    grid = Grid(grid_data, targets)
    print("The initial grid: ")
    for row in grid.expanded_grid:
        print(''.join(row))
    solver = Solver(grid, blocks, lasers, targets)

    # Create a solver object
    solver = Solver(grid, blocks, lasers, targets)

    # Attempt to solve the puzzle
    solution = solver.solve()

    # Use a lock to synchronize printing the solution or failure message
    with output_lock:
        solution_output = ""
        if solution:
            solution_output += f"Solution found for {file_path}:\n"
            for row in grid.expanded_grid:
                solution_output += ''.join(row) + "\n"
        else:
            solution_output += f"No solution found for {file_path}.\n"

        # Print the solution or failure message
        print(solution_output)

        # Extract the base file name without extension and path
        base_file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Construct the output file name
        output_file_name = base_file_name + '_solution.txt'

        # Write the solution or failure message to a text file
        with open(output_file_name, 'w') as file:
            file.write(solution_output)


def parallel_solve(bff_file):
    """
    Solve a laser puzzle from a BFF file in a separate thread.

    Parameters:
    bff_file : str
        The path to the BFF file containing the lazor puzzle data.

    Returns:
    None
    """
    # Create a new thread to solve the puzzle in parallel
    thread = threading.Thread(target=solve_puzzle, args=(bff_file,))
    thread.start()
    thread.join()


if __name__ == "__main__":
    bff_file = "./Lazor data/tiny_5.bff"  # replace with your .bff file name
    parallel_solve(bff_file)
