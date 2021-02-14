import os
import random

import neat
import pygame
import Settings
import Game

GEN = 0

def evalGenome(genomes, config):
    nets = []
    ge = []
    birds = []

    global GEN
    GEN += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Game.Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Game.Base(550)
    pipes = [Game.Pipe(Settings.PIPE_DIST)]
    win = pygame.display.set_mode((Settings.WIN_WIDTH, Settings.WIN_HEIGHT))

    # set the framerate
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        add_pipe = False
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # bird.jump()
                    pass

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        # bird.move()
        remove = []
        for pipe in pipes:

            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            pipe.move()
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5

            pipes.append(Game.Pipe(Settings.PIPE_DIST))

        for rem in remove:
            pipes.remove(rem)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 550 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        Game.draw_window(win, birds, pipes, base, score, GEN, False)

        if score > 50:
            break

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(evalGenome, 50)

    print('\nBest genome:\n{!s}'.format(winner))

def draw_Initwindow(win):
    win.blit(Settings.BG_IMG, (0, 0))

    HumanChoice = Settings.STAT_FONT.render("Press 1 to play the game : ", 1, (255, 255, 255))
    win.blit(HumanChoice, (10, 300))

    HumanChoice = Settings.STAT_FONT.render("Press 2 to train the Ai : ", 1, (255, 255, 255))
    win.blit(HumanChoice, (10, Settings.WIN_HEIGHT / 2 + 30))

    pygame.display.update()
