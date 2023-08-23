import pygame
import random
import sys


class Blocks:
    def __init__(self, block_num):
        self.board = GameBoard()
        self.block = block_num  # block number to identify colour
        self.rotations = 0
        self.x = 50 + (self.board.cols // 2 * 30) - 30  # x offset to start block in the middle
        self.y = 40  # y offset
        self.rotation = 0

    def block_position(self):
        # return whether or not the block is within the grid
        block_cells = self.rotations[self.rotation]  # list of current rotation coords
        moves = []  # list of previous moves

    def draw_block(self, game_page):
        for i in range(4):
            for j in range(4):
                # print(self.rotations[pos])
                for cell in self.rotations[self.rotation]:
                    # print(position)
                    # start_pos = (position[0] - 2, position[1])
                    # print(start_pos)
                    # self.cells.append(start_pos)
                    if (i == cell[0] and j == cell[1]):
                        block_colour = self.board.colours()
                        pygame.draw.rect(game_page, block_colour[self.block], (
                            j * self.board.cell_size + self.x, i * self.board.cell_size + self.y,
                            self.board.cell_size - 1, self.board.cell_size - 1))

    # i need to save the position of the blocks relative to the grid so i can know if they are within the grid
    # then next would be locking in the blocks, collisions, eliminating lines
    def drop_block(self):
        self.y += self.board.cell_size
        if self.y > (self.board.rows * self.board.cell_size + (
                self.board.cell_size * 2)):  # 60 to offset the shape beginning above the grid
            self.y -= self.board.cell_size

    def move_left(self):
        self.x -= self.board.cell_size
        if self.x < 50:
            self.x += self.board.cell_size

    def move_right(self):
        self.x += self.board.cell_size
        if self.x > (self.board.cols * self.board.cell_size):
            self.x -= self.board.cell_size

    def rotate_block(self):
        self.rotation = (self.rotation + 1) % len(self.rotations[self.rotation])


class I(Blocks):  # light blue
    def __init__(self):
        super().__init__(block_num=1)
        self.rotations = {
            0: [(2, 0), (2, 1), (2, 2), (2, 3)],
            1: [(0, 2), (1, 2), (2, 2), (3, 2)]
        }


class J(Blocks):  # blue
    def __init__(self):
        super().__init__(block_num=2)
        self.rotations = {
            0: [(1, 0), (2, 0), (2, 1), (2, 2)],
            1: [(1, 1), (1, 2), (2, 1), (3, 1)],
            2: [(2, 0), (2, 1), (2, 2), (3, 2)],
            3: [(3, 0), (3, 1), (2, 1), (1, 1)]
        }
class L(Blocks):  # orange
    def __init__(self):
        super().__init__(block_num=3)
        self.rotations = {
            0: [(1, 2), (2, 0), (2, 1), (2, 2)],
            1: [(1, 1), (3, 2), (2, 1), (3, 1)],
            2: [(2, 0), (2, 1), (2, 2), (3, 0)],
            3: [(1, 0), (3, 1), (2, 1), (1, 1)]
        }


class T(Blocks):  # purple
    def __init__(self):
        super().__init__(block_num=4)
        self.rotations = {
            0: [(2, 0), (2, 1), (2, 2), (1, 1)],
            1: [(1, 1), (2, 1), (3, 1), (2, 2)],
            2: [(2, 0), (2, 1), (2, 2), (3, 1)],
            3: [(1, 1), (2, 1), (3, 1), (2, 0)]
        }


class O(Blocks):  # yellow
    def __init__(self):
        super().__init__(block_num=5)
        self.rotations = {
            0: [(2, 1), (2, 2), (3, 1), (3, 2)]
        }


class S(Blocks):  # green
    def __init__(self):
        super().__init__(block_num=6)
        self.rotations = {
            0: [(1, 1), (2, 1), (2, 2), (3, 2)],
            1: [(3, 0), (3, 1), (2, 1), (2, 2)]
        }


class Z(Blocks):  # red
    def __init__(self):
        super().__init__(block_num=7)
        self.rotations = {
            0: [(2, 0), (3, 1), (2, 1), (3, 2)],
            1: [(1, 2), (2, 1), (2, 2), (3, 1)]
        }


# PLAYING BOARD
class GameBoard:
    def __init__(self):
        # these should be changeable
        self.rows = 20
        self.cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]


    def print_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.grid[i][j], end=" ")
            print("\n")

    def colours(self):
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
        for i in range(self.rows):
            for j in range(self.cols):
                cell_colour = self.grid[i][j]
                cell_colours = self.colours()
                pygame.draw.rect(game_page, cell_colours[cell_colour], (
                j * self.cell_size + 50, i * self.cell_size + 100, self.cell_size - 1, self.cell_size - 1))


class PlayGame:
    def __init__(self):
        self.board = GameBoard()
        self.blocks = [I(), J(), L(), O(), S(), T(), Z()]
        self.current_block = self.get_block()

        # self.game_over = False
        # self.score = 0

    def get_block(self):
        # blocks = [I(), J(), L(), O(), S(), T(), Z()]
        return random.choice(self.blocks)

    def draw_game(self, game_page):
        self.board.draw_board(game_page)
        self.current_block.draw_block(game_page)

    def block_falls(self):
        self.current_block.drop_block()

    def move_block(self, direction):
        if direction == True:
            self.current_block.move_right()
        else:
            self.current_block.move_left()

    def rotate(self):
        self.current_block.rotate_block()


### MAIN
pygame.init()

# Load and play background music
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# GAME SURFACES
# title, score, level, group, next block, game over, quit,
game_width = 1000
game_height = 700
game_page = pygame.display.set_mode((game_width, game_height))

clock = pygame.time.Clock()  # start clock
pygame.time.set_timer(pygame.USEREVENT, 300)

run = True  # run game variable
game = PlayGame()
rotate_sound = pygame.mixer.Sound("can_rotate.wav")

while run:

    # DISPLAY
    # fill screen with grid and surfaces
    game_page.fill((0, 0, 0))  # black background
    game.draw_game(game_page)

    # PLAYER ACTIONS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # *or escape key
            # *are you sure?
            run = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # move right
                game.move_block(True)
            if event.key == pygame.K_LEFT:  # move left
                game.move_block(False)
            if event.key == pygame.K_UP:  # rotate
                game.current_block.rotate_block()
                rotate_sound.play()
            if event.key == pygame.K_DOWN:  # move down
                game.block_falls()

        # if event.type == pygame.USEREVENT:
        #   game.block_falls()

    # REFRESH GAME
    pygame.display.update()
    clock.tick(30)

pygame.quit()
