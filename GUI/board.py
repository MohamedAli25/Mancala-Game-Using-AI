import pygame

WIDTH = 800  # these constatnts can't be changed as the pockets dims where calcukated using these dims
HEIGHT = 500  # these constatnts can't be changed as the pockets dims where calcukated using these dims


class Board:
    def __init__(self, screen, objects=None):
        self.__screen = screen
        self.__board_objects = []
        if objects is not None: self.add_objects(objects)

    def add_object(self, object) -> None:
        self.__board_objects.append(object)

    def add_objects(self, object_list: list) -> None:
        for obj in object_list:
            if obj not in self.__board_objects: self.__board_objects.append(obj)

    def render_board(self) -> None:
        img = pygame.image.load("GUI/assets/wood.jpg").convert()
        self.__screen.blit(img, [0, 0])
        board = pygame.image.load("GUI/assets/board.PNG")
        self.__screen.blit(board, [(WIDTH - board.get_width()) // 2, (HEIGHT - board.get_height()) // 2])
        for obj in self.__board_objects:
            obj.render(self.__screen)
        pygame.display.flip()
