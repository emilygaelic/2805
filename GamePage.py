import pygame
import random
import sys

from Blocks import *
from Board import GameBoard
 
# PlayGame Class for managing the game
class PlayGame:
    def __init__(self, boardLength, boardHeight, extension = False, AI = False, level = 1):
        self.length = boardLength
        self.height = boardHeight

        self.centre = (self.length // 2) * 30 - 10 # *30 for cell size, -10 for grid offset
        self.x = self.centre
        self.y = 100

        self.board = GameBoard(boardLength, boardHeight)
        self.blockFactory = BlockFactory()  # Create an instance of the BlockFactory
        self.currentBlock = self.GetBlock() # block to fall
        self.currentBlockID = self.currentBlock.GetBlockID()
        self.nextBlock = self.GetBlock() # next block to display to player 
        self.nextBlockID = self.nextBlock.GetBlockID()

        self.newBlock = True
        self.blockPosition = []

        # player metrics
        self.playerScore = 0
        self.eliminatedLines = 0
        self.playerLevel = 0

        self.gameOver = False


    def GetBlock(self):
        # return random type
        if not hasattr(self, 'blocks'):  # if list is empty or not defined
            self.blocks = ["I", "J", "L", "O", "S", "T", "Z"]  # Use block type names
        newBlockType = random.choice(self.blocks)
        #self.blocks.remove(newBlockType)
        return self.blockFactory.CreateBlock(newBlockType)


    def DrawGame(self, gamePage):
        self.board.DrawBoard(gamePage) # draws game board

        colours = self.board.Colours()
        blockColour = colours[self.currentBlockID]
        self.currentBlock.DrawBlock(gamePage, blockColour, self.x, self.y) # draw current block
        
        if self.newBlock: # initialise new block on board
            blockCells = self.currentBlock.GetBlockPos()
            self.blockPosition = self.board.PlaceBlock(blockCells) # gets block's position on grid
            self.newBlock = False

        # fonts and colours 
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
        self.nextBlock.DrawBlock(gamePage, nextBlockColour, 500, 100) # draw next block

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
        self.currentBlock.DropBlock() # move block down

        for pos in self.blockPosition:# change block position
            pos[0] += 1

        if (self.board.InsideBoard(self.blockPosition) == False): # if block out of bounds (OOB)
            for pos in self.blockPosition: # change block position back
                pos[0] -= 1
            
            # block stops, player gets next block
            self.board.LockBlock(self.blockPosition, self.currentBlock.GetBlockID()) # lock block in position
            # check if game is over
            for cell in self.blockPosition:
                if cell[0] == 0:
                    print("Game Over\n")
                    self.gameOver = True
            self.newBlock = True
            self.currentBlock = self.nextBlock # get next block
            self.currentBlockID = self.currentBlock.GetBlockID()
            self.nextBlock = self.GetBlock() # get new block
            self.nextBlockID = self.nextBlock.GetBlockID()


    def MoveBlock(self, direction):
        if direction == True: # move block right
            self.currentBlock.MoveRight()

            for pos in self.blockPosition: # change block position
                pos[1] += 1

            if (self.board.InsideBoard(self.blockPosition) == False): # if block OOB
                self.currentBlock.MoveLeft() # undo move 
                # PLAY ERROR NOISE
                for pos in self.blockPosition: # change block position back
                    pos[1] -= 1

        else: # move block left
            self.currentBlock.MoveLeft()

            for pos in self.blockPosition: # change block position
                pos[1] -= 1

            if (self.board.InsideBoard(self.blockPosition) == False): # if block OOB
                self.currentBlock.MoveRight() # undo move 
                # PLAY ERROR NOISE
                for pos in self.blockPosition: # change block position back
                    pos[1] += 1


    def Rotate(self):
        rotation = self.currentBlock.RotateBlock() # rotate block
        
        for i in range(len(self.blockPosition)): # change block position on grid
            for j in range(len(self.blockPosition[i])):
                self.blockPosition[i][j] += rotation[i][j]

        if (self.board.InsideBoard(self.blockPosition) == False): # if block OOB
            self.currentBlock.UndoRotation() # undo move
            # PLAY ERROR NOISE
            for i in range(len(self.blockPosition)): # change block position back
                for j in range(len(self.blockPosition[i])):
                    self.blockPosition[i][j] -= rotation[i][j]
