import math
import random
from tkinter.tix import COLUMN
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.display.set_caption('Snake_Game')

class cube (object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)): #setting dirnx to 1 makes sure that when the game starts the snake starts moving horizontally immediately.
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move (self, dirnx, dirny) :
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw (self, surface, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0] #rows
        j = self.pos[1] #columns

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis + centre - radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class snake (object):
    body = []
    turns = {} #helps us know where we've turned from to know the direction we're moving in
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # sets the current position of the head of the snake equal to where we turned so that we know where we turned

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1 
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #the [:] is a slice operator. It is a shortcut way to copy the original list or string keeping all object references the same in the copied list

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1: #removes the last turn from the list to prevent you from automatically turning when you reach that point again
                    self.turns.pop(p)

            else: #checks if we've reached the edge of the screen
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move (c.dirnx, c.dirny)

    def reset (self, pos): # for when the game resets
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube (self) :
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: #when moving right, we add the cube to the left side
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0: #when moving left, we add the cube to the right side
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1: #when moving down, we add the cube at the top
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1: #when moving up, we add the cube at the bottom
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw (self, surface) :
        for i, c in enumerate(self.body):
            if i == 0: # makes sure that we add eyes to the snake so we know what direction the snake is moving in
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid (w, rows, surface) :
    sizeBtwn = w  // rows

    x = 0 
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w)) #colour white, start position of line and end position of line
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redrawWindow (surface) :
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack (rows, item) :
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
           continue
        else:
            break

    return(x, y)
        
def message_box (subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

#main loop
def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color = (0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50) # the bigger the number, the faster it's gonna be
        clock.tick(10) # makes sure that the game doesn't run more than 10 frames per second #the bigger the number, the slower it's gonna be
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])): #when the snake collides with it's body
                print('Score: ', len(s.body))
                message_box('You hit yourself :(! Play again. Your score is...', len(s.body))
                s.reset((10, 10)) #resets the snake to the starting position
                break

        redrawWindow(win)
        
main()
