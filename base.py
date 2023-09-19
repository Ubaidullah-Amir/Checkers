import pygame
class Base:
    def __init__(self,len=8):
        self.board=[]
        for row in range(8):
            rowArr=[]
            for column in range(8):
                if (row < 3 )and ((column%2==1 and row%2==0) or (column%2==0 and row%2==1)) :
                    # Black Piece
                    rowArr.append(Piece(1,(row,column)))
                    continue
                if(row > 4) and ((column%2==1 and row%2==0) or ( column%2==0 and row%2==1)):
                    # White piece
                    rowArr.append(Piece(0,(row,column)))
                    continue
                rowArr.append(None)
            self.board.append(rowArr)
            rowArr=[]
    def __str__(self):
        string="."
        for row in range(8):
            string +="\t"
            for column in range(8):
                string += str(self.board[row][column]) +" "
                
            string += "\n"
        return string
    def nextPossibleMoves(self,selectedPiece):
        row,column = selectedPiece.position
        possibleLocations=[]
        # king can go any position irrespective black or white
        if selectedPiece.king:
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
            return {"isAllowed":False,"nextPosition":None,"opponent":False}
        if self.board[row][column] == None:
            return {"isAllowed":True,"nextPosition":nextPosition,"opponent":double}
        # oppennet piece at next position
        if  type(self.board[row][column]) ==Piece:
            if self.board[row][column].color != selectedPiece.color:
                oppenentPiece=self.board[row][column]
                oppRow,oppColumn=oppenentPiece.position
                # a special case if two opponents are in the same direction
                # a special base case to stop the function to run more than twice
                if double == True :
                    return {"isAllowed":False,"nextPosition":None,"opponent":None}
                if direction == "ne":
                    return self.allowedMove((row-1,column+1),"ne",True)
                if direction == "nw":
                    return self.allowedMove((row-1,column-1),"nw",True)
                if direction == "se":
                    return self.allowedMove((row+1,column+1),"se",True)
                if direction == "sw":
                    return self.allowedMove((row+1,column-1),"sw",True)
                
            else :
                # own piece at next position
                return {"isAllowed":False,"nextPosition":nextPosition,"opponent":False}
        
     
# attributes:

# isKing
# color
# position (row,column) or (y,x) for drawing

# img
# rect
class Piece:
    def __init__(self,color,position,isKing=False):
        self.isKing=isKing
        
        
        if color=="white":
            self.color="white"
            if isKing:
                self.img = pygame.image.load("whiteKing.png")
            else:
                self.img = pygame.image.load("whitepiece.png")
        elif color == "black":
            self.color="black"
            if isKing:
                self.img = pygame.image.load("blackKing.png")
            else:
                self.img = pygame.image.load("blackpiece.png")
        else:
            raise Exception("Color Not Given")
        self.img.convert()

        if not type(position) is tuple:
            raise TypeError("Only tuples are allowed for position")
        self.position=position
        self.rect = self.img.get_rect()
    # to draw a piece
    def draw(self,screen,color):
        size=60
        y,x=self.position
        x,y=x*size,y*size
        self.rect.topleft=x,y
        if color == self.color:
            screen.blit(self.img, self.rect)
            pygame.draw.rect(screen, (100, 3, 3), self.rect, 5)
        else:
            screen.blit(self.img, self.rect)
            pygame.draw.rect(screen, (252, 3, 3), self.rect, -1)
    
        
    def __str__(self):
        return "P"+str(self.color)+str(self.position)
class Box:
    def __init__(self,color,position):
        if color=="white":
            self.color="white"
        elif color == "black":
            self.color="black"
        else:
            raise Exception("Color Not Given")
        self.position=position
        size=60
        y,x=self.position
        x,y=x*size,y*size
        cordinate=(x,y,size,size)
        self.rect=pygame.Rect(cordinate)
    def draw(self,screen):  
        
        if self.color == "white":
            # white box
            # x,y,width,height
            # pygame.Rect(30, 30, 60, 60)
            pygame.draw.rect(screen,(255, 255, 255) , self.rect)
        elif self.color == "black":
            # black box
            pygame.draw.rect(screen,(0,0,0) ,self.rect)
    
    def __str__(self):
        return "B"+str(self.color)+str(self.position)
class Circle:
    def __init__(self,screen,position):
        y,x=position
        size=60
        x,y= (x*size)+(size/2) , (y*size)+(size/2)
        pygame.draw.circle(screen, (0, 255, 0),
                   [x,y], 10, 0)



                    

            
              
                