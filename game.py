
import pygame, sys
import random
from bitmapfont import BitmapFont
from pygame.locals import *

EMPTY = 0
MINES = 1
CLOSED = 0
OPENED = 1

WIN = 0
END = 1
CONTINUE = 2

class GameState: 
    def __init__(self, runner):
        self.runner = runner
    
    def on_enter(self, prev_state):
        pass

    def on_exit(self):
        pass

    def update(self, deltatime):
        pass

    def draw(self, surface):
        pass

class Runner:
    def __init__(self, name, height, width):
        self.name = name
        self.height = height
        self.width = width
        pygame.init()
        pygame.display.set_caption(self.name)
        self.WINDOWS = pygame.display.set_mode((self.width, self.height))
        self.fpsClock = pygame.time.Clock()
        self.font = BitmapFont("assets/fasttracker2-style_12x12.png", 12, 12)
        self.BLACK = pygame.Color(0,0,0)
        self.state = None
        self.mouseClick = None

    def change_state(self, newState):
        if self.state is not None:
            self.state.on_exit()

        if newState is None:
            pygame.quit()
            sys.exit()
        else:
            newState.on_enter(self.state)
            self.state = newState

    def run(self, initialState):
        self.change_state(initialState)

        while True:
            self.mouseClick = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == MOUSEBUTTONUP:
                    self.mouseClick = event.pos

            self.state.update(self.fpsClock.get_time())
            self.WINDOWS.fill(self.BLACK)
            self.state.draw(self.WINDOWS)
        
            pygame.display.update()
            self.fpsClock.tick(30)

class Block:
    def __init__(self, x, y, blockType=EMPTY):
        self.x = x
        self.y = y
        self.blockType = blockType
        self.num = 0
        self.state = CLOSED


class Board:
    def __init__(self, width, height, mines):
        self.height = height
        self.width = width
        self.arr = []
        self.mines = mines
        self.minesPos = []
        self.randomFlag = False
        self.sumOpen = self.width * self.height - self.mines
        self.currentsumOpen = 0

        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(Block(i, j))
            self.arr.append(row)

    def neighbors(self, x, y):
        dist = []
        direction = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))
        for i in direction:
            newX = x + i[0]
            newY = y + i[1]
            if newX >= 0 and newX < self.width and newY >= 0 and newY < self.height:
                dist.append((newX, newY))
        return dist

    def randomMines(self, x, y):
        i = 0
        neighbor = self.neighbors(x, y)

        while i < self.mines:
            randomX = random.randint(0, self.width-1)
            randomY = random.randint(0, self.height-1)

            if randomX == x and randomY == y:
                continue

            elif (randomX, randomY) in neighbor:
                continue

            elif self.arr[randomX][randomY].blockType == MINES:
                continue
            
            self.arr[randomX][randomY].blockType = MINES
            self.minesPos.append((randomX, randomY))
            i += 1
        self.randomFlag = True

    def printBoard(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.arr[i][j].state == CLOSED:
                    print(" ", end="")
                elif self.arr[i][j].blockType == MINES:
                    print("X", end="")
                elif self.arr[i][j].num > 0:
                    print(self.arr[i][j].num, end="")
        
                else:
                    print(".", end="")
            print()

    def number(self):
        for i, j in self.minesPos:
            for x, y in self.neighbors(i, j):
                if self.arr[x][y].blockType == EMPTY:
                    self.arr[x][y].num += 1
    
    def open(self, x, y):
        if self.arr[x][y].blockType == MINES or self.arr[x][y].state == OPENED:
            return 
        if self.arr[x][y].num > 0:
            self.arr[x][y].state = OPENED
            self.currentsumOpen += 1
            return
        self.arr[x][y].state = OPENED
        self.currentsumOpen += 1
        openneighbors = self.neighbors(x, y)
        for i in openneighbors:
            self.open(i[0], i[1])


    def openCell(self, x, y):

        if not self.randomFlag:
            self.randomMines(x, y)
            self.number()
            self.open(x, y)
            return CONTINUE
        
        if self.arr[x][y].blockType == MINES:
            for i, j in self.minesPos:
                self.arr[i][j].state = OPENED
            return END

        self.open(x, y)
        
        if self.currentsumOpen == self.sumOpen:
            return WIN
        else:
            return CONTINUE
        
        






if __name__ == '__main__':
    board = Board(14, 18, 30)
    board.openCell(6, 6)
    board.printBoard()
    
            






            
