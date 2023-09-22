import random

WIDTH = 10

ANT = '8'
DEAD_ANT = 'X'
FREE_SPACE = ' '
ANT_WITH_DEAD_ANT = '@'
ANT_CARRYING_DEAD_ANT = '9'
VISON_RADIUS = 1
#DADOS = [[-20.2],'B','C','D']
ANTS = []

class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.neighbors = []
        self.state = FREE_SPACE

    def get_pos(self):
        return self.row, self.col
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < WIDTH - 1: # DOWN
            self.neighbors.append(grid[self.row + VISON_RADIUS][self.col])
    
        if self.row > 0: # UP
            self.neighbors.append(grid[self.row - VISON_RADIUS][self.col])
        
        if self.col < WIDTH - 1: # RIGHT
            self.neighbors.append(grid[self.row][self.col + VISON_RADIUS])
        
        if self.col > 0: # LEFT
            self.neighbors.append(grid[self.row][self.col - VISON_RADIUS])
        
        # diagonais
        if self.row < WIDTH - 1 and self.col < WIDTH - 1: # diagonoal inferior direita
            self.neighbors.append(grid[self.row + VISON_RADIUS][self.col + VISON_RADIUS])
        if self.row < WIDTH - 1 and self.col > 0: # diagonal inferior esquerda
            self.neighbors.append(grid[self.row + VISON_RADIUS][self.col - VISON_RADIUS])
        if self.row > 0 and self.col < WIDTH -1: # diagonal superior direita
            self.neighbors.append(grid[self.row - VISON_RADIUS][self.col + VISON_RADIUS])
        if self.row > 0 and self.col > 0: # diagonal superior esquerda
            self.neighbors.append(grid[self.row - VISON_RADIUS][self.col - VISON_RADIUS])
        
        # mundo dá voltas
        if self.row == 0:
            self.neighbors.append(grid[WIDTH-1][self.col])
        if self.row == WIDTH:
            self.neighbors.append(grid[0][self.col])
        if self.col == 0:
            self.neighbors.append(grid[self.row][WIDTH-1])
        if self.col == WIDTH:
            self.neighbors.append(grid[self.row][0])

        # especiais
        if self.row == 0 and self.col == 0:
            self.neighbors.append(grid[WIDTH-1][WIDTH-1]) # diagonal superior esquerda
            self.neighbors.append(grid[WIDTH-1][WIDTH-1 - VISON_RADIUS]) # diagonal superior direita
            self.neighbors.append(grid[self.row + 1][WIDTH-1]) # diagonal inferior esquerda
            self.neighbors.append(grid[self.row+1][self.col+1]) # diagonal inferior direita
        if self.row == WIDTH-1 and self.col == WIDTH-1:
            self.neighbors.append(grid[self.row - VISON_RADIUS][0]) # diagonal superior direita
            self.neighbors.append(grid[0][0]) # diagonal inferior direita
            self.neighbors.append(grid[0][WIDTH - VISON_RADIUS]) # diganoal inferior esquerda
            self.neighbors.append(grid[self.row-1][self.col-1])# diagonal superior esquerda
        # acho que está okay
        if self.col == 0 :
            if self.row < WIDTH - 1 and self.row > 0:
                self.neighbors.append(grid[self.row - VISON_RADIUS][WIDTH-1]) # diagonal superior esquerda
                self.neighbors.append(grid[self.row + VISON_RADIUS][WIDTH-1]) # diagonal inferior esquerda
        if self.col == WIDTH-1:
            if self.row < WIDTH - 1 and self.row > 0:
                self.neighbors.append(grid[self.row - VISON_RADIUS][0]) # diagonal superior direita
                self.neighbors.append(grid[self.row + VISON_RADIUS][0]) # diagonal inferior direita
        if self.row == 0:
            if self.col < WIDTH - 1 and self.col > 0:
                self.neighbors.append(grid[WIDTH-1][self.col + VISON_RADIUS]) # diagonal superior direita
                self.neighbors.append(grid[WIDTH-1][self.col - VISON_RADIUS]) # diagonal superior esquerda
        if self.row == WIDTH-1:
            if self.col < WIDTH - 1 and self.col > 0:
                self.neighbors.append(grid[0][self.col + VISON_RADIUS]) # diagonal inferior direita
                self.neighbors.append(grid[0][self.col - VISON_RADIUS]) # diagonal inferior esquerda

    def picking_item(self):
        nDeadAround = 0
        for x in self.neighbors:
            if x.state == DEAD_ANT:
                nDeadAround = nDeadAround + 1
        
        picking = ( 1 / (1 + nDeadAround/8) )**2
        if picking == 1:
            self.state = ANT_CARRYING_DEAD_ANT
        elif picking >= random.uniform(0.0,1.0):
            self.state = ANT_CARRYING_DEAD_ANT
    
    def drop_item(self):
        nDeadAround = 0
        for x in self.neighbors:
            if x.state == DEAD_ANT:
                nDeadAround = nDeadAround + 1
        
        
        droping = ((nDeadAround/8) / (1 + nDeadAround/8))**2
        if droping < random.uniform(0.0,1.0):
            self.state = ANT_WITH_DEAD_ANT

def world_gen(grid):
    space = [ANT, FREE_SPACE, DEAD_ANT]
    for i in range(WIDTH):
        a = []
        for j in range(WIDTH):
            spot = Spot(i,j)
            spot.state = space[random.randint(0,2)]
            if(spot.state == ANT):
                ANTS.append(spot)
            a.append(spot)
        grid.append(a)

def fake_world(grid):
    for i in range(WIDTH):
        a = []
        for j in range(WIDTH):
            spot = Spot(i, j)
            if i == 1 and j == 1:
                spot.state = ANT
            elif i == 2 or i == 0 or j == 2:
                spot.state = DEAD_ANT 
            else:
                spot.state = FREE_SPACE
            a.append(spot)
            print(spot.state, end=' ')
        grid.append(a)
        print('\n')

def draw_world(grid):
    for i in range(WIDTH):
        for j in range(WIDTH):
            print(grid[i][j].state, end=' ')
        print()

def discovring_neighbors(grid):
    for i in range(WIDTH):
        for j in range(WIDTH):
            spot = grid[i][j]
            spot.update_neighbors(grid)

def move_to(spot, grid):
    neighbors = spot.neighbors
    for i in neighbors:
        if i.state == FREE_SPACE:
            if random.randint(0,1) == 1:
                if spot.state == ANT or spot.state == ANT_CARRYING_DEAD_ANT:
                    grid[i.row][i.col].state = spot.state
                    grid[spot.row][spot.col].state = FREE_SPACE
                elif spot.state == ANT_WITH_DEAD_ANT:
                    grid[i.row][i.col].state = ANT
                    grid[spot.row][spot.col].state = DEAD_ANT
                return
        elif i.state == DEAD_ANT:
            if spot.state != ANT_CARRYING_DEAD_ANT and random.randint(0,1) == 1:
                if spot.state == ANT:
                    grid[spot.row][spot.col].state = FREE_SPACE
                elif spot.state == ANT_WITH_DEAD_ANT:
                    grid[spot.row][spot.col].state = DEAD_ANT
                
                grid[i.row][i.col].state = ANT_WITH_DEAD_ANT
                return

if __name__ == '__main__':
    grid = []
    world_gen(grid)
    #fake_world(grid)
    discovring_neighbors(grid)
    print('-------------------------------------------------------')
    draw_world(grid)
    print('-------------------------------------------------------')
    z = 0
    while z < 1000000:
        for i in range(WIDTH):
            for j in range(WIDTH):
                spot = grid[i][j]
                if spot.state == ANT or spot.state == ANT_WITH_DEAD_ANT or spot.state == ANT_CARRYING_DEAD_ANT:
                    move_to(spot, grid)
                if spot.state == ANT_WITH_DEAD_ANT:
                    spot.picking_item()
                if spot.state == ANT_CARRYING_DEAD_ANT:
                    spot.drop_item()
        #draw_world(grid)
        #print('-------------------------------------------------------')
        z+=1
    z = 1
    while z:
        z = 0
        for i in range(WIDTH):
            for j in range(WIDTH):
                spot = grid[i][j]
                if spot.state == ANT_CARRYING_DEAD_ANT:
                    z = 1
                    move_to(spot, grid)
                    spot.drop_item()
                if spot.state == ANT_WITH_DEAD_ANT:
                    z = 1
                    spot.state = DEAD_ANT
                if spot.state == ANT:
                    z = 1
                    spot.state = FREE_SPACE
        print('-------------------------------------------------------')
        draw_world(grid)
