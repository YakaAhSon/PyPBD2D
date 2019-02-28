import sys, pygame
import pbf
pygame.init()

screen = pygame.display.set_mode((800,600))

clock = pygame.time.Clock()

myfont = pygame.font.SysFont('consolas', 15)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0,0,0))

    pbf.sim()
    pbf.render(screen)
    
    textsurface = myfont.render("FPS: %.0f"%(clock.get_fps()), False, (0, 255, 0))
    screen.blit(textsurface,(0,0))

    pygame.display.flip()

    clock.tick()
    