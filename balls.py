import sys, pygame
import random
pygame.init()

FRAME_RATE = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_SCALE = 100.0

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

clock = pygame.time.Clock()

myfont = pygame.font.SysFont('consolas', 15)

gravity = pygame.Vector2(0,9.8)

timestep = 1.0/FRAME_RATE

class Ball:
    def __init__(self,x,y,r):
        self.p_pre = pygame.Vector2(x,y)
        self.p_cur = pygame.Vector2(x,y)
        self.r = float(r)

    def update(self):
        tmp = self.p_cur
        self.p_cur = self.p_cur*2-self.p_pre + (timestep**2)*0.5*gravity
        self.p_pre = tmp

    def solveConstraint(self):
        self.p_cur.x = max(self.p_cur.x, self.r)
        self.p_cur.x = min(self.p_cur.x, SCREEN_WIDTH/SCREEN_SCALE - self.r)
        self.p_cur.y = max(self.p_cur.y, self.r)
        self.p_cur.y = min(self.p_cur.y, SCREEN_HEIGHT/SCREEN_SCALE - self.r)
        
    def handleCollision(self,b):
        n = b.p_cur-self.p_cur
        l = self.r+b.r-n.length()
        if l<=0:
            return
        n = n.normalize()

        m1 = self.r**2
        m2 = b.r**2
        d1 = l*m2/(m1+m2)*0.8
        d2 = l*m1/(m1+m2)*0.8
        self.p_cur-=n*d1
        b.p_cur+=n*d2

    
    def render(self):
        pygame.draw.circle(screen, (255,255,255), (int(self.p_cur.x*SCREEN_SCALE),int(self.p_cur.y*SCREEN_SCALE)), int(self.r*SCREEN_SCALE))

balls=[]
balls.append(Ball(1,1,0.3))

def randomNewBall():
    y = 1
    x = random.random()*6+1
    r = random.random()*0.3+0.05
    balls.append(Ball(x,y,r))

def sim():
    for ball in balls:
        ball.update()
        ball.solveConstraint()
        for b in balls:
            if b is not ball:
                ball.handleCollision(b)
def render():
    for ball in balls:
        ball.render()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==32:
                randomNewBall()
            elif event.key==273:
                gravity = pygame.Vector2(0,-9.8)
            elif event.key==274:
                gravity = pygame.Vector2(0,9.8)
            elif event.key==275:
                gravity = pygame.Vector2(9.8,0)
            elif event.key==276:
                gravity = pygame.Vector2(-9.8,0)
    screen.fill((0,0,0))

    sim()
    render()
    
    textsurface = myfont.render("FPS: %.0f;  %d Balls"%(clock.get_fps(),len(balls)), False, (0, 255, 0))
    screen.blit(textsurface,(0,0))

    pygame.display.flip()

    clock.tick(FRAME_RATE)
