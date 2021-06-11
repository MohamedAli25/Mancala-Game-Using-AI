import pygame
from GUI.board import Board, WIDTH, HEIGHT
from GUI.pocket import Pocket
from Core.SearchTree import SearchTree
from Core.TreeCreator import TreeCreator
from Core.Enums import MaxMinPlayer

class Player:
    PLAYERA = 0
    PLAYERB = 1

class PlayerType:
    AI = "AI"
    HUMAN = "Human"
    NETWORK = "Network"

class GameType:
    AI_HUMAN_MODE = 0
    NETWORK_HUMAN_MODE = 1
    HUMAN_MODE = 2
    NETWORK_AI_MODE = 3
    AI_AI_MODE = 4

class PlayerNumber:
    PLAYERA = MaxMinPlayer.MIN_PLAYER
    PLAYERB = MaxMinPlayer.MAX_PLAYER

class AIController:
    def __init__(
        self, 
        game_type:GameType=GameType.HUMAN_MODE, 
        current_player_type:PlayerType = PlayerType.HUMAN,
        player_number = PlayerNumber.PLAYERB,
        network_notify_cb = print,
        play_first = True,
        pA = "",
        pB = ""
    ):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.pockets = [
            Pocket("B1", (175+0*75, 185+82), (162, 264, 223, 316), self.myfont),
            Pocket("B2", (175+1*75, 185+82), (233, 260, 294, 318), self.myfont),
            Pocket("B3", (175+2*75, 185+82), (304, 263, 367, 316), self.myfont),
            Pocket("B4", (175+3*75+45, 185+82), (432, 260, 495, 315), self.myfont),
            Pocket("B5", (175+4*75+45, 185+82), (504, 264, 568, 318), self.myfont),
            Pocket("B6", (175+5*75+45, 185+82), (574, 262, 642, 319), self.myfont),
            Pocket("MB", (665,225), (0,0,0,0), self.myfont, 0),
            Pocket("A6", (175+5*75+45, 185), (576, 174, 640, 233), self.myfont),
            Pocket("A5", (175+4*75+45, 185), (504, 180, 569, 229), self.myfont),
            Pocket("A4", (175+3*75+45, 185), (429, 177, 492, 235), self.myfont),
            Pocket("A3", (175+2*75, 185), (308, 179, 371, 229), self.myfont),
            Pocket("A2", (175+1*75, 185), (237, 176, 294, 228), self.myfont),
            Pocket("A1", (175+0*75, 185), (160, 187, 210, 229), self.myfont),  
            Pocket("MA", (100,225), (0,0,0,0), self.myfont, 0)
        ]
        self.mancala_board = Board(self.screen, self.myfont, pA, pB, self.pockets)
        self.game_tree = SearchTree(MaxMinPlayer.MAX_PLAYER)
        self.game_type = game_type
        self.player_number = player_number
        self.current_player_type = current_player_type
        self.__set_pockets_vals()
        self.mancala_board.set_current_player("Player B")
        self.mancala_board.render_board()
        self.network_notify = network_notify_cb
    
    def __set_pockets_vals(self):
        game_state = self.game_tree.get_game_state()
        for i in range(len(game_state)):
            self.pockets[i].value = game_state[i]


    def get_selected_pocket(self, pos) -> Pocket:
        for p in self.pockets:
            pocket_pos = p.boundry
            if pos[0] >pocket_pos[0] and pos[0] < pocket_pos[2] and pos[1] > pocket_pos[1] and pos[1] < pocket_pos[3]:
                return p
    
    def start(self):
        clock = pygame.time.Clock()
        self.start_game(clock)

    def start_game(self, clock):
        self.mancala_board.render_board()
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_player_type == PlayerType.HUMAN:
                        self.process_pocket_click()
                        

    def check_player_turn(self, selected_pocket:Pocket):
        return  (selected_pocket.name[0] == "B" and self.player_number == MaxMinPlayer.MAX_PLAYER) or \
                (selected_pocket.name[0] == "A" and self.player_number == MaxMinPlayer.MIN_PLAYER)        

    def get_pocket_by_name(self, name) -> Pocket:
        for p in self.pockets:
            if p.name == name: return p

    def process_next_player_type(self):
        # if self.player_number == self.game_tree.get_current_player_number():
        #     print("bitch")
        #     return
        if self.game_type == GameType.HUMAN_MODE:
            self.current_player_type = PlayerType.HUMAN
        elif self.game_type == GameType.AI_HUMAN_MODE:
            if self.current_player_type == PlayerType.HUMAN: self.current_player_type = PlayerType.AI
            else: self.current_player_type = PlayerType.HUMAN
        elif self.game_type == GameType.NETWORK_HUMAN_MODE:
            if self.current_player_type == PlayerType.HUMAN: self.current_player_type = PlayerType.NETWORK
            else: self.current_player_type = PlayerType.HUMAN
        print(self.current_player_type)
                    
    def process_pocket_click(self):
        pos = pygame.mouse.get_pos()
        pocket = self.get_selected_pocket(pos)
        if pocket is not None and self.check_player_turn(pocket):
            self.process_move(pocket)
    
    def process_move(self, pocket:Pocket):
        pocket_index = self.pockets.index(pocket)
        self.game_tree.make_move(pocket_index)
        print("current p type", self.current_player_type)
        if self.game_type == GameType.NETWORK_HUMAN_MODE and self.current_player_type != PlayerType.NETWORK:
            self.notify_move(pocket.name)
        self.__set_pockets_vals()
        
        self.player_number = self.game_tree.get_current_player_number()

        if self.player_number == MaxMinPlayer.MAX_PLAYER:
            print("Player B")
            self.mancala_board.set_current_player("Player B")
        else:
            print("Player A")
            self.mancala_board.set_current_player("Player A")
        self.mancala_board.render_board()
        self.process_next_player_type()
    
    def notify_move(self, pocket_name):
        print("Sending", "Move:"+pocket_name)
        self.network_notify("Move:"+pocket_name)

    def callback_move(self, pocket_name):
        if "Move" in pocket_name:
            print("Callback move happended")
            pocket = self.get_pocket_by_name(pocket_name[5:])
            self.process_move(pocket)




