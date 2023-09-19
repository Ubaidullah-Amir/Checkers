import pygame

     
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
            pygame.draw.rect(screen, (100, 100, 3), self.rect, 2)
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



                    

            
              
                