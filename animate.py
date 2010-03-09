import pygame, sys, os, re
from pygame.locals import *

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 360), 0, 32)
    background = pygame.image.load('background.jpg').convert()
    screen.blit(background, (0,0))
    frames = []
    for path in os.listdir('.'):
        number = re.match(r'.*(\d+).png', path)
        if number:
            img = pygame.image.load(path).convert_alpha()
            i = int(number.group(1))
            frames.append((i, img))
    frames.sort(lambda f1, f2: cmp(f1[0], f2[0]))
    clock = pygame.time.Clock()
    t = frame_index = 0
    speed = 2
    pause = True
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN or (
                event.type == KEYDOWN and event.key == K_SPACE):
                pause = not pause
        milli = clock.tick()
        if not pause:
            seconds = milli/1000.0
            change = speed * seconds
            t += change
            frame_index = int(t)
            if frame_index >= len(frames):
                frame_index = 0
                t = 0
        screen.blit(background, (0,0))
        screen.blit(frames[frame_index][1], (0,0))
        pygame.display.update()
