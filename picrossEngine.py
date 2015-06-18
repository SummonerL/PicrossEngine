"""Picross Engine"""

#Our necessary imports
import pygame, sys

#initialize pygame
pygame.init()

#Declare constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
GAME_TITLE = "Picross Engine"

         #R   G   B
WHITE = (255,255,255)
BLACK = (0,  0,  0)
RED =   (255, 0, 0)
GREEN = (0, 255, 0)
BLUE =  (0, 0,   0)

GAME_FONT = "monospace"
FONT_SIZE = 15
HINT_FONT_SIZE = 12

BACKGROUND_COLOR = WHITE

BACKGROUND_FILE = "lib/background.jpg"

BOX_WIDTH = 15

#Set up the game environment
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption(GAME_TITLE)
screen.fill(BACKGROUND_COLOR)
background = pygame.image.load(BACKGROUND_FILE)

#Game Loop variables
exitGame = False

#Here are our game classes
class PicrossStage:
    length = 0
    columns = [[]]
    rows = [[]]
    stage = [[]]
    name = ""
    def __init__(self, length, stage, name):
        self.length = length
        self.stage = stage
        self.name = name
        self.columns = makeGridColumn(stage)
        self.rows = makeGridRow(stage)

class PicrossCollection:
    stages = []
    stageNames = []
    def __init__(self, picrossStage):
        self.stages.append(picrossStage)
        self.stageNames.append(picrossStage.name)

    def addStage(self, picrossStage):
        self.stages.append(picrossStage)
        self.stageNames.append(picrossStage.name)

class Box:
    width = 0
    enabled = False
    locationX = 0
    locationY = 0
    boxSprite = None 
    def __init__(self, width, locationX, locationY, enabled):
        self.width = width
        self.enabled = enabled
        self.locationX = locationX
        self.locationY = locationY
        self.boxSprite = pygame.Rect(self.locationX, self.locationY, self.width, self.width)
    def enable(self):
        self.enabled = True
    
#Here are our game functions
def makeGridColumn(stage):
    """This function calculates our column hints"""

    """Make a flipped version of stage"""
    newStage = [[]]
    column=[]
    for k in range(len(stage)):
        column = []
        for j in stage:
            column.append(j[k])
        newStage.append(column)
    newStage.pop(0)
    """And now the code is pretty much the same as makeGridRow"""
    columnHint = [[]]
    singleColumn = []
    streak = 0
    for i in newStage:
        streak = 0
        for index,j in enumerate(i):
            if j==1:
                streak += 1
            else:
                if streak > 0:
                    singleColumn.append(streak)
                streak = 0
            if (streak > 0 and (index+1 == len(newStage))):
                singleColumn.append(streak)
        columnHint.append(singleColumn)
        singleColumn = []
    columnHint.pop(0)
    return columnHint
    
            
            
            
#End of makeGridColumn function
            
def makeGridRow(stage):
    """This function calculates our row hints"""
    rowHint = [[]]
    singleRow = []
    streak = 0
    for i in stage:
        streak = 0
        for index, j in enumerate(i):
            if j==1:
                streak += 1
            else:
                if streak > 0:
                    singleRow.append(streak)
                streak = 0
            if (streak > 0 and (index+1 == len(stage))):
                singleRow.append(streak)
        rowHint.append(singleRow)
        singleRow = []
    rowHint.pop(0)
    return rowHint
    
def grabStage(path, index):
    """This function returns a stage"""
    searchString = "[Stage %s]\n" % index
    startReading = False
    readCounter = 0
    stageName = ""
    stageLength = 100000
    stage = [[]]
    with open(path) as f:
        for s in f.readlines():
            if startReading:
                if readCounter == 0:
                    stageName = (s.replace("\n",""))
                if readCounter == 1:
                    stageLength = int(s.replace("\n",""))
                if (readCounter > 1 and readCounter <= (stageLength+1)):
                    s = s.replace("\n", "")
                    sList = list(s)
                    stage.append([int(x) for x in sList])
                if readCounter > (stageLength + 1):
                    startReading = False
                readCounter += 1
            else:
                if s == searchString:
                    startReading = True
    """Remove empty element from list"""
    stage.pop(0)

    """Create a new picross stage"""
    return PicrossStage(stageLength,stage,stageName)

#End of GrabStage function

#This function will simplify the label making process
def drawLabel(font, size, color, text, location):
    """Use the global screen"""
    global screen
    myFont = pygame.font.SysFont(font, size)
    myLabel = myFont.render(text,1,color)
    screen.blit(myLabel, location)
    

#Draw Stage Function
def drawStage(picrossCollection, index):
    """Let's blit the background to the screen first"""
    screen.blit(background,(0,0))
    """Here we write a label to the screen displaying the stage name      -                                                                 NAME LOCATION"""
    drawLabel(GAME_FONT, FONT_SIZE, BLACK, ("Stage: %s" % picrossCollection.stages[index].name),(int(SCREEN_WIDTH*.392),(int(SCREEN_HEIGHT*.1175))))
    """Let's declare some shortcut variables to make this process easier"""
    tempStage = picrossCollection.stages[index]
    tempGrid = []
    """Here we set the location of the puzzle depending on the size"""
    tempStartingPointX = 0
    tempStartingPointY = 0
    if (tempStage.length == 5):
        tempStartingPointX = (SCREEN_WIDTH * .43)
        tempStartingPointY = (SCREEN_HEIGHT * .47)
    elif (tempStage.length == 10):
        tempStartingPointX = (SCREEN_WIDTH * .36)
        tempStartingPointY = (SCREEN_HEIGHT * .39)
    else:
        tempStartingPointX = (SCREEN_WIDTH * .375)
        tempStartingPointY = (SCREEN_HEIGHT * .3125)

    """Here we print the row/column hints to the screen"""
    """ROW"""
    for i in range(tempStage.length):
            tempStr = str(tempStage.rows[i]).replace("[","").replace("]","").replace(","," ")
            drawLabel(GAME_FONT,HINT_FONT_SIZE,BLACK,tempStr,(tempStartingPointX * .6,(tempStartingPointY+BOX_WIDTH) + (i*BOX_WIDTH)) )
    """COLUMN"""
    for i in range(tempStage.length):
             tempStr = str(tempStage.columns[i]).replace("[","").replace("]","").replace(",","\n").replace(" ","")
             tempCount = tempStr.count('\n')+1
             for j in range(tempCount):
                 tempStrList = tempStr.split('\n')
                 drawLabel(GAME_FONT,HINT_FONT_SIZE,BLACK,tempStrList[j],((tempStartingPointX+BOX_WIDTH) + (i*BOX_WIDTH),tempStartingPointY *.65 + (j*BOX_WIDTH)))

    """TEMPORARY - HERE WE ENABLE THE SQUARES"""
    for i in range(tempStage.length):
        for j in range(tempStage.length):
            enabled = False
            if (tempStage.stage[i][j] == 1):
                enabled = True
            """Here we create our boxes and add them to the grid"""
            tempGrid.append(Box(BOX_WIDTH,(((j+1)*BOX_WIDTH)+tempStartingPointX),(((i+1)*BOX_WIDTH)+tempStartingPointY), enabled))
            enabled = False
    """Now let's draw us some boxes!"""
    for i in tempGrid:
        tempWidth = 1
        if (i.enabled):
            tempWidth = 0
        pygame.draw.rect(screen, BLACK, i.boxSprite,tempWidth)
        tempWidth = 1
            

#GameStart
"""THIS WILL BE A LOOP IN THE FUTURE"""
myCollection = PicrossCollection(grabStage("stages.txt", 1))
myCollection.addStage(grabStage("stages.txt", 2))
myCollection.addStage(grabStage("stages.txt", 3))
myCollection.addStage(grabStage("stages.txt", 4))
myCollection.addStage(grabStage("stages.txt", 5))
myCollection.addStage(grabStage("stages.txt", 6))
myCollection.addStage(grabStage("stages.txt", 7))
myCollection.addStage(grabStage("stages.txt", 8))
#This index will be the current stage in our stage collection
CURRENT_STAGE = 8

for stages in PicrossCollection.stages:
    print "STAGE NAME - ",
    print stages.name
    print "STAGE LAYOUT - "
    print stages.stage
    print "COLUMN HINT - "
    print stages.columns
    print "ROW HINT - "
    print stages.rows

#Here is our gameLoop
while not exitGame:
    #Cap our game at 30 fps
    clock.tick(30)

    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame = True

    #Draw our stage
    drawStage(myCollection,CURRENT_STAGE-1)
            
    #Display Update
    pygame.display.update()

#Program Exit
pygame.quit()
sys.exit()
