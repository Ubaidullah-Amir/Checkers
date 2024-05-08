import pygame
from base import *
from game import TEXTCOLOR,WHITE

# gui checkers contains all the function to manuplite the underlying Base Class
class checker:
    def __init__(self,screen) -> None:
        # self.base = Base()
        # self.board= self.base.board
        self.guiBoard=[]
        self.whitePiecesArr=[]
        self.blackPiecesArr=[]
        self.whitePieces=12
        self.blackPieces=12
        self.heigh=30
        self.width=30
        self.screen=screen
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        
        for row in range(8):
            rowArr=[]
            for column in range(8):
                if row < 3 :
                    if ((column%2==1 and row%2==0) or (column%2==0 and row%2==1)) :
                        # Black Piece
                        piece=Piece("black",(row,column))
                        self.blackPiecesArr.append(piece)
                        rowArr.append(piece)
                        continue
                    else:
                        # white Box
                        box=Box("white",(row,column))
                        rowArr.append(box)
                        continue
                if row>4:
                    if((column%2==1 and row%2==0) or ( column%2==0 and row%2==1)):
                        # White piece
                        piece=Piece("white",(row,column))
                        self.whitePiecesArr.append(piece)
                        rowArr.append(piece)
                        continue
                    else:
                        # white Box
                        box=Box("white",(row,column))
                        rowArr.append(box)
                        continue
                # draw no Piece
                if row>2 and row <5:
                    if((column%2==1 and row%2==0) or ( column%2==0 and row%2==1)):
                        # Black Box
                        box=Box("black",(row,column))
                        rowArr.append(box)
                        continue
                    else:
                        # white Box
                        box=Box("white",(row,column))
                        rowArr.append(box)
                        continue
                    

            self.guiBoard.append(rowArr)
            rowArr=[]

    def drawGuiBoard(self,turn):
        for row in range(8):
            for column in range(8):
                if type(self.guiBoard[row][column]) is Piece:
                    self.guiBoard[row][column].draw(self.screen,turn)
                else:
                    self.guiBoard[row][column].draw(self.screen)
    def selectPiece(self,mousePos,color,opponentDict):
                if len(opponentDict)==0:
                    # if opponentDict is empty you can select any piece of specified color
                    for row in range(8):
                        for column in range(8):
                            collide=self.guiBoard[row][column].rect.collidepoint(mousePos)
                            isPiece=type(self.guiBoard[row][column]) is Piece
                            colorMatch=color ==self.guiBoard[row][column].color

                            if collide and isPiece and colorMatch:
                                return self.guiBoard[row][column]
                    return None
                else:
                    # but if it is not empty then you can select only pieces in opponentDict
                    for positionStr in opponentDict:
                        piece=opponentDict[positionStr]
                        collide=piece.rect.collidepoint(mousePos) #only this is necessary rest are redundant
                        isPiece=type(piece) is Piece
                        colorMatch=color ==piece.color

                        if collide and isPiece and colorMatch:
                            return piece
                    return None


                
    
    def nextPossibleMoves(self,selectedPiece):
        row,column = selectedPiece.position
        possibleLocations=[]
        # king can go any position irrespective black or white
        if selectedPiece.isKing:
            ne=(row-1,column+1) # north east
            nw=(row-1,column-1) # north west
            se=(row+1,column+1) # south east
            sw=(row+1,column-1) # south west
            totalMoves=[ne,nw,se,sw]
            dirArr= ["ne","nw","se","sw"]
            for index,move in enumerate(totalMoves):
                # direction from original positoin and the coordinates to reach next position
                dict = self.allowedMove(move,dirArr[index],selectedPiece)
                if dict["isAllowed"]:
                    possibleLocations.append(dict)
            return possibleLocations
        if selectedPiece.color =="white":
            
            ne=(row-1,column+1) # north east
            nw=(row-1,column-1) # north west
            totalMoves=[ne,nw]
            dirArr= ["ne","nw"]
            for index,move in enumerate(totalMoves):
                dict = self.allowedMove(move,dirArr[index],selectedPiece)
                if dict["isAllowed"]:
                    possibleLocations.append(dict)
            return possibleLocations
        else :
            
            se=(row+1,column+1) # south east
            sw=(row+1,column-1) # south west
            totalMoves=[se,sw]
            dirArr= ["se","sw"]
            for index,move in enumerate(totalMoves):
                dict = self.allowedMove(move,dirArr[index],selectedPiece)
                if dict["isAllowed"]:
                    possibleLocations.append(dict)
            return possibleLocations
    # the nextPosition and direction are of the next move
    def allowedMove(self,nextPosition,direction,selectedPiece,double=False):
        # double can be used for detecting if there is any opponent
        row,column=nextPosition
        
        # out of board
        if (row > 7 or row <0 ) or (column > 7 or column <0 ):
            return {"isAllowed":False,"nextPosition":None,"direction":direction,"opponent":False}
        if type(self.guiBoard[row][column]) ==Box:
            return {"isAllowed":True,"nextPosition":nextPosition,"direction":direction,"opponent":double}
        # oppennet piece at next position
        if  type(self.guiBoard[row][column]) ==Piece:
            if self.guiBoard[row][column].color != selectedPiece.color:
                oppenentPiece=self.guiBoard[row][column]
                oppRow,oppColumn=oppenentPiece.position
                # a special case if two opponents are in the same direction
                # a special base case to stop the function to run more than twice
                if double == True :
                    return {"isAllowed":False,"nextPosition":None,"direction":direction,"opponent":None}
                if direction == "ne":
                    return self.allowedMove((row-1,column+1),"ne",selectedPiece,True)
                if direction == "nw":
                    return self.allowedMove((row-1,column-1),"nw",selectedPiece,True)
                if direction == "se":
                    return self.allowedMove((row+1,column+1),"se",selectedPiece,True)
                if direction == "sw":
                    return self.allowedMove((row+1,column-1),"sw",selectedPiece,True)
                
            else :
                # own piece at next position
                return {"isAllowed":False,"nextPosition":nextPosition,"direction":direction,"opponent":False}        
         

    def highlightMoves(self,possibleMoves):
        for move in possibleMoves:
            # it draws a circle
            Circle(self.screen,move["nextPosition"])
    def moveToNextPosition(self,selectedPiece,possibleMoves,mousePos):
        # possible move is list of dictionary
        # here we also see whther there is a possiblity of a king
        becomeKing=False
        for move in possibleMoves:
            row,column=move["nextPosition"]
                
            collide=self.guiBoard[row][column].rect.collidepoint(mousePos)
            if collide :
                # creates a King or a Piece
                if selectedPiece.color == "white":
                    if row==0 and not selectedPiece.isKing:
                        # white piece becomes a King
                        self.guiBoard[row][column]=Piece("white",(row,column),True)
                        becomeKing=True
                    elif selectedPiece.isKing:
                        self.guiBoard[row][column]=Piece("white",(row,column),True)
                    else:
                        self.guiBoard[row][column]=Piece("white",(row,column))
                else:
                    if row==7 and not selectedPiece.isKing:
                        # black piece becomes a King
                        self.guiBoard[row][column]=Piece("black",(row,column),True)
                        becomeKing=True
                    elif selectedPiece.isKing:
                        self.guiBoard[row][column]=Piece("black",(row,column),True)
                    else:
                        self.guiBoard[row][column]=Piece("black",(row,column))
                
                oldrow,oldcol=selectedPiece.position
                self.guiBoard[oldrow][oldcol]=Box("black",(oldrow,oldcol))
                if move['opponent']:
                    if move["direction"] == "ne":
                        if self.guiBoard[oldrow-1][oldcol+1].color == "white":
                            self.whitePieces-=1
                        else:
                            self.blackPieces-=1
                        self.guiBoard[oldrow-1][oldcol+1]=Box("black",(oldrow-1,oldcol+1))
                    elif move["direction"] == "nw":
                        if self.guiBoard[oldrow-1][oldcol-1].color == "white":
                            self.whitePieces-=1
                        else:
                            self.blackPieces-=1
                        self.guiBoard[oldrow-1][oldcol-1]=Box("black",(oldrow-1,oldcol-1))
                    elif move["direction"] == "se":
                        if self.guiBoard[oldrow+1][oldcol+1].color == "white":
                            self.whitePieces-=1
                        else:
                            self.blackPieces-=1
                        self.guiBoard[oldrow+1][oldcol+1]=Box("black",(oldrow+1,oldcol+1))
                    elif move["direction"] == "sw":
                        if self.guiBoard[oldrow+1][oldcol-1].color == "white":
                            self.whitePieces-=1
                        else:
                            self.blackPieces-=1
                        self.guiBoard[oldrow+1][oldcol-1]=Box("black",(oldrow+1,oldcol-1))
                    return True,True,self.guiBoard[row][column],becomeKing
                
                return True,False,None,becomeKing
            
                

        return False,False,None,becomeKing
    def highlightOwnPieces(self,color):
        for row in range(8):
            for column in range(8):
                item=self.guiBoard[row][column]
                if type(item) is Piece and item.color==color:
                    item.highLight(self.screen)
    def showText(self,blackWin,whiteWin):
        if self.whitePieces==0:
            # winningTxt=self.font.render("black has won", True, TEXTCOLOR, WHITE)
            # winningtxtRect = winningTxt.get_rect()
            # winningtxtRect.center=(500,30)
            # self.screen.blit(winningTxt, winningtxtRect)
            return "BLACK_WON"
        if self.blackPieces==0:
            # winningTxt=self.font.render("white has won", True, TEXTCOLOR, WHITE)
            # winningtxtRect = winningTxt.get_rect()
            # winningtxtRect.center=(600,30)
            # self.screen.blit(winningTxt, winningtxtRect)
            return "WHITE_WON"

        BlackWonText=self.font.render("Black Won ---"+str(blackWin), True,TEXTCOLOR, WHITE)
        BlackWonTextRect = BlackWonText.get_rect()
        WhiteWonText=self.font.render("White Won ---"+str(whiteWin), True,TEXTCOLOR, WHITE)
        WhiteWonTextRect = WhiteWonText.get_rect()
        
        WhiteWonTextRect.center=(600,50)
        self.screen.blit(WhiteWonText, WhiteWonTextRect)
        BlackWonTextRect.center=(600,100)
        self.screen.blit(BlackWonText, BlackWonTextRect)



        # counts TEXTs
        whitePieceTxt=self.font.render("white count:"+str(self.whitePieces), True, TEXTCOLOR, WHITE)
        blackPieceTxt=self.font.render("black count:"+str(self.blackPieces), True, TEXTCOLOR, WHITE)
        whitePiecetxtRect = whitePieceTxt.get_rect()
        whitePiecetxtRect.center=(600,250)
        blackPiecetxtRect = blackPieceTxt.get_rect()
        blackPiecetxtRect.center=(600,300)
        self.screen.blit(whitePieceTxt, whitePiecetxtRect)
        self.screen.blit(blackPieceTxt, blackPiecetxtRect)


    def oppnentDictMaker(self,turn):
            oppDict={}
            for row in range(8):
                for column in range(8):
                    item = self.guiBoard[row][column]
                    if type(item) ==Piece and item.color==turn:
                        possibleMove=self.nextPossibleMoves(item)
                        for move in possibleMove:
                            if move["opponent"]:
                                oppDict[str(row)+","+str(column)]=self.guiBoard[row][column]
            return oppDict
                            

    def __str__(self):
        string="."
        for row in range(8):
            string +="\t"
            for column in range(8):
                string += str(self.guiBoard[row][column]) +" "
                
            string += "\n"
        return string
        