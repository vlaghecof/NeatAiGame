"# NeatAiGame"
# needs : pipe and ground fol collision , bird to fly

import os
import random

import neat
import pygame
import Settings

pygame.font.init()

GEN = 0


# Model the bird class
class Bird:
    IMGS = Settings.BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    # the main control loop
    def move(self):
        self.tick_count += 1
        disp = self.vel * self.tick_count + 1.5 * self.tick_count ** 2  # formula to calculate the displacement

        if disp >= 16:
            disp = 16
        if disp < 0:
            disp -= 2

        self.y += disp

        if disp < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img_count = 1

        self.img = self.IMGS[(self.img_count - 1) // 5]

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = Settings.GAPGL
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(Settings.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = Settings.PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 350)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    #     implementing collision using a mask( an image of the pixels , to achieve pefect pixel collision)
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bot_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bot_point:
            return True
        return False


class Base:
    VEL = 5
    WIDTH = Settings.BASE_IMG.get_width()
    IMG = Settings.BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.x2 < -650:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):

        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


def draw_window(win, birds, pipes, base, score, gen, human):
    win.blit(Settings.BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    score_label = Settings.STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (Settings.WIN_WIDTH - score_label.get_width() - 15, 10))

    gen = Settings.STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(gen, (10, 10))

    aliveBirds = Settings.STAT_FONT.render("Birds Alive: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(aliveBirds, (10, 40))

    if human:
        endMessage = Settings.STAT_FONT.render("Final Score : " + str(score), 1, (255, 255, 255))
        win.blit(endMessage, (300, 300))
        endMessage2 = Settings.STAT_FONT.render("Press Space to Play Again", 1, (255, 255, 255))
        win.blit(endMessage2, (50, 400))

    base.draw(win)

    for bird in birds:
        bird.draw(win)
    pygame.display.update()


def evalGenome(genomes, config):
    nets = []
    ge = []
    birds = []

    global GEN
    GEN += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(550)
    pipes = [Pipe(Settings.PIPE_DIST)]
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

            pipes.append(Pipe(Settings.PIPE_DIST))

        for rem in remove:
            pipes.remove(rem)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 550 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN, False)

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


def human():
    bird = Bird(230, 350)
    base = Base(550)
    pipes = [Pipe(Settings.PIPE_DIST)]
    win = pygame.display.set_mode((Settings.WIN_WIDTH, Settings.WIN_HEIGHT))

    # set the framerate
    clock = pygame.time.Clock()
    score = 0

    humanPl = False
    run = True
    decision = True

    while run:
        add_pipe = False
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()
        remove = []

        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                humanPl = True
                run = False

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
        if add_pipe:
            score += 1
            pipes.append(Pipe(Settings.PIPE_DIST))

        for rem in remove:
            pipes.remove(rem)

        if bird.y + bird.img.get_height() >= 550 or bird.y < 0:
            humanPl = True
            run = False

        base.move()

        draw_window(win, [bird], pipes, base, score, 0, humanPl)
    else:
        while decision:
            draw_window(win, [bird], pipes, base, score, 0, humanPl)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    decision = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        decision = False
                        human()




def draw_Initwindow(win):
    win.blit(Settings.BG_IMG, (0, 0))

    HumanChoice = Settings.STAT_FONT.render("Press 1 to play the game : ", 1, (255, 255, 255))
    win.blit(HumanChoice, (10, 300))

    HumanChoice = Settings.STAT_FONT.render("Press 2 to train the Ai : ", 1, (255, 255, 255))
    win.blit(HumanChoice, (10, Settings.WIN_HEIGHT / 2 + 30))

    pygame.display.update()


if __name__ == '__main__':
    win = pygame.display.set_mode((Settings.WIN_WIDTH, Settings.WIN_HEIGHT))
    runGame = True

    while runGame:
        draw_Initwindow(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    runGame = False
                    human()

                if event.key == pygame.K_2:
                    runGame = False
                    local_dir = os.path.dirname(__file__)
                    config_path = os.path.join(local_dir, "configuration_file")
                    run(config_path)


