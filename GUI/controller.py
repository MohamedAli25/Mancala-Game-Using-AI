import pygame

from GUI.board import *
from GUI.pocket import *


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


class MancalaController:
    
    def __init__(self, game_type:GameType=GameType.HUMAN_MODE, 
                    current_player_type:PlayerType = PlayerType.HUMAN,
                    network_notify_cb = print,
                    pA = "",
                    pB = ""):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.pockets = [
            Pocket("B1", (175 + 0 * 75, 185 + 82), (162, 264, 223, 316), self.myfont),
            Pocket("B2", (175 + 1 * 75, 185 + 82), (233, 260, 294, 318), self.myfont),
            Pocket("B3", (175 + 2 * 75, 185 + 82), (304, 263, 367, 316), self.myfont),
            Pocket("B4", (175 + 3 * 75 + 45, 185 + 82), (432, 260, 495, 315), self.myfont),
            Pocket("B5", (175 + 4 * 75 + 45, 185 + 82), (504, 264, 568, 318), self.myfont),
            Pocket("B6", (175 + 5 * 75 + 45, 185 + 82), (574, 262, 642, 319), self.myfont),
            Pocket("MB", (665, 225), (0, 0, 0, 0), self.myfont, 0),
            Pocket("A6", (175 + 5 * 75 + 45, 185), (576, 174, 640, 233), self.myfont),
            Pocket("A5", (175 + 4 * 75 + 45, 185), (504, 180, 569, 229), self.myfont),
            Pocket("A4", (175 + 3 * 75 + 45, 185), (429, 177, 492, 235), self.myfont),
            Pocket("A3", (175 + 2 * 75, 185), (308, 179, 371, 229), self.myfont),
            Pocket("A2", (175 + 1 * 75, 185), (237, 176, 294, 228), self.myfont),
            Pocket("A1", (175 + 0 * 75, 185), (160, 187, 210, 229), self.myfont),
            Pocket("MA", (100, 225), (0, 0, 0, 0), self.myfont, 0)
        ]
        print("names", pA, pB)
        self.mancala_board = Board(self.screen, self.myfont, pA, pB, self.pockets)
        self.game_type = game_type
        self.player_number = Player.PLAYERB
        self.current_player_type = PlayerType.HUMAN

    def get_selected_pocket(self, pos) -> Pocket:
        for p in self.pockets:
            pocket_pos = p.boundry
            if pos[0] > pocket_pos[0] and pos[0] < pocket_pos[2] and pos[1] > pocket_pos[1] and pos[1] < pocket_pos[3]:
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
                    if self.current_player_type == PlayerType.HUMAN: self.process_pocket_click()

    def notify_player_name(self):
        print(self.player_number)

    def check_extra_score(self, last_pocket: Pocket):
        if last_pocket.value != 0 and last_pocket.last_value == 0:
            if last_pocket.name[0] == "B":
                opponent_pocket_name = "A"
            elif last_pocket.name[0] == "A":
                opponent_pocket_name = "B"
            else:
                return
            val = last_pocket.value
            last_pocket.value = 0

            opponent_pocket_name += last_pocket.name[1:]
            opponent_pocket = self.get_pocket_by_name(opponent_pocket_name)
            val += opponent_pocket.value
            opponent_pocket.value = 0
            current_mancala = self.get_pocket_by_name("M" + last_pocket.name[0])
            current_mancala.value += val
            self.mancala_board.render_board()

    def get_pocket_by_name(self, name) -> Pocket:
        print("mancala", name)
        for p in self.pockets:
            if p.name == name: return p

    def get_current_player_number(self, pocket: Pocket):
        player_name = pocket.name[0]
        return Player.PLAYERA if player_name == "A" else Player.PLAYERB

    def process_next_player_number(self, pocket):
        if pocket.name[0] != "M":
            self.player_number = (self.player_number + 1) % 2
            self.process_next_player_type()

    def process_next_player_type(self):
        if self.game_type == GameType.HUMAN_MODE:
            self.current_player_type = PlayerType.HUMAN
        elif self.game_type == GameType.AI_HUMAN_MODE:
            if self.current_player_type == PlayerType.HUMAN:
                self.current_player_type = PlayerType.AI
            else:
                self.current_player_type = PlayerType.HUMAN
        elif self.game_type == GameType.NETWORK_HUMAN_MODE:
            if self.current_player_type == PlayerType.HUMAN:
                self.current_player_type = PlayerType.NETWORK
            else:
                self.current_player_type = PlayerType.HUMAN

    def process_pocket_click(self):
        pos = pygame.mouse.get_pos()
        pocket = self.get_selected_pocket(pos)
        if pocket is not None and self.player_number == self.get_current_player_number(pocket):
            self.process_move(pocket)

    def process_move(self, pocket: Pocket):
        old_val = pocket.value
        pocket.value = 0
        pocket_index = self.pockets.index(pocket)
        for _ in range(old_val):
            pocket_index += 1
            if pocket_index >= len(self.pockets): pocket_index -= len(self.pockets)
            self.pockets[pocket_index].value += 1
            self.mancala_board.render_board()
        if self.current_player_type != PlayerType.NETWORK: self.notify_move(pocket.name)
        self.process_next_player_number(self.pockets[pocket_index])
        self.check_extra_score(self.pockets[pocket_index])
        self.notify_player_name()

    def callback_move(self, pocket_name):
        pocket = self.get_pocket_by_name(pocket_name)
        self.process_move(pocket)
