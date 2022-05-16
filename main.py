import pygame as pg
import pprint
import random
from queue import Queue

pp = pprint.PrettyPrinter(width=30, compact=True)


class Main:
    def __init__(self):
        pg.init()
        self.Width = 600
        self.Height = 600
        self.Rows = 15
        self.Cols = 15
        self.Mines = 15
        self.size = self.Width // self.Rows
        self.screen = pg.display.set_mode((self.Width, self.Height))
        self.Nums_Colors = {-1: 'red', 0: "green", 1: 'blue', 2: 'green', 3: 'red', 4: 'darkblue'}
        self.covered_field = []
        self.clock = pg.time.Clock()
        self.field = []
        self.mine = pg.image.load("images/mine.png")
        self.Font = pg.font.Font(None, 20)
        self.click = 0
        self.running = True
        self.FPS = 30

    def get_neighbours(self, row, col):
        neighbours = []
        if row > 0:
            neighbours.append((row - 1, col))
        if row < self.Rows - 1:
            neighbours.append((row + 1, col))
        if col > 0:
            neighbours.append((row, col - 1))
        if col < self.Cols - 1:
            neighbours.append((row, col + 1))

        if row > 0 and col > 0:
            neighbours.append((row - 1, col - 1))
        if row < self.Rows - 1 and col < self.Cols - 1:
            neighbours.append((row + 1, col + 1))
        if row < self.Rows - 1 and col > 0:
            neighbours.append((row + 1, col - 1))
        if row > 0 and col < self.Cols - 1:
            neighbours.append((row - 1, col + 1))

        return neighbours

    def uncovered_field(self, row, col):
        q = Queue()
        q.put((row, col))
        visited = set()
        while not q.empty():
            current = q.get()
            neighbours = self.get_neighbours(*current)
            for row, col in neighbours:
                print(self.field[row][col])
                if (row, col) in visited or self.field[row][col] == -1:
                    continue
                self.covered_field[row][col] = 1
                if self.field[row][col] == 0:
                    q.put((row, col))
                visited.add((row, col))

    def do_matrix_field(self):
        self.field = [[0 for _ in range(self.Cols)] for _ in range(self.Rows)]
        self.covered_field = [[0 for _ in range(self.Cols)] for _ in range(self.Rows)]
        mine_position = set()
        while len(mine_position) < self.Mines:
            row = random.randint(0, self.Rows - 1)
            col = random.randint(0, self.Cols - 1)
            mine_position.add((row, col))
            self.field[row][col] = -1
        for mine in mine_position:
            neighbours = self.get_neighbours(*mine)
            for r, c in neighbours:
                if self.field[r][c] != -1:
                    self.field[r][c] += 1

    def draw_board(self):
        for i in range(self.Cols):
            y = i * self.size
            for j in range(self.Rows):
                x = j * self.size
                pg.draw.rect(self.screen, "gray", (x, y, self.size, self.size))
                pg.draw.rect(self.screen, "black", (x, y, self.size, self.size), 2)
                if self.covered_field[i][j] > 0:
                    pg.draw.rect(self.screen, "lightgray", (x, y, self.size, self.size))
                    pg.draw.rect(self.screen, "black", (x, y, self.size, self.size), 2)
                    if self.field[i][j] == -1:
                        self.screen.blit(self.mine, (x, y))
                        continue
                    if self.field[i][j] == 0:
                        continue
                    text = self.Font.render(f'{self.field[i][j]}', True, self.Nums_Colors[self.field[i][j]])
                    self.screen.blit(text, (x + (self.size // 2 - text.get_width() // 2),
                                            y + (self.size // 2 - text.get_height() // 2)))

    def lost(self):
        font = pg.font.Font(None, 50)
        text = font.render('You lost', True, "red")
        rect = text.get_rect(center=(self.Width // 2, self.Height // 2))
        self.screen.blit(text, rect)
        pg.display.update()
        pg.time.wait(5000 // 2)
        self.do_matrix_field()

    def mouse_clicked(self, mouse_pos):
        mx, my = mouse_pos
        row = int(my // self.size)
        col = int(mx // self.size)
        self.covered_field[row][col] = 1
        if self.click == 0:
            self.uncovered_field(row, col)
        self.click += 1
        if self.field[row][col] == -1:
            self.click = 0
            self.lost()

    def mainloop(self):
        self.do_matrix_field()
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mouse_clicked(pg.mouse.get_pos())
            self.clock.tick(self.FPS)
            self.screen.fill("white")
            self.draw_board()
            pg.display.update()


main = Main()
main.mainloop()
