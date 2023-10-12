import pygame
import random
import sys

from Blocks import *
from Board import GameBoard
from TetrisBeast import *

level_speeds = {
    "Easy": 1,  # Slowest speed
    "Medium": 2,
    "Hard": 3  # Fastest speed
}

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.font = pygame.font.SysFont('Courier', 30)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def ask(self):
        screen = pygame.display.get_surface()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                result = self.handle_event(event)
                if result is not None:
                    return result
            self.draw(screen)
            pygame.display.flip()

# PlayGame Class for managing the game
class PlayGame:
    def __init__(self, boardWidth, boardHeight, gameLevel, gameMode=None, playerMode=None, extensionEnabled=False,
                 AIEnabled=False):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        if extensionEnabled:
            self.extension = extensionEnabled
        else:
            self.extension = True if gameMode == "Extended" else False

        if AIEnabled:
            self.AI = AIEnabled
        else:
            self.AI = True if playerMode == "AI" else False

        self.level = gameLevel

        pygame.mixer.init()
        pygame.mixer.music.load('tetrismusic.wav')
        pygame.mixer.music.play(-1)

        self.blockFactory = BlockFactory()  # Create an instance of the BlockFactory
        self.currentBlock = self.GetBlock(self.extension)  # Get random block for user
        self.currentBlockID = self.currentBlock.GetBlockID()  # Get current block's ID
        self.nextBlock = self.GetBlock(self.extension)  # Get next block to display to the player
        self.nextBlockID = self.nextBlock.GetBlockID()  # Get next block's ID
        self.newBlock = True  # New block to be added to board
        self.blockPosition = []  # Stores falling block's position on board

        self.SetDroppingSpeed()  # Controls block dropping speed depending on level
        self.counter = 0  # Counter to control block movement speed

        # Falling block's initial offset, x is the center of the width
        self.x = (boardWidth // 2) * self.board.cell_size - (self.board.cell_size // 2)
        self.y = 0

        # Player metrics
        self.playerScore = 0
        self.eliminatedLines = 0
        self.playerLevel = 0
        self.gameOver = False

    def RunAi(self):
        # self.board.PrintBoard()
        self.AiMove = True  # AI has made move

        # get necessary variables for Tetris Beast
        currentBoard = self.board.GetBoard()
        block1 = self.currentBlock.GetRotations()
        block2 = self.nextBlock.GetRotations()

        moves = self.TB.RunAI(currentBoard, block1, block2, self.boardCentre)  # get move from Tetris Beast

        return moves

    def SetDroppingSpeed(self):
        # Define the speed for block dropping based on level
        level_speeds = {
            "Easy": 1,  # Slowest speed
            "Medium": 2,
            "Hard": 3  # Fastest speed
        }
        self.droppingSpeed = level_speeds.get(self.level, 1)  # Default to "Easy" speed if level is not recognized


    def GetBlock(self, extensionEnabled):
        # return random type
        if not hasattr(self, 'blocks'):  # if list is empty or not defined
            if extensionEnabled:
                self.blocks = ["I", "J", "L", "O", "S", "T", "Z", "Ex_I", "Ex_J"]  # include extension blocks
            else:
                self.blocks = ["I", "J", "L", "O", "S", "T", "Z"]  # Use block type names
        newBlockType = random.choice(self.blocks)
        #self.blocks.remove(newBlockType)
        return self.blockFactory.CreateBlock(newBlockType)

    def DrawGame(self, gamePage):
        self.board.DrawBoard(gamePage)  # Draws game board

        colours = self.board.Colours()
        blockColour = colours[self.currentBlockID]
        self.currentBlock.DrawBlock(gamePage, blockColour, self.x, self.y)  # Draw current block

        if self.newBlock:  # Initialise new block on board
            self.AiMove = False  # This line is from the second version
            blockCells = self.currentBlock.GetBlockPos()
            self.blockPosition = self.board.PlaceBlock(blockCells)  # Gets block's position on grid
            self.newBlock = False

        # Fonts and colours
        white = (255, 255, 255)
        titleFont = pygame.font.SysFont("Courier", 50)
        font = pygame.font.SysFont("Courier", 30)
        font2 = pygame.font.SysFont("Courier", 20)

        # Game Display from the 1st version (dynamic positioning)
        offsetX = (self.boardWidth + 2) * self.board.cell_size + 20

        title = titleFont.render("Tetris", True, white)
        group = font2.render("Group 44", True, white)
        gamePage.blit(title, (offsetX, 20))
        gamePage.blit(group, (offsetX, 70))

        spacing = 50  # Vertical spacing
        next_offset = 140
        score_offset = next_offset + spacing * 3 + 20
        eliminate_offset = score_offset + spacing * 2 + 20
        level_offset = eliminate_offset + spacing * 2 + 20
        info_offset = level_offset + spacing * 2

        next = font.render("Next Block: ", True, white)
        gamePage.blit(next, (offsetX, next_offset))
        nextBlockColour = colours[self.nextBlockID]
        self.nextBlock.DrawBlock(gamePage, nextBlockColour, offsetX, next_offset + spacing)

        score = font.render("Score: ", True, white)
        scoreValue = font.render(str(self.playerScore), True, white)
        gamePage.blit(score, (offsetX, score_offset))
        gamePage.blit(scoreValue, (offsetX + 110, score_offset))

        eliminate = font.render("Eliminated Lines:", True, white)
        eliminated = font.render(str(self.eliminatedLines), True, white)
        gamePage.blit(eliminate, (offsetX, eliminate_offset))
        gamePage.blit(eliminated, (offsetX + 310, eliminate_offset))

        level = font.render("Level: ", True, white)
        levelValue = font.render(str(self.playerLevel), True, white)
        gamePage.blit(level, (offsetX, level_offset))
        gamePage.blit(levelValue, (offsetX + 110, level_offset))

        info = font2.render("Game Details: Normal version, Player mode", True, white)
        gamePage.blit(info, (offsetX, info_offset))

    def BlockFalls(self):
        self.currentBlock.DropBlock()  # Move block down
        self.counter += 1

        if self.counter >= self.droppingSpeed:
            self.counter = 0

            # Make a tentative move by moving the block down
            movedPosition = [[pos[0] + 1, pos[1]] for pos in self.blockPosition]

            # If block can't move down, lock the block in place
            if not self.board.IsValidPosition(movedPosition):
                removed_lines = self.board.LockBlock(self.blockPosition, self.currentBlock.GetBlockID())
                self.eliminatedLines += removed_lines

                # Scoring logic
                score_map = {1: 100, 2: 300, 3: 600, 4: 1000}
                self.playerScore += score_map.get(removed_lines, 0)

                # Game over check
                for cell in self.blockPosition:
                    if cell[0] == 0:
                        self.gameOver = True
                        action = self.game_over_screen()  # Not present in the 2nd version but retained from the 1st
                        if action == "QUIT":
                            pygame.quit()
                            sys.exit()
                        elif action == "RESTART":
                            self.restart_game()
                            return

                # Get a new block
                self.newBlock = True
                self.currentBlock = self.nextBlock
                self.currentBlockID = self.currentBlock.GetBlockID()
                self.nextBlock = self.GetBlock(self.extension)
                self.nextBlockID = self.nextBlock.GetBlockID()

                # Reset the block's starting position
                self.x = (self.boardWidth // 2) * self.board.cell_size - (self.board.cell_size // 2)
                self.y = 0
            else:
                self.blockPosition = movedPosition

    def MoveBlock(self, direction):
        if direction == True:  # Move block right
            self.currentBlock.MoveRight()
            for pos in self.blockPosition:  # Change block position
                pos[1] += 1
            if not self.board.IsValidPosition(self.blockPosition):  # If block OOB
                self.currentBlock.MoveLeft()  # Undo move
                for pos in self.blockPosition:  # Change block position back
                    pos[1] -= 1
        else:  # Move block left
            self.currentBlock.MoveLeft()
            for pos in self.blockPosition:  # Change block position
                pos[1] -= 1
            if not self.board.IsValidPosition(self.blockPosition):  # If block OOB
                self.currentBlock.MoveRight()  # Undo move
                for pos in self.blockPosition:  # Change block position back
                    pos[1] += 1

    def Rotate(self):
        rotation = self.currentBlock.RotateBlock()  # rotate block
        for i in range(len(self.blockPosition)):  # change block position on grid
            for j in range(len(self.blockPosition[i])):
                self.blockPosition[i][j] += rotation[i][j]

        if not self.board.IsValidPosition(self.blockPosition): # if block OOB
            self.currentBlock.UndoRotation()  # undo move
            # PLAY ERROR NOISE
            for i in range(len(self.blockPosition)):  # change block position back
                for j in range(len(self.blockPosition[i])):
                    self.blockPosition[i][j] -= rotation[i][j]

    def handleConfiguration(self):  # Handle level configuration
        self.level = "Easy"  # Set "Easy" to the default level
        level_speeds = {
            "Easy": 1,
            "Medium": 2,
            "Hard": 3
        }
        self.speed = level_speeds[self.level]

    def game_over_actions(self):
        scores = self.get_top_scores_from_file()
        if len(scores) < 10 or self.playerScore > scores[-1][1]:
            # Prompt user for their name
            input_box = InputBox(self.boardHeight * 30 // 2, 350, 140, 32)
            name = input_box.ask()
            scores.append((name, self.playerScore))
            scores.sort(key=lambda x: x[1], reverse=True)
            scores = scores[:10]
            self.save_scores_to_file(scores)

            # Stop the background music and play game over sound
            pygame.mixer.music.stop()  # Stop the background music
            game_over_sound = pygame.mixer.Sound('gameover.wav')  # Load the game over sound
            game_over_sound.play()  # Play the game over sound

            # Transition to TopscorePage
            from TopscorePage import HighscorePage
            HighscorePage.show_top_scores()

    def game_over_screen(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()

        game_over_font = pygame.font.SysFont("Courier", 50)
        game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2 - 60))

        restart_font = pygame.font.SysFont("Courier", 30)
        restart_text = restart_font.render("RESTART", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width / 2, screen_height / 2 + 20))

        quit_font = pygame.font.SysFont("Courier", 30)
        quit_text = quit_font.render("QUIT", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(screen_width / 2, screen_height / 2 + 60))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        return "RESTART"
                    if quit_rect.collidepoint(event.pos):
                        return "QUIT"

            screen.fill((0, 0, 0))
            screen.blit(game_over_text, game_over_rect.topleft)
            screen.blit(restart_text, restart_rect.topleft)
            screen.blit(quit_text, quit_rect.topleft)
            pygame.display.flip()

    @staticmethod
    def save_scores_to_file(scores):
        with open("highscores.txt", "w") as file:
            for name, score in scores:
                file.write(f"{name},{score}\n")

    @staticmethod
    def get_top_scores_from_file():
        try:
            with open("highscores.txt", "r") as file:
                lines = file.readlines()
                scores = [(line.split(",")[0], int(line.split(",")[1])) for line in lines]
                scores.sort(key=lambda x: x[1], reverse=True)
                return scores
        except FileNotFoundError:
            return []
