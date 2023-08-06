import pygame
import numpy
import random
import time

"6/16: added rudimentary animal reproduction"

"""
6/15: animal movement should be working as intended now - reproduction next and then done with v1?
"""

"""
6/14:
weird animal error fixed - used placement code more similar to plant one
next: animal movement/reproduction
"""

"""
6/13:
see lines in 180s - something very wrong with both generating way too many animals and not displaying them
"""

"""
6/11:
fixed disappearing error
worked on animals eating plants - still a Q or two to sort out there
next: animal movement/reproduction
"""

"end of 6/6: find out why plants disappear soon after spawning even on high starting energy (consider 5/24 bullet point)"
"""
NEXT CHANGES (end of 5/24):
fix new plants dying immediately (probably just tinkering w variables)
 - should plants have an energy constant (or range) or half of the original's energy?
make animals move (toward plants if possible, randomly if not)
make animals eat plants
"""


"""
NEXT CHANGES (end of 2/25):
add animal populate function
add delay of X turns before animals are populated
add animal interaction with plants to grid (already on base code)
change newXSplit functions as noted
find way to update label every turn
"""


def populateBoard(gridSize, startPlants, energyPerPlantMin, energyPerPlantMax):
    """Creates a board and populates it with plants based on entry parameters"""
    blankDict = {"plantY": False, "pEnergy": 0, "animalY": False, "aEnergy": 0} #to fill in "blank" spaces
    arr = []
    for i in range(gridSize): #creates grid of dimensions (gridSize,gridSize), fills with blankDict
        row = []
        for j in range(gridSize):
            #arr[i][j] = blankDict
            row.append(blankDict)
        arr.append(row)
    for i in range(startPlants): #adds startPlants number of plants to the starting grid in random locations
        x1 = random.randint(0, gridSize - 1)
        y1 = random.randint(0, gridSize - 1)
        if arr[x1][y1]["plantY"] == False:  #checks to make sure there isn't a plant there already
            arr[x1][y1] = {"plantY": True, "pEnergy": random.randrange(energyPerPlantMin,energyPerPlantMax), "animalY": False, "aEnergy": 0}
        else: #if there is, a different spot is picked
            "recursion here? or just a while loop"
            # a = random.randint(0, gridSize - 1)
            # b = random.randint(0, gridSize - 1)
            # (arr[a][b]) = {"plantY": True, "pEnergy": random.randrange(energyPerPlantMin,energyPerPlantMax), "animalY": False, "aEnergy": 0}
    return arr

grid = populateBoard(15,20,15,25) #creates the grid

# print(grid)

# dic1 = {"one": True, "two": False}
# dic2 = {"one": False, "two": True}
#
# grid = [[dic1,dic1,dic2,dic1,dic2],[dic1,dic1,dic2,dic1,dic2],[dic1,dic1,dic2,dic1,dic2],[dic1,dic1,dic2,dic1,dic2],[dic1,dic1,dic2,dic1,dic2]]

BLACK = (0, 0, 0) #sets colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

color = WHITE

WIDTH = 25 #width/height/margin of each square in the grid
HEIGHT = 25
MARGIN = 5

gridSize = 15 #the number of rows/columns in the grid
turns = 100 #the number of turns to be iterated
turn = 1

animalIntroTurn = 10  # the turn on which animals are introduced to the board
numAnimals = 10  # number of animals

plantGainPerTurn = 3 #the amount of energy each plant gains per turn #think abt varying energy per day or changing plant spawn energy or something so they don't all split at once
animalDailyLoss = 1 #the amount of energy each animal loses per turn


plantDivMin = 22 #the amount of energy a plant will divide if it surpasses
plantDivCost = 0 #the amount of energy it costs a plant to divide
animalDivMin = 20
animalDivCost = 0


enPerPlantMin = 15 #energy that each plant/animal starts with
enPerPlantMax = 25
enPerAnimalMin = 15
enPerAnimalMax = 25
"MAKE SURE THIS LINES UP WITH INPUT VALUE - SCOPE ISSUE"
"these vals dictate animal spawn info and plant "

eatRate = 5

def newPlantSplit(x, y, originalEnergy):
    """Creates a new plant on an adjacent square"""
    # grid[x][y]["plantY"] = True
    # grid[x][y]["pEnergy"] = thing["pEnergy"] // 2
    grid[x][y] = {"plantY": True, "pEnergy": originalEnergy // 2, "animalY": False, "aEnergy": 0}


def newAnimalSplit(x,y,originalEnergy):
    """Creates a new animal on an adjacent square""" #need two animals to split? 
    # grid[x][y]["animalY"] = True
    # grid[x][y]["aEnergy"] = thing["aEnergy"] // 2
    grid[x][y] = {"plantY": False, "pEnergy": 0, "animalY": True, "aEnergy": grid[x][y]["aEnergy"] // 2}

def animalMove(x,y,newX,newY):
    origSquare = grid[x][y]
    moveSquare = grid[newX][newY]
    origEnergy = origSquare["aEnergy"]
    origSquare["animalY"] = False
    origSquare["aEnergy"] = 0
    moveSquare["animalY"] = True
    moveSquare["aEnergy"] = origEnergy

pygame.init()

WINDOW_SIZE = [500,500] #sets pixel size of screen
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Title") #see if caption can be changed to update as turns go on

done = False #keeps window open

clock = pygame.time.Clock() #not actually sure what this does

screen.fill(BLACK) #sets background color

blankDict = {"plantY": False, "pEnergy": 0, "animalY": False, "aEnergy": 0}

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True #if user Xes out, close window

    for row in range(gridSize): #color things
        for col in range(gridSize):
            loc = grid[row][col]
            if loc is not None and loc != blankDict: #if the location exists (not sure if this is necessary in updated format) #dunno if the blankDict half is necessary either
                if loc["plantY"] == True and loc["animalY"] == True: #if it's a plant, color is green, if plant and animal, color is yellow
                        color = BLUE
                elif loc["plantY"] == True and loc["animalY"] == False:
                        color = GREEN
                elif loc["plantY"] == False and loc["animalY"] == True:
                    color = RED
                else: #if nothing, white
                    color = WHITE
            else:
                color = WHITE
            pygame.draw.rect(screen, color,
                            [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH, HEIGHT]) #draws/updates the grid

    clock.tick(60) #runs fine without this but not sure if it needs to be kept

    pygame.display.flip() #updates grid visualization

    "Plant functionality things:"

    if turn <= turns:
        print("Turn: ", turn) #test
        if turn == animalIntroTurn: #on the animal intro turn, add animals
            """populate board with animals"""
            for i in range(numAnimals):
                x = random.randint(0, gridSize - 1)
                y = random.randint(0, gridSize - 1)

                "counter test"
                animalCount = 0
                for p in range(gridSize):
                    for q in range(gridSize):
                        pqSquare = grid[p][q]
                        if pqSquare["animalY"] == True:
                            animalCount = animalCount + 1
                print("ANIMALS, TURN: ", animalCount, i+1)

                print(x,y)
                square = grid[x][y] #changed square to grid[x][y] in later references
                print(square)
                if grid[x][y]["animalY"] == False:
                    if grid[x][y]["plantY"] == True:
                        grid[x][y] = {"plantY": False, "pEnergy": 0, "animalY": True, "aEnergy": random.randrange(enPerAnimalMin,enPerAnimalMax)}
                    else:
                        pEn = grid[x][y]["pEnergy"]
                        grid[x][y] = {"plantY": True, "pEnergy": pEn, "animalY": True, "aEnergy": random.randrange(enPerAnimalMin,enPerAnimalMax)}
                    # grid[x][y]["animalY"] = True
                    # grid[x][y]["aEnergy"] = random.randrange(enPerAnimalMin,enPerAnimalMax)
            print(grid)

        for row in range(gridSize): #Loops through every element of the grid
            for col in range(gridSize):
                thing = grid[row][col] #gives cell a name for easy referencing

                if (thing["plantY"] == True) and (thing["animalY"] == True): #if there is a plant AND an animal on the square
                    "animal takes energy from plant"
                    thing["pEnergy"] = thing["pEnergy"] - eatRate #plant loses certain amount of energy
                    thing["aEnergy"] = thing["aEnergy"] + eatRate # animal gains that amount
                    "decide whether plant should still gain energy from sun/animal should still lose (some?) energy"

                    if thing["pEnergy"] <= 0: #same check for plant death as in plant directions
                        thing["plantY"] = False
                        thing["pEnergy"] = 0

                elif thing["plantY"] == True: #if there is ONLY a plant on the square
                    if thing["pEnergy"] <= 0: #if the plant is dead
                        thing["plantY"] = False #plant dies - reset all plant attributes
                        thing["pEnergy"] = 0
                    else:
                        thing["pEnergy"] = thing["pEnergy"] + plantGainPerTurn #gains energy from sun

                        if thing["pEnergy"] >= plantDivMin: #if enough energy to divide
                            thing["pEnergy"] = thing["pEnergy"] - plantDivCost #Plant loses division cost
                            thing["pEnergy"] = thing["pEnergy"] // 2  # Halves original energy

                            posList = ["upleft","upmid","upright","left","right","downleft","downmid","downright"] #make sure they split onto an empty
                            dir = random.choice(posList) #picks a random adjacent square

                            if dir == "upleft": #this bit is very clunky/space consuming but works - change anyway? #could do one for vert and one for horiz
                                row2 = row-1
                                col2 = col-1
                            elif dir == "upmid":
                                row2 = row-1
                                col2 = col
                            elif dir == "upright":
                                row2 = row-1
                                col2 = col+1
                            elif dir == "left":
                                row2 = row
                                col2 = col-1
                            elif dir == "right":
                                row2 = row
                                col2 = col+1
                            elif dir == "downleft":
                                row2 = row+1
                                col2 = col-1
                            elif dir == "downmid":
                                row2 = row+1
                                col2 = col
                            elif dir == "downright":
                                row2 = row+1
                                col2 = col+1

                            if row2 >= gridSize:
                                row2 = 0
                            elif row2 < 0:
                                row2 = gridSize - 1

                            if col2 >= gridSize:
                                col2 = 0
                            elif col2 < 0:
                                col2 = gridSize - 1

                            newPlantSplit(row2, col2,thing["pEnergy"])

                elif thing["animalY"] == True: #if there is ONLY an animal on the square
                    thing["aEnergy"] = thing["aEnergy"] - animalDailyLoss #animal burns some energy

                    if thing["aEnergy"] <= 0: #if the animal is dead
                        thing["animalY"] = False #animal dies - reset all animal attributes
                        thing["aEnergy"] = 0

                    elif thing["plantY"] == False: #the animal only moves if there is no plant on its current square
                        "1/9 chance that animal stays still"
                        rowList = [row-1,row,row+1]
                        newRow = random.choice(rowList)

                        colList = [col - 1,col, col + 1]
                        newCol = random.choice(colList)

                        if newRow >= gridSize:
                            newRow = 0
                        elif newRow < 0:
                            newRow = gridSize - 1

                        if newCol >= gridSize:
                            newCol = 0
                        elif newCol < 0:
                            newCol = gridSize - 1


                        if grid[newRow][newCol]["animalY"] == False:

                            pEnOrig = grid[row][col]["pEnergy"]
                            aEnOrig = grid[row][col]["aEnergy"] #original cell's animal energy (to be transported when it moves)
                            pEnNew = grid[newRow][newCol]["pEnergy"] #new cell's plant energy (to be kept on new cell)

                            if grid[row][col]["plantY"] == True: #this if statement shouldn't be true but just in case
                                grid[row][col] = {"plantY": True, "pEnergy": pEnOrig, "animalY": False, #sets original location to animal-less
                                              "aEnergy": 0}
                            elif grid[row][col]["plantY"] == False:
                                grid[row][col] = {"plantY": False, "pEnergy": False, "animalY": False,
                                                  "aEnergy": 0}

                            if grid[newRow][newCol]["plantY"] == True:
                                grid[newRow][newCol] = {"plantY": True, "pEnergy": pEnNew, "animalY": True,
                                              "aEnergy": aEnOrig}
                            elif grid[newRow][newCol]["plantY"] == False:
                                grid[newRow][newCol] = {"plantY": False, "pEnergy": 0, "animalY": True,
                                              "aEnergy": aEnOrig}
                    if thing["aEnergy"] >= animalDivMin:
                        """note - this means animal will only reproduce when not eating (which is good, i think)"""
                        rowList = [row - 1, row, row + 1]
                        newRow2 = random.choice(rowList)

                        colList = [col - 1, col, col + 1]
                        newCol2 = random.choice(colList)

                        if newRow2 >= gridSize:
                            newRow2 = 0
                        elif newRow2 < 0:
                            newRow2 = gridSize - 1

                        if newCol2 >= gridSize:
                            newCol2 = 0
                        elif newCol2 < 0:
                            newCol2 = gridSize - 1 #up to here is just spot selection stuff

                        aEnOrig2 = grid[row][col]["aEnergy"]  # original cell's animal energy (to be transported when it moves)
                        pEnNew2 = grid[newRow2][newCol2]["pEnergy"]  # new cell's plant energy (to be kept on new cell)

                        if grid[newRow2][newCol2]["animalY"] == False: #find a way to make it keep searching for a different square if animalY is true
                            if grid[newRow2][newCol2]["plantY"] == True:
                                grid[newRow2][newCol2] = {"plantY": True, "pEnergy": pEnNew2, "animalY": True, "aEnergy": aEnOrig2 // 2}
                            elif grid[newRow2][newCol2]["plantY"] == False:
                                grid[newRow2][newCol2] = {"plantY": False, "pEnergy": 0, "animalY": True, "aEnergy": aEnOrig2 // 2}






        turn = turn + 1

        pygame.draw.rect(screen, color,
                         [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN,
                          WIDTH, HEIGHT])

        clock.tick(6)
        time.sleep(0.1)
        pygame.display.flip() #not sure if an additional set of grid update things within the loop is redundant

        # plantC = 0
        # for row in range(gridSize):
        #     for col in range(gridSize):
        #         loc = grid[row][col]
        #         if 'plantY' in loc:
        #             print("YES")
        #         print(loc)
        #         if loc['PlantY'] == True:
        #             plantC = plantC + 1
        # print("Turn: ", turn)
        # print("Plants: ", plantC)


pygame.quit()


