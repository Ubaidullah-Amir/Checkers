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
        NewGame=font.render(text, True, (0,100,150), (100,12,160))
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
            
            
            NewGameRect.center=(500,30)
            screen.blit(NewGame, NewGameRect)
            # Update the display
            pygame.display.flip()
    def showFinishMenu(self,text):
        font = pygame.font.Font('freesansbold.ttf', 32)
        TryAgain=font.render("Try Again", True, (0,100,150), (100,12,160))
        TryAgainRect = TryAgain.get_rect()
        BlackWonText=font.render("Black Won ---"+str(self.blackWin), True, (0,100,150), (100,12,160))
        BlackWonTextRect = BlackWonText.get_rect()
        WhiteWonText=font.render("White Won ---"+str(self.whiteWin), True, (0,100,150), (100,12,160))
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
            WhiteWonTextRect.center=(500,200)
            screen.blit(WhiteWonText, WhiteWonTextRect)
            BlackWonTextRect.center=(500,100)
            screen.blit(BlackWonText, BlackWonTextRect)
            TryAgainRect.center=(500,30)
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
            screen.fill(GREEN)
            self.checker.drawGuiBoard(self.turn)
            gameEnded = self.checker.showText()
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
game=Game(screen)
