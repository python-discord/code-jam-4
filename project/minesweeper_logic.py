

class Minesweeper:

    UNDISCOVERED = 0  # a tile which hasn't been clicked yet
    DISCOVERED = 1  # a tile which has been clicked and is viewable
    MINE = 2  # a tile which is a mine

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Initialise the game
        self.initialise_grid()

    def initialise_grid(self):
        '''This refreshes self.grid variable into an array with all tiles being of value EMPTY'''
        self.grid = [[self.UNDISCOVERED for _ in range(self.width)] for _ in range(self.height)]

    def put_bombs_in_grid(self, amount):
        '''This puts X amount of bombs onto the grid in random places'''
        pass

    def click_tile(self, x, y) -> bool:
        '''This clicks a certain tile at point (x, y)
        The grid should update and the tiles should change from
        UNDISCOVERED to DISCOVERED, depending on where they are.
        returns True if the tile is a mine, returns false otherwise'''
        if self.grid[y][x] == self.MINE:
            return True

    def get_tile_number(self, x, y) -> int:
        '''This returns the "tile number" (i.e. how many tiles surrounding said tile is a bomb)
        returns an integer between 0 and 8'''
        pass

    def print_grid(self):
        '''This prints the grid, used for debugging purposes'''
        print_characters = {self.UNDISCOVERED: 'X', self.DISCOVERED: ' ', self.MINE: 'B'}
        for row in self.grid:
            for tile in row:
                print(print_characters[tile], end=' ')
            print()


if __name__ == '__main__':
    game = Minesweeper(16, 16)
    game.print_grid()

    # Test for the bombs in grid function
    game.put_bombs_in_grid(10)
    assert [tile for tile_list in game.grid for tile in tile_list].count(game.MINE) == 10, \
        'There are not mines in the grid'

    # Test for the click_tile function to make tiles discoverable
    game_over = game.click_tile(5, 5)
    assert game.DISCOVERED in [tile for tile_list in game.grid for tile in tile_list], \
        'None of the tiles have been discovered after clicking'

    # Test the get_tile_number function returns an integer
    tile_number = game.get_tile_number(5, 5)
    assert isinstance(tile_number, int), \
        'The get_tile_number function didn\'t return an integer'

    game.print_grid()
