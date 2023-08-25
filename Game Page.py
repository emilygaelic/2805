import pygame
import random
import sys

class Blocks:
    def __init__(self, block_num):
        self.board = GameBoard()
        self.block = block_num  # block number to identify colour
        self.rotations = 0
        self.x = 140 #(self.board.cols // 2 * 30) -10  # x offset to start block in the middle
        self.y = 40  # y offset
        self.rotation = 0
       # self.moves = []

    def valid_space(self): # return whether or not the block is within the grid
        if self.block == 1:
            if (self.x < 50) or (self.x > (self.board.cols * self.board.cell_size-60) or
                             self.y > (self.board.rows * self.board.cell_size)):
                return False
        else:        
            if (self.x < 50) or (self.x > (self.board.cols * self.board.cell_size - 30) or
                                self.y > (self.board.rows * self.board.cell_size)):
                return False
        return True

    def draw_block(self, game_page, x = 0, y = 0):
        for i in range(4):
            for j in range(4):
                for cell in self.rotations[self.rotation]:
                    if (i == cell[0] and j == cell[1]):
                        block_colour = self.board.colours()
                        pygame.draw.rect(game_page, block_colour[self.block], (
                            j * self.board.cell_size + (self.x + x), i * self.board.cell_size + (self.y + y),
                            self.board.cell_size - 1, self.board.cell_size - 1))
                    
    def drop_block(self):
        self.y += self.board.cell_size
        if not self.valid_space():
            self.y -= self.board.cell_size

    def move_left(self):
        self.x -= self.board.cell_size
        if not self.valid_space():
            self.x += self.board.cell_size

    def move_right(self):
        self.x += self.board.cell_size
        if not self.valid_space(): 
            self.x -= self.board.cell_size

    def rotate_block(self):
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(self.rotations)
        if not self.valid_space(): 
            self.rotation = old_rotation




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
            
            0: [(2, 0), (2, 1), (2, 2), (3, 2)],
            1: [(3, 0), (3, 1), (2, 1), (1, 1)],
            2: [(1, 0), (2, 0), (2, 1), (2, 2)],
            3: [(1, 1), (1, 2), (2, 1), (3, 1)]
        }

class L(Blocks):  # orange
    def __init__(self):
        super().__init__(block_num=3)
        self.rotations = {
            0: [(2, 0), (2, 1), (2, 2), (3, 0)],
            1: [(1, 0), (3, 1), (2, 1), (1, 1)],
            2: [(1, 2), (2, 0), (2, 1), (2, 2)],
            3: [(1, 1), (3, 2), (2, 1), (3, 1)]
        }

class T(Blocks):  # purple
    def __init__(self):
        super().__init__(block_num=4)
        self.rotations = {
            0: [(2, 0), (2, 1), (2, 2), (3, 1)],
            1: [(1, 1), (2, 1), (3, 1), (2, 0)],
            2: [(2, 0), (2, 1), (2, 2), (1, 1)],
            3: [(1, 1), (2, 1), (3, 1), (2, 2)]
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
            0: [(3, 0), (3, 1), (2, 1), (2, 2)], 
            1: [(1, 1), (2, 1), (2, 2), (3, 2)]
        }

class Z(Blocks):  # red
    def __init__(self):
        super().__init__(block_num=7)
        self.rotations = {
            0: [(2, 0), (3, 1), (2, 1), (3, 2)],
            1: [(1, 2), (2, 1), (2, 2), (3, 1)],
        }

# PLAYING BOARD
class GameBoard:
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]\

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

 #   def inside_board(self, cells):
    #    for cell in cells:


class PlayGame:
    def __init__(self):
        self.board = GameBoard()
        self.blocks = [I(), J(), L(), O(), S(), T(), Z()]
        self.current_block = self.get_block()
        self.next_block = self.get_block()
        self.board_filled = False

        self.white = (255, 255, 255)
        self.title_font = pygame.font.SysFont("Courier", 50)
        self.font = pygame.font.SysFont("Courier", 30)
        self.font2 = pygame.font.SysFont("Courier", 20)

        self.title = self.title_font.render("Tetris", True, self.white)
        self.group = self.font2.render("Group 44", True, self.white)

        self.next = self.font.render("Next Block: ", True, self.white)

        self.player_score = 0
        self.score = self.font.render("Score: ", True, self.white)
        self.score_value = self.font.render(str(self.player_score), True, self. white)

        self.eliminated_lines = 0
        self.eliminate = self.font.render("Eliminated Lines: ", True, self.white)
        self.eliminated = self.font.render(str(self.eliminated_lines), True, self. white)

        self.player_level = 0
        self.level = self.font.render("Level: ", True, self.white)
        self.level_value = self.font.render(str(self.player_level), True, self. white)

        self.info = self.font2.render("Game Details: Normal version, Player mode", True, self.white) # display actual 

        self.game_over = self.font.render("GAME OVER", True, self.white)
        
        self.quit_surface = self.font.render("Are you sure you want to quit?", True, self.white)
        self.warning = self.font.render("Progress may be lost.", True, self.white)
        self.yes = self.font.render("Quit", True, self.white)
        self.no = self.font.render("Cancel", True, self.white)
        

    def get_block(self):
        if len(self.blocks) == 0: #if list is empty
            self.blocks = [I(), J(), L(), O(), S(), T(), Z()]
        new_block = random.choice(self.blocks)
        self.blocks.remove(new_block)
        return new_block

    def draw_game(self, game_page):
        self.board.draw_board(game_page)
        self.current_block.draw_block(game_page)

        #cells = self.current_block.rotations[self.current_block.rotation]
       # self.board.inside_board(cells) # initialise i, j for block

        game_page.blit(self.title, (120, 20))
        game_page.blit(self.group, (300, 70))
        game_page.blit(self.next, (500, 50))
        self.next_block.draw_block(game_page, 360, 40)

        game_page.blit(self.score, (500, 250))
        game_page.blit(self.score_value, (610, 250))

        game_page.blit(self.eliminate, (500, 400))
        game_page.blit(self.eliminated, (810, 400))

        game_page.blit(self.level, (500, 550))
        game_page.blit(self.level_value, (610, 550))
        
        game_page.blit(self.info, (500, 650))


    def block_falls(self):
        self.current_block.drop_block()

    def move_block(self, direction):
        if direction == True:
            self.current_block.move_right()
        else:
            self.current_block.move_left()

    def rotate(self):
        self.current_block.rotate_block()

    # def lock_block(self):
    #     cells = self.current_block.rotations[self.current_block.rotation]
    #     i = (self.current_block.y - 40) // 30 
    #     j = (self.current_block.x - 140) // 30
    #     for cell in cells:
    #         self.board.grid[i][j] = self.current_block.block_num
    #     self.current_block = self.next_block
    #     self.next_block = self.get_block()

    def quit_game(self, game_page):

        quit_screen = pygame.display.set_mode((1000, 700))

        red = (255,0,0)

        quit_rect = pygame.Rect(250, 250, 600, 200)
        yes_rect = pygame.Rect(350, 390, 100, 30)
        no_rect = pygame.Rect(600, 390, 100, 30)
        
        pygame.draw.rect(quit_screen, (red), quit_rect)
        pygame.draw.rect(quit_screen, (red), yes_rect)
        pygame.draw.rect(quit_screen, (red), no_rect)
        

        while True:

            quit_screen.blit(self.quit_surface, (300, 300))
            quit_screen.blit(self.warning, (300, 330))
            quit_screen.blit(self.yes, (350, 390))
            quit_screen.blit(self.no, (600, 390))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if yes_rect.collidepoint(mouse):
                        return True
                    elif no_rect.collidepoint(mouse):
                        return False



def main():
    pygame.init()

    # Load and play background music
    pygame.mixer.music.load("background.wav")
    pygame.mixer.music.play(-1)

    # GAME SURFACES
    game_width = 1000
    game_height = 700
    pygame.display.set_caption('Tetris 44')
    game_page = pygame.display.set_mode((game_width, game_height))

    clock = pygame.time.Clock()  # start clock
    pygame.time.set_timer(pygame.USEREVENT, 300)

    run = True  # run game variable
    game = PlayGame()
    rotate_sound = pygame.mixer.Sound("can_rotate.wav")

    while run:

        # DISPLAY - fill screen with grid and surfaces
        game_page.fill((0, 0, 0))  # black background
        game.draw_game(game_page)

        # PLAYER ACTIONS
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # user quits
                if (game.quit_game(game_page)):
                    run = False
                else:
                    continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# quits with escape key
                    if (game.quit_game(game_page)):
                        run = False
                    else:
                        continue

                if event.key == pygame.K_RIGHT:  # move right
                    game.move_block(True)
                if event.key == pygame.K_LEFT:  # move left
                    game.move_block(False)
                if event.key == pygame.K_UP:  # rotate
                    game.current_block.rotate_block()
                    rotate_sound.play()
                if event.key == pygame.K_DOWN:  # move down
                    game.block_falls()

            if event.type == pygame.USEREVENT:
              game.block_falls()

        if game.board_filled == True:
            game.blit(game.game_over, (250, 250, 600, 200))

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
