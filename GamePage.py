import pygame
import random
import sys

from Blocks import *
from Board import GameBoard
from TetrisBeast import *
from ConfigurePage import *

# PlayGame Class for managing the game
class PlayGame:
    def __init__(self, boardWidth, extensionEnabled, AIEnabled, gameLevel):
        self.boardWidth = boardWidth
        self.boardHeight = 20

        self.extension = extensionEnabled
        self.AI = AIEnabled
        if self.AI:
            self.TB = TetrisBeast(boardWidth)
            self.AiMove = False

        self.droppingSpeed = gameLevel

        pygame.mixer.init()
        pygame.mixer.music.load('tetrismusic.wav')
        pygame.mixer.music.play(-1)

        self.board = GameBoard(boardWidth)  # create game board
        self.blockFactory = BlockFactory()  # Create an instance of the BlockFactory
        self.currentBlock = self.GetBlock()  # Get random block for user
        self.currentBlockID = self.currentBlock.GetBlockID()  # Get current block's ID
        self.nextBlock = self.GetBlock()  # Get next block to display to the player
        self.nextBlockID = self.nextBlock.GetBlockID()  # Get next block's ID
        self.newBlock = True  # New block to be added to board
        self.blockPosition = []  # Stores falling block's position on board

        # Falling block's initial offset, x is the center of the width
        self.x = (boardWidth // 2) * self.board.cellSize - 10  # 10 is grid offset
        self.y = 100

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
        centre = self.boardWidth // 2

        moves = self.TB.RunAI(currentBoard, block1, block2, centre)  # get move from Tetris Beast
        return moves

    def GetBlock(self):
        # return random type
        if not hasattr(self, 'blocks'):  # if list is empty or not defined
            if self.extension:
                self.blocks = ["I", "J", "L", "O", "S", "T", "Z", "Ex_I", "Ex_J"]  # include extension blocks
            else:
                self.blocks = ["I", "J", "L", "O", "S", "T", "Z"]  # Use block type names
        newBlockType = random.choice(self.blocks)
        # self.blocks.remove(newBlockType)
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

        # Game Display
        title = titleFont.render("Tetris", True, white)
        group = font2.render("Group 44", True, white)
        next = font.render("Next Block: ", True, white)
        gamePage.blit(title, (120, 20))
        gamePage.blit(group, (300, 70))
        gamePage.blit(next, (500, 50))

        nextBlockColour = colours[self.nextBlockID]
        self.nextBlock.DrawBlock(gamePage, nextBlockColour, 500, 100)  # draw next block

        score = font.render("Score: ", True, white)
        scoreValue = font.render(str(self.playerScore), True, white)
        gamePage.blit(score, (500, 250))
        gamePage.blit(scoreValue, (610, 250))

        eliminate = font.render("Eliminated Lines: ", True, white)
        eliminated = font.render(str(self.eliminatedLines), True, white)
        gamePage.blit(eliminate, (500, 400))
        gamePage.blit(eliminated, (810, 400))

        level = font.render("Level: ", True, white)
        levelValue = font.render(str(self.playerLevel), True, white)
        gamePage.blit(level, (500, 550))
        gamePage.blit(levelValue, (610, 550))

        info = font2.render("Game Details: Normal version, Player mode", True, white)  # DISPLAY ACTUAL
        gamePage.blit(info, (500, 650))
    
    def BlockFalls(self):
        self.currentBlock.DropBlock()  # Move block down

        # Make a tentative move by moving the block down
        for pos in self.blockPosition: # change block position
            pos[0] += self.droppingSpeed

        # If block can't move down, lock the block in place
        if not self.board.IsValidPosition(self.blockPosition):
            for pos in self.blockPosition: # change block position back
                pos[0] -= self.droppingSpeed

            removed_lines = self.board.LockBlock(self.blockPosition, self.currentBlock.GetBlockID())
            self.eliminatedLines += removed_lines

            # Scoring logic
            score_map = {1: 100, 2: 300, 3: 600, 4: 1000}
            self.playerScore += score_map.get(removed_lines, 0)

            # Game over check
            for cell in self.blockPosition:
                if cell[0] == 0:
                    print("Game Over\n")
                    self.gameOver = True

            # Get a new block
            self.newBlock = True
            self.currentBlock = self.nextBlock
            self.currentBlockID = self.currentBlock.GetBlockID()
            self.nextBlock = self.GetBlock()
            self.nextBlockID = self.nextBlock.GetBlockID()

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

        if not self.board.IsValidPosition(self.blockPosition):  # if block OOB
            self.currentBlock.UndoRotation()  # undo move
            # PLAY ERROR NOISE
            for i in range(len(self.blockPosition)):  # change block position back
                for j in range(len(self.blockPosition[i])):
                    self.blockPosition[i][j] -= rotation[i][j]
