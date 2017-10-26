## TurnTiles by Julia Balla

from tkinter import *
import time
import random
import math

boardHash = {} #hash map of all board states to maximize efficiency

# Initialize the data which will be used to draw on the screen.
def init(data):
    data.rows, data.cols = 8, 8 #default board dimensions
    data.topMargin = 30
    data.botMargin = 10
    data.selectedRow, data.selectedCol = 0, 0
    initDefaultGameBoard(data)
    data.memorizedBoard = data.board
    resetGame(data)
    boardDimButtons(data)
    #for the main menu update the color of the buttons every 5 frames:
    data.startFrameCounter = 0 
    initSpinningSquares(data)
    
# Only resets this data when going back to the main menu
def resetGame(data):
    data.curPlayer = 1
    data.gameStart = False
    data.isPaused = False
    data.isGameOver = False
    data.isSinglePlayer = False
    data.isMultiplayer = False
    data.isHardAI = False
    data.isSmartAI = False
    data.showInstructions1 = False
    data.showInstructions2 = False
    data.showSettings = False
    data.editBoard = False
    data.sideMargin = 220
    data.backgroundColor = "red"
    data.board = data.memorizedBoard
    resetBoard(data)

  
## Board Data ##
def initDefaultGameBoard(data):
    data.board = []
    for row in range(data.rows):
        data.board.append([0] * data.cols) #0 denotes empty space
    placeCorners(data)
    
def initCustomGameBoard(data):
    data.board = []
    for row in range(data.rows):
        data.board.append([0] * data.cols) 
    placeCorners(data)
    
def resetBoard(data):
    for row in range(data.rows):
        for col in range(data.cols):
            if(data.board[row][col] != 5):
                data.board[row][col] = 0 #clear all non-barriers
    placeCorners(data)
    
def placeCorners(data): #place 2 tiles for each player in the corners
    data.board[0][0] = 1
    data.board[0][data.cols-1] = 1
    data.board[data.rows-1][data.cols-1] = 2
    data.board[data.rows-1][0] = 2
    
def memorizeBoard(data): #store barrier arrangement
    data.memorizedBoard = data.board
            
    

    
    
## Spinning Square in the background ##  
def initSpinningSquares(data): 
    data.wheelCenter = [data.width/2, data.height/2]
    data.wheelRadius = 700
    data.vertices = 4
    data.wheelColor = "white"
    data.wheelSpinRate = -10*math.pi/180
    data.wheelSpinIncrement = -10*math.pi/180
    

  

# CONTROLLERS

### Mouse Pressed #
def mousePressed(event, data):
    mx, my = event.x, event.y
    w,h=data.width-2*data.sideMargin,data.height-data.topMargin-data.botMargin
    cellW, cellH = w / data.cols, h / data.rows
    #check which main menu button is pressed:
    if(not data.gameStart and not data.isSinglePlayer):
        if(not data.showSettings and not data.showInstructions1 and not \
            data.showInstructions2):
            checkMainMenuButtons(data, mx, my)
        elif(data.showSettings): checkSettingsButtons(data, mx, my)
    #AI selection screen
    elif(not data.gameStart and data.isSinglePlayer):
        if(mx >= data.easyAICoords[0] and mx<= data.easyAICoords[2] 
        and my >= data.easyAICoords[1] and my<= data.easyAICoords[3]):
            data.isSmartAI, data.gameStart = True, True
        if(mx >= data.hardAICoords[0] and mx<= data.hardAICoords[2] 
        and my >= data.hardAICoords[1] and my<= data.hardAICoords[3]):
            data.isHardAI, data.gameStart = True, True
    #Actual game play
    elif(mx>= data.sideMargin and mx<=w+data.sideMargin and my>=data.topMargin \
    and my<data.height-data.botMargin and data.gameStart and not data.isPaused):
        selectedRow, selectedCol = data.selectedRow, data.selectedCol
        selectCell(data, my, cellH, mx, cellW, selectedRow, selectedCol)

## Main Menu Buttons ##
def checkMainMenuButtons(data, mx, my):
    if(mx >= data.instructionsCoords[0] and mx<= data.instructionsCoords[2] 
    and my>=data.instructionsCoords[1] and my<= data.instructionsCoords[3]):
        data.showInstructions1 = True
    if(mx >= data.singlePlayerCoords[0] and mx<= data.singlePlayerCoords[2] 
    and my>=data.singlePlayerCoords[1] and my<= data.singlePlayerCoords[3]):
        data.isSinglePlayer = True
    if(mx >= data.multiplayerCoords[0] and mx<= data.multiplayerCoords[2] 
    and my >= data.multiplayerCoords[1] and my<= data.multiplayerCoords[3]):
        data.isMultiplayer, data.gameStart = True, True
    if(mx >= data.settingsCoords[0] and mx<= data.settingsCoords[2] 
    and my >= data.settingsCoords[1] and my<= data.settingsCoords[3]):
        data.showSettings = True
        
## Settings Buttons ##
        
def boardDimButtons(data):
    data.rowsButtonDim = 60
    data.colsButtonDim = data.rowsButtonDim
    data.rowsButtonCoords =[data.sideMargin/3,data.height/4,data.sideMargin/3 +\
        data.rowsButtonDim, data.height/4 + data.rowsButtonDim]
    data.colsButtonCoords=[data.sideMargin/3,3*data.height/4,data.sideMargin/3+\
        data.colsButtonDim, 3*data.height/4 + data.colsButtonDim]
    data.addRows = [data.rowsButtonCoords[0], data.rowsButtonCoords[1]-5,\
        data.rowsButtonCoords[2],data.rowsButtonCoords[1]-data.rowsButtonDim-5]
    data.subtractRows = [data.rowsButtonCoords[0], data.rowsButtonCoords[3]+5, \
        data.rowsButtonCoords[2],data.rowsButtonCoords[3]+data.rowsButtonDim+5]
    data.addCols = [data.colsButtonCoords[0],data.colsButtonCoords[1]-\
        5,data.colsButtonCoords[2],data.colsButtonCoords[1]-data.colsButtonDim-\
        5]
    data.subtractCols = [data.colsButtonCoords[0], data.colsButtonCoords[3]+\
        5,data.colsButtonCoords[2],data.colsButtonCoords[3]+data.colsButtonDim+\
        5]
        
def checkSettingsButtons(data, mx, my):
    if(mx >= data.addRows[0] and mx<= data.addRows[2] 
    and my>=data.addRows[3] and my<= data.addRows[1] and data.rows < 8):
        data.rows += 1
        initCustomGameBoard(data)
    if(mx >= data.subtractRows[0] and mx<= data.subtractRows[2] 
    and my>=data.subtractRows[1] and my<= data.subtractRows[3] and data.rows>3):
        data.rows -= 1
        initCustomGameBoard(data)
    if(mx >= data.addCols[0] and mx<= data.addCols[2] 
    and my>=data.addCols[3] and my<= data.addCols[1] and data.cols < 8):
        data.cols += 1
        initCustomGameBoard(data)
    if(mx >= data.subtractCols[0] and mx<= data.subtractCols[2] 
    and my>=data.subtractCols[1] and my<= data.subtractCols[3] and data.cols>3):
        data.cols -= 1
        initCustomGameBoard(data)
    w,h=data.width-2*data.sideMargin,data.height-data.topMargin-data.botMargin
    cellW, cellH = w / data.cols, h / data.rows
    if(mx>= data.sideMargin and mx<=w+data.sideMargin and my>=data.topMargin 
        and my<data.height-data.botMargin):
        selectedRow, selectedCol = data.selectedRow, data.selectedCol
        editCell(data, my, cellH, mx, cellW, selectedRow, selectedCol)
    if(mx >= data.clearAllCoords[0] and mx<= data.clearAllCoords[2] 
    and my>=data.clearAllCoords[1] and my<= data.clearAllCoords[3]):
        clearAll(data)
    if(mx >= data.fillAllCoords[0] and mx<= data.fillAllCoords[2] 
    and my>=data.fillAllCoords[1] and my<= data.fillAllCoords[3]):
        fillAll(data)
    
def clearAll(data): #makes every cell empty except for corners
    initCustomGameBoard(data)
    memorizeBoard(data)
    
def fillAll(data): #fills every cell with a barrier except for corners
    data.board = []
    for row in range(data.rows):
        data.board.append([5] * data.cols) #5 denotes a barrier
    placeCorners(data)
    memorizeBoard(data)
    
# Create/Remove barriers
def editCell(data, my, cellH, mx, cellW, selectedRow, selectedCol):
    cellRowIndex = int(((my-data.topMargin)/cellH)//1)
    cellColIndex = int(((mx-data.sideMargin)/cellW)//1)
    if(data.board[cellRowIndex][cellColIndex] == 0): #delete cell
        data.board[cellRowIndex][cellColIndex] = 5
        memorizeBoard(data)
    elif(data.board[cellRowIndex][cellColIndex] == 5): #replace cell
        data.board[cellRowIndex][cellColIndex] = 0
        memorizeBoard(data)
        
## Gameplay ##
def selectCell(data, my, cellH, mx, cellW, selectedRow, selectedCol):
    cellRowIndex = int(((my-data.topMargin)/cellH)//1)
    cellColIndex = int(((mx-data.sideMargin)/cellW)//1)
    if(data.board[cellRowIndex][cellColIndex]==1 and data.curPlayer==1): #select
        selectedPlayer1(data,cellRowIndex,cellColIndex,selectedRow, selectedCol)
    elif(data.board[cellRowIndex][cellColIndex]==2 and data.curPlayer==2):
        selectedPlayer2(data,cellRowIndex,cellColIndex,selectedRow, selectedCol)
    elif(data.board[cellRowIndex][cellColIndex] == -1 or \
        data.board[cellRowIndex][cellColIndex] == -2):  #deselect
        data.board[cellRowIndex][cellColIndex] = \
            abs(data.board[cellRowIndex][cellColIndex])
        hideInnerMoves(data, data.selectedRow, data.selectedCol)
        hideOuterMoves(data, data.selectedRow, data.selectedCol)
    elif(data.board[cellRowIndex][cellColIndex] == 3): #duplicate
        duplicate(data,cellRowIndex, cellColIndex, selectedRow, selectedCol)
        switchPieces(data, cellRowIndex, cellColIndex)
        swapPlayer(data)
    elif(data.board[cellRowIndex][cellColIndex] == 4): #teleport
        teleport(data,cellRowIndex, cellColIndex, selectedRow, selectedCol)
        switchPieces(data, cellRowIndex, cellColIndex)
        swapPlayer(data)
            
def selectedPlayer1(data,cellRowIndex, cellColIndex, selectedRow, selectedCol):
    if(data.board[selectedRow][selectedCol]==-1):
        data.board[selectedRow][selectedCol]=1
        hideInnerMoves(data, data.selectedRow, data.selectedCol)
        hideOuterMoves(data, data.selectedRow, data.selectedCol)
    data.board[cellRowIndex][cellColIndex] = -1
    data.selectedRow = cellRowIndex
    data.selectedCol = cellColIndex
    showInnerMoves(data, cellRowIndex, cellColIndex)
    showOuterMoves(data, cellRowIndex, cellColIndex)
    
def selectedPlayer2(data,cellRowIndex, cellColIndex, selectedRow, selectedCol):
    if(data.board[selectedRow][selectedCol]==-2):
        data.board[selectedRow][selectedCol]=2
        hideInnerMoves(data, data.selectedRow, data.selectedCol)
        hideOuterMoves(data, data.selectedRow, data.selectedCol)
    data.board[cellRowIndex][cellColIndex] = -2
    data.selectedRow = cellRowIndex
    data.selectedCol = cellColIndex
    showInnerMoves(data, cellRowIndex, cellColIndex)
    showOuterMoves(data, cellRowIndex, cellColIndex)


def duplicate(data,cellRowIndex, cellColIndex, selectedRow, selectedCol):
    if (data.curPlayer==1): 
        data.board[data.selectedRow][data.selectedCol] = 1
        data.board[cellRowIndex][cellColIndex] = 1
    else: 
        data.board[data.selectedRow][data.selectedCol] = 2
        data.board[cellRowIndex][cellColIndex] = 2
    hideInnerMoves(data, data.selectedRow, data.selectedCol)
    hideOuterMoves(data, data.selectedRow, data.selectedCol)
    
    
def teleport(data,cellRowIndex, cellColIndex, selectedRow, selectedCol):
    data.board[data.selectedRow][data.selectedCol] = 0
    if (data.curPlayer == 1):data.board[cellRowIndex][cellColIndex] = 1
    else: data.board[cellRowIndex][cellColIndex] = 2
    hideInnerMoves(data, data.selectedRow, data.selectedCol)
    hideOuterMoves(data, data.selectedRow, data.selectedCol)
    
def switchPieces(data,cellRowIndex, cellColIndex):
    #turn all adjactent enemy tiles to friendly tiles
    if(data.curPlayer == 1): 
        friendlyPiece = 1
        enemyPiece = 2
    else: 
        friendlyPiece = 2
        enemyPiece = 1
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        row = cellRowIndex + drow
        col = cellColIndex + dcol
        if (row < 0 or row >= data.rows or col < 0 or col >= data.cols or \
            data.board[row][col] != enemyPiece):
            continue
        else:
            data.board[row][col] = friendlyPiece 
            

def swapPlayer(data):
    if (data.curPlayer == 1): data.curPlayer = 2
    else: data.curPlayer = 1
    
        
def showInnerMoves(data, cellRowIndex, cellColIndex):
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        row = cellRowIndex + drow
        col = cellColIndex + dcol
        if (row < 0 or row >= data.rows or col < 0 or col >= data.cols or \
            (data.board[row][col] != 0)):
            continue
        else:
            data.board[row][col] = 3   
           
            
def showOuterMoves(data, cellRowIndex, cellColIndex):
    dirs = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
            (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
            ( 0, -2), ( 0, -1),          ( 0, 1), ( 0, 2),
            ( 1, -2), ( 1, -1), ( 1, 0), ( 1, 1), ( 1, 2),
            ( 2, -2), ( 2, -1), ( 2, 0), ( 2, 1), ( 2, 2)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        row = cellRowIndex + drow
        col = cellColIndex + dcol
        if (row < 0 or row >= data.rows or col < 0 or col >= data.cols or \
            (data.board[row][col] != 0)):
            continue
        else:
            data.board[row][col] = 4   
            
def hideOuterMoves(data, cellRowIndex, cellColIndex):
    dirs = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
            (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
            ( 0, -2), ( 0, -1),          ( 0, 1), ( 0, 2),
            ( 1, -2), ( 1, -1), ( 1, 0), ( 1, 1), ( 1, 2),
            ( 2, -2), ( 2, -1), ( 2, 0), ( 2, 1), ( 2, 2)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        row = cellRowIndex + drow
        col = cellColIndex + dcol
        if (row < 0 or row >= data.rows or col < 0 or col >= data.cols or \
            data.board[row][col] != 4):
            continue
        else:
            data.board[row][col] = 0      
            
def hideInnerMoves(data, cellRowIndex, cellColIndex):
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        row = cellRowIndex + drow
        col = cellColIndex + dcol
        if (row < 0 or row >= data.rows or col < 0 or col >= data.cols or \
            data.board[row][col] != 3):
            continue
        else:
            data.board[row][col] = 0 
       
    
## Key Pressed ##
def keyPressed(event, data):
    if(event.char == "m" and (data.isPaused or not data.gameStart or \
        data.isGameOver)): 
        resetGame(data) #go to main menu
    elif(event.char == "p"):
        if(data.isPaused): data.isPaused = False
        else: data.isPaused = True 
    elif(event.char == "i" and data.gameStart and not data.isGameOver):
        data.showInstructions1 = True #shows first page of instructions
    elif(event.char == "b" and data.gameStart):
        data.showInstructions1 = False
        data.showInstructions2 = False #back to paused screen
    elif(data.showInstructions1 and event.keysym == "Right"):
        data.showInstructions1 = False
        data.showInstructions2 = True #show page 2 of instructions
    elif(data.showInstructions2 and event.keysym == "Left"):
        data.showInstructions2 = False
        data.showInstructions1 = True #show page 1 of instructions
        
        
## Timer Fired ##
def timerFired(data):
    #end the game if either 1) the whole board is full, 2) one of the players
    #has no pieces left, 3) one of the players has no moves left
    if(data.gameStart and (numEmptySpaces(data) == 0 or numPlayerTiles(data, 1)\
        == 0 or numPlayerTiles(data, 2) == 0 or totalMoves(data,1) == 0 or \
        totalMoves(data,2) == 0)):
        time.sleep(1)
        data.isGameOver = True 
    #if in single player mode, place an AI move as Player 2
    if(not data.isGameOver and data.isSinglePlayer and data.curPlayer == 2 and\
        not data.isPaused and not data.showInstructions1 and \
        not data.showInstructions2):
        if(data.isHardAI):
            time.sleep(0.5) #hard AI moves quickly, easy AI has natural delay
        placeAIMove(data)
    data.wheelSpinRate += data.wheelSpinIncrement #make background spin
   
## Board Check ##
def numEmptySpaces(data):
    result = 0
    for row in range(data.rows):
        for col in range(data.cols):
            if(data.board[row][col] != abs(1) and data.board[row][col]!=abs(2)):
                result += 1
    return result
    
def numPlayerTiles(data, player):
    result = 0
    for row in range(data.rows):
        for col in range(data.cols):
            if(abs(data.board[row][col]) == player):
                result += 1
    return result
                
def numInnerMoves(data, player, cellRowIndex, cellColIndex):
    moveCount = 0
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        row = cellRowIndex + drow
        col = cellColIndex + dcol
        if (row < 0 or row >= data.rows or col < 0 or col >= data.cols or \
            data.board[row][col] == 1 or data.board[row][col] == 2 or\
            data.board[row][col] == 5):
            continue
        else:
            moveCount+=1
    return moveCount

def numOuterMoves(data, player, cellRowIndex, cellColIndex):
    moveCount = 0
    dirs = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
            (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
            ( 0, -2), ( 0, -1),          ( 0, 1), ( 0, 2),
            ( 1, -2), ( 1, -1), ( 1, 0), ( 1, 1), ( 1, 2),
            ( 2, -2), ( 2, -1), ( 2, 0), ( 2, 1), ( 2, 2)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        row = cellRowIndex + drow
        col = cellColIndex + dcol
        if (row < 0 or row >= data.rows or col < 0 or col >= data.cols or \
            data.board[row][col] == 1 or data.board[row][col] == 2 or \
            data.board[row][col] == 5):
            continue
        else:
            moveCount += 1
    return moveCount
    
#find total number of possible moves
def totalMoves(data, player):
    moves = 0
    for row in range (data.rows):
        for col in range (data.cols):
            if(abs(data.board[row][col]) == player):
                moves += numInnerMoves(data,player, row, col) + \
                         numOuterMoves(data, player, row, col)
    return moves
    

## Score ##
def getPlayerScore(data, player):
    return numPlayerTiles(data, player)
    
def getWinner(data):
    player1Score = getPlayerScore(data, 1)
    player2Score = getPlayerScore(data, 2)
    if(player1Score > player2Score): return "Player 1 is the winner!"
    if(player1Score < player2Score): return "Player 2 is the winner!"
    if(player1Score == player2Score): return "It's a tie!"
    
    
## Place AI Move ##
    
def placeAIMove(data):
    if(data.isHardAI):
        bestMove = bestImmediateMove(data)
    else:
        bestMove = smartMove(data, 2, 0)[0]
    if(bestMove == []): 
        data.isGameOver = True
        return
    oldRow = bestMove[0]
    oldCol = bestMove[1]
    newRow = bestMove[2]
    newCol = bestMove[3]
    innerOrOuter = bestMove[4]
    data.board[newRow][newCol] = 2
    if(innerOrOuter == "outer"):
        data.board[oldRow][oldCol] = 0
    switchPieces(data, newRow, newCol)
    data.curPlayer = 1  
    
    
## Easy AI ## (recursively looks 3 steps ahead)
    
def smartMove(data, player, depth):
    boardStr = str(data.board) #don't check the same board state twice
    if((boardStr, player) in boardHash): return boardHash[(boardStr,player)]
    if(player == 1): opp = 2
    else: opp = 1
    if(totalMoves(data, player) == 0 or depth >= 3): #maximum AI depth = 3
        boardHash[(boardStr,player)] = ([], numPlayerTiles(data, player)- \
            numPlayerTiles(data, opp))
        return boardHash[(boardStr,player)]
    maxVal, bestMove = -(data.rows * data.cols), []
    for row in range (data.rows):
        for col in range (data.cols):
            if(data.board[row][col] == player):
                #finds best possible move in general
                maxVal, bestMove = innerMoves(data,player,opp,row,col,maxVal,\
                                              bestMove, depth)
                maxVal, bestMove = outerMoves(data,player,opp,row,col,maxVal,\
                                              bestMove, depth)
    boardHash[(boardStr,player)] = (bestMove, maxVal) #add board state to map
    return (bestMove, maxVal)
    
def innerMoves(data,player,opp,row,col,maxVal,bestMove,depth):
    #find best inner move
    dirs = [(-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        newRow = row + drow
        newCol = col + dcol
        if (newRow < 0 or newRow >= data.rows or newCol < 0 or \
            newCol >= data.cols or data.board[newRow][newCol] == 1\
            or data.board[newRow][newCol]==2 or data.board[newRow][newCol]==5):
            continue
        else:
            data.board[newRow][newCol] = player
            curVal = -(smartMove(data, opp, depth+1)[1]) 
            if(curVal > maxVal): 
                maxVal = curVal
                bestMove = [row, col, newRow, newCol, "inner"]
            data.board[newRow][newCol] = 0
    return maxVal, bestMove
    
def outerMoves(data,player,opp,row,col,maxVal,bestMove,depth):
    #find best outer move and compare it to best inner move to get best move
    #in general
    dirs = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
            (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
            ( 0, -2), ( 0, -1),          ( 0, 1), ( 0, 2),
            ( 1, -2), ( 1, -1), ( 1, 0), ( 1, 1), ( 1, 2),
            ( 2, -2), ( 2, -1), ( 2, 0), ( 2, 1), ( 2, 2)]
    for dir in range (len(dirs)):
        (drow, dcol) = dirs[dir]
        newRow = row + drow
        newCol = col + dcol
        if (newRow < 0 or newRow >= data.rows or newCol < 0 or \
            newCol >= data.cols or data.board[newRow][newCol] == 1 \
            or data.board[newRow][newCol]==2 or data.board[newRow][newCol]==5):
            continue
        else:
            data.board[newRow][newCol] = player
            data.board[row][col] == 0
            curVal = -(smartMove(data, opp, depth+1)[1])
            if(curVal > maxVal): 
                maxVal = curVal
                bestMove = [row, col, newRow, newCol, "outer"]
            data.board[newRow][newCol] = 0
            data.board[row][col] = player
    return maxVal, bestMove

    
## Hard AI ## (finds move that gives it the most peices immediately)
def evalMove(data, row, col, newRow, newCol, innerOrOuter):
    value = 0 #number of friendly pieces - number of enemy pieces
    #don't modify board when evaluating 
    oldBoardState = [[] for row in range(data.rows)]  #create copy
    for row in range(data.rows):
        for col in range(data.cols):
            oldBoardState[row].append(data.board[row][col])
    data.board[newRow][newCol] = 2 #AI is always player 2
    if(innerOrOuter == "outer"):
        data.board[row][col] = 0
    switchPieces(data, newRow, newCol)
    for row in range(data.rows):
        for col in range(data.cols):
            if(abs(data.board[row][col]) == 2): value += 1
            elif(abs(data.board[row][col]) == 1): value -= 1
    data.board = oldBoardState #return to old board state
    return value
    

def bestImmediateMove(data):
    bestInnerMoveVal = findBestInnerMove(data)[1]
    bestOuterMoveVal = findBestOuterMove(data)[1]
    bestInnerMove = findBestInnerMove(data)[0]
    bestOuterMove = findBestOuterMove(data)[0]
    if(bestInnerMoveVal >= bestOuterMoveVal or bestOuterMove == []):
        return bestInnerMove
    else:
        return bestOuterMove
    

def findBestInnerMove(data):
    bestInnerMove = []
    bestInnerMoveVal = -(data.rows*data.cols)
    for row in range(data.rows):
        for col in range(data.cols):
            if(abs(data.board[row][col]) != 2): continue
            dirs = [(-1, -1), (-1, 0), (-1, 1),
                    ( 0, -1),          ( 0, 1),
                    ( 1, -1), ( 1, 0), ( 1, 1)]
            for dir in range (len(dirs)):
                (drow, dcol) = dirs[dir]
                newRow = row + drow
                newCol = col + dcol
                if (newRow < 0 or newRow >= data.rows or newCol < 0 or \
                    newCol >= data.cols or data.board[newRow][newCol] != 0):
                    continue
                elif(evalMove(data, row, col, newRow, newCol, "inner") \
                    > bestInnerMoveVal): 
                    bestInnerMove = [row, col, newRow, newCol, "inner"]
                    bestInnerMoveVal = evalMove(data, row, col, newRow, newCol,\
                        "inner")
    return (bestInnerMove, bestInnerMoveVal)
    
def findBestOuterMove(data):
    bestOuterMove = []
    bestOutMoveVal = -(data.rows*data.cols)
    for row in range (data.rows):
        for col in range(data.cols):
            if(abs(data.board[row][col]) != 2): continue
            dirs = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                    ( 0, -2), ( 0, -1),          ( 0, 1), ( 0, 2),
                    ( 1, -2), ( 1, -1), ( 1, 0), ( 1, 1), ( 1, 2),
                    ( 2, -2), ( 2, -1), ( 2, 0), ( 2, 1), ( 2, 2)]
            for dir in range (len(dirs)):
                (drow, dcol) = dirs[dir]
                newRow = row + drow
                newCol = col + dcol
                if (newRow < 0 or newRow >= data.rows or newCol < 0 or \
                    newCol >= data.cols or data.board[newRow][newCol] != 0):
                    continue
                elif(evalMove(data, row, col, newRow, newCol,"outer") \
                    >= bestOutMoveVal): 
                    bestOuterMove = [row, col, newRow, newCol, "outer"]
                    bestOutMoveVal = evalMove(data, row, col, newRow, newCol,\
                        "outer")
    return bestOuterMove, bestOutMoveVal
    

# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.

## Graphics ##
def redrawAll(canvas, data):
    #checks what screen to display
    if(not data.gameStart and not data.isSinglePlayer and not
        data.showInstructions1 and not data.showInstructions2 and not \
        data.showSettings):
        drawStartScreen(canvas, data)
    elif(data.showInstructions1):
        drawInstructions1(canvas, data)
    elif(data.showInstructions2):
        drawInstructions2(canvas, data)
    elif(data.showSettings):
        drawSettings(canvas, data)
    elif(not data.gameStart and data.isSinglePlayer and not data.isGameOver):
        drawAISelectionScreen(canvas, data)
    elif(not data.isGameOver):
        w = data.width
        h = data.height
        drawGame(canvas, data)
    else:
        drawEndScreen(canvas, data)
        

def rgbString(red, green, blue): #from course notes
    return "#%02x%02x%02x" % (red, green, blue)
    
## Draw spinning square in background (fancy wheel code from HW 4.1) ##
def drawSpinningSquares(canvas, data): 
    cx, cy = data.wheelCenter[0], data.wheelCenter[1]
    r, color, vertices = data.wheelRadius, data.wheelColor, data.vertices
    #The diagonals of a regular polygon have N/2 different sizes. The floor
    #division by 2 accounts for an odd number of vertices:
    diagonals = data.vertices//2
    spinAngle = data.wheelSpinRate
    startX, startY = cx+r*math.cos(spinAngle), cy-r*math.sin(spinAngle)
    drawSquareSides(canvas,data,cx,cy,r,vertices,diagonals,startX,startY,0,\
                    color,spinAngle)
    #certain diagonals are skipped because of even number of vertices:
    
                  
def drawSquareSides(canvas, data, cx, cy, r,vertices,diagonals, startX, startY,\
                  diagAngle, color, spinAngle): #fancy wheel code from HW 4.1
    polygonCoords = []
    curX, curY = 0, 0
    firstIteration = True
    floatApprox = 0.0000000001
    while(abs(startX-curX)>floatApprox or abs(startY-curY)> floatApprox):
        if(firstIteration == True): 
            curX, curY = startX, startY
            polygonCoords.append(curX)
            polygonCoords.append(curY)
            firstIteration = False
        diagAngle += 2*math.pi/vertices
        nextX = cx + r * math.cos(diagAngle+spinAngle)
        nextY = cy - r * math.sin(diagAngle+spinAngle)
        polygonCoords.append(nextX)
        polygonCoords.append(nextY)
        curX, curY = nextX, nextY 
    canvas.create_polygon(polygonCoords[0], polygonCoords[1], polygonCoords[2],\
        polygonCoords[3], polygonCoords[4], polygonCoords[5], polygonCoords[6],\
        polygonCoords[7], fill = "black")
        
## Random color switcher ##
def switchColors(data, colors):
    data.instructionsButtonFill = random.choice(colors)
    data.singlePlayerButtonFill = random.choice(colors)
    data.multiplayerButtonFill = random.choice(colors)
    data.settingsButtonFill = random.choice(colors)
    data.easyAIButtonFill = random.choice(colors)
    data.hardAIButtonFill = random.choice(colors)
    data.backgroundColor = random.choice(colors)

## Main Menu ##
def drawStartScreen(canvas, data):
    offset = 10
    buttonW = 250 #button width
    buttonH = 50 #button height
    colors = ["spring green", "tomato", "yellow", "orange", \
              "pink", "turquoise1", "purple1"]
    canvas.create_rectangle(-offset, -offset, data.width + offset, \
        data.height + offset, fill = data.backgroundColor)
    drawSpinningSquares(canvas, data)
    canvas.create_image(data.width/2, data.height/4, image = data.logo)
    if(data.startFrameCounter % 15 == 0):
        data.startFrameCounter = 1
        switchColors(data, colors)
    else:
        data.startFrameCounter += 1
    drawInstructionsButton(canvas, data, buttonW, buttonH)
    drawSinglePlayerButton(canvas, data, buttonW, buttonH)
    drawMultiplayerButton(canvas, data, buttonW, buttonH)
    drawSettingsButton(canvas, data, buttonW, buttonH)
    
        
def drawInstructionsButton(canvas, data, buttonW, buttonH):
    data.instructionsCoords = [data.width/2-buttonW/2,18*data.height/40-\
        buttonH/2, data.width/2 + buttonW/2, 18*data.height/40 + buttonH/2]
    canvas.create_rectangle(data.width/2 - buttonW/2, 18*data.height/40 - \
        buttonH/2, data.width/2 + buttonW/2, 18*data.height/40 + buttonH/2, \
        fill = data.instructionsButtonFill, activeoutline = "white", width=3)
    canvas.create_text(data.width/2, 18*data.height/40, text="Instructions", \
        font = "System 16")
   
        
def drawSinglePlayerButton(canvas, data, buttonW, buttonH):
    data.singlePlayerCoords = [data.width/2-buttonW/2,23*data.height/40-\
        buttonH/2, data.width/2 + buttonW/2, 23*data.height/40 + buttonH/2]
    canvas.create_rectangle(data.width/2 - buttonW/2, 23*data.height/40 - \
        buttonH/2, data.width/2 + buttonW/2, 23*data.height/40 + buttonH/2, \
        fill = data.singlePlayerButtonFill, activeoutline = "white", width=3)
    canvas.create_text(data.width/2, 23*data.height/40, text="Single Player", \
        font = "System 16")
        
def drawMultiplayerButton(canvas, data, buttonW, buttonH):
    data.multiplayerCoords = [data.width/2-buttonW/2,28*data.height/40-\
        buttonH/2, data.width/2 + buttonW/2, 28*data.height/40 + buttonH/2]
    canvas.create_rectangle(data.width/2 - buttonW/2, 28*data.height/40 - \
        buttonH/2, data.width/2 + buttonW/2, 28*data.height/40 + buttonH/2, \
        fill = data.multiplayerButtonFill, activeoutline = "white", width=3)
    canvas.create_text(data.width/2, 28*data.height/40, text="Multiplayer", \
        font = "System 16")
        
def drawSettingsButton(canvas, data, buttonW, buttonH):
    data.settingsCoords = [data.width/2-buttonW/2,33*data.height/40-\
        buttonH/2, data.width/2 + buttonW/2, 33*data.height/40 + buttonH/2]
    canvas.create_rectangle(data.width/2 - buttonW/2, 33*data.height/40 - \
        buttonH/2, data.width/2 + buttonW/2, 33*data.height/40 + buttonH/2, \
        fill = data.settingsButtonFill, activeoutline = "white", width=3)
    canvas.create_text(data.width/2, 33*data.height/40, text="Game Settings", \
        font = "System 16")
    
## AI Selection Screen ##
def drawAISelectionScreen(canvas, data):
    offset = 10
    buttonW = 250
    buttonH = 50
    colors = ["spring green", "tomato", "yellow", "orange", \
              "pink", "turquoise1", "purple1"]
    canvas.create_rectangle(-offset, -offset, data.width + offset, \
        data.height + offset, fill = data.backgroundColor)
    drawSpinningSquares(canvas, data)
    if(data.startFrameCounter % 15 == 0):
        data.startFrameCounter = 1
        switchColors(data, colors)
    else:
        data.startFrameCounter += 1
    drawEasyAIButton(canvas,data,buttonW,buttonH)
    drawHardAIButton(canvas,data,buttonW,buttonH)
    canvas.create_text(data.width/2,20,text="Press 'M' to go back to the " +\
        " main menu...", font = "System 16", fill = "white")
    
def drawEasyAIButton(canvas,data,buttonW,buttonH):
    data.easyAICoords = [data.width/3-buttonW/2,data.height/2-\
        buttonH/2, data.width/3 + buttonW/2, data.height/2 + buttonH/2]
    canvas.create_rectangle(data.width/3 - buttonW/2, data.height/2 - \
        buttonH/2, data.width/3 + buttonW/2, data.height/2 + buttonH/2, \
        fill = data.hardAIButtonFill, activeoutline = "white", width=3)
    canvas.create_text(data.width/3, data.height/2, text="Easy AI", \
        font = "System 16")
        
def drawHardAIButton(canvas,data,buttonW,buttonH):
    data.hardAICoords = [2*data.width/3-buttonW/2,data.height/2-\
        buttonH/2, 2*data.width/3 + buttonW/2, data.height/2 + buttonH/2]
    canvas.create_rectangle(2*data.width/3 - buttonW/2, data.height/2 - \
        buttonH/2, 2*data.width/3 + buttonW/2, data.height/2 + buttonH/2, \
        fill = data.easyAIButtonFill, activeoutline = "white", width=3)
    canvas.create_text(2*data.width/3, data.height/2, text="Hard AI", \
        font = "System 16")
        
## Game Over Screen ##
def drawEndScreen(canvas, data):
    offset = 10
    canvas.create_rectangle(-offset, -offset, data.width + offset, \
        data.height + offset, fill = "black")
    canvas.create_image(data.width/2, data.height/4, image = data.gameOverImg)
    winner = getWinner(data)
    canvas.create_text(data.width/2, 3*data.height/8, text = winner, \
        font = "System 20", fill = "white")
    data.sideMargin = data.width/2
    drawScores(canvas, data)
    canvas.create_text(data.width/2, 3*data.height/4, text = "Press 'M' to " + \
        "return to the main menu...", font = "System 20", fill = "white")
    
## Gameplay Drawing ##
def drawGame(canvas, data):
    offset = 10
    canvas.create_rectangle(-offset, -offset, data.width + offset, \
        data.height + offset, fill = "black")
    drawBoard(canvas, data)
    drawScores(canvas, data)
    drawPlayPauseText(canvas, data)
    if(data.isPaused):
        canvas.create_rectangle(data.width/3, data.height/3, 2*data.width/3, \
            2*data.height/3, fill = "white")
        canvas.create_text(data.width/2, data.height/3+30, text="Game Paused", \
            font = "System 25")
        canvas.create_text(data.width/2, data.height/3+80, text = "Press 'I' "+\
            "for instructions...", font = "System 16")
        canvas.create_text(data.width/2, data.height/3+130, text ="Press 'M' "+\
            "to go back to the main menu...", font = "System 16")
        if(data.showInstructions1):
            drawInstructions1(canvas,data)
        if(data.showInstructions2):
            drawInstructions2(canvas, data)
            
def drawScoreOutline(canvas, data):
    outline = 4
    if(data.curPlayer == 1 and not data.isGameOver):
        canvas.create_rectangle(data.sideMargin/5-outline, data.height/2 - 60 \
            -outline, 4*data.sideMargin/5+outline, data.height/2+20 + outline, \
            fill = "white")
        canvas.create_text(data.sideMargin/5, data.height/2-60, anchor = NW,\
            text="Waiting for \n Player 1...",font ="System 10")
    elif(not data.isGameOver):
        canvas.create_rectangle(data.width - data.sideMargin/5 + outline, \
            data.height/2 - 60 - outline,data.width - 4*data.sideMargin/5 - \
            outline, data.height/2+20 + outline, fill = "white")
        canvas.create_text(data.width - 4*data.sideMargin/5, data.height/2-60, \
            anchor=NW,text="Waiting for \n Player 2...",font ="System 10")

        
def drawScores(canvas, data):
    if(not data.isGameOver):
        drawScoreOutline(canvas, data)
    sideMargin = data.sideMargin/5
    boxWidth = 3*data.sideMargin/5
    boxHeight = 40
    data.player1Score = str(getPlayerScore(data,1))
    data.player2Score = str(getPlayerScore(data,2))
    p1Box = [sideMargin, data.height/2 - boxHeight/2, sideMargin + boxWidth, \
            data.height/2 + boxHeight/2]
    p2Box = [data.width - sideMargin - boxWidth, data.height/2 - boxHeight/2, \
            data.width - sideMargin, data.height/2 + boxHeight/2]
    canvas.create_rectangle(p1Box[0],p1Box[1], p1Box[2], p1Box[3],fill = "cyan")
    canvas.create_text(p1Box[0] + boxWidth/2, p1Box[1]+boxHeight/2, \
        text = "Player 1 Score: " + data.player1Score ,font = "System")
    canvas.create_rectangle(p2Box[0],p2Box[1],p2Box[2],p2Box[3],fill ="tomato")
    canvas.create_text(p2Box[0] + boxWidth/2, p2Box[1]+boxHeight/2,\
        text="Player 2 Score: " + data.player2Score, font = "System")
        
## Instructions Pages ##
def drawInstructions1(canvas, data):
    offset = 10
    canvas.create_rectangle(-offset, -offset, data.width + offset, \
        data.height + offset, fill = "black")
    canvas.create_image(data.width/2,data.height/2,image=data.instructions1)
    if(data.gameStart):
        canvas.create_text(data.width-30,20,text="Press 'B' to go back to " +\
            "the game...", font = "System 16", anchor = E)
    else:
        canvas.create_text(data.width-30,20,text="Press 'M' to go back to " +\
            "the main menu...", font = "System 16", anchor = E)
            
def drawInstructions2(canvas, data):
    offset = 10
    canvas.create_rectangle(-offset, -offset, data.width + offset, \
        data.height + offset, fill = "black")
    canvas.create_image(data.width/2,data.height/2,image=data.instructions2)
    if(data.gameStart):
        canvas.create_text(data.width-30,20,text="Press 'B' to go back to " +\
            "the game...", font = "System 16", anchor = E)
    else:
        canvas.create_text(data.width-30,20,text="Press 'M' to go back to " +\
            "the main menu...", font = "System 16", anchor = E)

## Pause Screen ##
def drawPlayPauseText(canvas, data):
    if(data.isPaused):
        canvas.create_text(data.width/2,20,text="Press 'P' to unpause the game",
            font = "System 16", fill = "white")
    else:
        canvas.create_text(data.width/2, 20, text="Press 'P' to pause the game",
            font = "System 16", fill = "white")
            
## Settings Screen ##
def drawSettings(canvas, data):
    offset = 10
    canvas.create_rectangle(-offset, -offset, data.width + offset, \
        data.height + offset, fill = "black")
    drawBoard(canvas, data)
    canvas.create_text(data.width/2, 15, text="Settings",
        font = "System 18", fill = "white")
    canvas.create_text(data.width-30,20,text="Press 'M' to go back to " +\
        "the main menu...", font = "System 16", fill = "white", anchor = E)
    canvas.create_text(data.width-110,data.height/3,text="Click " +\
        "on any empty space\nto create or remove a\ngrey barrier where tiles" +\
        "\ncannot be placed.",font = "System 16", fill = "white")
    canvas.create_text(data.width-110,data.height/2,text="Remember " +\
        "to leave\nroom for each player's\ninitial moves!",font = "System 16", \
        fill = "white")
    drawRowsButtons(canvas, data)
    drawColsButtons(canvas, data)
    drawClearAllButton(canvas, data)
    drawFillAllButton(canvas, data)
    
def drawClearAllButton(canvas, data):
    buttonWidth = 200
    buttonHeight = 50
    clearAllCoords = [data.width-data.sideMargin+10, 2*data.height/3 - \
        buttonHeight/2, data.width-data.sideMargin+10+buttonWidth, \
        2*data.height/3 + buttonHeight/2]
    data.clearAllCoords = clearAllCoords
    canvas.create_rectangle(clearAllCoords[0], clearAllCoords[1], \
        clearAllCoords[2],clearAllCoords[3],fill="grey", activeoutline="white")
    canvas.create_text(data.width-data.sideMargin+10+buttonWidth/2, \
        2*data.height/3, text = "Clear All", font = "System 20")
        
def drawFillAllButton(canvas, data):
    buttonWidth = 200
    buttonHeight = 50
    fillAllCoords = [data.width-data.sideMargin+10, 4*data.height/5 - \
        buttonHeight/2, data.width-data.sideMargin+10+buttonWidth, \
        4*data.height/5 + buttonHeight/2]
    data.fillAllCoords = fillAllCoords
    canvas.create_rectangle(fillAllCoords[0],fillAllCoords[1],fillAllCoords[2],\
        fillAllCoords[3], fill = "grey", activeoutline = "white")
    canvas.create_text(data.width-data.sideMargin+10+buttonWidth/2, \
        4*data.height/5, text = "Fill All", font = "System 20")
    
def drawRowsButtons(canvas, data):
    canvas.create_rectangle(data.rowsButtonCoords[0], data.rowsButtonCoords[1],\
        data.rowsButtonCoords[2], data.rowsButtonCoords[3], fill = "white")
    canvas.create_text(data.rowsButtonCoords[0]+data.rowsButtonDim/2,\
        data.rowsButtonCoords[1]+data.rowsButtonDim/2, text = str(data.rows), \
        font = "System 20")
    canvas.create_rectangle(data.addRows[0], data.addRows[1], data.addRows[2],\
        data.addRows[3], fill = "grey", activeoutline = "white")
    canvas.create_rectangle(data.subtractRows[0], data.subtractRows[1], \
        data.subtractRows[2], data.subtractRows[3], fill = "grey", \
        activeoutline = "white")
    canvas.create_text(data.rowsButtonCoords[0]+data.rowsButtonDim/2,\
        data.rowsButtonCoords[3]+data.rowsButtonDim/2,text="-",font="System 20")
    canvas.create_text(data.rowsButtonCoords[0]+data.rowsButtonDim/2,\
        data.rowsButtonCoords[1]-data.rowsButtonDim/2,text="+",font="System 20")
    canvas.create_text(data.rowsButtonCoords[0]+data.rowsButtonDim/2,\
        data.rowsButtonCoords[1]-100,text="Rows:",font="System 20",fill="white")

def drawColsButtons(canvas, data):
    canvas.create_rectangle(data.colsButtonCoords[0], data.colsButtonCoords[1],\
        data.colsButtonCoords[2], data.colsButtonCoords[3], fill = "white")
    canvas.create_text(data.colsButtonCoords[0]+data.colsButtonDim/2, \
        data.colsButtonCoords[1]+ data.colsButtonDim/2, text = str(data.cols),\
        font = "System 20")
    canvas.create_rectangle(data.addCols[0], data.addCols[1], data.addCols[2], \
        data.addCols[3], fill = "grey", activeoutline = "white")
    canvas.create_rectangle(data.subtractCols[0], data.subtractCols[1], \
        data.subtractCols[2], data.subtractCols[3], fill = "grey", \
        activeoutline = "white")
    canvas.create_text(data.colsButtonCoords[0]+data.colsButtonDim/2,\
        data.colsButtonCoords[3]+data.colsButtonDim/2, text = "-", \
        font = "System 20")
    canvas.create_text(data.colsButtonCoords[0]+data.colsButtonDim/2,\
        data.colsButtonCoords[1]-data.colsButtonDim/2, text = "+", \
        font = "System 20")
    canvas.create_text(data.colsButtonCoords[0]+data.colsButtonDim/2,\
        data.colsButtonCoords[1]-100,text="Cols:",font="System 20",fill="white")
    
    
## Display Board ##
def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col)
            
def drawCell(canvas, data, row, col):
    outline = 1
    w,h=data.width-2*data.sideMargin,data.height-data.topMargin-data.botMargin
    cellW, cellH = w / data.cols, h / data.rows
    x0 = cellW * col + data.sideMargin       #top left corner of new cell:
    y0 = cellH * row + data.topMargin
    x1 = cellW * (col + 1) + data.sideMargin #bottom right corner of new cell:
    y1 = cellH * (row + 1) + data.topMargin
    fill = "SeaGreen1"
    if(data.board[row][col] == 1): fill = "cyan"
    elif(data.board[row][col] == -1): fill = "turquoise"
    elif(data.board[row][col] == 2): fill = "tomato"
    elif(data.board[row][col] == -2): fill = "tomato3"
    elif(data.board[row][col] == 3): fill = "SpringGreen4"
    elif(data.board[row][col] == 4): fill = "SpringGreen2"
    elif(data.board[row][col] == 5): fill = "grey"
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+outline, y0+outline, x1-outline, y1-outline, \
                            fill=fill, activeoutline = "white", width = 2)
            

## Run Code


def run(width=1000, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    class Struct(object): pass
    data = Struct()
    data.width, data.height = width, height
    data.timerDelay = 100 # milliseconds
    init(data)
    
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    data.logo = PhotoImage(file = "logo.gif") 
    data.gameOverImg = PhotoImage(file = "gameOver.gif")
    data.instructions1 = PhotoImage(file = "Instructions1.gif")
    data.instructions2 = PhotoImage(file = "Instructions2.gif")
    #logo from: http://www6.flamingtext.com
    #gameOverImage from: http://www6.flamingtext.com
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop()  
run()
