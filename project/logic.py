from itertools import product
import random


class Minesweeper:

    UNDISCOVERED = 0  # a tile which hasn't been clicked yet
    DISCOVERED = 1  # a tile which has been clicked and is viewable
    MINE = 2  # a tile which is a mine

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []

        # Initialise the game
        self.initialise_grid()

    def initialise_grid(self):
        '''This refreshes self.grid variable into an array with all tiles being of value EMPTY'''
        self.grid = [[self.UNDISCOVERED for _ in range(self.width)] for _ in range(self.height)]

    def put_mines_in_grid(self, amount) -> set:
        '''This puts X amount of mines onto the grid in random places'''
        coordinates = set()
        while len(coordinates) < amount:
            x, y = random.randrange(self.width), random.randrange(self.height)
            coordinates.add((x, y))
            self.grid[y][x] = self.MINE
        return coordinates

    def click_tile(self, x, y) -> bool:
        '''This clicks a certain tile at point (x, y)
        The grid should update and the tiles should change from
        UNDISCOVERED to DISCOVERED, depending on where they are.
        returns True if the tile is a mine, returns false otherwise'''
        if self.grid[y][x] == self.MINE:
            return True
        elif self.grid[y][x] == self.UNDISCOVERED:
            self.walk_discovered_tiles(x, y)
        return False

    def walk_discovered_tiles(self, x, y):
        '''This method walks through all the tiles which are adjacent to each other
        and also have a tile number of 0, turning them into discovered tiles'''
        self.grid[y][x] = self.DISCOVERED
        if not self.get_tile_number(x, y):
            surrounding = self.__surrounding_tiles(x, y)
            for x1, y1 in surrounding:
                if self.grid[y1][x1] != self.DISCOVERED and not self.get_tile_number(x1, y1):
                    self.walk_discovered_tiles(x1, y1)
                elif self.get_tile_number(x1, y1):
                    self.grid[y1][x1] = self.DISCOVERED

    def get_tile_number(self, x, y) -> int:
        '''This returns the "tile number" (i.e. how many tiles surrounding said tile is a bomb)
        returns an integer between 0 and 8'''
        tiles = [self.__get_tile_safe(x1, y1) for x1, y1 in self.__surrounding_tiles(x, y)]
        return tiles.count(self.MINE)

    def __surrounding_tiles(self, x, y) -> list:
        '''This returns the coordinates of the tiles surrounding (x,y)'''
        tiles = product((x - 1, x, x + 1), (y - 1, y, y + 1))  # This gets a 9x9 square at (x,y)
        tiles = filter(lambda c: 0 <= c[0] < self.width and 0 <= c[1] < self.height, tiles)
        tiles = list(tiles)
        tiles.remove((x, y))
        return tiles

    def __get_tile_safe(self, x, y):
        '''This returns the tile with the coordinates (x, y)
        Returns None if the tile doesnt exist
        Returns None if x or y are negative'''
        if x < 0 or y < 0:
            return None
        try:
            return self.grid[y][x]
        except IndexError:
            return None

    def print_grid(self):
        '''This prints the grid, used for debugging purposes'''
        print_characters = {self.UNDISCOVERED: 'X', self.DISCOVERED: ' ', self.MINE: 'B'}
        for row in self.grid:
            for tile in row:
                print(print_characters[tile], end=' ')
            print()
        print()


if __name__ == '__main__':
    game = Minesweeper(16, 16)
    game.print_grid()

    # Minesweeper Tests

    # Test for the bombs in grid function
    game.put_mines_in_grid(10)
    assert [tile for tile_list in game.grid for tile in tile_list].count(game.MINE) == 10, \
        'There are not mines in the grid'
    game.print_grid()

    # Test for the click_tile function to make tiles discoverable
    game_over = game.click_tile(5, 5)
    assert game.DISCOVERED in [tile for tile_list in game.grid for tile in tile_list], \
        'None of the tiles have been discovered after clicking'
    game.print_grid()

    # Test the get_tile_number function returns an integer
    tile_number = game.get_tile_number(5, 5)
    assert isinstance(tile_number, int), \
        'The get_tile_number function didn\'t return an integer'
    game.print_grid()
