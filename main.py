import pygame
from quadtree import QuadTree, AABB, vec

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

point_tree = QuadTree(AABB(vec(400, 300), vec(200, 150)))

def display_aabb(quadtree):
    if quadtree.has_children and quadtree.aabb:
        aabb = quadtree.aabb
        center_x, center_y = aabb.center
        pygame.draw.line(screen, "green", (center_x + aabb.ext.x, center_y), (center_x - aabb.ext.x, center_y))
        pygame.draw.line(screen, "green", (center_x, center_y + aabb.ext.y), (center_x, center_y - aabb.ext.y))

def display_points(quadtree):
    display_aabb(quadtree)
    if quadtree.point:
        pygame.draw.circle(screen, "red", quadtree.point, 3)

    if quadtree.has_children:
        for node in quadtree.nodes:
            display_points(node)

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

    rect = pygame.Rect(point_tree.aabb.x_start, point_tree.aabb.y_start, point_tree.aabb.ext.x * 2, point_tree.aabb.ext.y * 2)
    pygame.draw.rect(screen, 'green', rect, 1)

    display_points(point_tree)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

