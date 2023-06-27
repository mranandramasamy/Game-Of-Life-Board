
import pygame, sys, time, random, json
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 1000, 600
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=64
ft=pygame.time.Clock()
pygame.display.set_caption('Life..!!!')

pygame.font.init()
message_font = pygame.font.SysFont("Arial", 17)

MAT = (60, 100)

class App:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (10, 20, 30),
            "cell": (220, 240, 230),
            "land": (120, 60, 30),
            "avatar": (10, 30, 210)
        }
        self.cell_height = HEIGHT/MAT[0]
        self.cell_width = WIDTH/MAT[1]
        self.cells = []
        self.initialize_cells(randomize=True)
        self.run_state = False
    def initialize_cells(self, randomize=False):
        self.cells = []
        for i in range(MAT[0]):
            row = []
            for j in range(MAT[1]):
                if randomize:
                    row.append(random.choice([0, 1]))
                else:
                    row.append(0)
            self.cells.append(row[::])
    def clear_cells(self):
        self.cells = []
        for i in range(MAT[0]):
            row = [0]*MAT[1]
            self.cells.append(row[::])
    def get_neighbours(self, x, y):
        neighs = 0
        for i in range(-1, 2):
            adj_x = (x+i+MAT[1])%MAT[1]
            for j in range(-1, 2):
                adj_y = (y+j+MAT[0])%MAT[0]
                neighs += self.cells[adj_y][adj_x]
        neighs -= self.cells[y][x]
        return neighs
    def render(self):
        for i in range(MAT[0]):
            y = i*self.cell_height
            for j in range(MAT[1]):
                x = j*self.cell_width
                if self.cells[i][j]==1:
                    pygame.draw.rect(self.surface, self.color["cell"], (x, y, self.cell_width, self.cell_height))
                    pygame.draw.rect(self.surface, self.color["background"], (x, y, self.cell_width, self.cell_height), 1)
    def replica_cells(self, cells):
        new_cells = []
        for row in cells:
            new_cells.append(row[::])
        return new_cells
    def produce_next_generation(self):
        # GAME OF LIFE
        new_cells = self.replica_cells(self.cells)
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                neighs = self.get_neighbours(j, i)
                if self.cells[i][j] == 0:
                    if neighs == 3:
                        new_cells[i][j] = 1
                elif self.cells[i][j] == 1:
                    if neighs<2 or neighs>3:
                        new_cells[i][j] = 0
        self.cells = self.replica_cells(new_cells)
    def draw_new_cells(self):
        if 1 in [self.click[0], self.click[2]]:
            x, y = self.mouse
            i = int(y//self.cell_height)
            j = int(x//self.cell_width)
            if self.click[0]==1:
                self.cells[i][j] = 1
            elif self.click[2]==1:
                self.cells[i][j] = 0
    def action(self):
        if self.run_state:
            self.produce_next_generation()
        self.draw_new_cells()
    def run(self):
        while self.play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
                    elif event.key==K_RETURN:
                        self.initialize_cells(randomize=True)
                    elif event.key==K_BACKSPACE:
                        self.clear_cells()
                    elif event.key==K_SPACE:
                        self.run_state = not self.run_state
            #--------------------------------------------------------------
            self.render()
            self.action()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    app = App(surface)
    app.run()


