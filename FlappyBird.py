import random
import pygame
import sys
from itertools import cycle
from pygame.locals import *

FPS = 60

WINDOWWIDTH = 300
WINDOWHIEGHT = 512
BASEHEIGHT = 100
PIPEWIDTH = 100
GAPSIZE = 100
BIRDX = 100
birdColors = ('red', 'green', 'yellow', 'blue', 'purple')
backGrounds = ('Day', 'Forest', 'Night', 'Moon')
bases = ('Day', 'Night')
pipeColors = ('red', 'green', 'blue')


def main():
    global SURF, FPSCLOCK
    pygame.init()
    SURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHIEGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_F4)):
                pygame.quit()
                sys.exit()

        birdColor = birdColors[random.randrange(0, 5)]
        n = random.randrange(0, len(backGrounds))
        global IMAGES
        IMAGES = {}
        IMAGES['BG'] = pygame.image.load('assets/Sprites/Backgrounds/background_' + backGrounds[n] + '.png')
        SURF.blit(IMAGES['BG'], (0, 0,))
        IMAGES['BIRD'] = (pygame.image.load('assets/Sprites/Birds/birdFlapUp_' + birdColor + '.png'),
                          pygame.image.load('assets/Sprites/Birds/birdFlap_' + birdColor + '.png'),
                          pygame.image.load('assets/Sprites/Birds/birdFlapDown_' + birdColor + '.png'))
        n = 0 if (n == 0 or n == 1) else 1
        IMAGES['BASE'] = pygame.image.load('assets/Sprites/Bases/' + bases[n] + '.png')
        n = random.randrange(0, len(pipeColors))
        IMAGES['PIPES'] = (
            pygame.transform.flip(pygame.image.load('assets/Sprites/Pipes/pipe_' + pipeColors[n] + '.png'), False,
                                  True),
            pygame.image.load('assets/Sprites/Pipes/pipe_' + pipeColors[n] + '.png'))
        pygame.display.update()
        IMAGES['NUMBERS'] = []
        for i in range(0, 10):
            IMAGES['NUMBERS'].append(pygame.image.load('assets/Sprites/Numbers/'+str(i)+'.png'))

        IMAGES['SCREENS'] = (pygame.image.load('assets/Sprites/Screens/Start.png'),
                             pygame.image.load('assets/Sprites/Screens/End.png'))
        start = startGame()
        game = playGame(start[0], start[1])
        endGame(game[0], game[1], game[2], game[3])
        FPSCLOCK.tick(FPS)


def startGame():
    baseShift = 0
    birdIndex = cycle([0, 1, 2, 1])
    index = next(birdIndex)
    birdDeviation = 0
    loopIter = 0
    vel = 1
    up = True
    maxDeviation = 20
    startScreenPos = (WINDOWWIDTH/2 - IMAGES['SCREENS'][0].get_width()/2,
                      (WINDOWHIEGHT-BASEHEIGHT)/2 - IMAGES['SCREENS'][0].get_height()/2 )
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_F4)):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return (birdDeviation, baseShift)
        # -------------Start Blitting Images------------
        SURF.blit(IMAGES['BG'], (0, 0,))
        SURF.blit(IMAGES['BASE'], (baseShift, WINDOWHIEGHT - BASEHEIGHT))
        if baseShift >= -90:
            baseShift -= 2
        else:
            baseShift = 0
        if (loopIter + 1) % 5 == 0:
            index = next(birdIndex)
        birdImg = IMAGES['BIRD'][index]
        SURF.blit(birdImg, (BIRDX-50, int((WINDOWHIEGHT - BASEHEIGHT) / 2) + birdDeviation))
        SURF.blit(IMAGES['SCREENS'][0], startScreenPos)
        # ------------End Blitting Images------------

        # SHM Motion of the BIRD
        if up:
            birdDeviation = birdDeviation + vel
        else:
            birdDeviation = birdDeviation - vel
        if birdDeviation >= maxDeviation:
            up = False
        elif birdDeviation <= (-maxDeviation):
            up = True
        # ------------ Motion END --------
        loopIter = (loopIter + 1) % FPS
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def playGame(birdDeviation, baseShift):
    loopIter = index = 0
    gravity = 30 / FPS
    maxVelDown = 240 / FPS
    vel = 0
    ascendVal = 360 / FPS
    indices = cycle([0, 1, 2, 1])
    rotationSpeed = 60 / FPS
    rotation = 0
    pipeSpeed = 90 / FPS
    flapping = False
    pipes = [generatePipes(IMAGES['PIPES']), generatePipes(IMAGES['PIPES'])]
    pipes[1][0][0] += 200
    pipes[1][1][0] += 200
    score = 0
    birdY = int((WINDOWHIEGHT - BASEHEIGHT) / 2) + birdDeviation
    pipeWidth = IMAGES['PIPES'][0].get_width()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flapping = True
            if event.type == KEYDOWN and (event.key == K_s):
                score = 6969*2

        birdY += vel
        # -------------Start Blitting Images------------
        SURF.blit(IMAGES['BG'], (0, 0,))
        for pipe in pipes:
            SURF.blit(IMAGES['PIPES'][0], tuple(pipe[0]))
            SURF.blit(IMAGES['PIPES'][1], tuple(pipe[1]))
        SURF.blit(IMAGES['BASE'], (baseShift, WINDOWHIEGHT - BASEHEIGHT))
        if baseShift >= -90:
            baseShift -= 2
        else:
            baseShift = 0
        if (loopIter + 1) % 5 == 0:
            index = next(indices)
        birdImg = pygame.transform.rotate(IMAGES['BIRD'][index], rotation)
        SURF.blit(birdImg, (BIRDX, birdY))
        showScore(score)
        # ------------End Blitting Images------------
        # ------------MOVEMENTS-----------------------
        # ------------BIRD---------------------------
        if rotation >= -90:
            rotation -= rotationSpeed

        if vel < maxVelDown and not flapping:
            vel += gravity

        elif flapping:
            rotation = 30
            vel = -ascendVal
            flapping = False
        # ------------PIPES-----------------------
        for pipe in pipes:
            for PIPE in pipe:
                PIPE[0] -= pipeSpeed
                if BIRDX - pipeSpeed < PIPE[0]+pipeWidth <= BIRDX:
                    score += 1
        if pipes[len(pipes) - 1][0][0] <= WINDOWWIDTH - 200:
            pipes.append(generatePipes(IMAGES['PIPES']))
        if pipes[0][0][0] <= -IMAGES['PIPES'][0].get_width():
            pipes.pop(0)
        # ------------ check for collision--------------
        if collisionDetection(birdImg, birdY, pipes, IMAGES['PIPES'][0]):
            return [birdY, rotation, score, pipes]
        loopIter = (loopIter + 1) % FPS
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generatePipes(PIPES):
    height = random.randrange(GAPSIZE, WINDOWHIEGHT - BASEHEIGHT - 2 * GAPSIZE)
    pipe1 = [WINDOWWIDTH, height - PIPES[0].get_height()]
    pipe2 = [WINDOWWIDTH, height + GAPSIZE]
    return [pipe1, pipe2]


def collisionDetection(bird, birdY, pipes, PIPE):
    pipeHeight = PIPE.get_height()
    pipeWidth = PIPE.get_width()
    birdTop = birdY
    birdBottom = birdTop + bird.get_height()
    birdWidth = bird.get_width()
    birdLeft = BIRDX
    if birdY >= WINDOWHIEGHT - BASEHEIGHT - bird.get_height() + 8:
        return True
    for pipePair in pipes:
        upperPipeBottom = pipePair[0][1] + pipeHeight
        lowerPipeTop = pipePair[1][1]
        pipeLeft = pipePair[0][0]
        pipeRight = pipeLeft + pipeWidth
        if (birdTop < upperPipeBottom - 8 or birdBottom > lowerPipeTop + 4) and (
                (pipeLeft - birdWidth) + 4 < birdLeft < pipeRight - 4):
            return True

    return False


def endGame(birdY, rotation, score, pipes):

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
        if birdY <= WINDOWHIEGHT - BASEHEIGHT-IMAGES['BIRD'][0].get_width():
            birdY += 4
            if rotation >= -90:
                rotation -= 10
        birdImg = pygame.transform.rotate(IMAGES['BIRD'][0], rotation)
        SURF.blit(IMAGES['BG'], (0, 0,))
        for pipe in pipes:
            SURF.blit(IMAGES['PIPES'][0], tuple(pipe[0]))
            SURF.blit(IMAGES['PIPES'][1], tuple(pipe[1]))
        SURF.blit(IMAGES['BASE'], (0, WINDOWHIEGHT - BASEHEIGHT))
        SURF.blit(birdImg, (BIRDX, birdY))
        showScore(score)
        SURF.blit(IMAGES['SCREENS'][1], ((WINDOWWIDTH - IMAGES['SCREENS'][1].get_width()) / 2, 150))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def showScore(score):
    score = int(score/2)
    numberOfDigits = len(str(score))
    digitWidth = IMAGES['NUMBERS'][0].get_width()
    scoreWidth = digitWidth * numberOfDigits
    startX = WINDOWWIDTH/2 + scoreWidth/2 - digitWidth
    if score == 0:
        SURF.blit(IMAGES['NUMBERS'][0], (startX, 64))
    while score>0:
        print(score)
        digit = score%10
        score = int(score/10)

        SURF.blit(IMAGES['NUMBERS'][digit], (startX, 64))
        startX -= digitWidth

if __name__ == '__main__':
    main()
