from checker import *
# Initialize Pygame
pygame.init()
import sys
# Constants for colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Checkers")
class Game:
    def __init__(self,screen) -> None:
        self.checker=checker(screen)
        self.turn="white"
        self.selectedPiece=None
        self.possibleMoves=None #these serves as allowable boxes to move the pieces
        self.start()
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # first check if the clicking on nextMove otherwise selectedPiece will be none
                    if self.possibleMoves:
                        print(self.selectedPiece,self.possibleMoves)
                        hasMoved =self.checker.moveToNextPosition(self.selectedPiece,self.possibleMoves,pygame.mouse.get_pos()) #it does all internal board work
                        if hasMoved:
                            if self.selectedPiece.color =="white":
                                self.turn="black"
                            else:
                                self.turn= "white"
                            self.selectedPiece=None
                            self.possibleMoves=None
                            print(self.checker)
                        
                    # to select a piece of a specific player
                    self.selectedPiece =self.checker.selectPiece(pygame.mouse.get_pos(),self.turn) #selectedPiece can be None
                    # select the next box to move to 
                    # return True if moved so change turn and all attributes here 
                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Clear the screen
            screen.fill(GREEN)
            self.checker.drawGuiBoard()
            self.checker.showText()
            if(self.selectedPiece):
                self.possibleMoves = self.checker.nextPossibleMoves(self.selectedPiece)
                print(self.selectedPiece," moves:",self.possibleMoves)
                # to highlight the possibleBoxes
                self.checker.highlightMoves(self.possibleMoves)
            # Update the display
            pygame.display.flip()
game=Game(screen)
