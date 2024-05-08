from checker import *
# Initialize Pygame
pygame.init()
import sys
# Constants for colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTBLUE = (171, 203, 255)
TEXTCOLOR = (3, 99, 255)

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Checkers")
class Game:
    def __init__(self,screen) -> None:
        self.checker=checker(screen)
        self.turn="white"
        self.hasEliminated=False
        self.selectedPiece=None
        self.possibleMoves=[] #these serves as allowable boxes to move the pieces
        self.opponentDict=self.checker.oppnentDictMaker(self.turn)
        self.blackWin=0
        self.whiteWin=0
        self.showMenu("New Game")
        while True:
            gameWon = self.start()
            if gameWon == "BLACK_WON":
                self.blackWin+=1
                self.showFinishMenu(" try again")
            if gameWon == "WHITE_WON":
                self.whiteWin+=1
                self.showFinishMenu(" try again")

    def showMenu(self,text):
        font = pygame.font.Font('freesansbold.ttf', 32)
        NewGame=font.render(text, True, TEXTCOLOR, WHITE)
        NewGameRect = NewGame.get_rect()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    collide=NewGameRect.collidepoint(pygame.mouse.get_pos())
                    if collide:
                        return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill(WHITE)
            
            
            NewGameRect.center=(width/2,30)
            screen.blit(NewGame, NewGameRect)
            # Update the display
            pygame.display.flip()
    def showFinishMenu(self,text):
        font = pygame.font.Font('freesansbold.ttf', 32)
        TryAgain=font.render("Try Again", True,TEXTCOLOR, WHITE)
        TryAgainRect = TryAgain.get_rect()
        BlackWonText=font.render("Black Won ---"+str(self.blackWin), True,TEXTCOLOR, WHITE)
        BlackWonTextRect = BlackWonText.get_rect()
        WhiteWonText=font.render("White Won ---"+str(self.whiteWin), True,TEXTCOLOR, WHITE)
        WhiteWonTextRect = WhiteWonText.get_rect()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    collide=TryAgainRect.collidepoint(pygame.mouse.get_pos())
                    if collide:
                        return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill(WHITE)
            WhiteWonTextRect.center=(width/2,200)
            screen.blit(WhiteWonText, WhiteWonTextRect)
            BlackWonTextRect.center=(width/2,100)
            screen.blit(BlackWonText, BlackWonTextRect)
            TryAgainRect.center=(width/2,30)
            screen.blit(TryAgain, TryAgainRect)
            # Update the display
            pygame.display.flip()
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.hasEliminated:
                        value=self.checker.selectPiece(pygame.mouse.get_pos(),self.turn,self.opponentDict)
                        if value:
                            self.selectedPiece=value
                            self.possibleMoves = self.checker.nextPossibleMoves(self.selectedPiece)
                            opponentArr=[]
                            for move in self.possibleMoves:
                                if move["opponent"]:
                                    opponentArr.append(move)
                            if len(opponentArr)>0:
                                self.possibleMoves=opponentArr
                            continue
                    if self.selectedPiece:
                        hasMoved,hasEliminated,piece,becameKing =self.checker.moveToNextPosition(self.selectedPiece,self.possibleMoves,pygame.mouse.get_pos()) #it does all internal board work
                        if hasMoved and becameKing:
                            # switch turn
                            if self.selectedPiece.color =="white":
                                self.turn="black"
                            else:
                                self.turn= "white"
                            self.selectedPiece=None
                            self.possibleMoves=[]
                            self.hasEliminated=False
                            # oppnentDictMaker bcoz board has changed and turn also changed
                            self.opponentDict=self.checker.oppnentDictMaker(self.turn)
                            continue
                        if hasMoved and not hasEliminated:
                            # switch turn
                            if self.selectedPiece.color =="white":
                                self.turn="black"
                            else:
                                self.turn= "white"
                            self.selectedPiece=None
                            self.possibleMoves=[]
                            self.hasEliminated=False
                            # oppnentDictMaker bcoz board has changed and turn also changed
                            self.opponentDict=self.checker.oppnentDictMaker(self.turn)
                        if hasMoved and hasEliminated:

                            self.hasEliminated=True
                            self.selectedPiece=piece #newPiece
                            self.possibleMoves = self.checker.nextPossibleMoves(self.selectedPiece)
                            opponentArr=[]
                            for move in self.possibleMoves:
                                if move["opponent"]:
                                    opponentArr.append(move)
                            if len(opponentArr)>0:
                                self.possibleMoves=opponentArr
                                # oppnentDictMaker bcoz board has changed but turn remains same 
                                self.opponentDict=self.checker.oppnentDictMaker(self.turn)
                            else:
                                # switch turn
                                if self.selectedPiece.color =="white":
                                    self.turn="black"
                                else:
                                    self.turn= "white"
                                self.selectedPiece=None
                                self.possibleMoves=[]
                                self.hasEliminated=False
                                # oppnentDictMaker bcoz board has changed and turn also changed
                                self.opponentDict=self.checker.oppnentDictMaker(self.turn)
                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Clear the screen
            screen.fill(LIGHTBLUE)
            self.checker.drawGuiBoard(self.turn)
            gameEnded = self.checker.showText(self.blackWin,self.whiteWin)
            if gameEnded == "BLACK_WON" or gameEnded == "WHITE_WON":
                self.checker=checker(screen)
                self.turn="white"
                self.hasEliminated=False
                self.selectedPiece=None
                self.possibleMoves=[] 
                self.opponentDict=self.checker.oppnentDictMaker(self.turn)
                return gameEnded
            if(self.selectedPiece):
                
                self.checker.highlightMoves(self.possibleMoves)
            # Update the display
            pygame.display.flip()

if __name__ == "__main__":
    game=Game(screen)
