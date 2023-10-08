from Board import GameBoard
import pygame

class BlockFactory:
    # Choose random black
    @staticmethod
    def create_block(block_type):
        if block_type == "I":
            return I()
        elif block_type == "J":
            return J()
        elif block_type == "L":
            return L()
        elif block_type == "O":
            return O()
        elif block_type == "S":
            return S()
        elif block_type == "T":
            return T()
        elif block_type == "Z":
            return Z()

class Blocks:
    # parent class for all blocks
    def __init__(self, block_num):
        self.cell_size = 30
        self.block = block_num  # block id number  
        self.rotation = 0 # defines current rotation of block
        self.x = 0 # tracks current block's x axis location
        self.y = 0 # tracks current block's y axis location
    
    def get_cells(self):
        return self.rotations[self.rotation]
    
    def get_num(self):
        return self.block
    
    def block_colours(self):
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
    
    # pass in block colour
    def draw_block(self, game_page, x=0, y=0):
        #  colour active rotation cells in block grid
        for i in range(4):
            for j in range(4):
                for cell in self.rotations[self.rotation]:
                    if (i == cell[0] and j == cell[1]):
                        block_colour = self.block_colours()
                        pygame.draw.rect(game_page, block_colour[self.block], (
                            j * self.cell_size + (self.x + x), i * self.cell_size + (self.y + y),
                            self.cell_size - 1, self.cell_size - 1))

    def drop_block(self): # drop block down y axis by 1 cell
        self.y += self.cell_size

    def move_left(self): # move block left across x axis by 1 cell
        self.x -= self.cell_size

    def move_right(self): # move block right across x axis by 1 cell
        self.x += self.cell_size


    def rotate_block(self): # rotate block
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(self.rotations)
        new_position = []
        # compare difference between positions
        for i in range(len(self.rotations[self.rotation])):
            new = []
            for j in range(len(self.rotations[self.rotation][i])):
                new.append(self.rotations[self.rotation][i][j] - self.rotations[old_rotation][i][j])
            new_position.append(new)
        return new_position

    def undo_rotate(self):
        self.rotation = (self.rotation - 1) % len(self.rotations)



# Child classes for each block type
class I(Blocks):  # light blue
    def __init__(self):
        super().__init__(block_num=1) # block number 1
        # defines the grid position of block for each rotation
        self.rotations = {
            0: [[0, 1], [1, 1], [2, 1], [3, 1]],
            1: [[1, 0], [1, 1], [1, 2], [1, 3]],
            2: [[0, 2], [1, 2], [2, 2], [3, 2]],
            3: [[2, 0], [2, 1], [2, 2], [2, 3]]
            
        }


class J(Blocks):  # blue
    def __init__(self):
        super().__init__(block_num=2) # block number 2
        self.rotations = {
            0: [[0, 0], [1, 0], [1, 1], [1, 2]], 
            1: [[0, 1], [0, 2], [1, 1], [2, 1]],
            2: [[1, 0], [1, 1], [1, 2], [2, 2]],
            3: [[0, 1], [1, 1], [2, 0], [2, 1]]
        }


class L(Blocks):  # orange
    def __init__(self):
        super().__init__(block_num=3) # block number 3
        self.rotations = {
            0: [[0, 1], [1, 1], [2, 1], [2, 2]],
            1: [[1, 0], [1, 1], [1, 2], [2, 0]], 
            2: [[0, 0], [0, 1], [1, 1], [2, 1]],
            3: [[0, 2], [1, 0], [1, 1], [1, 2]]
        }


class T(Blocks):  # purple
    def __init__(self):
        super().__init__(block_num=4) # block number 4
        self.rotations = {
            0: [[0, 1], [1, 0], [1, 1], [1, 2]],
            1: [[0, 1], [1, 1], [1, 2], [2, 1]],
            2: [[1, 0], [1, 1], [1, 2], [2, 1]],
            3: [[0, 1], [1, 0], [1, 1], [2, 1]]
        }


class O(Blocks):  # yellow
    def __init__(self):
        super().__init__(block_num=5) # block number 5
        self.rotations = {
            0: [[0, 0], [0, 1], [1, 0], [1, 1]]
        }


class S(Blocks):  # green
    def __init__(self):
        super().__init__(block_num=6) # block number 6
        self.rotations = {
            0: [[0, 1], [0, 2], [1, 0], [1, 1]],
            1: [[0, 0], [1, 0], [1, 1], [2, 1]]
        }


class Z(Blocks):  # red
    def __init__(self):
        super().__init__(block_num=7) # block number 7
        self.rotations = {
            0: [[0, 0], [0, 1], [1, 1], [1, 2]],
            1: [[0, 2], [1, 1], [1, 2], [2, 1]],
        }

