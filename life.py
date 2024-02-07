import pygame
import time
import random
import fileinput

random.seed(0)

color = input("Would you like random colors? (y/n): ")

# cell class
class Cell(pygame.sprite.Sprite):
    def __init__(self, life, x, y):
        super().__init__()
        self.surf = pygame.Surface((100,100))
        if life:
            self.alive = True
            if color == 'y':
                self.surf.fill((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
            else:
                self.surf.fill((255, 255, 255))
        else:
            self.alive = False
            self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(center = (x, y))

    def update(self, life):
        if life:
            self.surf.fill((128,255,40))
        else:
            self.surf.fill((0,0,0))
        self.alive = life

    def getAlive(self):
        return self.alive




def getNumberOfAliveAround(board, row, col):
    numAlive = 0
    if(row != 0):
        if(board[row-1][col].getAlive() == True):
            numAlive += 1
    if(row != len(board) - 1):
        if(board[row+1][col].getAlive() == True):
            numAlive += 1
    
    if(col != 0):
        if(board[row][col-1].getAlive() == True):
            numAlive += 1
    if(col != len(board[row]) - 1):
        if(board[row][col+1].getAlive() == True):
            numAlive += 1
    
    if(row != 0):
        if(col != 0):
            if(board[row-1][col-1].getAlive() == True):
                numAlive += 1
        if(col != len(board[row]) - 1):
            if(board[row-1][col+1].getAlive() == True):
                numAlive += 1
    if(row != len(board) - 1):
        if(col != 0):
            if(board[row+1][col-1].getAlive() == True):
                numAlive += 1
        if(col != len(board[row]) - 1):
            if(board[row+1][col+1].getAlive() == True):
                numAlive += 1

    return numAlive

def printBoard(board):
    for row in board:
        print("")
        for col in row:
            print(col.getAlive(), end = " ")

def updateBoard(board):
    newBoard = []
    for row in range(len(board)):
        newRow = []
        for col in range(len(board[row])):
            numAlive = getNumberOfAliveAround(board, row, col)
            if(board[row][col].getAlive() == True):
                if(numAlive < 2):
                    tempCell = Cell(life=False, x=((col*100) + 50), y=((row*100)+50))
                    newRow.append(tempCell)
                    # newRow[col].update(False)
                if(numAlive == 2 or numAlive == 3):
                    tempCell = Cell(life=True, x=((col*100) + 50), y=((row*100)+50))
                    newRow.append(tempCell)
                if(numAlive > 3):
                    tempCell = Cell(life=False, x=((col*100) + 50), y=((row*100)+50))
                    newRow.append(tempCell)
            else:
                if(numAlive == 3):
                    tempCell = Cell(life=True, x=((col*100) + 50), y=((row*100)+50))
                    newRow.append(tempCell)
                else:
                    tempCell = Cell(life=False, x=((col*100) + 50), y=((row*100)+50))
                    newRow.append(tempCell)
        newBoard.append(newRow)
    return newBoard


board = []
width = 100
height = 100
fileForInput = input("Would you like to use a file for input (if no then it will use manual)? (y/n): ")
if fileForInput.lower() == 'y':
    print("Enter your file name")
    filename = input("FILENAME> ")

    i = 0

    for line in fileinput.input(files = filename):
        lineSep = line.split(' ')
        if i == 0:
            width = int(lineSep[0]) * 100
            height = int(lineSep[1][:-1]) * 100
            i += 1
            continue
        else:
            tempList = []
            for x in range(len(lineSep)):
                if lineSep[x][0] == 'D':
                    tempCell = Cell(life=False, x=((x*100) + 50), y=((i*100)+50))
                    tempList.append(tempCell)
                else:
                    tempCell = Cell(life=True, x=((x*100) + 50), y=((i*100)+50))
                    tempList.append(tempCell)
            board.append(tempList)
        

if fileForInput.lower() != 'y':
    width = int(input("COLUMNS> ")) * 100
    height = int(input("ROWS> ")) * 100

if fileForInput.lower() != 'y':
    # creates board from inputs
    board = []
    for i in range(int(height/100)):
        row = input("Row"+str(i)+">")
        row = row.split(" ")
        tempList = []
        for cell in range(len(row)):
            if row[cell] == "D":
                tempCell = Cell(life=False, x=((cell*100) + 50), y=((i*100)+50))
                tempList.append(tempCell)
            else:
                tempCell = Cell(life=True, x=((cell*100) + 50), y=((i*100)+50))
                tempList.append(tempCell)

        board.append(tempList)

pygame.init()
# FramePerSec = pygame.time.Clock()
displaySurface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")


all_sprites = pygame.sprite.Group()
for row in board:
    for entity in row:
        all_sprites.add(entity)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == 256:
            pygame.quit()

    displaySurface.fill((0,0,0))

    for entity in all_sprites:
        displaySurface.blit(entity.surf, entity.rect)
 
    # printBoard(board)
    pygame.display.update()
    board = updateBoard(board)
    all_sprites = pygame.sprite.Group()
    for row in board:
        for entity in row:
            all_sprites.add(entity)
    time.sleep(1)
