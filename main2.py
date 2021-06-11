import pygame
from Controllers.controller import AIController

pygame.init()
pygame.font.init()

pygame.display.set_caption("MANCALA!")
game = AIController()
game.start()