# ethan

import sys, pygame
from random import randint
from pygame import gfxdraw
from extras import *


class tileObj(object):
    """
    num: Tile Number

    color: Bckg Color

    pos: (0-3,0-3) TL=(0,0)
    """
    def __init__(self,num,color,pos):
        self.value = num
        self.color = color
        self.pos = pos
        self.check()

    def check(self):
        if type(self.value) != int: raise TypeError('self.value must be an intager')

        if type(self.color) != tuple: raise TypeError('self.color must be a tuple')
        elif len(self.color) != 3: raise TypeError('self.color must have three values')
        else:
            for color in self.color:
                if color > 255 or color < 0:raise ValueError('each value of self.color must be in the range of 0-255')
        if type(self.pos) != tuple: raise TypeError('self.pos must be a tuple')
        elif len(self.pos) != 2: raise TypeError('self.pos must have two values')
        else:
            for point in self.pos:
                if point > 3 or point < 0:raise ValueError('each value of self.pos must be in the range of 0-3')
    
    def genTile(self):
        tile = pygame.Surface((132,132))
        return tile
    def addNum(self,tile):
        font = pygame.font.SysFont('', 145)
        if self.value != 2 and self.value != 4:
            text = font.render(str(self.value), True, (255,255,255))
        else: text = font.render(str(self.value), True, (0,0,0))
        rect = text.get_rect()
        pos = (tile.get_width()/2 - (rect.width/2), tile.get_height()/2 - (rect.height/2))
        tile.blit(text,pos)
        return tile
   
    def pickColor(self):
        v = self.value
        print(type(v), v)
        if v == 2: c = (230,230,230)
        elif v == 4: c = (203, 203, 203)
        elif v == 8: c = (255,204,102)
        elif v == 16: c = (255, 170, 0)
        elif v == 32: c = (255, 112, 77)
        elif v == 64: c = (179, 36, 0)
        elif v == 128: c = (255, 255, 153)
        elif v == 256: c = (255, 255, 51)
        elif v == 512: c = (230, 230, 0)
        elif v == 1024: c = (179, 179, 0)
        else: 
            c = (153, 153, 0)
            print('bbbbb')
        
        return c

    def draw(self):
        tile = self.genTile()
        tile.fill(self.pickColor())
        tile  = self.addNum(tile)

        offset = 165
        x = 146.25*self.pos[0]
        y = 146.25*self.pos[1]
        pos = (x+offset,y+offset)

        screen.blit(tile,pos)


def spawnTile(tiles=[]):
    x=randint(1,2)
    x=x*2

    while True:
        x1 = randint(0,3)
        x2 = randint(0,3)
        check = True
        for tile in tiles:
            if tile.pos == (x1,x2):
                check == False
        if check: break
            

    x = tileObj(x,(0,125,125),(x1,x2))

    return x

def sortTiles(tiles,move):
    if move[0] != 0:
        t=[]
        while len(tiles)>0:
            close = tiles[0]
            for tile in tiles:
                p = tile.pos[0]
                if abs(move[0]-p) < abs(move[0]-close.pos[0]):
                    close = tile
            t.append(close)
            tiles.remove(close)
        return t
    if move[1] != 0:
        t=[]
        while len(tiles)>0:
            close = tiles[0]
            for tile in tiles:
                p = tile.pos[1]
                if abs(move[1]-p) < abs(move[1]-close.pos[1]):
                    close = tile
            t.append(close)
            tiles.remove(close)
        return t


size = (900,800)

pygame.init()
screen = pygame.display.set_mode(size)
init(screen, size)
screen.fill((255,255,255))
pygame.display.flip()

mouse = pygame.Rect(0, 0, 2, 2)

border = pygame.Rect(150,150,600,600)

x=spawnTile()
tiles = [x]
y=spawnTile(tiles)

tiles = [x,y]
movement = (0,0)
while True:
    xm, ym = pygame.mouse.get_pos()
    mouse.center = (xm,ym)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


    ##GRID
    pygame.draw.rect(screen,(125,125,125),border)
    border_width = 15
    pygame.draw.rect(screen,(155,155,155),pygame.Rect(border.left+border_width,border.top+border_width,border.width-(border_width*2),border.height-(border_width*2)))
    
    for i in range(3):
        start = border.left + border_width/2
        step = border.width/4 - border_width/4
        start = start + (step*(1+i))
        start = int(start)
        end = (start,border.bottom-5)
        start = (start,border.top+5)
        
        pygame.draw.line(screen,(125,125,125),start,end,border_width)

        s,d = start
        x,c = end
        start = (d,s)
        end = (c,x) 
        pygame.draw.line(screen,(125,125,125),start,end,border_width)
        

    ##DrawTiles
    for tile in tiles:
        tile.draw()
    ##--##
        
    ##--##

    ##keyCheck

    keys = getKeys()
    if 'right' in keys or 'd' in keys: movement = (1,0)
    elif 'left' in keys or 'a' in keys: movement = (-1,0)
    elif 'up' in keys or 'w' in keys: movement = (0,-1)
    elif 'down' in keys or 's' in keys: movement = (0,1)

    ##--##

    ##MoveTiles:
    if movement != (0,0) and moveSpam:
        moveSpam = False
        tiles = sortTiles(tiles, (movement[0]*5, movement[1]*5))
    
        didMove = True
        movedOnce = False
        while didMove:
            print(len(tiles))
            for tile in tiles:
                pos = tile.pos
                pos = (pos[0]+movement[0], pos[1]+movement[1])
                check = False
                if pos[0] >= 0 and pos[0] <= 3 and pos[1] >= 0 and pos[1] <= 3:
                    check = True
                    for t2 in tiles:
                        if pos == t2.pos and tile != t2:
                              check = False
                if check: 
                    tile.pos = pos
                    didMove = True
                    movedOnce = True
                else: didMove = False

    
    
    ##--##

    ##SpawnNew
    if movement != (0,0) and spamMeasure and movedOnce:
        spamMeasure = False
        t = spawnTile(tiles)
        tiles.append(t)
    if movement == (0,0):
        spamMeasure = True
        moveSpam = True

    movement = (0,0)
    ##--##

    pygame.display.flip()
    screen.fill((255,255,255))


