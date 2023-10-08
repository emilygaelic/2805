import pygame
import random
import sys

from blocks import *
from board import GameBoard
 
# PlayGame Class for managing the game
class PlayGame:
    def __init__(self, board_length, board_height, extension = False, AI = False, level = 1):
        self.length = board_length
        self.height = board_height

        self.centre = (self.length // 2) * 30 - 10 # *30 for cell size, -10 for grid offset
        self.x = self.centre
        self.y = 100

        self.board = GameBoard(board_length, board_height)
        self.block_factory = BlockFactory()  # Create an instance of the BlockFactory
        self.current_block = self.get_block() # block to fall
        self.next_block = self.get_block() # next block to display to player 
        

        self.new_block = True
        self.block_position = []


        # player metrics
        self.player_score = 0
        self.eliminated_lines = 0
        self.player_level = 0

        self.game_over = False
      #  self.font = pygame.font.SysFont("Courier", 30)
       # self.game_finished = self.font.render("GAME OVER", True, (255, 255, 255))

    def get_block(self):
        # return random type
        if not hasattr(self, 'blocks'):  # if list is empty or not defined
            self.blocks = ["I", "J", "L", "O", "S", "T", "Z"]  # Use block type names
        new_block_type = random.choice(self.blocks)
        #self.blocks.remove(new_block_type)
        return self.block_factory.create_block(new_block_type)


    def draw_game(self, game_page):
        self.board.draw_board(game_page) # draws game board

        self.current_block.draw_block(game_page, self.x, self.y) # draw current block
        
        if self.new_block: # initialise new block on board
            block_cells = self.current_block.get_cells()
            self.block_position = self.board.place_block(block_cells) # gets block's position on grid
            self.new_block = False

        # fonts and colours 
        white = (255, 255, 255)
        title_font = pygame.font.SysFont("Courier", 50)
        font = pygame.font.SysFont("Courier", 30)
        font2 = pygame.font.SysFont("Courier", 20)

        # Game Display
        title = title_font.render("Tetris", True, white)
        group = font2.render("Group 44", True, white)
        next = font.render("Next Block: ", True, white)
        game_page.blit(title, (120, 20))
        game_page.blit(group, (300, 70))
        game_page.blit(next, (500, 50))

        self.next_block.draw_block(game_page, 500, 100) # draw next block

        score = font.render("Score: ", True, white)
        score_value = font.render(str(self.player_score), True, white)
        game_page.blit(score, (500, 250))
        game_page.blit(score_value, (610, 250))

        eliminate = font.render("Eliminated Lines: ", True, white)
        eliminated = font.render(str(self.eliminated_lines), True, white)
        game_page.blit(eliminate, (500, 400))
        game_page.blit(eliminated, (810, 400))

        level = font.render("Level: ", True, white)
        level_value = font.render(str(self.player_level), True, white)
        game_page.blit(level, (500, 550))
        game_page.blit(level_value, (610, 550))

        info = font2.render("Game Details: Normal version, Player mode", True, white)  # DISPLAY ACTUAL
        game_page.blit(info, (500, 650))


    def block_falls(self):
        self.current_block.drop_block() # move block down

        for pos in self.block_position:# change block position
            pos[0] += 1

        if (self.board.inside_board(self.block_position) == False): # if block out of bounds (OOB)
            for pos in self.block_position: # change block position back
                pos[0] -= 1
            
            # block stops, player gets next block
            self.board.lock_block(self.block_position, self.current_block.get_num()) # lock block in position
            # check if game is over
            for cell in self.block_position:
                if cell[0] == 0:
                    print("Game Over\n")
                    self.game_over = True
            self.new_block = True
            self.current_block = self.next_block # get next block
            self.next_block = self.get_block() # get new block


    def move_block(self, direction):
        if direction == True: # move block right
            self.current_block.move_right()

            for pos in self.block_position: # change block position
                pos[1] += 1

            if (self.board.inside_board(self.block_position) == False): # if block OOB
                self.current_block.move_left() # undo move 
                # PLAY ERROR NOISE
                for pos in self.block_position: # change block position back
                    pos[1] -= 1

        else: # move block left
            self.current_block.move_left()

            for pos in self.block_position: # change block position
                pos[1] -= 1

            if (self.board.inside_board(self.block_position) == False): # if block OOB
                self.current_block.move_right() # undo move 
                # PLAY ERROR NOISE
                for pos in self.block_position: # change block position back
                    pos[1] += 1


    def rotate(self):
        rotation = self.current_block.rotate_block() # rotate block
        
        for i in range(len(self.block_position)): # change block position on grid
            for j in range(len(self.block_position[i])):
                self.block_position[i][j] += rotation[i][j]

        if (self.board.inside_board(self.block_position) == False): # if block OOB
            self.current_block.undo_rotate() # undo move
            # PLAY ERROR NOISE
            for i in range(len(self.block_position)): # change block position back
                for j in range(len(self.block_position[i])):
                    self.block_position[i][j] -= rotation[i][j]


    def quit_game(self):
        # new quit screen for confirming game exit
        quit_screen = pygame.display.set_mode((1000, 700))

        red = (255, 0, 0)
        white = (255, 255, 255)
        font = pygame.font.SysFont("Courier", 30)

        quit_rect = pygame.Rect(250, 250, 600, 200)
        yes_rect = pygame.Rect(350, 390, 100, 30)
        no_rect = pygame.Rect(600, 390, 100, 30)

        pygame.draw.rect(quit_screen, (red), quit_rect)
        pygame.draw.rect(quit_screen, (red), yes_rect)
        pygame.draw.rect(quit_screen, (red), no_rect)

        quit_surface = font.render("Are you sure you want to quit?", True, white)
        warning = font.render("Progress may be lost.", True, white)
        yes = font.render("Quit", True, white)
        no = font.render("Cancel", True, white)
        
        while True:

            quit_screen.blit(quit_surface, (300, 300))
            quit_screen.blit(warning, (300, 330))
            quit_screen.blit(yes, (350, 390))
            quit_screen.blit(no, (600, 390))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if yes_rect.collidepoint(mouse):
                        return True
                    elif no_rect.collidepoint(mouse):
                        return False
