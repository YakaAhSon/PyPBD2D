import sys, pygame
import random
import math

pygame.init()

FRAME_RATE = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_SCALE = 100.0

SPACE_WIDTH = SCREEN_WIDTH/SCREEN_SCALE
SPACE_HEIGHT = SCREEN_HEIGHT/SCREEN_SCALE

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

clock = pygame.time.Clock()

myfont = pygame.font.SysFont('consolas', 15)

gravity = pygame.Vector2(0,9.8)

timestep = 1.0/FRAME_RATE

class Box:
    def __init__(self,x,y,w,h, a = 0.0):
        self.p_pre = pygame.Vector2(x,y)
        self.p_cur = pygame.Vector2(x,y)
        self.a_pre = float(a)
        self.a_cur = float(a)
        self.w = float(w)
        self.h = float(h)
        self.m = self.w*self.h
        self.moi = self.m*(self.w*self.w+self.h*self.h)/12.0

    def update(self):
        tmp = self.p_cur
        self.p_cur = self.p_cur*2-self.p_pre + (timestep**2)*0.5*gravity
        self.p_pre = tmp

        tmp = self.a_cur
        self.a_cur = 2*self.a_cur-self.a_pre
        self.a_pre = tmp

    # aplly position impulse d*n at p
    def apllyImpulse(self,p,i,n):
        # delta_w = i*cross(r,n)/moi
        # delta_v_com = i/m*n
        # i/m+i*cross(r,n)^2/moi = delta_v
        # i = delta_v/(1/m+cross(r,n)/moi*r.length)
        r = p-self.p_cur
        r_normal = r.cross(n)
        
        #i = d/(1/self.m+r_normal**2/self.moi*r.length())
        delta_a = i*r_normal/self.moi
        delta_v_com = i/self.m
        self.a_cur+=delta_a*180/math.pi
        self.p_cur+=n*delta_v_com

    def apllyPositionImpulse(self,p,d,n):
        # delta_w = i*cross(r,n)/moi
        # delta_v_com = i/m*n
        # i/m+i*cross(r,n)^2/moi = delta_v
        # i = delta_v/(1/m+cross(r,n)/moi*r.length)
        r = p-self.p_cur
        r_normal = r.cross(n)
        
        i = d/(1/self.m+r_normal**2/self.moi*r.length())
        delta_a = i*r_normal/self.moi
        delta_v_com = i/self.m
        self.a_cur+=delta_a*180/math.pi
        self.p_cur+=n*delta_v_com
    def vertix(self,i):
        vertix_offset=[(0.5,0.5),(0.5,-0.5),(-0.5,0.5),(-0.5,-0.5)]
        p = pygame.Vector2(self.w*vertix_offset[i][0],self.h*vertix_offset[i][1])
        return self.p_cur+p.rotate(self.a_cur)

    def solveConstraint(self):
        for i in range(4):
            v = self.vertix(i)
            if v.x<0:
                self.apllyPositionImpulse(v,0-v.x,pygame.Vector2(1,0))
            elif v.x>SPACE_WIDTH:
                self.apllyPositionImpulse(v,v.x-SPACE_WIDTH,pygame.Vector2(-1,0))
            if v.y<0:
                self.apllyPositionImpulse(v,0-v.y,pygame.Vector2(0,1))
            elif v.y>SPACE_HEIGHT:
                self.apllyPositionImpulse(v,v.y-SPACE_HEIGHT,pygame.Vector2(0,-1))

    def solveCollisiton(self, b, p, d, n):
        r_A = p-self.p_cur
        r_normal_A = r_A.cross(n)
        r_B = p-b.p_cur
        r_normal_B = r_B.cross(n)
        i = d/(1/self.m+r_normal_A**2/self.moi*r_A.length() + 1/b.m+r_normal_B**2/b.moi*r_B.length())
        self.apllyImpulse(p,i,-n)
        b.apllyImpulse(p,i,n)
        #self.apllyPositionImpulse(p,d/2,-n)
        #b.apllyPositionImpulse(p,d/2,n)

    def handleCollision(self,b):
        for i in range(4):
            v = b.vertix(i)
            vv = (v-self.p_cur).rotate(-self.a_cur)
            x = self.w*0.5-abs(vv.x)
            y = self.h*0.5-abs(vv.y)
            if x<0 or y<0:
                continue
            if x<y:
                if vv.x>0:
                    self.solveCollisiton(b,v,x,pygame.Vector2(1,0).rotate(self.a_cur))
                else:
                    self.solveCollisiton(b,v,x,pygame.Vector2(-1,0).rotate(self.a_cur))
            else:
                if vv.y>0:
                    self.solveCollisiton(b,v,y,pygame.Vector2(0,1).rotate(self.a_cur))
                else:
                    self.solveCollisiton(b,v,y,pygame.Vector2(0,-1).rotate(self.a_cur))
    
    def render(self):
        image_orig = pygame.Surface((self.w*SCREEN_SCALE ,self.h*SCREEN_SCALE))
        image_orig.set_colorkey((0,0,0))
        image_orig.fill((255,255,255))
        new_image = pygame.transform.rotate(image_orig , -self.a_cur)
        rect = new_image.get_rect()
        rect.center = self.p_cur*SCREEN_SCALE
        screen.blit(new_image , rect) 

boxes=[]
#boxes.append(Box(2,2,2,1,0))
boxes.append(Box(3,1,2,0.9,0))
boxes.append(Box(5,3,3,0.9,45))

def randomBox():
    boxes.append(Box(random.random()*3+2,2,random.random()*0.7+0.3,random.random()*0.7+0.3))

def sim():
    for box in boxes:
        box.update()
        box.solveConstraint()
    for i in range(len(boxes)):
        for j in range(i+1,len(boxes)):
            boxes[i].handleCollision(boxes[j])
            boxes[j].handleCollision(boxes[i])

def render():
    for box in boxes:
        box.render()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running = False
            elif event.key==32:
                randomBox()
            elif event.key==273:
                gravity = pygame.Vector2(0,-9.8)
            elif event.key==274:
                gravity = pygame.Vector2(0,9.8)
            elif event.key==275:
                gravity = pygame.Vector2(9.8,0)
            elif event.key==276:
                gravity = pygame.Vector2(-9.8,0)
            

    screen.fill((0,0,0))
    
    textsurface = myfont.render("FPS: %.0f"%(clock.get_fps()), False, (0, 255, 0))
    screen.blit(textsurface,(0,0))

    sim()
    render()

    pygame.display.flip()

    clock.tick(FRAME_RATE)
