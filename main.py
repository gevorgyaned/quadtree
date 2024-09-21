import pygame

from quadtree import QuadTree, AABB, vec

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

point_tree = QuadTree(AABB(vec(WIDTH / 2, HEIGHT / 2), vec(120, 100)))

def display_aabb(quadtree):
    if quadtree.has_children:
        aabb = quadtree.aabb
        center_x, center_y = aabb.center
        pygame.draw.line(screen, 'green', (center_x + aabb.ext.x, center_y), (center_x - aabb.ext.x, center_y))
        pygame.draw.line(screen, 'green', (center_x, center_y + aabb.ext.y), (center_x, center_y - aabb.ext.y))

def display_quadtree(quadtree):
    display_aabb(quadtree)

    if quadtree.point:
        pygame.draw.circle(screen, 'red', quadtree.point, 4)

    if quadtree.has_children:
        for node in quadtree.nodes:
            display_quadtree(node)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            try: 
                point_tree.insert(vec(x, y))

            except ValueError:
               print("value is not in the range") 

    screen.fill('blue')

    # drawing the main rectangle
    rect = pygame.Rect(point_tree.aabb.x_start, point_tree.aabb.y_start, point_tree.aabb.ext.x * 2, point_tree.aabb.ext.y * 2)
    pygame.draw.rect(screen, 'green', rect, 1)

    # drawing other smaller rectangles
    display_quadtree(point_tree)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

