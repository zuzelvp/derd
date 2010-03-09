import pydot
import pygame, sys, tempfile
from pygame.locals import *


def get_diagram():
    erd = pydot.Dot(graph_type='graph')
    student = pydot.Node('STUDENT', shape='box')
    erd.add_node(student)
    with tempfile.NamedTemporaryFile() as f:
        erd.write_dot(f.name)
        dot = pydot.graph_from_dot_file(f.name)
        nodes = []
        for node in dot.get_nodes():
            text = node.get_name()
            pos = node.get_pos()
            width = node.get_width()
            height = node.get_height()
            if pos and width and height:
                nodes.append({
                    'text': text,
                    'pos': [float(c) for c in pos.strip('"').split(',')],
                    # inches to point conversion.
                    'width': float(width.strip('"')) * 72,
                    'height': float(height.strip('"')) * 72,
                })
        return nodes


def paint_node(screen, node):
    centerx, centery = node['pos']
    width = node['width']
    height = node['height']
    x = centerx - width/2
    y = centery - height/2
    screen.lock()
    pygame.draw.rect(screen, (140, 240, 130), Rect((x, y), (width, height)))
    screen.unlock()
    text = font.render(node['text'], True, (255, 255, 255), (140, 240, 130))
    text_rect = text.get_rect()
    text_rect.centerx = centerx
    text_rect.centery = centery
    screen.blit(text, text_rect)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 360), 0, 32)
    nodes = get_diagram()
    # Search for Verdana and create a Font object
    times_roman = pygame.font.match_font('Times-Roman')
    font = pygame.font.Font(times_roman, 14)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        for node in nodes:
            paint_node(screen, node)
        pygame.display.update()
