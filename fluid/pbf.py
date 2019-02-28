import pygame
import math
import kernel


GRID_SIZE = 70

XRANGE = int(1000/GRID_SIZE)
YRANGE = int(1000/GRID_SIZE)

DENSITY_REST = 0.0008
KERNEL_RANGE = 60
KERNEL_REST = DENSITY_REST*KERNEL_RANGE**2*math.pi


class Grid:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.neighbourhood=[]
        self.particles=set()

    def setNeighbourhood(self):
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                x = self.x + dx
                y = self.y + dy
                if 0 < x < XRANGE and 0 < y < YRANGE:
                    self.neighbourhood.append(grids[x][y])

grids = [[Grid(x,y) for y in range(YRANGE)] for x in range(XRANGE)]

for x in range(XRANGE):
    for y in range(YRANGE):
        grids[x][y].setNeighbourhood()

def findGrid(p):
    #x = min(max(int(p.x/GRID_SIZE),0),XRANGE - 1)
    #y = min(max(int(p.y/GRID_SIZE),0),YRANGE - 1)
    x = int(p.x/GRID_SIZE)
    y = int(p.y/GRID_SIZE)
    return grids[x][y]

class Particle:
    def __init__(self,x,y):
        self.p_cur = pygame.Vector2(x,y)
        self.p_pre = pygame.Vector2(x,y)
        self.grid = Grid(-1,-1)
        self.grid.particles.add(self)
        self.setGrid()
        
    def setGrid(self):
        newGrid = findGrid(self.p_cur)
        if newGrid is not self.grid:
            self.grid.particles.remove(self)
            newGrid.particles.add(self)
            self.grid = newGrid

    def predict(self):
        tmp = self.p_cur
        vg = pygame.Vector2(0,0.5*9.8*0.333333333333333333**2)
        self.p_cur = self.p_cur + self.p_cur - self.p_pre + vg
        self.p_pre = tmp

    def solveEdgeConstraint(self):
        self.p_cur.x = max(10,min(self.p_cur.x,790))
        self.p_cur.y = max(10,min(self.p_cur.y,590))

    def solvePBF(self):
        neighbours=[]
        for grid_cell in self.grid.neighbourhood:
            for particle in grid_cell.particles:
                pos = particle.p_cur-self.p_cur
                l = pos.length()
                if l<KERNEL_RANGE:
                    kernel_d_by_l = kernel.kernel_d_by_x(l/KERNEL_RANGE)/KERNEL_RANGE
                    gradient = pos*kernel_d_by_l
                    neighbours.append((particle,pos,l,gradient))
        
        density = 0
        gradient_squared = 0
        for n in neighbours:
            density += kernel.kernel(n[2]/float(KERNEL_RANGE))
            gradient_squared += n[3].length_squared()

        density = KERNEL_REST - density

        #print(gradient_squared)
        if density>0:
            return
        gradient_squared = max(0.00000001,gradient_squared)
        gradient_lambda = density/gradient_squared

        accumulated_ds = pygame.Vector2(0,0)
        for n in neighbours:
            ds = n[3]*gradient_lambda*0.5
            accumulated_ds += ds
            n[0].p_cur += ds

        accumulated_ds = accumulated_ds*(-1.0/len(neighbours))

        for n in neighbours:
            n[0].p_cur += accumulated_ds

particles=[]
for x in range(30):
    for y in range(30):
        particles.append(Particle(x*20+20, y*20+20))

def sim():
    for particle in particles:
        particle.predict()
    for particle in particles:
        particle.solveEdgeConstraint()
    for particle in particles:
        particle.setGrid()
    for particle in particles:
        particle.solvePBF()
    

def render(screen):
    for p in particles:
        pygame.draw.circle(screen, (255,255,255), (int(p.p_cur.x), int(p.p_cur.y)), 2)