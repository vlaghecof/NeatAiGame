"# NeatAiGame"
# needs : pipe and ground fol collision , bird to fly

import os
import random

import neat
import pygame
import Settings
import Game
import AiConfig

pygame.font.init()


if __name__ == '__main__':
    win = pygame.display.set_mode((Settings.WIN_WIDTH, Settings.WIN_HEIGHT))
    runGame = True

    while runGame:
        AiConfig.draw_Initwindow(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    runGame = False
                    Game.human()

                if event.key == pygame.K_2:
                    runGame = False
                    local_dir = os.path.dirname(__file__)
                    config_path = os.path.join(local_dir, "configuration_file")
                    AiConfig.run(config_path)


