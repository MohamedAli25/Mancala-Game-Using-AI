import pygame

from GUI.controller import MancalaController


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("MANCALA!")
    game = MancalaController()
    game.start()
    pygame.quit()


main()
