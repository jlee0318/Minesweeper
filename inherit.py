from game import GameState, Runner, Board
import pygame
from pygame.locals import *
from bitmapfont import BitmapFont
import game

class MainMenu(GameState):
    def __init__(self, runner, nextState):
        super().__init__(runner)
        self.nextState = nextState
        self.arr = ["START", "EXIT"]
        self.currentSelection = 0
        self.delayTime = 200

    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        if self.delayTime > 0:
            self.delayTime -= deltatime
        else:
            if keys[K_UP]:
                self.currentSelection = 0
                self.delayTime = 200
            elif keys[K_DOWN]:
                self.currentSelection = 1
                self.delayTime = 200

            elif keys[K_SPACE]:
                if self.currentSelection == 0:
                    self.runner.change_state(self.nextState)
                    self.delayTime = 200

                else:
                    self.runner.change_state(None)
                    self.delayTime = 200

        if self.delayTime < 0:
            self.delayTime = 0

    def draw(self, surface):
        self.runner.font.centre(surface, "MINESWEEPER", self.runner.height * 0.3)
        for i, j in enumerate(self.arr):
            if i == self.currentSelection:
                msg = ">" + j + "<"
            else:
                msg = j
            self.runner.font.centre(surface, msg, self.runner.height * 0.5 + 18* i)


class OptionMenu(GameState):
    def __init__(self, runner, mainmenuState, InGameState):
        super().__init__(runner)
        self.mainmenuState = mainmenuState
        self.InGameState = InGameState
        self.mines = 30
        self.arr = ["Mines " + str(self.mines), "Start", "Return"]
        self.currentSelection = 0
        self.delayTime = 200

    def on_enter(self, mainmenuState):
        self.mines = 30
        self.currentSelection = 0
        self.arr = ["Mines " + str(self.mines), "Start", "Return"]


    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        if self.delayTime > 0:
            self.delayTime -= deltatime

        else:

            if keys[K_UP] and self.currentSelection > 0:
                self.currentSelection -= 1
                self.delayTime = 200
            elif keys[K_DOWN] and self.currentSelection < 2:
                self.currentSelection += 1
                self.delayTime = 200
            elif keys[K_LEFT] and self.currentSelection == 0 and self.mines > 20:
                self.mines -= 1
                self.arr[0] = "Mines " + str(self.mines)
                self.delayTime = 200
            elif keys[K_RIGHT] and self.currentSelection == 0 and self.mines < 40:
                self.mines += 1
                self.arr[0] = "Mines " + str(self.mines)
                self.delayTime = 200
            elif keys[K_SPACE]:
                if self.currentSelection == 1:
                    self.runner.change_state(self.InGameState)
                    self.delayTime = 200
                elif self.currentSelection == 2:
                    self.runner.change_state(self.mainmenuState)
                    self.delayTime = 200

        if self.delayTime < 0:
            self.delayTime = 0


    def draw(self, surface):
        self.runner.font.centre(surface, "Setup", self.runner.height * 0.3)
        for i, j in enumerate(self.arr):
            if i == self.currentSelection:
                msg = ">" + j + "<"
            else:
                msg = j
            self.runner.font.centre(surface, msg, self.runner.height * 0.5 + 18* i)

class InGame(GameState):
    def __init__(self, runner, mainmenuState, rows, col):
        super().__init__(runner)
        self.mainmenuState = mainmenuState
        self.minesImage = pygame.image.load("assets/mine.png")
        self.openedImage = pygame.image.load("assets/opened.png")
        self.hiddenImage = pygame.image.load("assets/hidden.png")
        self.font = BitmapFont("assets/colorfont.png", 12, 12)
        self.rows = rows
        self.col = col
        self.endFlag = False

    def on_enter(self, OptionMenuState):
        self.mines = OptionMenuState.mines
        self.board = Board(self.col, self.rows, self.mines)
        self.endFlag = False
        #self.board.openCell(5,5)

    def draw(self, surface):
        for i in range(self.rows):
            for j in range(self.col):
                x, y = j * 32, i * 32
                rect = Rect(x, y, 32, 32)
                currentCell = self.board.arr[j][i]
                if currentCell.state == game.CLOSED:
                    surface.blit(self.hiddenImage, rect)
                elif currentCell.blockType == game.MINES:
                    surface.blit(self.minesImage, rect)
                else:
                    surface.blit(self.openedImage, rect)
                    if currentCell.num > 0:
                        self.font.draw(surface, str(currentCell.num), x+10, y+10)

    def update(self, deltatime):
        if self.runner.mouseClick is not None and not self.endFlag:
            mouseX, mouseY = self.runner.mouseClick
            x = int(mouseX/32)
            y = int(mouseY/32)

            openCell = self.board.openCell(x, y)
            #print(openCell)
            if openCell != game.CONTINUE:
                self.endFlag = True
        elif self.endFlag:
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                self.runner.change_state(self.mainmenuState)
                #print(x, y)
            


            







    


        

if __name__ == '__main__':
    runner = Runner('Minesweeper', 14*32, 18*32)
    mainmenu = MainMenu(runner, None)
    optionmenu = OptionMenu(runner, mainmenu, None)
    ingamemenu = InGame(runner, mainmenu, 14, 18)
    mainmenu.nextState = optionmenu
    optionmenu.InGameState = ingamemenu
    runner.run(mainmenu)




    
