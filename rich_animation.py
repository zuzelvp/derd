from __future__ import with_statement
import pydot
import tempfile
import pygame
import sys
from pygame.locals import *


STUDENT = 'STUDENT'
STUDENT_ID = 'STUDENT_ID'
STUDENT_NAME = 'STUDENT_NAME'
MAJOR = 'MAJOR'
CREDITS = 'CREDITS'
MATH = ' = \'MATH\''
GREEN = 'green'
PINK = 'pink'

def generate_erd_with_layout():
    erd = pydot.Dot(graph_type='graph')
    student = pydot.Node(STUDENT, shape='box', fillcolor=GREEN)
    student_id = pydot.Node(STUDENT_ID, fillcolor=GREEN)
    student_name = pydot.Node(STUDENT_NAME, fillcolor=GREEN)
    major = pydot.Node(MAJOR, fillcolor=PINK)
    credits = pydot.Node(CREDITS, fillcolor=GREEN)
    student_2_student_id = pydot.Edge(student.get_name(), student_id.get_name())
    student_2_student_name = pydot.Edge(student.get_name(), student_name.get_name())
    major_2_student = pydot.Edge(major.get_name(), student.get_name(), label=MATH)
    student_2_credits = pydot.Edge(student.get_name(), credits.get_name())
    erd.add_node(student)
    erd.add_node(student_id)
    erd.add_node(student_name)
    erd.add_node(major)
    erd.add_node(credits)
    erd.add_edge(student_2_student_id)
    erd.add_edge(student_2_student_name)
    erd.add_edge(major_2_student)
    erd.add_edge(student_2_credits)
    # get erd with layout.
    with tempfile.NamedTemporaryFile() as f:
        erd.write_dot(f.name)
        return pydot.graph_from_dot_file(f.name)


def generate_animation(erd):
    frames = [
        None,
        erd.get_node(MAJOR),
        erd.get_edge(MAJOR, STUDENT),
        erd.get_node(STUDENT),
        erd.get_edge(STUDENT, STUDENT_NAME),
        erd.get_node(STUDENT_NAME),
        erd.get_edge(STUDENT, STUDENT_ID),
        erd.get_node(STUDENT_ID),
        erd.get_edge(STUDENT, CREDITS),
        erd.get_node(CREDITS),
        None, None, None,
    ]
    # Preprocess attributes.
    offset = 40
    factor = 72
    for frame in frames:
        if isinstance(frame, pydot.Node) and frame.get_fillcolor():
            pos = frame.get_pos()
            frame.set_pos([float(c) + offset for c in pos.strip('"').split(',')])
            # convertion from inches to points.
            frame.set_width(float(frame.get_width().strip('"')) * factor)
            frame.set_height(float(frame.get_height().strip('"')) * factor)
            frame.set_fillcolor(pygame.color.THECOLORS[frame.get_fillcolor()])
            if frame.get_shape() == 'box':
                frame.set_shape(pygame.draw.rect)
            else:
                frame.set_shape(pygame.draw.ellipse)
        elif isinstance(frame, pydot.Edge):
            pos = []
            for point in frame.get_pos().strip('"').split():
                pos.append([int(c) + offset for c in point.split(',')])
            frame.set_pos(pos)
            if frame.get_lp():
                lp = frame.get_lp().strip('"').split(',')
                frame.set_lp([int(c) + offset for c in lp])
    return frames


def paint_frame(screen, frame, font, i, t):
    black = pygame.color.THECOLORS['black']
    white = pygame.color.THECOLORS['white']
    if isinstance(frame, pydot.Node) and frame.get_fillcolor():
        centerx, centery = frame.get_pos()
        width = frame.get_width()
        height = frame.get_height()
        x = centerx - width/2
        y = centery - height/2
        fillcolor = frame.get_fillcolor()
        paint_shape = frame.get_shape()
        paint_shape(screen, black, Rect((x, y), (width, height)))
        paint_shape(screen, fillcolor, Rect((x+2, y+2), (width-4, height-4)))
        text = font.render(frame.get_name(), True, black, fillcolor)
        text_rect = text.get_rect()
        text_rect.centerx = centerx
        text_rect.centery = centery
        if text_rect.width + 4 < width and text_rect.height + 4 < height:
            screen.blit(text, text_rect)
        if i == int(t):
            scale = 1 - t + int(t)
            paint_shape(screen, white, Rect((x, y), (width, scale * height)))
    elif isinstance(frame, pydot.Edge):
        pos = frame.get_pos()
        if i == int(t):
            point_index = int((t-int(t))/(1.0/len(pos)))
        else:
            point_index = len(pos) - 1
        if point_index > 0:
            pygame.draw.aalines(screen, black, False, pos[:point_index+1])
        if (i < int(t) or (i == int(t) and t - int(t) > 1.0/2)) and frame.get_lp():
            text = font.render(frame.get_label().strip('"'), True, black, (255, 255, 255))
            text_rect = text.get_rect()
            centerx, centery = frame.get_lp()
            text_rect.centerx = centerx
            text_rect.centery = centery
            screen.blit(text, text_rect)

if __name__ == '__main__':
    erd = generate_erd_with_layout()
    frames = generate_animation(erd)
    pygame.init()
    screen = pygame.display.set_mode((640, 360), 0, 32)
    background = pygame.image.load('background.jpg').convert()
    screen.blit(background, (0,0))
    times_roman = pygame.font.match_font('Times-Roman')
    font = pygame.font.Font(times_roman, 14)
    clock = pygame.time.Clock()
    t = frame_index = 0
    speed = 2.5
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
        for i in xrange(frame_index + 1):
            paint_frame(screen, frames[i], font, i, t)
        pygame.display.update()
