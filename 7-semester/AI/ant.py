import random
import math

WIDTH = 40
FILE = 'dados.txt'

ANT = '8'
DEAD_ANT = 'X'
FREE_SPACE = ' '
ANT_WITH_DEAD_ANT = '@'
ANT_CARRYING_DEAD_ANT = '9'
VISON_RADIUS = 1

NANTS = 10
ANTS = []
ITENS = []
NDEAD = 400

class Item:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.state = DEAD_ANT
        self.vals = []

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
        neighbor = self.neighbors[random.randint(0, len(self.neighbors)-1 )]
        self.row = neighbor.row
        self.col = neighbor.col
        self.update_neighbors(grid)
    
    def pick_item(self, grid):
        nDeadAround = 0
        for x in self.neighbors:
            if x.state == DEAD_ANT:
                nDeadAround = nDeadAround + 1
        
        f = float(nDeadAround)/8.0
        picking = ( 2 / (2 + f) )**2
        if picking == 1 or picking >= random.uniform(0.0,1.0):
            self.state = ANT_CARRYING_DEAD_ANT
            grid[self.row][self.col] = FREE_SPACE

    def drop_item(self, grid):
        nDeadAround = 0
        for x in self.neighbors:
            if x.state == DEAD_ANT:
                nDeadAround = nDeadAround + 1
        
        f = float(nDeadAround)/8.0
        droping = ( f / (2 + f) )**2
        if droping >= random.uniform(0.0,1.0):
            self.state = ANT
            grid[self.row][self.col] = DEAD_ANT

def create_ants():
    for a in range(NANTS):
        ant = Ant()
        ant.row = random.randint(0, WIDTH - 1)
        ant.col = random.randint(0, WIDTH - 1)
        ANTS.append(ant)

def create_itens():
    for x in range(NDEAD):
        item = Item()
        item.row = random.randint(0, WIDTH - 1)
        item.col = random.randint(0 , WIDTH - 1)
        okay = 0
        while okay != 1:
            okay = 1
            for i in ITENS:
                if(item.row == i.row and item.col == i.col):
                    okay = 0
                    item.row = random.randint(0, WIDTH - 1)
                    item.col = random.randint(0 , WIDTH - 1)
        ITENS.append(item)

def gen_world(grid):
    for row in range(WIDTH):
        r = []
        for col in range(WIDTH):
            dead = 0
            for i in ITENS:
                if(i.row == row and i.col == col):
                    r.append(DEAD_ANT)
                    dead = 1
            if(dead == 0):
                r.append(FREE_SPACE)
        grid.append(r)

def draw_world(grid):
    for row in range(WIDTH):
        for col in range(WIDTH):
            f = 0
            for ant in ANTS:
                if(ant.row == row and ant.col == col):
                    if(grid[row][col] == DEAD_ANT):
                        print(ANT_WITH_DEAD_ANT, end=' ')
                    else:
                        print(ant.state, end=' ')
                    f = 1
                    break
            if(f == 0):
                print(grid[row][col], end=' ')
        print()
    print('===========')

def euclid_distance(item1, item2):
    sum = 0
    for i in range(len(item1.vals)):
        square_sum = ( item1.vals[i] - item2.vals[i] )**2 + sum
    distance = math.sqrt(square_sum)
    return distance

def get_itens_from_file(file):
    f = open(file,'r')

    for line in f:
        item =  Item()
        fields = line.split(';')
        item.vals.append(float(fields[0]))
        item.vals.append(float(fields[1]))
        item.state = float(fields[2])
        ITENS.append(item)
    f.close()

if __name__ == '__main__':
    grid = []
    create_ants()
    get_itens_from_file(FILE) #create_itens()
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

    for n in range(1000000): #1000000
        for a in ANTS:
            a.move_to(grid)
            if(a.state == ANT and grid[a.row][a.col] == DEAD_ANT):
                a.pick_item(grid)
            elif(a.state == ANT_CARRYING_DEAD_ANT and grid[a.row][a.col] == FREE_SPACE):
                a.drop_item(grid)
    
    draw_world(grid)
    ## situação da formiga e quem são os vizinhos
    for a in ANTS:
        a.update_neighbors(grid)
        print(a.row, a.col, end='[ ')
        for n in a.neighbors:
            print(n.state+',', end='')
        print(']')
    print('---')