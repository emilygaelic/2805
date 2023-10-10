import pygame

# GameBoard class for managing the board
class GameBoard:
    def __init__(self, length, height):
        # board size (((pass in as parameters)))
        self.rows = height #20
        self.cols = length #10
        self.cell_size = 30 # size of grid cells
        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]


    def PrintBoard(self):
        # prints game board
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.grid[i][j], end=" ")
            print("\n")

    def Colours(self):
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

    def DrawBoard(self, gamePage):
        # draws the board on the screen
        for i in range(self.rows): # for the size of the board
            for j in range(self.cols):
                cellColour = self.grid[i][j] # check number on grid for which colour to draw
                cellColours = self.Colours() # get colour
                # draw cell in colour assigned by grid number
                pygame.draw.rect(gamePage, cellColours[cellColour], (
                    j * self.cell_size + 50, i * self.cell_size + 100, self.cell_size - 1, self.cell_size - 1))
                # 50 and 100 is the board offset, cell size reduced by 1 to produce grid lines


    def PlaceBlock(self, blockCells): # place the new block on grid
        blockPosition = [] # identify block's position on board
        center = self.cols // 2 - 2 # subtract 2 for size of block
        for i in range(self.rows): # use block co-ords to find grid location
            for j in range(self.cols):
                for blockCell in blockCells:
                    if i == blockCell[0] and j == blockCell[1]:
                        blockPosition.append([i, j + center])
        return blockPosition

    def InsideBoard(self, cells):
        # Check if cells is a single coordinate (integer)
        if isinstance(cells, int):
            x = cells
            y = cells
            return x >= 0 and x < self.rows and y >= 0 and y < self.cols

        # Check if cells is a list of coordinates
        for cell in cells:
            if cell[0] < 0 or cell[0] >= self.rows or cell[1] >= self.cols or cell[1] < 0:
                return False
            # Check if block has collaided with locked blocked
            x = cell[0]
            y = cell[1]
            if self.grid[x][y] != 0:
                return False
        return True

    def LockBlock(self, cells, blockID): # lock block in grid
        # assign block position with block number on board
        for i in range(len(cells)):
            x = cells[i][0]
            y = cells[i][1]
            self.grid[x][y] = blockID
        self.eliminate()

    def eliminate(self):
        for i in self.grid:
            count = 0
            for j in self.grid:
                if j != 0:
                    count += 1
                    if self.cols == count:
                        self.grid.remove(i)
                        new_row = []
                        for j in self.rows:
                            new_row.append(0)
                        self.grid.append(new_row)
        self.PrintBoard()

