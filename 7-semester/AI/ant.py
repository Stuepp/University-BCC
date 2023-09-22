import random

WIDTH = 10

ANT = '8'
DEAD_ANT = 'X'
FREE_SPACE = ' '
ANT_WITH_DEAD_ANT = '@'
ANT_CARRYING_DEAD_ANT = '9'
VISON_RADIUS = 1

NANTS = 5
ANTS = []
NDEAD = 20

class Neighbor:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.state = 0


class Ant:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.neighbors = []
        self.state = ANT
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < WIDTH - 1: # DOWN
            neighbor = Neighbor()
            neighbor.row = (self.row + VISON_RADIUS)
            neighbor.col = self.col
            neighbor.state = grid[self.row + VISON_RADIUS][self.col]
            self.neighbors.append(neighbor)
    
        if self.row > 0: # UP
            neighbor = Neighbor()
            neighbor.row = (self.row - VISON_RADIUS)
            neighbor.col = self.col
            neighbor.state = grid[self.row - VISON_RADIUS][self.col]
            self.neighbors.append(neighbor)
        
        if self.col < WIDTH - 1: # RIGHT
            neighbor = Neighbor()
            neighbor.row = self.row
            neighbor.col = self.col + VISON_RADIUS
            neighbor.state = grid[self.row][self.col + VISON_RADIUS]
            self.neighbors.append(neighbor)
        
        if self.col > 0: # LEFT
            neighbor = Neighbor()
            neighbor.row = self.row
            neighbor.col = self.col - VISON_RADIUS
            neighbor.state = grid[self.row][self.col - VISON_RADIUS]
            self.neighbors.append(neighbor)
        
        # diagonais
        if self.row < WIDTH - 1 and self.col < WIDTH - 1: # diagonoal inferior direita
            neighbor = Neighbor()
            neighbor.row = self.row + VISON_RADIUS
            neighbor.col = self.col + VISON_RADIUS
            neighbor.state = grid[self.row + VISON_RADIUS][self.col + VISON_RADIUS]
            self.neighbors.append(neighbor)
        
        if self.row < WIDTH - 1 and self.col > 0: # diagonal inferior esquerda
            neighbor = Neighbor()
            neighbor.row = self.row + VISON_RADIUS
            neighbor.col = self.col - VISON_RADIUS
            neighbor.state = grid[self.row + VISON_RADIUS][self.col - VISON_RADIUS]
            self.neighbors.append(neighbor)
        
        if self.row > 0 and self.col < WIDTH -1: # diagonal superior direita
            neighbor = Neighbor()
            neighbor.row = self.row - VISON_RADIUS
            neighbor.col = self.col + VISON_RADIUS
            neighbor.state = grid[self.row - VISON_RADIUS][self.col + VISON_RADIUS]
            self.neighbors.append(neighbor)
        
        if self.row > 0 and self.col > 0: # diagonal superior esquerda
            neighbor = Neighbor()
            neighbor.row = self.row - VISON_RADIUS
            neighbor.col = self.col - VISON_RADIUS
            neighbor.state = grid[self.row - VISON_RADIUS][self.col - VISON_RADIUS]
            self.neighbors.append(neighbor)
    
    def move_to(self, grid):
        for neighbor in self.neighbors:
            decision = random.randint(0,1)
            if(neighbor.state == FREE_SPACE and decision == 1):

                grid[neighbor.row][neighbor.col] = self.state
                if(grid[self.row][self.col] != ANT_WITH_DEAD_ANT): # ou seja é uma formiga ou uma formiga carregando outra
                    grid[self.row][self.col] = FREE_SPACE
                else:
                    grid[self.row][self.col] = DEAD_ANT
                
                self.row = neighbor.row
                self.col = neighbor.col

                self.update_neighbors(grid)
                return
            elif(neighbor.state == DEAD_ANT and decision == 1):
                
                grid[neighbor.row][neighbor.col] = ANT_WITH_DEAD_ANT
                if(grid[self.row][self.col] != ANT_WITH_DEAD_ANT): # ou seja é uma formiga ou uma formiga carregando outra
                    grid[self.row][self.col] = FREE_SPACE
                else:
                    grid[self.row][self.col] = DEAD_ANT

                self.row = neighbor.row
                self.col = neighbor.col

                self.update_neighbors(grid)
                return

def create_ants():
    for a in range(NANTS):
        ant = Ant()
        ANTS.append(ant)

def gen_world(grid):
    nAnts = NANTS-1
    nDead = NDEAD-1
    for row in range(WIDTH):
        r = []
        for col in range(WIDTH):
            decison = random.randint(0,2)
            if ( decison == 1 and nAnts >= 0):
                ant = ANTS[nAnts]
                ant.row = row
                ant.col = col
                nAnts-=1
                r.append(ant.state)
            elif (decison == 2 and nDead >= 0):
                nDead-=1
                r.append(DEAD_ANT)
            else:
                r.append(FREE_SPACE)
        grid.append(r)

def draw_world(grid):
    for row in range(WIDTH):
        for col in range(WIDTH):
            print(grid[row][col], end=' ')
        print()

if __name__ == '__main__':
    grid = []
    create_ants()
    gen_world(grid)
    draw_world(grid)
    print('-')

    for a in ANTS:
        a.update_neighbors(grid)
        print(a.row, a.col, end='[ ')
        for n in a.neighbors:
            print(n.state+',', end='')
        print(']')
    print('---')

    for n in range(5):
        for a in ANTS:
            a.move_to(grid)
        draw_world(grid)
        print('-')
        for a in ANTS:
            a.update_neighbors(grid)
            print(a.row, a.col, end='[ ')
            for n in a.neighbors:
                print(n.state+',', end='')
            print(']')
        print('---')