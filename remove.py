import pygame
import sys
from checker import *
# Initialize Pygame
pygame.init()

# Constants for colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("checker")
checker=checker(screen)
print(checker)
# Main game loop
selectedPiece=None
while True:
      for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                  selectedPiece=checker.selectPiece(pygame.mouse.get_pos(),"white")
            if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()
      
      # Clear the screen
      screen.fill(GREEN)
      checker.drawGuiBoard()
      if(selectedPiece):
            possibleMoves = checker.nextPossibleMoves(selectedPiece)
            temp=[]
            for move in possibleMoves:
                  temp.append(move["nextPosition"])
            possibleMoves=temp
            print(selectedPiece," possible moves ",possibleMoves)
            # to highlight the possibleBoxes
            checker.highlightMoves(possibleMoves)
            
      # Update the display
      pygame.display.flip()
