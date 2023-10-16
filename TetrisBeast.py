import copy

class TetrisBeast:
    def __init__(self, boardLength):
        
        self.length = boardLength # 10
        self.height = 20
        self.board = None
        self.block1 = None
        self.block2 = None

        self.bestScore = None
        self.bestRotation = None
        self.bestOffset = None

        self.A =  -3.7 # height multiplier
        self.B =  +2.0 # clear
        self.C = -4.0 # hole
        self.D = -0.8 # blockade

    def PrintBoard(self):
        # prints game board
        for i in range(self.height):
            for j in range(self.length):
                #print(self.board[i][j], end=" ")
                print("(", i, j, ")", end=" ")
            print("\n")
        print("\n")

    def ColHeight(self, col):
        for i in range(self.height): # find height of column
            if self.board[i][col] != 0: # found height
                return self.height - i
        return 0

    def CountBlockages(self, col):
        blockCount = 0
        block = None
        for j in range(self.length):
            for i in range(self.height - col):
                if self.board[i][col] != 0:
                    if block is None or block != self.board[i][j]:
                        block = self.board[i][j]
                        blockCount += 1
        return blockCount
    
    def Heuristics(self):
        heights = [] # get current height of blocks on board 
        for j in range(self.length): # for each column
            heights.append(self.ColHeight(j))

        heightSum = sum(heights) # aggregate height

        blockages = [] # number of blocks above each holes
        # find number of holes
        holes = []
        for j in range(self.length): # for each column
            holeCount = 0 # hole count for each column
            for i in range(self.height): # find height of column
                if self.board[i][j] == 0 and (self.height - i < heights[j]): # if there is a hole in column
                    holeCount += 1
                    # count how many blocks above it
                    blockages.append(self.CountBlockages(j))

            holes.append(holeCount) 
        holeCount = sum(holes)
        blockagesCount = sum(blockages)

        # check if lines are completed
        linesCleared = 0 # complete lines
        for i in range(self.height):
            if 0 not in self.board[i]:
                linesCleared += 1

        # +3.0 for each edge touching another block
        # +3.5 for each edge touching the wall
        # +2.0 for each edge touching the floor

        # calculate heuristic
        score = ( self.A * heightSum 
                + self.B * linesCleared 
                + self.C * holeCount 
                + self.D * blockagesCount)
        print(score)
        return score

    def ScorePosition(self, block, xOffset, rotation):
        blockLen = block[-1][1] + 1
        blockHeight = block[-1][0] + 1

        if xOffset + blockLen > self.length or xOffset < 0:  # block doesn't fit in board
            return

        # add x offset to block
        for coord in block: 
            coord[1] += xOffset 
        
        # find y offset
        yOffset = self.height - blockHeight 
        for coord in block: # find how far block can drop
            for y in range(self.height): # look through cell column
                if self.board[y][coord[1]] != 0 and y < yOffset: # find lowest point block can drop
                    yOffset = y

        # add y offset to block
        for coord in block:
            coord[0] += yOffset 

        # put block in temp board
        for i in range(len(block)): 
            x = block[i][0]
            y = block[i][1]
            self.board[x][y] = 8

        # score position based on board holes, bumpiness, lines cleared 
        score = self.Heuristics()

        # update best score if necessary
        if self.bestScore == None or self.bestScore > score:
            self.bestScore = score
            self.bestOffset = xOffset
            self.bestRotation = rotation

        # undo grid for next test
        for i in range(len(block)): 
            x = block[i][0]
            y = block[i][1]
            self.board[x][y] = 0


    def RunAI(self, board, block1, block2, centre):
        moves = [] # store moves
        self.board = copy.deepcopy(board) # copy game board
        self.block1 = block1 # current block
        self.block2 = block2 # next block

        # print("board for AI")
        # self.PrintBoard()

        for rotation in range(len(self.block1)): # for each block rotation 
            for offset in range(self.length): # for the length of the board
                self.ScorePosition(self.block1[rotation], offset, rotation) # score each rotation of block in each grid position

        offset = self.bestOffset - centre # minus board centre

        # find moves that get block in best position
        for _ in range(1, self.bestRotation):
            moves.append("up")
        for _ in range(0, abs(offset)):
            if offset > 0:
                moves.append("right")
            else:
                moves.append("left")
        return moves
