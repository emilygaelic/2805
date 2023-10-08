import pygame

# GameBoard class for managing the board
class GameBoard:
    def __init__(self, length, height):
        # board size (((pass in as parameters)))
        self.rows = height #20
        self.cols = length #10
        self.cell_size = 30 # size of grid cells
        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]


    def print_board(self):
        # prints game board
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.grid[i][j], end=" ")
            print("\n")

    def colours(self):
        # colour configurations
        dark_grey = (25, 30, 40)
        light_blue = (21, 204, 209)
        blue = (13, 64, 216)
        orange = (226, 116, 17)
        purple = (166, 0, 247)
        yellow = (237, 234, 4)
        green = (47, 230, 23)
        red = (232, 18, 18)
        return [dark_grey, light_blue, blue, orange, purple, yellow, green, red]

    def draw_board(self, game_page):
        # draws the board on the screen  
        for i in range(self.rows): # for the size of the board
            for j in range(self.cols):
                cell_colour = self.grid[i][j] # check number on grid for which colour to draw
                cell_colours = self.colours() # get colour 
                # draw cell in colour assigned by grid number
                pygame.draw.rect(game_page, cell_colours[cell_colour], (
                    j * self.cell_size + 50, i * self.cell_size + 100, self.cell_size - 1, self.cell_size - 1))
                # 50 and 100 is the board offset, cell size reduced by 1 to produce grid lines

    def place_block(self, block_cells): # place the new block on grid
        block_position = [] # identify block's position on board
        center = self.cols // 2 - 2 # subtract 2 for size of block
        for i in range(self.rows): # use block co-ords to find grid location
            for j in range(self.cols):
                for block_cell in block_cells:
                    if i == block_cell[0] and j == block_cell[1]:
                        block_position.append([i, j + center])
        return block_position


    def inside_board(self, cells): 
        for cell in cells: 
            # check if block in on grid
            if (cell[0] >= self.rows) or (cell[1] >= self.cols or cell[1] < 0):
                return False # block is outside grid
            
            # block has collaided with locked blocked
            x = cell[0]
            y = cell[1]
            print(self.grid[x][y])

            if self.grid[x][y] != 0:
                print("collision")
                return False

        return True # block is within grid


    def lock_block(self, cells, block_num): # lock block in grid
        # assign block position with block number on board
        for i in range(len(cells)): 
            x = cells[i][0]
            y = cells[i][1]
            self.grid[x][y] = block_num
        
