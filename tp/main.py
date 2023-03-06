#################################################

# 15-112 Term Project:
# Overcooked!
# Name: Yiting Zhang
# Andrew id: yitingzh

#################################################

import math, copy, random, pickle
from os.path import exists
import pandas as pd
from cmu_112_graphics import *

#################################################
# Citing
#################################################
# Special thanks to all the people who made and 
# released these awesome resources for free:
    # Icons by Emoji (https://twitter.com/googledocs/status/730087240156643328)
    # Figure Images by OVERCOOKED!
        # (https://ghosttowngames.com/overcooked-merchandise/)
        # ...

#################################################
# model
#################################################

def appStarted(app):
    # mode = ['title','level','instruction','NorthAmerica','Asia','gameOver','gameWin']
    # modeIndex = [0,1,2,3,4,5,6]
    app.modeIndex = 0
    app.name = 'Demo'
    app.timerDelay = 1000
    allOther(app)

# all helper
def allOther(app):
    # game
    dimensions(app)
    interface(app)
    informationDefine(app)
    tableLayOut(app)
    # modeLayout(app)
    restart(app)
    # gameEnd
    forGameEnd(app)

def canvasDimensions(app):
    rows = 15
    cols = 15
    cellSize = 30
    margin = 80
    return (rows, cols, cellSize, margin)

def dimensions(app):
    dimensions = canvasDimensions(app)
    app.rows = dimensions[0]
    app.cols = dimensions[1]
    app.cellSize = dimensions[2]
    app.margin = dimensions[3]

def interface(app):
    # mouse
    app.handX = -20
    app.handY = -20
    app.handImage = app.loadImage('hand.png')
    app.handTime = 1
    app.hintTime = 2
    # images
    app.iconImage = app.loadImage('icons.png')
    app.carImage = app.loadImage('car.png')
    # bg
    if app.modeIndex == 3:
        app.emptyColor = 'slategray4'
        app.board = [([app.emptyColor] * app.cols) for row in range(app.rows)]
    elif app.modeIndex == 4:
        app.emptyColor = 'burlywood1'
        app.board = [([app.emptyColor] * app.cols) for row in range(app.rows)]

def informationDefine(app):
    app.charNames = ['Crocodile','Platypus','Dog']
    app.charsColor = ['seagreen','deeppink2','cobalt']
    app.charsImage = ['Crocodile.png','Platypus.gif','Dog.png']
    app.image1 = app.loadImage(app.charsImage[0])
    app.image2 = app.image1.transpose(Image.FLIP_LEFT_RIGHT)
    app.image5 = app.loadImage(app.charsImage[2])
    app.image6 = app.image5.transpose(Image.FLIP_LEFT_RIGHT)
    '''
    drinkName = ['cone','coffee','tea']
    ingreName = ['fish','rice','herb','shrimp','potato','meat','tomato']
    foodName = ['sushi','poke','soup','burger','fries']
    '''
    # import all images
    app.imageFish   = app.loadImage('fish.png')
    app.imageRice   = app.loadImage('rice.png')
    app.imageHerb   = app.loadImage('herb.png')
    app.imageShrimp = app.loadImage('shrimp.png')
    app.imagePotato = app.loadImage('potato.png')
    app.imageMeat   = app.loadImage('meat.png')
    app.imageTomato = app.loadImage('tomato.png')
    app.imageCone   = app.loadImage('cone.png')
    app.imageCoffee = app.loadImage('coffee.png')
    app.imageTea    = app.loadImage('tea.png')
    app.imageSushi  = app.loadImage('sushi.png')
    app.imageCookSushi  = app.loadImage('cooksushi.png')
    app.imagePoke   = app.loadImage('poke.png')
    app.imageCookPoke   = app.loadImage('cookpoke.png')
    app.imageSoup   = app.loadImage('soup.png')
    app.imageCookSoup   = app.loadImage('cooksoup.png')
    app.imageBurger = app.loadImage('burger.png')
    app.imageCookBurger = app.loadImage('cookburger.png')
    app.imageFries  = app.loadImage('fries.png')
    app.imageCookFries  = app.loadImage('cookfries.png')
    # code them
    app.drinkCode = [[1,0,0],[0,1,0],[0,0,1]]
    app.foodCode = [[2,1,0,0,0,0,0],[0,1,1,1,0,0,0],[0,0,1,0,2,1,0],[0,0,2,0,0,1,1],[0,0,1,0,1,0,0]]
    # recipe
    app.imageRecipe = app.loadImage('recipe.png')
    # edge dog
    app.imageGameOverDog = app.loadImage('gameoverdog.png')

def restart(app):
    interface(app)
    modeLayout(app)
    app.gameStart = True
    app.game_score = 0
    app.game_time = 120
    app.isPaused = False
    app.isClickLegal = None
    app.instructShow = False
    app.recipeShow = False
    app.hintShow = False
    app.iconShow = True
    charParameter(app)
    placeRandomOrder(app) 

def charParameter(app):
    # player
    app.charRow = 4
    app.charCol = 3
    app.inHand = [[0,0,0,0,0,0,0],[0,0,0],[0,0,0,0,0]] # [[ingre],[drink],[food]]
    # customer
    app.customer = [(9,4), (9,7), (9,10), (9,13)]
    customerLocation(app)
    app.orders = [[[0,0,0,0,0,0,0],[0,0,0]], [[0,0,0,0,0,0,0],[0,0,0]],
                [[0,0,0,0,0,0,0],[0,0,0]], [[0,0,0,0,0,0,0],[0,0,0]]]

def placeRandomOrder(app):
    for i in range(len(app.orders)):
        if app.orders[i] == [[0,0,0,0,0,0,0],[0,0,0]]:
            if app.modeIndex == 3:
                app.orders[i][0] = app.foodCode[random.randint(3,4)]
                app.orders[i][1] = app.drinkCode[random.randint(0,1)]
            else:
                app.orders[i][0] = app.foodCode[random.randint(0,2)]
                app.orders[i][1] = app.drinkCode[random.randint(0,2)]

def tableLayOut(app):
    app.image3 = app.loadImage('table.png')
    app.table1Image = app.scaleImage(app.image3, 0.045)
    app.image4 = app.loadImage('graytable.png')
    app.table2Image = app.scaleImage(app.image4, 0.045)
    app.grid = [([0] * app.cols) for row in range(app.rows)]
    app.helpL = []   

def modeLayout(app):
    if app.modeIndex == 3:
        app.helpL = generateLayout(9)
    elif app.modeIndex == 4:
        app.helpL = generateLayout(3)
    if app.modeIndex == 3 or app.modeIndex == 4:    
        for (row, col) in app.helpL[0]:
            app.grid[row][col] = 1
        for (row, col) in app.helpL[1]:
            app.grid[row][col] = 2 

def customerLocation(app):
    for (row, col) in app.customer:
        app.grid[row][col] = 3

def forGameEnd(app):
    app.imageTitle = app.loadImage('title.png')
    app.imageGameStart = app.loadImage('7-continents.png')
    app.imageGameOver = app.loadImage('gameover.png')
    app.imageGameWin = app.loadImage('gamewin.png')

# bonus
# 01 save state  
def saveState(app):
    name = app.name
    modeIndex = app.modeIndex
    score = app.game_score
    inHand = app.inHand
    time = app.game_time
    row = app.charRow
    col = app.charCol
    orders = app.orders
    currList = [name, modeIndex, score, inHand, time, row, col, app.orders]
    #create the pickle file
    picklefile = open('currentPlayer', 'wb')
    #pickle the dataframe
    pickle.dump(currList, picklefile)
    #close file
    picklefile.close()

def loadState(app):
    #read the pickle file
    picklefile = open('currentPlayer', 'rb')
    #unpickle the dataframe
    loadedList = pickle.load(picklefile)
    #close file
    picklefile.close()
    print(loadedList)
    app.name = loadedList[0]
    app.modeIndex = loadedList[1]
    app.game_score = loadedList[2]
    app.inHand = loadedList[3]
    app.game_time = loadedList[4]
    app.charRow = loadedList[5]
    app.charCol = loadedList[6]
    app.orders = loadedList[7]
    modifiedRestart(app)

def modifiedRestart(app):
    interface(app)
    modeLayout(app)
    app.gameStart = True
    app.isPaused = True
    app.isClickLegal = None
    app.instructShow = False
    app.recipeShow = False
    app.hintShow = False
    app.iconShow = True
    app.customer = [(9,4), (9,7), (9,10), (9,13)]
    customerLocation(app)

# 02 leaderboard
def leaderboard(app):
    filename = 'leaderboard.csv'
    if exists(filename):
        df = pd.read_csv(filename)  
    else:
        df = pd.DataFrame({'Name': ['Null','Null','Null'],
                    'Score' : [3,2,1]})
        df.to_csv(filename,index=False)      
    currName = app.name
    currScore = app.game_score
    dfCurr = {'Name': currName, 'Score': currScore}
    df = df.append(dfCurr, ignore_index = True)
    df.drop(df[df['Score'] == df['Score'].min()].index, inplace=True)
    dfSorted = df.sort_values(by=['Score'], ascending=False)
    df.to_csv(filename,index=False)
    print(dfSorted.to_string(index=False))

#################################################
# main
#################################################

# cartesian to isometric coordinate
def cartToIso(x, y):
    isoX = x  - y
    isoY = (x + y)/2
    return (isoX, isoY)
# isometric to cartesian coordinate
def isoToCart(x, y):
    cartX = (y*2 + x)/2
    cartY = (y*2 - x)/2
    return (cartX, cartY)

# move char
def isMoveLegal(app, row, col):
    # for row in range(app.rows):
    #     for col in range(app.cols):
    #         if app.grid[row][col] == True:
                helpRow = app.charRow
                helpCol = app.charCol
                # 1. the cell is in fact on the board
                if (helpRow > row) or (helpRow < 0) or \
                    (helpCol > col) or (helpCol < 0):
                    return False
                else:
                    # 2. the color there on the board is emptyColor
                    if app.grid[helpRow][helpCol] != 0:
                        return False

def moveChar(app, dr, dc):
    # modifying the app values storing the location of the left-top corner
    app.charRow += dr
    app.charCol += dc
    if isMoveLegal(app, 8, app.cols - 1) == False:
        # undo the move
        app.charRow -= dr
        app.charCol -= dc
        return False
    else:
        return True

# place table
def placeEfficiently(startRow,endRow,startCol,endCol):
    L = []
    for row in range(startRow,endRow+1):
        for col in range(startCol,endCol+1):
            L.append((row,col))
    return L

def generateLayout(n):
    L = []
    #L = [[table1],[table2]]
    # '9' type
    if n == 9:
        L1 = placeEfficiently(0,0,0,14)
        L2 = placeEfficiently(1,14,0,0)
        L3 = placeEfficiently(14,14,1,14)
        L4 = placeEfficiently(1,8,14,14)
        L5 = placeEfficiently(8,8,4,13)
        L1.extend(L2)
        L1.extend(L3)
        L1.extend(L4)
        L1.extend(L5)
        Lpoint = [(8, 10)]
        L.append(L1)
        L.append(Lpoint)
    elif n == 3:
        L1 = placeEfficiently(0,0,0,14)
        L2 = placeEfficiently(1,14,0,0)
        L3 = placeEfficiently(14,14,1,14)
        L4 = placeEfficiently(1,8,14,14)
        L5 = placeEfficiently(8,8,4,13)
        L6 = placeEfficiently(4,4,4,10)
        L1.extend(L2)
        L1.extend(L3)
        L1.extend(L4)
        L1.extend(L5)
        L1.extend(L6)
        Lpoint = []
        L.append(L1)
        L.append(Lpoint)
    return L

# bouns
# 03 find the shortest ways to customers who player can serve, and draw
def ai_findThoseCustomers(app):
    # find target customers
    customers = []
    for i in range(len(app.orders)):
        index = i
        if app.orders[i] != [[0,0,0,0,0,0,0],[0,0,0]]:
            (orderFood, orderDrink) = (app.orders[i][0], app.orders[i][1])
            indexFood = app.foodCode.index(orderFood)
            indexDrink = app.drinkCode.index(orderDrink)
            # if food in hand >= 1:
            if app.inHand[2][indexFood] > 0 and app.inHand[1][indexDrink] > 0:
                customers.append(index)
    return customers

def ai_findShortestWay(app, index): # for easy mode/ hint
    # targetIndex to target R&C
    targets = ai_findThoseCustomers(app)
    if len(targets) == 0:
        return None
    else:
        (targetR, targetC) = app.customer[index]
        targetR = 7
        (startR, startC) = (app.charRow, app.charCol+1) # may change for 2nd player
        path = [(startR, startC)]
        if startR >= 4:
            path.append((targetR, startC))
            path.append((targetR, targetC))
        else:
            if startC <= 4 or startC >= 12:
                path.append((targetR, startC))
                path.append((targetR, targetC))
            else:
                if targetC < 5 or targetC > 11:
                    path.append((startR, targetC))
                    path.append((targetR, targetC))
                else:
                    if startC-4+abs(startC-targetC) >= 12-startC+abs(startC-targetC):
                        path.append((startR, 12))
                        path.append((targetR, 12))
                        path.append((targetR, targetC))
                    else:
                        path.append((startR, 4))
                        path.append((targetR, 4))
                        path.append((targetR, targetC))
        return path

def ai_getallpaths(app):
    paths = []
    targets = ai_findThoseCustomers(app)
    for index in targets:
        path = ai_findShortestWay(app, index)
        paths.append(path)
    return paths

#################################################
# controller
#################################################
def keyPressed(app, event):
    if (event.key == '0'):
        if app.modeIndex == 3 or app.modeIndex == 4 and app.gameStart != 120:
            saveState(app)
            print("Saved!! You can load by pressing '9' later")
    elif (event.key == '9'):
        loadState(app)
        print("Loaded!! Press 'p' to unpause.")
    elif (event.key == 'l'):
        if app.modeIndex == 6:
            leaderboard(app)
    # game mode (modeIndex = 3/4)
    if app.gameStart == True and app.game_time != 0:
        if (event.key == 'p'):
            app.isPaused = not app.isPaused
        elif (event.key == 'r'):
            restart(app)
        elif (event.key == 'w'):
            moveChar(app, -1, 0)
            app.charImage = app.scaleImage(app.image2,0.2)
        elif (event.key == 's'):
            moveChar(app, 1, 0)
            app.charImage = app.scaleImage(app.image1,0.2)
        elif (event.key == 'a'):
            moveChar(app, 0, -1)
            app.charImage = app.scaleImage(app.image1,0.2)
        elif (event.key == 'd'):
            moveChar(app, 0, 1)
            app.charImage = app.scaleImage(app.image2,0.2)

def mousePressed(app, event):
    (app.handX, app.handY) = (event.x, event.y)
    if app.modeIndex == 0:
        if 0 <= app.handX <= app.width and 0 <= app.handY <= app.height:
            app.modeIndex = 1
    elif app.modeIndex == 1:
        if 0 <= app.handX <= app.width and 0 <= app.handY <= app.height:
            app.modeIndex = 2
    elif app.modeIndex == 2:
        if 0 <= app.handX <= app.width and 0 <= app.handY <= app.height:
            app.modeIndex = 3
            allOther(app)
    elif app.modeIndex == 3 or app.modeIndex == 4:
        if app.game_time > 0:
            if 120 <= app.handX <= 160 and 25 <= app.handY <= 60:
                app.instructShow = not app.instructShow
                if app.instructShow == True:
                    app.isPaused = True
                else:
                    app.isPaused = False
            elif 75 <= app.handX <= 115 and 25 <= app.handY <= 60:
                app.recipeShow = not app.recipeShow
                if app.recipeShow == True:
                    app.isPaused = True
                else:
                    app.isPaused = False
            elif 30 <= app.handX <= 70 and 25 <= app.handY <= 60:
                app.hintShow = not app.hintShow
            app.handTime = 1
            app.hintTime = 2
            pickOrCookOrServe(app)
            if app.orders == [[[0,0,0,0,0,0,0],[0,0,0]], [[0,0,0,0,0,0,0],[0,0,0]],
                        [[0,0,0,0,0,0,0],[0,0,0]], [[0,0,0,0,0,0,0],[0,0,0]]]:
                placeRandomOrder(app)
        elif app.game_time == 0:
            if app.game_score < 30:
                app.modeIndex = 5
                app.gameStart = False
            else:
                if app.modeIndex == 3:
                    app.modeIndex = 4
                    restart(app)
                elif app.modeIndex == 4:
                    app.modeIndex = 6
    elif app.modeIndex == 5:
        if 0 <= app.handX <= app.width and 0 <= app.handY <= app.height:
            app.modeIndex = 2
            allOther(app)

def timerFired(app):
    if app.modeIndex == 3 or app.modeIndex == 4:
        app.gameStart == True
    if app.gameStart == True and app.isPaused == False:
        if app.game_time > 0:
            app.game_time -= 1
    if app.handTime != 0:
        app.handTime -= 1
    if app.hintTime != 0:
        app.hintTime -= 1

# get clicked cell and update counts
def getCell(app, x, y):
    rowNum = int((y - app.margin) / app.cellSize)+3
    colNum = int((x - app.margin) / app.cellSize)-8
    return (rowNum, colNum)
def isLegalList(L): # non-negative
    for ele in L:
        if ele < 0:
            return False
    else:
        return True

def legalCook(app, L1, L2, n):
    # L1 = inHand[0], L2 = ricipeOfOneFood
    temp = app.inHand[2][n]
    for i in range(len(L1)):
        L1[i] -= L2[i]
        app.inHand[2][n] = temp + 1
    if isLegalList(L1) == False:
        for i in range(len(L1)):
            L1[i] += L2[i]
        app.inHand[2][n] -= 1

def legalServe(app, n): # n means nth costumer
    (orderFood, orderDrink) = (app.orders[n][0], app.orders[n][1])
    if orderFood != [0,0,0,0,0,0,0] and orderDrink != [0,0,0]:
        # if food in hand >= 1:
        indexFood = app.foodCode.index(orderFood)
        indexDrink = app.drinkCode.index(orderDrink)
        if app.inHand[2][indexFood] > 0 and app.inHand[1][indexDrink] > 0:
            app.inHand[2][indexFood] -= 1
            app.inHand[1][indexDrink] -= 1
            if app.game_time >= 15:
                app.game_score += 6
            elif app.game_time < 15:
                if app.game_score < 24:
                    app.game_score += 8
                else:
                    app.game_score += 6
            app.orders[n] = [[0,0,0,0,0,0,0],[0,0,0]] # wait for the next turn

def pickOrCookOrServe(app):
    (cartHandX, cartHandY) = isoToCart(app.handX, app.handY + app.cellSize)
    (row, col) = getCell(app, cartHandX, cartHandY)
    limit = 10
    # isClickLegal
    if (app.charRow - 1 <= row <= app.charRow + 1) and \
        (app.charCol - 1 <= col <= app.charCol + 1):
        if app.modeIndex == 3:
            # pick
            if (row, col) == (1,0) and app.inHand[0][2] < limit: 
                app.inHand[0][2] += 1 # herb
            elif (row, col) == (2,0) and app.inHand[0][6] < limit: 
                app.inHand[0][6] += 1 # tomato
            elif (row, col) == (3,0) and app.inHand[0][4] < limit: 
                app.inHand[0][4] += 1 # potato
            elif (row, col) == (0,1) and app.inHand[0][5] < limit: 
                app.inHand[0][5] += 1 # meat
            elif (row, col) == (0,3) and app.inHand[1][0] < limit: 
                app.inHand[1][0] += 1 # cone
            elif (row, col) == (0,4) and app.inHand[1][1] < limit: 
                app.inHand[1][1] += 1 # coffee
            # cook
            elif (row, col) == (4,0): # burger
                legalCook(app, app.inHand[0], app.foodCode[3], 3)
            elif (row, col) == (5,0): # fries
                legalCook(app, app.inHand[0], app.foodCode[4], 4)
            # serve
            elif (row, col) == (7,4):
                legalServe(app, 0)
            elif (row, col) == (7,7):
                legalServe(app, 1)
            elif (row, col) == (7,10):
                legalServe(app, 2)
            elif (row, col) == (7,13):
                legalServe(app, 3)
        elif app.modeIndex == 4:
            # pick
            if (row, col) == (1,0) and app.inHand[0][2] < limit: 
                app.inHand[0][2] += 1 # herb
            elif (row, col) == (2,0) and app.inHand[0][1] < limit: 
                app.inHand[0][1] += 1 # rice
            elif (row, col) == (3,0) and app.inHand[0][4] < limit: 
                app.inHand[0][4] += 1 # potato
            elif (row, col) == (3,4) and app.inHand[0][0] < limit: 
                app.inHand[0][0] += 1 # fish
            elif (row, col) == (3,5) and app.inHand[0][3] < limit: 
                app.inHand[0][3] += 1 # shrimp
            elif (row, col) == (3,6) and app.inHand[0][5] < limit: 
                app.inHand[0][5] += 1 # meat
            elif (row, col) == (3,8) and app.inHand[1][0] < limit: 
                app.inHand[1][0] += 1 # cone
            elif (row, col) == (3,9) and app.inHand[1][1] < limit: 
                app.inHand[1][1] += 1 # coffee
            elif (row, col) == (3,10) and app.inHand[1][2] < limit: 
                app.inHand[1][2] += 1 # tea
            # cook
            elif (row, col) == (4,0): # sushi
                legalCook(app, app.inHand[0], app.foodCode[0], 0)
            elif (row, col) == (5,0): # poke
                legalCook(app, app.inHand[0], app.foodCode[1], 1)
            elif (row, col) == (6,0): # soup
                legalCook(app, app.inHand[0], app.foodCode[2], 2)
            # serve
            elif (row, col) == (7,4):
                legalServe(app, 0)
            elif (row, col) == (7,7):
                legalServe(app, 1)
            elif (row, col) == (7,10):
                legalServe(app, 2)
            elif (row, col) == (7,13):
                legalServe(app, 3)

#################################################
# View
#################################################

# instruction
def drawInstructionBg(app, canvas):
    if app.modeIndex == 2:
        canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = 'dimgray', width = 0)

def drawInstruction(app, canvas):
    # base
    canvas.create_rectangle(app.width*0.19,app.height*0.137,
                            app.width*0.81,app.height*0.863, 
                            fill = 'white', width = 3)
    canvas.create_rectangle(app.width*0.2,app.height*0.15,
                            app.width*0.8,app.height*0.25,
                            fill = 'lightsteelblue', 
                            outline = 'black', width = 0)
    
    canvas.create_rectangle(app.width*0.2,app.height*0.265,
                            app.width*0.8,app.height*0.85,
                            fill = 'slategrey', 
                            outline = 'black', width = 0)
    
    # text
    canvas.create_text(app.width//2 + 5, app.height*0.2 + 4,
                            fill = 'slategrey', 
                            text = "I N S T R U C T I O N S",
                            font = "Arial 24 bold italic")
    canvas.create_text(app.width//2, app.height*0.2,
                            fill = 'white', text = "I N S T R U C T I O N S",
                            font = 'Arial 24 bold italic')
    messages = ['Input you name as "app.name" before starting game.',
                '("w", "s", "a", "d") == (Up, Down, Left, Right)',
                '"p" == pause game       "r" == restart game',
                '"0" == save state           "9" == load state',
                '"l" == save and print the local leaderboard in terminal',
                '(You can save state after starting the game, unpause to',
                'start after loading. Try to save your score in leaderboard.)',
                'Click the icons in the upper left corner to show tips,',
                'recipes, and instructions, and click icons again to close.',
                '',
                'If ingredients or drinks is next to you, you can click them',
                'multiple times to collect (<= 10). For using the cooktop,',
                'click on the translucent foods. Get more than 30 to win!!!'
               ]
    i = 0
    while i < len(messages):
        canvas.create_text(app.width*0.23+2, app.height*0.3+2+i*25,
                            anchor = 'w', fill = 'black',
                            text = messages[i], font = 'Arial 12 italic')
        canvas.create_text(app.width*0.23, app.height*0.3+i*25, 
                            anchor = 'w', fill = 'white',
                            text = messages[i], font = 'Arial 12 italic')
        i += 1

def drawRecipe(app, canvas):
    # base
    canvas.create_rectangle(app.width*0.19,app.height*0.137,
                            app.width*0.81,app.height*0.863, 
                            fill = 'white', width = 3)
    canvas.create_rectangle(app.width*0.2,app.height*0.15,
                            app.width*0.8,app.height*0.25,
                            fill = 'burlywood', 
                            outline = 'black', width = 0) 
    # text
    canvas.create_text(app.width//2 + 5, app.height*0.2 + 4,
                            fill = 'burlywood4', 
                            text = 'R E C I P E',
                            font = 'Arial 24 bold italic')
    canvas.create_text(app.width//2, app.height*0.2,
                            fill = 'white', text = 'R E C I P E',
                            font = 'Arial 24 bold italic')
    # image
    canvas.create_image(app.width//2,app.height*0.58,image=ImageTk.PhotoImage(app.scaleImage(app.imageRecipe, 0.6)))
    canvas.create_text(app.width*0.37, app.height*0.3,
                            fill = 'gray', text = 'North America',
                            font = 'Arial 14 bold italic')
    canvas.create_text(app.width*0.3, app.height*0.55,
                            fill = 'gray', text = 'Asia',
                            font = 'Arial 14 bold italic')

# game_background
def game_drawCell(app, canvas, row, col, color):
    x0 = app.margin + col * app.cellSize
    y0 = app.margin + row * app.cellSize
    x1 = app.margin + (col+1) * app.cellSize
    y1 = app.margin + (row+1) * app.cellSize
    # canvas.create_polygon(x0,y0,x1,y0,x1,y1,x0,y1,
    #                         fill = color, outline = 'white', width = 1)
    (isoX0, isoY0) = cartToIso(x0,y0)
    (isoX1, isoY1) = cartToIso(x1,y0)
    (isoX2, isoY2) = cartToIso(x1,y1)
    (isoX3, isoY3) = cartToIso(x0,y1)
    move1 = app.width//2
    move2 = app.cellSize*2
    canvas.create_polygon(isoX0 + move1, isoY0 + move2,
                            isoX1 + move1, isoY1 + move2, 
                            isoX2 + move1, isoY2 + move2, 
                            isoX3 + move1, isoY3 + move2,
                            fill = color, outline = 'white', width = 1) 

def game_drawImage(app, canvas, row, col, image, color1, color2):
    x0 = app.margin + (col-1) * app.cellSize
    y0 = app.margin + (row-1) * app.cellSize
    (isoX0, isoY0) = cartToIso(x0,y0)
    move1 = app.width//2
    move2 = app.cellSize*2
    canvas.create_oval(isoX0 + move1 - 20, isoY0 + move2+10,
                        isoX0 + move1 + 20, isoY0 + move2+20,
                        fill = color1, width = 0)
    canvas.create_oval(isoX0 + move1 - 15, isoY0 + move2+12,
                        isoX0 + move1 + 15, isoY0 + move2+18,
                        outline = color2, width = 1)
    canvas.create_image(isoX0 + move1, isoY0 + move2,
                        image=ImageTk.PhotoImage(app.scaleImage(image,0.5)))  

def game_placeOnTable1(app, canvas):
    if app.modeIndex == 3:
        game_drawImage(app, canvas, 1, 0, app.imageHerb, 'black', 'gray')
        game_drawImage(app, canvas, 2, 0, app.imageTomato, 'black', 'gray')
        game_drawImage(app, canvas, 3, 0, app.imagePotato, 'black', 'gray')
        game_drawImage(app, canvas, 5, 0, app.imageCookBurger, 'red', 'tomato')
        game_drawImage(app, canvas, 6, 0, app.imageCookFries, 'red', 'salmon')
    elif app.modeIndex == 4:
        game_drawImage(app, canvas, 1, 0, app.imageHerb, 'black', 'gray')
        game_drawImage(app, canvas, 2, 0, app.imageRice, 'black', 'gray')
        game_drawImage(app, canvas, 3, 0, app.imagePotato, 'black', 'gray')
        game_drawImage(app, canvas, 5, 0, app.imageCookSushi, 'red', 'tomato')
        game_drawImage(app, canvas, 6, 0, app.imageCookPoke, 'red', 'salmon')
        game_drawImage(app, canvas, 7, 0, app.imageCookSoup, 'red', 'salmon')

def game_placeOnTable2(app, canvas):
    if app.modeIndex == 4:
        game_drawImage(app, canvas, 4, 4, app.imageFish, 'black', 'gray')
        game_drawImage(app, canvas, 4, 5, app.imageShrimp, 'black', 'gray')
        game_drawImage(app, canvas, 4, 6, app.imageMeat, 'black', 'gray')
        game_drawImage(app, canvas, 4, 8, app.imageCone, 'black', 'gray')
        game_drawImage(app, canvas, 4, 9, app.imageCoffee, 'black', 'gray')
        game_drawImage(app, canvas, 4, 10, app.imageTea, 'black', 'gray')
    elif app.modeIndex == 3:
        game_drawImage(app, canvas, 0, 1, app.imageMeat, 'black', 'gray')
        game_drawImage(app, canvas, 0, 3, app.imageCone, 'black', 'gray')
        game_drawImage(app, canvas, 0, 4, app.imageCoffee, 'black', 'gray')

def game_drawBoard(app, canvas):
    # bg
    canvas.create_rectangle(0, 0, app.width, app.height//2,
                            fill = 'slategray3', width = 0)
    canvas.create_rectangle(0, app.height//2, app.width, app.height,
                            fill = 'dimgray', width = 0)
    # road
    canvas.create_polygon(0, app.height//2, 
                            0, app.height*0.8,
                            app.width//2, app.height*1.1,
                            app.width, app.height*0.8, 
                            app.width, app.height//2,
                            fill = 'lightyellow4',
                            outline = 'lightyellow3', width = 4)
    # pavement
    canvas.create_line(0, app.height*0.82,
                            app.width//2, app.height*1.12,
                            app.width, app.height*0.82,
                            fill = 'goldenrod', width = 4)
    # wall
    canvas.create_polygon(0, app.height//4 + 20, app.width//2, 0,
                            app.width//2, -15, 0, app.height//4,
                            fill = 'maroon', width = 0)
    canvas.create_polygon(app.width, app.height//2 + 20, app.width//2, 0,
                            app.width//2, -15, app.width, app.height//4, 
                            fill = 'maroon', width = 0)
    canvas.create_polygon(0, app.height//4 + 20, app.width//2, 0,
                            app.width//2, app.height//2, 0, app.height//2, 
                            fill = 'darksalmon', outline = 'tomato', width = 2)
    canvas.create_polygon(app.width, app.height//4 + 20, app.width//2, 0,
                            app.width//2, app.height//2, app.width, app.height//2, 
                            fill = 'darksalmon', outline = 'tomato', width = 2)
    # floor
    for row in range(app.rows):
        for col in range(app.cols):
            game_drawCell(app, canvas, row, col, app.board[row][col])
    for row in range(app.rows):
        for col in range(app.cols):
            if (row + col) % 2 == 0:
                game_drawCell(app, canvas, row, col, 'wheat')
    # entry
    for row in range(9,14):
        game_drawCell(app, canvas, row, 14, 'gray32')
    game_drawCell(app, canvas, 10, 14, 'darkred')
    game_drawCell(app, canvas, 11, 14, 'red')
    game_drawCell(app, canvas, 12, 14, 'darkred') 

def game_drawIcon(app, canvas):
    if app.iconShow == True:
        # base
        canvas.create_rectangle(app.cellSize, app.cellSize*0.8,
                                app.cellSize*5.8, app.cellSize*2.3,
                                outline = 'white', width = 2)
        canvas.create_rectangle(app.cellSize*0.8, app.cellSize*0.6,
                                app.cellSize*5.6, app.cellSize*2.12,
                                fill = 'white', width = 2)
        # icon
        canvas.create_image(app.cellSize*3.25, app.cellSize*1.35,
                                image=ImageTk.PhotoImage(app.scaleImage(app.iconImage,0.25)))
    canvas.create_image(app.width*0.9, app.height*0.9,
                                image=ImageTk.PhotoImage(app.scaleImage(app.carImage,0.8)))

# game_parameter
def game_drawPack(app, canvas):
    color = 'gray40'
    font = 'Arial 14 bold'
    if app.modeIndex == 3:
        # bg
        canvas.create_rectangle(app.width*0.74, app.cellSize*0.8, 
                                app.width-app.cellSize*0.6, app.height*0.384,
                                outline = 'white', width = 2)
        canvas.create_rectangle(app.width*0.73, app.cellSize*0.6, 
                                app.width-app.cellSize*0.8, app.height*0.375,
                                fill = 'white', width = 2)
        # ingre
        canvas.create_image(app.width*0.77, app.cellSize*1.5,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageHerb,0.5)))
        canvas.create_text(app.width*0.815, app.cellSize*1.5, text = str(app.inHand[0][2]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.87, app.cellSize*1.5,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageMeat,0.5)))
        canvas.create_text(app.width*0.915, app.cellSize*1.5, text = str(app.inHand[0][5]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.77, app.cellSize*3,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imagePotato,0.5)))
        canvas.create_text(app.width*0.815, app.cellSize*3, text = str(app.inHand[0][4]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.87, app.cellSize*3,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageTomato,0.5)))
        canvas.create_text(app.width*0.915, app.cellSize*3, text = str(app.inHand[0][6]),
                            fill = color, font = font)
        # drink
        canvas.create_image(app.width*0.77, app.cellSize*4.8,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageCone,0.5)))
        canvas.create_text(app.width*0.815, app.cellSize*4.8, text = str(app.inHand[1][0]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.87, app.cellSize*4.8,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageCoffee,0.5)))
        canvas.create_text(app.width*0.915, app.cellSize*4.8, text = str(app.inHand[1][1]),
                            fill = color, font = font)
        # food
        canvas.create_image(app.width*0.77, app.cellSize*6.6,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageBurger,0.5)))
        canvas.create_text(app.width*0.815, app.cellSize*6.6, text = str(app.inHand[2][3]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.87, app.cellSize*6.6,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageFries,0.5)))
        canvas.create_text(app.width*0.915, app.cellSize*6.6, text = str(app.inHand[2][4]),
                            fill = color, font = font)
        # split line
        canvas.create_line(app.width*0.75, app.cellSize*4, 
                            app.width*0.948, app.cellSize*4,
                            fill = 'lightgray', width = 2)
        canvas.create_line(app.width*0.75, app.cellSize*5.7, 
                            app.width*0.948, app.cellSize*5.7,
                            fill = 'lightgray', width = 2)
    elif app.modeIndex == 4:
        # bg
        canvas.create_rectangle(app.width*0.63, app.cellSize*0.6, 
                                app.width-app.cellSize*0.8, app.height*0.375,
                                fill = 'white', width = 2)
        # ingre and their nums
        canvas.create_image(app.width*0.67, app.cellSize*1.5,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageHerb,0.5)))
        canvas.create_text(app.width*0.715, app.cellSize*1.5, text = str(app.inHand[0][2]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.77, app.cellSize*1.5,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageMeat,0.5)))
        canvas.create_text(app.width*0.815, app.cellSize*1.5, text = str(app.inHand[0][5]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.87, app.cellSize*1.5,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imagePotato,0.5)))
        canvas.create_text(app.width*0.915, app.cellSize*1.5, text = str(app.inHand[0][4]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.67, app.cellSize*3,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageRice,0.5)))
        canvas.create_text(app.width*0.715, app.cellSize*3, text = str(app.inHand[0][1]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.77, app.cellSize*3,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageFish,0.5)))
        canvas.create_text(app.width*0.815, app.cellSize*3, text = str(app.inHand[0][0]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.87, app.cellSize*3,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageShrimp,0.5)))
        canvas.create_text(app.width*0.915, app.cellSize*3, text = str(app.inHand[0][3]),
                            fill = color, font = font)
        # drink
        canvas.create_image(app.width*0.67, app.cellSize*4.8,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageCone,0.5)))
        canvas.create_text(app.width*0.715, app.cellSize*4.8, text = str(app.inHand[1][0]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.77, app.cellSize*4.8,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageCoffee,0.5)))
        canvas.create_text(app.width*0.815, app.cellSize*4.8, text = str(app.inHand[1][1]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.87, app.cellSize*4.8,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageTea,0.5)))
        canvas.create_text(app.width*0.915, app.cellSize*4.8, text = str(app.inHand[1][2]),
                            fill = color, font = font)
        # food
        canvas.create_image(app.width*0.67, app.cellSize*6.6,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageSushi,0.5)))
        canvas.create_text(app.width*0.715, app.cellSize*6.6, text = str(app.inHand[2][0]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.77, app.cellSize*6.6,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imagePoke,0.5)))
        canvas.create_text(app.width*0.815, app.cellSize*6.6, text = str(app.inHand[2][1]),
                            fill = color, font = font)
        canvas.create_image(app.width*0.87, app.cellSize*6.6,
                            image=ImageTk.PhotoImage(app.scaleImage(app.imageSoup,0.5)))
        canvas.create_text(app.width*0.915, app.cellSize*6.6, text = str(app.inHand[2][2]),
                            fill = color, font = font)
        # split line
        canvas.create_line(app.width*0.65, app.cellSize*4, 
                            app.width*0.948, app.cellSize*4,
                            fill = 'lightgray', width = 2)
        canvas.create_line(app.width*0.65, app.cellSize*5.7, 
                            app.width*0.948, app.cellSize*5.7,
                            fill = 'lightgray', width = 2)

def game_drawScore(app, canvas):
    # base
    (x0, y0, x1, y1) = (app.cellSize, app.height - app.cellSize*3, \
                        app.cellSize*3, app.height - app.cellSize)
    canvas.create_oval(x0, y0, x1, y1, fill = 'gold', 
                        outline = 'goldenrod', width = 2)
    canvas.create_oval(x0 + app.cellSize*0.4, y0 + app.cellSize*0.4, 
                        x1 - app.cellSize*0.4, y1 - app.cellSize*0.4, 
                        fill = 'goldenrod', outline = 'darkgoldenrod', width = 2)                      
    # text
    canvas.create_text(app.cellSize*1.93+3, app.height - app.cellSize*2+3, 
                        text = str(app.game_score),
                        fill = 'goldenrod4', font = "Arial 24 bold italic")
    canvas.create_text(app.cellSize*1.93, app.height - app.cellSize*2, 
                        text = str(app.game_score),
                        fill = 'white', font = "Arial 24 bold italic")

def game_drawTimer(app, canvas):
    # base
    (x0, y0, x1, y1) = (app.width - app.cellSize*3, 
                        app.height - app.cellSize*3,
                        app.width - app.cellSize, 
                        app.height - app.cellSize)
    canvas.create_oval(x0, y0, x1, y1, fill = 'lightsteelblue', 
                        outline = 'slategrey', width = 2)
    canvas.create_oval(x0 + app.cellSize*0.4, y0 + app.cellSize*0.4, 
                        x1 - app.cellSize*0.4, y1 - app.cellSize*0.4, 
                        fill = 'slategrey', outline = 'white', width = 2)
    # text
    minite = app.game_time//60
    second = app.game_time%60
    canvas.create_text(app.width - app.cellSize*2+3, app.height - app.cellSize*2+3, 
                        text = f'{minite:02d}'+':'+f'{second:02d}',
                        fill = 'darkslategray', font = "Arial 24 bold italic")                    
    canvas.create_text(app.width - app.cellSize*2, app.height - app.cellSize*2, 
                        text = f'{minite:02d}'+':'+f'{second:02d}',
                        fill = 'white', font = "Arial 24 bold italic")

def game_drawTimeOut(app, canvas):
    # base
    canvas.create_rectangle(0, app.height//2 - app.cellSize,
                        app.width, app.height//2 + app.cellSize,
                        fill = 'gold', outline = 'orange', width = 2)
    canvas.create_rectangle(0, app.height//2 - app.cellSize*1.2,
                        app.width, app.height//2 + app.cellSize*1.2,
                        outline = 'white', width = 5)
    # text
    canvas.create_text(app.width//2 + 3, app.height//2 - 2, 
                        text = "TIME'S UP!",
                        fill = 'cyan4', font = "Arial 40 bold italic")
    canvas.create_text(app.width//2 + 5, app.height//2 - 3, 
                        text = "TIME'S UP!",
                        fill = 'cyan4', font = "Arial 40 bold italic")
    canvas.create_text(app.width//2, app.height//2, 
                        text = "TIME'S UP!",
                        fill = 'cyan3', font = "Arial 40 bold italic")

# game_layout & chars
def game_drawStove(app, canvas):
    for row in range(4, 7):
        game_drawCell(app, canvas, row, -1, 'darkred')
def game_drawchar(app, canvas):
    index = 0
    x = app.margin + app.charCol * app.cellSize
    y = app.margin + app.charRow * app.cellSize
    (isoX, isoY) = cartToIso(x, y)
    (move1, move2) = (720//2, app.cellSize*2)
    (newX, newY) = (isoX + move1, isoY + move2 - app.cellSize*1.2)
    canvas.create_oval(newX-20, newY+45,newX+20, newY+55,
                        fill = app.charsColor[index], 
                        outline = 'white', width = 1)
    canvas.create_image(newX, newY,
                        image=ImageTk.PhotoImage(app.scaleImage(app.image1,0.2)))
    canvas.create_text(newX+8, newY - app.cellSize*1.4,
                        fill = app.charsColor[index], 
                        anchor = 's', text = "Player",
                        font = 'Arial 14 bold italic')
    canvas.create_text(newX+6, newY - app.cellSize*1.4-2,
                        fill = 'white', anchor = 's', text = "Player",
                        font = 'Arial 14 bold italic')

def game_drawTables1(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):           
            x = app.margin + col * app.cellSize
            y = app.margin + row * app.cellSize
            (isoX, isoY) = cartToIso(x, y)
            (move1, move2) = (720//2, app.cellSize*2)
            (newX, newY) = (isoX + move1 - app.cellSize*0.05, 
                            isoY + move2)
            if app.grid[row][col] == 1:
                canvas.create_image(newX, newY,
                                    image=ImageTk.PhotoImage(app.table1Image))
            elif app.grid[row][col] == 2:
                canvas.create_image(newX, newY,
                                    image=ImageTk.PhotoImage(app.table2Image))

def game_drawTables2(app, canvas):
    for row in range(app.charRow, app.rows):
        for col in range(app.charCol, app.cols):
            x = app.margin + col * app.cellSize
            y = app.margin + row * app.cellSize
            (isoX, isoY) = cartToIso(x, y)
            (move1, move2) = (720//2, app.cellSize*2)
            (newX, newY) = (isoX + move1 - app.cellSize*0.05, 
                            isoY + move2)
            if app.grid[row][col] == 1:
                canvas.create_image(newX, newY,
                                    image=ImageTk.PhotoImage(app.table1Image))
            elif app.grid[row][col] == 2:
                canvas.create_image(newX, newY,
                                    image=ImageTk.PhotoImage(app.table2Image))

def game_drawCounter(app,canvas):
    for col in range(3, 13):
        game_drawCell(app, canvas, 7, col, 'turquoise4')

def game_drawSelection1(app, canvas):
    direct = [(-1, 0), (0, -1), (-1, -1)]
    for (drow, dcol) in direct:
        row = app.charRow + drow
        col = app.charCol + dcol
        if 0 <= row < app.rows and 0 <= col < app.cols and app.grid[row][col] != 0:
            x0 = app.margin + col * app.cellSize
            y0 = app.margin + row * app.cellSize
            x1 = app.margin + (col+1) * app.cellSize
            y1 = app.margin + (row+1) * app.cellSize
            (isoX0, isoY0) = cartToIso(x0,y0)
            (isoX1, isoY1) = cartToIso(x1,y0)
            (isoX2, isoY2) = cartToIso(x1,y1)
            (isoX3, isoY3) = cartToIso(x0,y1)
            move1 = app.width//2
            move2 = app.cellSize
            canvas.create_line(isoX0 + move1, isoY0 + move2,
                                isoX1 + move1, isoY1 + move2, 
                                fill = 'red', width = 3)
            canvas.create_line(isoX1 + move1, isoY1 + move2,
                                isoX2 + move1, isoY2 + move2, 
                                fill = 'red', width = 3)
            canvas.create_line(isoX2 + move1, isoY2 + move2,
                                isoX3 + move1, isoY3 + move2, 
                                fill = 'red', width = 3)
            canvas.create_line(isoX3 + move1, isoY3 + move2,
                                isoX0 + move1, isoY0 + move2, 
                                fill = 'red', width = 3)

def game_drawSelection2(app, canvas):
    direct = [(1, 0), (0, 1), (1, 1),(1, -1), (-1, 1)]
    for (drow, dcol) in direct:
        row = app.charRow + drow
        col = app.charCol + dcol
        if 0 <= row < app.rows and 0 <= col < app.cols and app.grid[row][col] != 0:
            x0 = app.margin + col * app.cellSize
            y0 = app.margin + row * app.cellSize
            x1 = app.margin + (col+1) * app.cellSize
            y1 = app.margin + (row+1) * app.cellSize
            (isoX0, isoY0) = cartToIso(x0,y0)
            (isoX1, isoY1) = cartToIso(x1,y0)
            (isoX2, isoY2) = cartToIso(x1,y1)
            (isoX3, isoY3) = cartToIso(x0,y1)
            move1 = app.width//2
            move2 = app.cellSize
            canvas.create_line(isoX0 + move1, isoY0 + move2,
                                isoX1 + move1, isoY1 + move2, 
                                fill = 'red', width = 3)
            canvas.create_line(isoX1 + move1, isoY1 + move2,
                                isoX2 + move1, isoY2 + move2, 
                                fill = 'red', width = 3)
            canvas.create_line(isoX2 + move1, isoY2 + move2,
                                isoX3 + move1, isoY3 + move2, 
                                fill = 'red', width = 3)
            canvas.create_line(isoX3 + move1, isoY3 + move2,
                                isoX0 + move1, isoY0 + move2, 
                                fill = 'red', width = 3)

def game_drawCustomer(app, canvas): 
    for i in range(len(app.customer)):
        (row, col) = app.customer[i]
        x = app.margin + col * app.cellSize
        y = app.margin + row * app.cellSize
        (isoX, isoY) = cartToIso(x, y)
        (move1, move2) = (720//2, app.cellSize*1.3)
        (newX, newY) = (isoX + move1 - app.cellSize*0.05, isoY + move2)
        # image
        canvas.create_oval(newX+10, newY-15, newX+50, newY-5, fill = 'white', outline = 'gray', width = 1)
        canvas.create_oval(newX+16, newY-13, newX+44, newY-7, fill = 'white', outline = 'lightgray', width = 2)
        canvas.create_image(newX, newY, image=ImageTk.PhotoImage(app.scaleImage(app.image6, 0.18)))
        if app.orders[i] != [[0,0,0,0,0,0,0],[0,0,0]]:
            # order bubble
            canvas.create_rectangle(newX-120, newY-10, newX-30, newY+30,
                                    fill = 'white', outline = 'darkgray', width = 2)
            canvas.create_polygon(newX-33, newY+29, newX-33, newY+19, newX-15, newY+29,
                                    fill = 'white', width = 0)
            canvas.create_line(newX-30, newY+30, newX-15, newY+30, newX-30, newY+20,
                                    fill = 'darkgray', width = 2)
            # foods in order
            if app.orders[i][0] == [2,1,0,0,0,0,0]:
                canvas.create_image(newX-97, newY+9,
                                    image=ImageTk.PhotoImage(app.scaleImage(app.imageSushi,0.5)))
            elif app.orders[i][0] == [0,1,1,1,0,0,0]:
                canvas.create_image(newX-97, newY+9,
                                    image=ImageTk.PhotoImage(app.scaleImage(app.imagePoke,0.5)))
            elif app.orders[i][0] == [0,0,1,0,2,1,0]:
                canvas.create_image(newX-97, newY+9,
                                    image=ImageTk.PhotoImage(app.scaleImage(app.imageSoup,0.5)))
            elif app.orders[i][0] == [0,0,2,0,0,1,1]:
                canvas.create_image(newX-97, newY+9,
                                    image=ImageTk.PhotoImage(app.scaleImage(app.imageBurger,0.5)))
            elif app.orders[i][0] == [0,0,1,0,1,0,0]:
                canvas.create_image(newX-97, newY+9,
                                    image=ImageTk.PhotoImage(app.scaleImage(app.imageFries,0.5)))
            # drinks in order
            if app.orders[i][1] == [1,0,0]:
                canvas.create_image(newX-50, newY+9,
                                    image=ImageTk.PhotoImage(app.scaleImage(app.imageCone,0.5)))
            elif app.orders[i][1] == [0,1,0]:
                canvas.create_image(newX-50, newY+9,
                                    image=ImageTk.PhotoImage(app.scaleImage(app.imageCoffee,0.5)))
            elif app.orders[i][1] == [0,0,1]:
                canvas.create_image(newX-50, newY+9,
                                    image=ImageTk.PhotoImage(app.scaleImage(app.imageTea,0.5)))
            # split line in order
            canvas.create_line(newX-73, newY+24, newX-73, newY-4, 
                                    fill = 'darkgray', width = 2)

# mouse icon
def game_drawHand(app, canvas):
    if app.handTime != 0:
        canvas.create_image(app.handX, app.handY,
                            image=ImageTk.PhotoImage(app.scaleImage(app.handImage,0.08)))

# draw shortest ways with different colors
def ai_drawShortestWays(app,canvas):
    # target R&C to specific location to draw
    if app.hintShow == True:
        paths = ai_getallpaths(app)
        colors = ['red','green','blue','yellow']
        for i in range(len(paths)):
            path = paths[i]
            color = colors[i]
            (row0,col0) = path[0]
            (row1,col1) = path[1]
            (row2,col2) = path[2]
            x0 = app.margin + col0 * app.cellSize
            y0 = app.margin + row0 * app.cellSize
            x1 = app.margin + col1 * app.cellSize
            y1 = app.margin + row1 * app.cellSize
            x2 = app.margin + col2 * app.cellSize
            y2 = app.margin + row2 * app.cellSize
            (isoX0, isoY0) = cartToIso(x0,y0)
            (isoX1, isoY1) = cartToIso(x1,y1)
            (isoX2, isoY2) = cartToIso(x2,y2)
            move1 = app.width//2 + i*5
            move2 = app.cellSize*2 + i*5
            isoX0 += move1
            isoY0 += move2
            isoX1 += move1
            isoY1 += move2
            isoX2 += move1
            isoY2 += move2
            if len(path) == 3:
                canvas.create_line(isoX0, isoY0, isoX1, isoY1, isoX2, isoY2,
                                    fill = color, width = 2)
                canvas.create_oval(isoX2-3, isoY2-3,isoX2+3, isoY2+3,
                                    fill = color, width = 0)
            elif len(path) == 4:
                (row3,col3) = path[3]
                x3 = app.margin + col3 * app.cellSize
                y3 = app.margin + row3 * app.cellSize
                (isoX3, isoY3) = cartToIso(x3,y3)
                isoX3 += move1
                isoY3 += move2
                canvas.create_line(isoX0, isoY0, isoX1, isoY1,
                                    isoX2, isoY2, isoX3, isoY3,
                                    fill = color, width = 2)                                   

def game_drawHint(app, canvas):
    if app.hintTime != 0:
        ai_drawShortestWays(app,canvas)

# graphics for other modes
def drawTitle(app, canvas):
    canvas.create_image(app.width//2,app.height//2,image=ImageTk.PhotoImage(app.scaleImage(app.imageTitle, 0.5)))
    canvas.create_text(app.width*0.7, app.height*0.9, 
                        text = 'Click anywhere to continue',
                        fill = 'goldenrod4', font = "Arial 20 bold italic")

def drawGameStart(app, canvas):
    canvas.create_image(app.width//2,app.height//2,image=ImageTk.PhotoImage(app.scaleImage(app.imageGameStart, 1)))
    canvas.create_text(app.width*0.7, app.height*0.9, 
                        text = 'Click anywhere to continue',
                        fill = 'goldenrod4', font = "Arial 20 bold italic")

def drawGameOver(app, canvas):
    canvas.create_image(app.width//2,app.height//2,image=ImageTk.PhotoImage(app.scaleImage(app.imageGameOver, 0.9)))

def drawGameOverDog(app, canvas):
    canvas.create_image(app.width//2,app.height*0.738,image=ImageTk.PhotoImage(app.scaleImage(app.imageGameOverDog, 2)))

def drawGameWin(app, canvas):
    canvas.create_text(app.width*0.6, app.height*0.1, 
                        text = 'Y O U  W O N',
                        fill = 'goldenrod4', font = "Arial 50 bold italic")
    canvas.create_text(app.width*0.6-5, app.height*0.1-5, 
                        text = 'Y O U  W O N',
                        fill = 'gold', font = "Arial 50 bold italic")
    canvas.create_image(app.width*0.55,app.height*0.65,image=ImageTk.PhotoImage(app.scaleImage(app.imageGameWin, 0.7)))

# the order
def redrawAll(app, canvas):
    # game mode
    if app.modeIndex == 3 or app.modeIndex == 4:
        game_drawBoard(app, canvas)
        game_drawIcon(app, canvas)
        game_drawScore(app, canvas)
        game_drawTimer(app, canvas)
        game_drawTables1(app, canvas)
        game_drawStove(app, canvas)
        game_drawSelection1(app, canvas)
        game_placeOnTable1(app, canvas)
        
        game_drawchar(app, canvas)
        game_drawTables2(app, canvas)
        game_placeOnTable2(app, canvas)
        game_drawCounter(app,canvas)
        game_drawSelection2(app, canvas)
        game_drawCustomer(app, canvas)
        game_drawPack(app, canvas)
        game_drawHint(app, canvas)
        if app.game_time == 0:
            game_drawTimeOut(app, canvas)    
    # instruction mode
    if app.modeIndex == 2:
        drawInstructionBg(app, canvas)
    if app.instructShow == True or app.modeIndex == 2:
        drawInstruction(app, canvas)
    if app.recipeShow == True:
        drawRecipe(app, canvas)
    # mouse
    game_drawHand(app, canvas)
    # other
    if app.modeIndex == 5:
        drawGameOver(app, canvas)
        drawGameOverDog(app, canvas)
    elif app.modeIndex == 6:
        drawGameWin(app, canvas)
    elif app.modeIndex == 1:
        drawGameStart(app, canvas)
    elif app.modeIndex == 0:
        drawTitle(app, canvas)

#################################################
# main
#################################################

def main():
    runApp(width = 720, height = 600)

if __name__ == '__main__':
    main()
