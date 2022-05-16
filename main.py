import pygame as pg
import pprint
import random

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
        self.clock = pg.time.Clock()
        self.field = []
        self.running = True
        self.FPS = 30

    def matrix_field(self):
        self.field = [[0 for _ in range(self.Cols)] for _ in range(self.Rows)]
        # pp.pprint(self.field)
        mine_position = set()
        while len(mine_position) < self.Mines:
            row = random.randint(0, self.Rows - 1)
            col = random.randint(0, self.Cols - 1)
            mine_position.add((row, col))
            self.field[row][col] = -1

    def draw_board(self):
        for i in range(self.Cols):
            y = i * self.size
            for j in range(self.Rows):
                x = j * self.size
                pg.draw.rect(self.screen, "gray", (x, y, self.size, self.size))
                pg.draw.rect(self.screen, "black", (x, y, self.size, self.size), 2)

    def mainloop(self):
        self.matrix_field()
        while self.running:
            # self.screen.fill("white")
            self.draw_board()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            self.clock.tick(self.FPS)
            pg.display.update()


main = Main()
main.mainloop()
