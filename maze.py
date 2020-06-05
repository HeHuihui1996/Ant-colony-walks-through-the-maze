#!/usr/bin/python3
#coding=utf-8
import random
import tkinter as tk

class Cell():
    TOP = (0)
    RIGHT = (1)
    BOTTOM = (2)
    LEFT = (3)
    def __init__(self, x, y):
        self.index = 0
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]
        self.visited = False
    def __str__(self):
        return 'x:{}-y:{}, walls:{}'.format(self.x, self.y, self.walls)
    def Walls(self):
        return self.walls
    def delTop(self):
        self.walls[0] = False
    def delRight(self):
        self.walls[1] = False
    def delBottom(self):
        self.walls[2] = False
    def delLeft(self):
        self.walls[3] = False
    def setWall(self, isWall, index):
        if index not in [0, 1, 2, 3]:
            return
        self.walls[index] = isWall
    def XY(self):
        return [self.x, self.y]
    def X(self):
        return self.x
    def Y(self):
        return self.y
    def isVisited(self):
        return self.visited
    def setVisited(self):
        self.visited = True

class Maze():
    SIZE = (18)
    START = (0, 0)
    def __init__(self):
        self.size = self.SIZE
        self.bfsBuffer = []
        self.cells = \
                [[Cell(y, x) for x in range(self.SIZE)] \
                for y in range(self.SIZE)]

        self.current = self.cells[self.START[0]][self.START[1]]


    def __str__(self):
        info = ''
        for rows in self.cells:
            for cell in rows:
                info += str(cell)
        return info
    def trblWalls(self, x, y):
        return self.cells[x][y].Walls()
    def visited(self, x, y):
        return self.cells[x][y].isVisited()
    def CurrentCell(self):
        return self.current
    def setCurrent(self, cell):
        self.current = cell
    def topCell(self):
        if 0 == self.current.Y():
            return None
        return self.cells[self.current.X()][self.current.Y() - 1]
    def rightCell(self):
        if self.current.X() == (self.SIZE - 1):
            return None
        return self.cells[self.current.X() + 1][self.current.Y()]
    def bottomCell(self):
        if self.current.Y() == (self.SIZE - 1):
            return None
        return self.cells[self.current.X()][self.current.Y() + 1]
    def leftCell(self):
        if 0 == self.current.X():
            return None
        return self.cells[self.current.X() - 1][self.current.Y()]
    def delWall(self, current, neighbor):
        x = current.X()
        y = current.Y()
        x2 = neighbor.X()
        y2 = neighbor.Y()
        #print("({}x{}) and ({}x{})".format(x, y, x2, y2))

        if (1 == (x - x2)):
            current.delLeft()
            neighbor.delRight()
        elif (-1 == (x - x2)):
            current.delRight()
            neighbor.delLeft()
        if (1 == (y - y2)):
            current.delTop()
            neighbor.delBottom()
        elif (-1 == (y - y2)):
            current.delBottom()
            neighbor.delTop()

    def checkNeighbor(self):
        neighbor = []
        top = self.topCell()
        right = self.rightCell()
        bottom = self.bottomCell()
        left = self.leftCell()
        if (None != top and not top.isVisited()):
            neighbor.append(self.topCell())
        if (None != right and not right.isVisited()):
            neighbor.append(self.rightCell())
        if (None != bottom and not bottom.isVisited()):
            neighbor.append(self.bottomCell())
        if (None != left and not left.isVisited()):
            neighbor.append(self.leftCell())
        count = len(neighbor)
        if 0 == count:

            if (len(self.bfsBuffer) == 0):
                return
            self.current = self.bfsBuffer.pop()
            self.checkNeighbor()

            return

        old = self.current

        self.current = neighbor[random.randint(0, count - 1)]

        self.delWall(old, self.current)
        #print('neighbor count:{} ->{}'.format(count, str(self.current)))
        self.setUp()

    def setUp(self):
        self.current.setVisited()
        self.bfsBuffer.append(self.current)
        self.checkNeighbor()

class MazeUI():
    winWidth = (600)
    winHeight = (600)
    def __init__(self):
        self.maze = Maze()
        self.ui = tk.Tk()
        self.centeredDisplay()

        self.createMaze()

        self.ui.mainloop()
    def centeredDisplay(self):
        self.ui.title('Maze by jianc')
        self.ui.geometry('{}x{}+{}+{}'.format( \
                self.winWidth, self.winHeight, \
                int((self.ui.winfo_screenwidth() - self.winWidth)/2), \
                int((self.ui.winfo_screenheight() - self.winHeight)/2)))
        self.ui.resizable(False, False)
    def createMaze(self):
        self.cs = tk.Canvas(self.ui, bg = '#5f3c23')

        self.cs.pack(side = tk.TOP, fill = 'both', expand=1, \
                padx=0, ipadx=0, pady=0, ipady=0)

        self.maze.setUp()

        #print(self.maze)
        self.drawCells()

    def drawCells(self):
        w = float(self.winWidth / self.maze.SIZE)
        h = float(self.winHeight / self.maze.SIZE)
        current = self.maze.CurrentCell()
        y = current.X()
        x = current.Y()
        self.cs.create_rectangle(y * w + 4, x * h + 4, (y + 1) * w - 4, (x + 1) * h - 4, \
                fill='#ff0000', width = 0)



        for rows in range(self.maze.SIZE):
            for cols in range(self.maze.SIZE):
                top, right, bottom, left = self.maze.trblWalls(cols, rows)
                #print("top:{} right:{} bottom:{} left:{}".format(top, right, bottom, left))
                bVisited = self.maze.visited(rows, cols)

                """if bVisited:
                    self.cs.create_rectangle(rows * w + 10, cols * h + 10, \
                            (rows + 1) * w - 10, (cols+ 1) * h - 10, fill='#00ff00', width = 0)
                """
                if top:
                    self.cs.create_line(cols * w, rows * h, \
                            (cols + 1) * w, rows * h, width=5)
                if right:
                    self.cs.create_line((cols + 1) * w, rows * h, \
                            (cols + 1) * w, (rows + 1) * h, width=5)
                if bottom:
                    self.cs.create_line((cols + 1) * w, (rows + 1) * h, \
                            cols * w, (rows + 1) * h, width=5)
                if left:
                    self.cs.create_line(cols * w, (rows + 1) * h, \
                            cols * w, rows * h, width=5)

        current = self.maze.CurrentCell()
        y = current.X()
        x = current.Y()
        self.cs.create_rectangle(y * w + 5, x * h + 5, (y + 1) * w - 5, (x + 1) * h - 5, \
                fill='#ff0000', width = 0)



maze = MazeUI()