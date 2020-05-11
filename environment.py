from random import randint

class Environment:
    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.grid = {}
        self.live_cells = []
        self.delta_cells = []
        self.generate_grid()
        self.populate_grid()
        self.generation = 0
        self.DEBUG = True
        self.probability = 20
        

    def generate_grid(self):
        for i in range(self.width):
            for j in range(self.height):
                loc = (i, j)
                self.grid[loc] = False

    def populate_grid(self):
        for i in range(self.width):
            for j in range(self.height):
                n = randint(0, 100)
                if n <= self.probability:
                    self.grid[(i, j)] = True
                    self.live_cells.append((i, j))

    
    def tick(self):
        """
        Rules
        1. If a cell has 2 or 3 neighbors (including diagonals) it survives
        2. If a cell has 0 or 1 neighbor it dies by underpopulation
        3. If a cell has more than 3 neighbors it dies by overpopulation
        4. If a dead cell has 3 live neighbors it becomes live by repopulation
        """
        if self.DEBUG:
            max_len = self.width * self.height
            if len(self.live_cells) > max_len:
                print("Garbage buildup in live_cell list.")
            if len(self.delta_cells) > max_len:
                print('Garbage buildup in delta_cells list.')
                print(self.delta_cells)

        def execute(kill_these, populate_these):
            self.generation +=1
            self.delta_cells = None
            self.delta_cells = kill_these + populate_these
            for i in kill_these:
                self.grid[i] = False
                self.live_cells.remove(i)
            for i in populate_these:
                self.grid[i] = True
                if i not in self.live_cells:
                    self.live_cells.append(i)
        reproduce = []
        kill = []
        for cell in self.live_cells:
            x = cell[0]
            y = cell[1]
            neighbors = 0
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    #WRAP BORDERS
                    i = self.width-1 if i <0 else 0 if i == self.width else i
                    j = self.height-1 if j <0 else 0 if j == self.height else j
                    if i !=x and j !=y and self.grid[(i, j)] == True:
                        neighbors +=1
                    if i !=x and j !=y and self.grid[(i, j)] == False:
                        if (i, j) not in reproduce:
                            reproduce.append((i, j))
            if neighbors != 2 or neighbors !=3:
                if (x, y) not in kill:
                    kill.append((x, y))

        for r in reproduce: #This is wrong
            x = r[0]
            y = r[1]
            neighbors = 0
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    #WRAP BORDERs
                    i = self.width-1 if i <0 else 0 if i == self.width else i
                    j = self.height-1 if j <0 else 0 if j == self.height else j
                    if i !=x and j !=y and self.grid[(i, j)]:
                        neighbors +=1
            if neighbors != 3:
                reproduce.remove((x, y))

        execute(kill, reproduce)
        kill = []
        reproduce = []

if __name__ == '__main__':
    my_sandbox = Environment(1000, 1000)
    for i in range(10):
        my_sandbox.tick()
        print("Epoch:" + str(i))
    
