import pygame
import time
from GUI.controller import GameType, PlayerType
from Core.Network import Client, Server
from Controllers.controller import AIController, PlayerNumber
from GUI.controller import MancalaController



def main():
    pygame.init()
    print("Select Game Mode: \n\t1-Human vs. Human  \n\t2-Human vs. Human (Network) \n\t3- Human vs. AI \n\t4-Load")
    mode = input()
    if mode == "1":
            pygame.display.set_caption("MANCALA!")
            game = AIController(pA=PlayerType.HUMAN,
                                pB=PlayerType.HUMAN)
            game.start()
    elif mode == "2":
        try:
            server = Server()
            print("No Server was found, creating new server...")
            pygame.display.set_caption("MANCALA! Server")
            server.start()
            while len(server.get_conn_clients()) == 0: time.sleep(1)
            game = AIController(game_type=GameType.NETWORK_HUMAN_MODE,
                                    current_player_type=PlayerType.HUMAN,
                                    network_notify_cb=server.send_to_active_client,
                                    pA=PlayerType.NETWORK,
                                    pB=PlayerType.HUMAN,
                                    player_number=PlayerNumber.PLAYERB)
            server.recv(callback=game.callback_move)
            game.start()
        except: 
            print("Server was found, connecting to server...")
            pygame.display.set_caption("MANCALA! Client")
            client = Client()
            client.connect()
            game = AIController(game_type=GameType.NETWORK_HUMAN_MODE,
                                    current_player_type=PlayerType.NETWORK,
                                    network_notify_cb=client.send,
                                    pA=PlayerType.HUMAN,
                                    pB=PlayerType.NETWORK,
                                    player_number=PlayerNumber.PLAYERA)
            client.recv(callback=game.callback_move)
            game.start()
    elif mode == "3":
        game = AIController(game_type=GameType.AI_HUMAN_MODE,
                            current_player_type=PlayerType.HUMAN,
                            pA=PlayerType.AI,
                            pB=PlayerType.HUMAN,
                            player_number=PlayerNumber.PLAYERB)
        game.start()
    elif mode == "4":
        game = AIController.load()
        game.start()
    pygame.quit()

main()
