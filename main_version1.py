import itertools
import os


def read_bff_file(filename):
    """
     This function reads the input bff file and returns target information

     Parameters:

         filename: *str*
             the name of input file

     Returns:

         grid: *list*
             2D list containing the original appearance of grid

         lasers: *list*
             a 2D list, each containing the position and direction of a lazor

         targets: *set*
             each tuple in the set represents a target point

         blocks: *dict*
             contain number of each type of blocks

     """
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

            elif line.startswith('A ') or line.startswith('B ')\
                    or line.startswith('C '):
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
    """
    This function calculate the expanded gird and put target points in

    Parameters:

        raw_grid: *list*
            original form of grid containing 'x' and 'o'

        targets: *list*
            each tuple in the list represents a target point


    Returns:

        expanded_grid: *list*
            2D list contains numbers for each symbol
    """

    # calculate the expanded grid size
    expanded_height = len(raw_grid) * 2 + 1
    expanded_width = len(raw_grid[0]) * 2 + 1

    # initialize the grid
    expanded_grid = [['0' for i in range(expanded_width)]
                     for i in range(expanded_height)]

    for y, row in enumerate(raw_grid):

        for x, value in enumerate(row):
            # transform elements into the expanded grid
            center_y = 2 * y + 1
            center_x = 2 * x + 1

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


class Block:
    def __init__(self, block_type, position):
        """
        Initializes a new instance of the Block class.

        Parameters:
            block_type: *str*
                types of the block
                'A' : reflect block
                'B' : opaque block
                'C' : refract block

            position: *tuple*
                coordinates of the block

        """

        self.block_type = block_type
        self.position = position

    def interact_with_Lazor(self, Lazor_position, Lazor_direction):
        """
        This function calculates the interaction between lazor and block

        Parameters:
            Lazor_position: *tuple*
                position of lazor

            Lazor_direction: *tuple*
                directon of lazor

        Returns: *list*
            new lazor direction
        """

        # Determine the direction laser came from
        # center:(2k+1, 2k+1)
        # interaction point:(2k+1, 2k) or (2k, 2k+1)

        x_in = (Lazor_position[0] % 2 == 0)  # interaction on left or right
        y_in = (Lazor_position[1] % 2 == 0)  # interaction on top or bottom

        # Interact with Lazor based on Block type
        if self.block_type == 'A':  # reflect

            if x_in and not y_in:
                # left or right, change x
                return -Lazor_direction[0], Lazor_direction[1]

            elif y_in and not x_in:
                # top or bottom, change y
                return Lazor_direction[0], -Lazor_direction[1]

        elif self.block_type == 'C':  # refract
            # one laser direction unchanged
            # adds a reflection direction

            if x_in and not y_in:
                return [(Lazor_direction[0], Lazor_direction[1]),
                        (-Lazor_direction[0], Lazor_direction[1])]
            elif y_in and not x_in:
                return [(Lazor_direction[0], Lazor_direction[1]),
                        (Lazor_direction[0], -Lazor_direction[1])]

        # other types of blocks or does not interact
        return None


class Lazor:
    def __init__(self, position, direction):
        """
        Parameters:
            position: *tuple*
                postions of lazor

            direction: *tuple*
                direction of lazor
        """
        self.position = position
        self.direction = direction

    def move(self):
        # Move lazor to the next position based on its direction
        self.position = (self.position[0] + self.direction[0],
                         self.position[1] + self.direction[1])


def meet_block(lazor, blocks_dict):
    """
    This function checks if the lazor interacts with a block

    Parameters:
        lazor: *list*
            2 tuples represent lazor position and direction

        blocks_dict: *dict*
           number and types of all  blocks

    Returns:
        new_Lazors: *object*
            new lazor positions and directions after interaction

    """
    x, y = lazor.position
    dx, dy = lazor.direction
    new_Lazors = []

    # Check both adjacent points
    adjacent_positions = [(x + dx, y), (x, y + dy)]

    for position in adjacent_positions:

        if position in blocks_dict:

            block = blocks_dict[position]

            interaction_result = block.interact_with_Lazor(lazor.position,
                                                           lazor.direction)

            if interaction_result is None:
                # Return a Lazor with no direction change (stopped)
                return []

            if interaction_result and isinstance(interaction_result, list):
                # refractive block generates multiple new Lazors
                for new_direction in interaction_result:
                    new_Lazors.append(Lazor(lazor.position, new_direction))
            else:
                # reflective block, change the direction
                new_Lazors.append(Lazor(lazor.position, interaction_result))

            # If interaction, do not check other points
            break

    if not new_Lazors:
        # If no interaction, the Lazor continues in the same direction
        new_Lazors.append(Lazor(lazor.position, lazor.direction))

    return new_Lazors


def generate_possible_grids(initial_grid, block_dict):
    """
    This function generates the possible grids with all blocks placed

    Parameters:
        initial_grid: *list*
            the original empty grid contains 'x' and 'o'

        block_dict: *dict*
            number and types of all the blocks to be placed

    Returns:
        result_grids: *list*
           main_version1.py All the possible new grid with blocks placed
    """

    empty_positions = [(x, y) for y in range(len(initial_grid))
                       for x in range(len(initial_grid[0]))
                       if initial_grid[y][x] == 'o']

    block_types = sorted([b for b, count in block_dict.items()
                          for i in range(count)])
    total_blocks = len(block_types)

    result_grids = []

    # generate all the possible ways of placement
    for positions in itertools.combinations(empty_positions, total_blocks):

        for block_order in set(itertools.permutations(block_types,
                                                      total_blocks)):
            # copy the original grid for placement
            new_grid = [row[:] for row in initial_grid]

            for position, block_type in zip(positions, block_order):
                x, y = position
                new_grid[y][x] = block_type

            result_grids.append(new_grid)
    return result_grids


def pos_chk(grid, Lazor):
    """
    This function checks if the lazor is inside the grid

    Parameters:
        grid: *list*
            The expanded grid

        Lazor: *object*
            lazor to be checked with positions and directions

    Returns: *bool*
        True: lazer is out of the grid
    """

    grid_size = (len(grid[0]), len(grid))

    return (Lazor.position[0] < 0 or Lazor.position[0] >= grid_size[0] or
            Lazor.position[1] < 0 or Lazor.position[1] >= grid_size[1])


def simulate(grid, Lazors, blocks):
    """
    This function simulate the lazor path and finds
    all the passed target points

    Parameters:
        grid: *list*
            expanded grid
        Lazors: *list*
            position and direction of all the lazors
        blocks: *list*
            all the blocks objects

    Returns:
        hit_targets: *set*
            all the positions of passed targets

    """
    # original state of each Lazor
    original_states = [(lazor.position, lazor.direction) for lazor in Lazors]

    def reset_Lazors():
        """
        reset Lazors to their original states
        """
        for i, lazor in enumerate(Lazors):
            orig_pos, orig_dir = original_states[i]
            lazor.position = orig_pos
            lazor.direction = orig_dir

    blocks_dict = {block.position: block for block in blocks}

    # initialize
    active_Lazors = Lazors.copy()

    # store Lazor positions that hit targets
    hit_targets = set()

    # Initial block interaction check for each Lazor at starting position
    new_Lazors = []

    for lazor in active_Lazors:
        interaction_results = meet_block(lazor, blocks_dict)

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
                # Skip to the next Lazor
                continue

            # Block interaction check after moving
            interaction_results = meet_block(lazor, blocks_dict)
            for result in interaction_results:
                if not pos_chk(grid, result):
                    new_Lazors.append(result)

                    # Check if Lazor hits a target
                    if grid[result.position[1]][result.position[0]] == 't':
                        hit_targets.add(result.position)

        active_Lazors = new_Lazors

    # After simulation, reset Lazors to their original states
    reset_Lazors()

    return hit_targets


def save_grid(grid, filename):
    """
    This function saves the solution as a txt file

    Parameters:
        grid:

        filename: *str*
            name of the file to be solved
    """

    if not filename.endswith('.txt'):
        filename += '.txt'

    with open(filename, 'w') as file:
        for row in grid:
            file.write(' '.join(row) + '\n')


def solve(grids, lazors, targets, filename):
    """
    This function solves the lazor question and save the solution as a txt file

    Parameters:
        grids:*list*
            all the possible grid with blocks in

        lazors:*list*
            lazor positions and directions

        targets: *set*
             each tuple in the set represents a target point

        filename:*str*
            question filename, also the output filename
    """
    for grid in grids:
        expanded_grid = expand_grid(grid, targets)
        blocks_list = []

        for y, row in enumerate(expanded_grid):
            for x, value in enumerate(row):
                if value in 'ABC':
                    block = Block(value, (x, y))
                    blocks_list.append(block)

        passed_targets = simulate(expanded_grid, lazors, blocks_list)

        if targets == passed_targets:
            save_grid(grid, filename)
            break


if __name__ == "__main__":
    bff_file = "./Lazor data/tiny_5.bff"  # replace with .bff file name
    name = os.path.basename(bff_file[:-4])

    grid, lazors, targets, blocks = read_bff_file(bff_file)
    grids = generate_possible_grids(grid, blocks)
    solve(grids, lazors, targets, name)
