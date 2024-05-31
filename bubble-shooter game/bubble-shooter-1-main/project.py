import math,random,os,sys,time,pygame,copy
import pygame.gfxdraw
from  pygame.locals import *
FPS          = 120
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480
TEXT_HEIGHT   = 20
BUBBLE_RADIUS = 20
BUBBLE_WIDTH  = BUBBLE_RADIUS * 2
BUBBLE_LAYERS = 5
BUBBLE_ADJUST = 5
X = WINDOW_WIDTH / 2
Y = WINDOW_HEIGHT - 27
ARRAYWIDTH = 16
ARRAYHEIGHT = 14
## specifying the colors##         
##           R    G    B  ##
BLACK =(0,0,0)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
RIGHT = 'right'
LEFT  = 'left'
BLANK = '.'
Background_COLOR = WHITE
COLORLIST = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN]
## create a class that creats a rect attribute,defines the position,color,dim of an object ##
class Bubble(pygame.sprite.Sprite):
## creating the constructor ##
    def __init__(self, color, row=0, column=0):
       ## calling the parent class constructor##   
        super().__init__()
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.centerx = X
        self.rect.centery = Y
        self.speed = 10
        self.color = color
        self.radius = BUBBLE_RADIUS
        self.row = row
        self.column = column
        self.angle = 0

    def update(self):

        if self.angle == 90:
            move_x = 0
            move_y = self.speed * -1
        elif self.angle < 90:
            move_x= self.xcalculate(self.angle)
            move_y = self.ycalculate(self.angle)
        elif self.angle > 90:
            move_x = self.xcalculate(180 - self.angle) * -1
            move_y= self.ycalculate(180 - self.angle)
        

        self.rect.x += move_x
        self.rect.y += move_y
    def xcalculate(self, angle):
        radians = math.radians(angle)
        
        move_x = math.cos(radians)*(self.speed)
        return move_x
    def ycalculate(self, angle):
        radians = math.radians(angle)
        
        move_y = math.sin(radians)*(self.speed) * -1
        return move_y

 ## for creating the filled circles##

    def draw(self):
        ## draws the filled circle(surface,X(coordinate of center of the circle),Y,R ##

        pygame.gfxdraw.filled_circle(SURFACE , self.rect.centerx, self.rect.centery, self.radius, self.color)
        pygame.gfxdraw.aacircle(SURFACE, self.rect.centerx, self.rect.centery, self.radius, BLACK)
class Arrow(pygame.sprite.Sprite):
      def __init__(self):
         super().__init__()
         self.angle=90
         arrowImage = pygame.image.load('Arrow.png')
         arrowImage.convert_alpha()
         arrowRect = arrowImage.get_rect()
         self.image = arrowImage
         self.transformImage = self.image
         self.rect = arrowRect
         self.rect.centerx = X 
         self.rect.centery = Y

      def update(self, direction):
        
         if direction == LEFT and self.angle < 180:
            self.angle += 1
         elif direction == RIGHT and self.angle > 0:        
            self.angle -= 1
   
         self.transformImage = pygame.transform.rotate(self.image, self.angle)
         self.rect = self.transformImage.get_rect()
         self.rect.centerx = X 
         self.rect.centery = Y
      def draw(self):
          SURFACE.blit(self.transformImage, self.rect)
class Score(object):
    def __init__(self):
        self.total = 0
        self.font = pygame.font.SysFont('Helvetica', 20)
        self.render = self.font.render('Score: ' + str(self.total), True, BLACK, WHITE)
        self.rect = self.render.get_rect()
        self.rect.left = 5
        self.rect.bottom = WINDOW_HEIGHT -5
        
        
    def update(self, deleteList):
        self.total += ((len(deleteList)) * 10)
        self.render = self.font.render('Score: ' + str(self.total), True, BLACK, WHITE)

    def draw(self):
        SURFACE.blit(self.render, self.rect)
def main():
    global FPSCLOCK, SURFACE, DISPLAYRECT, MAINFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('BOUNCING BALL')
    MAINFONT = pygame.font.SysFont('Helvetica', TEXT_HEIGHT)
    SURFACE, DISPLAYRECT = makeDisplay()
    while True:
        score, winorlose = runGame()
        endScreen(score, winorlose)
def runGame():
    gameColorList = copy.deepcopy(COLORLIST)
    direction = None
    launchBubble = False
    newBubble = None
    arrow = Arrow()
    bubbleArray = makeBlankBoard()
    setBubbles(bubbleArray, gameColorList)
    
    nextBubble = Bubble(gameColorList[0])
    nextBubble.rect.right = WINDOW_WIDTH - 5
    nextBubble.rect.bottom = WINDOW_HEIGHT - 5

    score = Score()
    while True:
         SURFACE.fill(Background_COLOR)
        
         for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT):
                    direction = LEFT
                elif (event.key == K_RIGHT):
                    direction = RIGHT
                    
            elif event.type == KEYUP:
                direction = None
                if event.key == K_SPACE:
                    launchBubble = True
                elif event.key == K_ESCAPE:
                    terminate()

         if launchBubble == True:
            if newBubble == None:
                newBubble = Bubble(nextBubble.color)
                newBubble.angle = arrow.angle
                

            newBubble.update()
            newBubble.draw()
            
            
            if newBubble.rect.right >= WINDOW_WIDTH - 5:
                newBubble.angle = 180 - newBubble.angle
            elif newBubble.rect.left <= 5:
                newBubble.angle = 180 - newBubble.angle


            launchBubble, newBubble, score = stopBubble(bubbleArray, newBubble, launchBubble, score)

            finalBubbleList = []
            for row in range(len(bubbleArray)):
                for column in range(len(bubbleArray[0])):
                    if bubbleArray[row][column] != BLANK:
                        finalBubbleList.append(bubbleArray[row][column])
                        if bubbleArray[row][column].rect.bottom > (WINDOW_HEIGHT - arrow.rect.height - 10):
                            return score.total, 'lose'

            
            
            if len(finalBubbleList) < 1:
                return score.total, 'win'
                                        
                        
            
            gameColorList = updateColorList(bubbleArray)
            random.shuffle(gameColorList)
            
                    
                            
            if launchBubble == False:
                
                nextBubble = Bubble(gameColorList[0])
                nextBubble.rect.right = WINDOW_WIDTH - 5
                nextBubble.rect.bottom = WINDOW_HEIGHT - 5
         nextBubble.draw()
         if launchBubble == True:
            coverNextBubble()
        
         arrow.update(direction)
         arrow.draw()


        
         setArrayPos(bubbleArray)
         drawBubbleArray(bubbleArray)

         score.draw()

            
        
         pygame.display.update()
         FPSCLOCK.tick(FPS)


## creating a blank board ##

def makeBlankBoard():
    array = []
    
    for row in range(ARRAYHEIGHT):
        column = []
        for i in range(ARRAYWIDTH):
            column.append(BLANK)
        array.append(column)

    return array
## setting the bubbles to the window##

def setBubbles(array, gameColorList):
    for row in range(BUBBLE_LAYERS):
        for column in range(len(array[row])):
            random.shuffle(gameColorList)
            newBubble = Bubble(gameColorList[0], row, column)
            array[row][column] = newBubble 
            
    setArrayPos(array)
def setArrayPos(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.x = (BUBBLE_WIDTH * column) + 5
                array[row][column].rect.y = (BUBBLE_WIDTH * row) + 5

    for row in range(1, ARRAYHEIGHT, 2):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.x += BUBBLE_RADIUS
                

    for row in range(1, ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.y -= (BUBBLE_ADJUST * row)

    deleteExtraBubbles(array)

def deleteExtraBubbles(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                if array[row][column].rect.right > WINDOW_WIDTH:
                    array[row][column] = BLANK



def updateColorList(bubbleArray):
    newColorList = []

    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[0])):
            if bubbleArray[row][column] != BLANK:
                newColorList.append(bubbleArray[row][column].color)

    colorSet = set(newColorList)

    if len(colorSet) < 1:
        colorList = []
        colorList.append(WHITE)
        return colorList

    else:

        return list(colorSet)
def checkForFloaters(bubbleArray):
    bubbleList = [column for column in range(len(bubbleArray[0]))
                         if bubbleArray[0][column] != BLANK]

    newBubbleList = []

    for i in range(len(bubbleList)):
        if i == 0:
            newBubbleList.append(bubbleList[i])
        elif bubbleList[i] > bubbleList[i - 1] + 1:
            newBubbleList.append(bubbleList[i])

    copyOfBoard = copy.deepcopy(bubbleArray)

    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[0])):
            bubbleArray[row][column] = BLANK
    

    for column in newBubbleList:
        popFloaters(bubbleArray, copyOfBoard, column)
def popFloaters(bubbleArray, copyOfBoard, column, row=0):
    if (row < 0 or row > (len(bubbleArray)-1)
                or column < 0 or column > (len(bubbleArray[0])-1)):
        return
    
    elif copyOfBoard[row][column] == BLANK:
        return

    elif bubbleArray[row][column] == copyOfBoard[row][column]:
        return

    bubbleArray[row][column] = copyOfBoard[row][column]
    

    if row == 0:
        popFloaters(bubbleArray, copyOfBoard, column + 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column - 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column,     row + 1)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row + 1)

    elif row % 2 == 0:
        popFloaters(bubbleArray, copyOfBoard, column + 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column - 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column,     row + 1)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column,     row - 1)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row - 1)

    else:
        popFloaters(bubbleArray, copyOfBoard, column + 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column - 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column,     row + 1)
        popFloaters(bubbleArray, copyOfBoard, column + 1, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column,     row - 1)
        popFloaters(bubbleArray, copyOfBoard, column + 1, row - 1)
def stopBubble(bubbleArray, newBubble, launchBubble, score):
    deleteList = []
   
    
    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[row])):
            
            if (bubbleArray[row][column] != BLANK and newBubble != None):
                if (pygame.sprite.collide_rect(newBubble, bubbleArray[row][column])) or newBubble.rect.top < 0:
                    if newBubble.rect.top < 0:
                        newRow, newColumn = addBubbleToTop(bubbleArray, newBubble)
                        
                    elif newBubble.rect.centery >= bubbleArray[row][column].rect.centery:

                        if newBubble.rect.centerx >= bubbleArray[row][column].rect.centerx:
                            if row == 0 or (row) % 2 == 0:
                                newRow = row + 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                
                            else:
                                newRow = row + 1
                                newColumn = column + 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                        elif newBubble.rect.centerx < bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row + 1
                                newColumn = column - 1
                                if newColumn < 0:
                                    newColumn = 0
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                            else:
                                newRow = row + 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                    elif newBubble.rect.centery < bubbleArray[row][column].rect.centery:
                        if newBubble.rect.centerx >= bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row - 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                            else:
                                newRow = row - 1
                                newColumn = column + 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                        elif newBubble.rect.centerx <= bubbleArray[row][column].rect.centerx:
                            if row == 0 or row % 2 == 0:
                                newRow = row - 1
                                newColumn = column - 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                
                            else:
                                newRow = row - 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn


                    popBubbles(bubbleArray, newRow, newColumn, newBubble.color, deleteList)
                    
                    if len(deleteList) >= 3:
                        for pos in deleteList:
                           
                            row = pos[0]
                            column = pos[1]
                            bubbleArray[row][column] = BLANK
                        checkForFloaters(bubbleArray)
                        
                        score.update(deleteList)

                    launchBubble = False
                    newBubble = None

    return launchBubble, newBubble, score

                    

def addBubbleToTop(bubbleArray, bubble):
    posx = bubble.rect.centerx
    leftSidex = posx - BUBBLERADIUS

    columnDivision = math.modf(float(leftSidex) / float(BUBBLEWIDTH))
    column = int(columnDivision[1])

    if columnDivision[0] < 0.5:
        bubbleArray[0][column] = copy.copy(bubble)
    else:
        column += 1
        bubbleArray[0][column] = copy.copy(bubble)

    row = 0
    

    return row, column
def popBubbles(bubbleArray, row, column, color, deleteList):
    if row < 0 or column < 0 or row > (len(bubbleArray)-1) or column > (len(bubbleArray[0])-1):
        return

    elif bubbleArray[row][column] == BLANK:
        return
    
    elif bubbleArray[row][column].color != color:
        return

    for bubble in deleteList:
        if bubbleArray[bubble[0]][bubble[1]] == bubbleArray[row][column]:
            return

    deleteList.append((row, column))

    if row == 0:
        popBubbles(bubbleArray, row,     column - 1, color, deleteList)
        popBubbles(bubbleArray, row,     column + 1, color, deleteList)
        popBubbles(bubbleArray, row + 1, column,     color, deleteList)
        popBubbles(bubbleArray, row + 1, column - 1, color, deleteList)

    elif row % 2 == 0:
        
        popBubbles(bubbleArray, row + 1, column,         color, deleteList)
        popBubbles(bubbleArray, row + 1, column - 1,     color, deleteList)
        popBubbles(bubbleArray, row - 1, column,         color, deleteList)
        popBubbles(bubbleArray, row - 1, column - 1,     color, deleteList)
        popBubbles(bubbleArray, row,     column + 1,     color, deleteList)
        popBubbles(bubbleArray, row,     column - 1,     color, deleteList)

    else:
        popBubbles(bubbleArray, row - 1, column,     color, deleteList)
        popBubbles(bubbleArray, row - 1, column + 1, color, deleteList)
        popBubbles(bubbleArray, row + 1, column,     color, deleteList)
        popBubbles(bubbleArray, row + 1, column + 1, color, deleteList)
        popBubbles(bubbleArray, row,     column + 1, color, deleteList)
        popBubbles(bubbleArray, row,     column - 1, color, deleteList)
            


def drawBubbleArray(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].draw()
def makeDisplay():
    SURFACE= pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    DISPLAYRECT = SURFACE.get_rect()
    SURFACE.fill(Background_COLOR)
    SURFACE.convert()
    pygame.display.update()

    return SURFACE, DISPLAYRECT
    
 
def terminate():
    pygame.quit()
    sys.exit()
def coverNextBubble():
    whiteRect = pygame.Rect(0, 0, BUBBLE_WIDTH, BUBBLE_WIDTH)
    whiteRect.bottom = WINDOW_HEIGHT
    whiteRect.right = WINDOW_WIDTH
    pygame.draw.rect(SURFACE, Background_COLOR, whiteRect)
def endScreen(score, winorlose):
    endFont = pygame.font.SysFont('Helvetica', 20)
    endMessage1 = endFont.render('You ' + winorlose + '! Your Score is ' + str(score) + '. Press Enter to Play Again.', True, BLACK, Background_COLOR)
    endMessage1Rect = endMessage1.get_rect()
    endMessage1Rect.center = DISPLAYRECT.center

    SURFACE.fill(Background_COLOR)
    SURFACE.blit(endMessage1, endMessage1Rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_RETURN:
                    return
                elif event.key == K_ESCAPE:
                    terminate()
main()


                                                                                                                                            


    
    



 



         
        


   
