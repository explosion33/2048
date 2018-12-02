"Main Code for 2048 game"

import sys
import ctypes
from random import randint
import pygame
#from pygame import gfxdraw
import extras


class tileObj:
    """
    num: Tile Number

    color: Bckg Color

    pos: (0-3,0-3) TL=(0,0)
    """
    def __init__(self, num, color, pos):
        self.value = num
        self.color = color
        self.pos = pos
        self.check()
        self.justSpawned = False
        self.justMerged = False
        self.mergeAnim = 11
        self.lastPosition = self.pos
        self.size = None
        self.alpha = 255
        self.posOffset = (0,0)

    def pop(self, tile):
        "Pops up the tile for the purpous of merging"
        print('pop')
        x,y = self.size
        x += 40
        y += 40
        tile = pygame.transform.smoothscale(tile, (x,y))
        self.posOffset = (-20,-20)
        return tile

    def check(self):
        "Checks to make sure all class requirements are met"

        if type(self.value) != int:
            raise TypeError('self.value must be an intager')
        if type(self.color) != tuple:
            raise TypeError('self.color must be a tuple')
        elif len(self.color) != 3:
            raise TypeError('self.color must have three values')
        else:
            for color in self.color:
                if color > 255 or color < 0:
                    raise ValueError('each value of self.color must be in the range of 0-255')
        if type(self.pos) != tuple:
            raise TypeError('self.pos must be a tuple')
        elif len(self.pos) != 2:
            raise TypeError('self.pos must have two values')
        else:
            for point in self.pos:
                if point > 3 or point < 0:
                    raise ValueError('each value of self.pos must be in the range of 0-3')

    def genTile(self):
        "The Code to generate a tile"
        tile = pygame.Surface((132, 132))
        self.size = (132,132)
        return tile
    def addNum(self, tile, size):
        "The code to add the number to the blank tile"
        font = pygame.font.SysFont('', size)
        if self.value != 2 and self.value != 4:
            text = font.render(str(self.value), True, (255, 255, 255))
        else: text = font.render(str(self.value), True, (0, 0, 0))
        rect = text.get_rect()
        pos = (tile.get_width()/2 - (rect.width/2), tile.get_height()/2 - (rect.height/2))
        tile.blit(text, pos)
        return tile

    def pickColor(self):
        "Defines preset colors for values"
        v = self.value
        size = 145

        if v == 2: c = (230, 230, 230)
        elif v == 4: c = (203, 203, 203)
        elif v == 8: c = (255, 204, 102)
        elif v == 16: c = (255, 170, 0)
        elif v == 32: c = (255, 112, 77)
        elif v == 64: c = (179, 36, 0)
        elif v == 128:
            c = (255, 255, 153)
            size = 100
        elif v == 256:
            c = (255, 255, 51)
            size = 90
        elif v == 512:
            c = (230, 230, 0)
            size = 90
        elif v == 1024:
            c = (255,223,0)
            size = 80
        else:
            c = (255,223,0)
            size = 75
        if v > 10000: size = 60

        return c,size

    def draw(self):
        "Draws the tile onto the screen surface at a specific coordinate point"
        tile = self.genTile()
        c,size = self.pickColor()
        tile.fill(c)
        tile = self.addNum(tile,size)

        offset = 165
        x = 146.25*self.pos[0]
        y = 146.25*self.pos[1]
        tile.set_alpha(self.alpha)
        if self.justMerged:
            tile = self.pop(tile)
            self.posOffset = (-20,-20)
        pos = (x+offset+self.posOffset[0], y+offset+self.posOffset[1])
        screen.blit(tile, pos)


def spawnTile(grid):
    "Randomly spawns tiles on the board"
    num = randint(1, 2)
    num = num*2
    grd = grid


    while True:
        x = randint(0, 3)
        y = randint(0, 3)
        if grd[y][x] == 0:
            grd[y][x] = num
            break

    x = tileObj(num, (0, 125, 125), (x, y))
    x.justSpawned = True
    return x, grd


def sortTiles(tiles, move):
    "Sorts tiles in a list based on keyPress"

    if move[0] != 0:
        t = []
        while tiles:
            close = tiles[0]
            for tile in tiles:
                p = tile.pos[0]
                if abs((move[0]*5)-p) < abs((move[0]*5)-close.pos[0]):
                    close = tile
            t.append(close)
            tiles.remove(close)
        return t
    if move[1] != 0:
        t=[]
        while tiles:
            close = tiles[0]
            for tile in tiles:
                p = tile.pos[1]
                if abs((move[1]*5)-p) < abs((move[1]*5)-close.pos[1]):
                    close = tile
            t.append(close)
            tiles.remove(close)
        return t
    return tiles

def reset():
    "Resets game variables for purpous of the retry button"
    global tiles
    global grid
    global enableInput
    global movement
    global keySpam
    global mode
    global fadeIn
    global score

    tiles = []
    grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    x, grid = spawnTile(grid)
    y, grid = spawnTile(grid)

    tiles = [x,y]
    movement = (0,0)

    enableInput = True
    keySpam = False
    mode = 'game'
    fadeIn = [True,0]
    score = [0,0]

def cont():
    "Function to be used for the continue button on winning"
    global movement
    global keySpam
    global mode
    global fadeIn
    global score
    global canWin

    movement = (0,0)
    keySpam = False
    mode = 'game'
    fadeIn = [True,0]
    score = [0,0]
    canWin = False

def onKeyPress(velocity, grid, tiles):
    "Logic for when a key is pressed"
    ##Move

    t = sortTiles(tiles,velocity)
    mergedTiles = []
    loop = True
    movedOnce = False
    while loop:
        didMove = False
        for tile in t:
            newPos = (tile.pos[0]+velocity[0], tile.pos[1]+velocity[1])
            if newPos[0] <= 3 and newPos[0] >= 0 and newPos[1] >= 0 and newPos[1] <= 3:
                check = True, None
                for k in t:
                    if newPos == k.pos:
                        check = False, k

                if check[0]:
                    grid[tile.pos[1]][tile.pos[0]] = 0
                    tile.pos = newPos
                    grid[newPos[1]][newPos[0]] = tile.value
                    didMove = True
                    movedOnce = True
                elif tile.value == check[1].value and (tile not in mergedTiles) and (check[1] not in mergedTiles):
                    x,y = tile.pos
                    grid[y][x] = 0

                    tile.value = tile.value*2
                    tile.pos = check[1].pos

                    x,y = tile.pos
                    grid[y][x] = tile.value

                    t.remove(check[1])
                    mergedTiles.append(tile)
                    tile.justMerged = True

                    didMove = True
                    movedOnce = True
        if not didMove: loop = False

    ##--##

    if movedOnce:
        newTile,grid = spawnTile(grid)
        t.append(newTile)


    if len(t) == 16:
        arePossibleMoves = False
        for tile in t:
            x,y = tile.pos
            val = tile.value
            for i in [-1,1]:
                x1 = x+i
                try:
                    if grid[y][x1] == val:
                        if x1 >= 0:
                            arePossibleMoves = True
                            print((x,y),(x1,y),grid[y][x1])
                except IndexError: pass
            for i in [-1,1]:
                y1 = y+i
                try:
                    if grid[y1][x] == val:
                        if y1 >= 0:
                            arePossibleMoves = True
                            print((x,y),(x,y1),grid[y1][x])
                except IndexError: pass

        if not arePossibleMoves:
            global mode
            mode = 'lose'

    for tile in t:
        global canWin
        if tile.value == 2048 and canWin:
            mode = 'win'

    return grid, t


ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

size = (900,900)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('2048')
extras.init(screen, size)
screen.fill((255,255,255))
pygame.display.flip()

mouse = pygame.Rect(0, 0, 2, 2)

border = pygame.Rect(150,150,600,600)

grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

x, grid = spawnTile(grid)
tiles = [x]
y, grid = spawnTile(grid)

tiles = [x,y]
movement = (0,0)

enableInput = True
keySpam = False
mode = 'game'
fadeIn = [True, 0]
score = [0,0]
canWin = True


print(grid)



while True:
    xm, ym = pygame.mouse.get_pos()
    mouse.center = (xm,ym)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.FULLSCREEN:
            pygame.display.toggle_fullscreen()


    if mode == 'game':
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
            if tile.justSpawned:
                tile.alpha = 30
                tile.justSpawned = False
            elif tile.alpha < 255:
                tile.alpha += 5

            if tile.justMerged and tile.mergeAnim == 11:
                tile.mergeAnim = 0
            elif tile.mergeAnim < 7:
                tile.mergeAnim += 1
            elif tile.mergeAnim == 7:
                tile.mergeAnim = 11
                tile.justMerged = False
                tile.posOffset = (0,0)

            tile.draw()
        ##--##


        ##keyCheck

        keys = extras.getKeys()
        if 'right' in keys or 'd' in keys: movement = (1,0)
        elif 'left' in keys or 'a' in keys: movement = (-1,0)
        elif 'up' in keys or 'w' in keys: movement = (0,-1)
        elif 'down' in keys or 's' in keys: movement = (0,1)

        if keys and keySpam and enableInput:
            keySpam = False
            grid, tiles = onKeyPress(movement, grid, tiles)
            print(grid, movement, len(tiles))
        elif not keys:
            keySpam = True
        ##--##

        font = pygame.font.SysFont('', 40)
        credit = font.render('Created by Ethan Armstrong', True, (0,0,0))

        screen.blit(credit, (20,size[1]-40))


    if mode == 'lose':
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

        if fadeIn[0]:
            score[1] = 0
            for tile in tiles:
                score[1] += tile.value

            score[0] += score[1]*(5/220)

            chng = 5
            fadeIn[1] = fadeIn[1] + 5

            if fadeIn[1] == 220:
                fadeIn[0] = False

        grey = pygame.Surface((size[0],size[1]))
        grey.fill((125,125,125))

        font = pygame.font.SysFont('', 155)

        title = font.render('Game Over', True, (255,255,255))
        grey.blit(title, (size[0]/2 - title.get_width()/2 ,60))

        font = pygame.font.SysFont('', 135)

        scoreText = font.render('Score: ' + str(int(score[0])), True, (255,255,255))
        grey.blit(scoreText, (size[0]/2 - scoreText.get_width()/2, 210))

        resetB = extras.word('Play Again',['center',360],reset,[],'',(255,255,255),(200,200,200),135)


        if fadeIn[0]:
            resetB.render(grey)

        resetB.isHovered(mouse)

        grey.set_alpha(fadeIn[1])
        screen.blit(grey, (0,0))

        if not fadeIn[0]:
            resetB.render(screen)
            screen.blit(scoreText, (size[0]/2 - scoreText.get_width()/2, 210))
            screen.blit(title, (size[0]/2 - title.get_width()/2 ,60))

            score[0] = score[1]

    if mode == 'win':
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

        if fadeIn[0]:
            score[1] = 0
            for tile in tiles:
                score[1] += tile.value

            score[0] += score[1]*(5/220)

            chng = 5
            fadeIn[1] = fadeIn[1] + 5

            if fadeIn[1] == 220:
                fadeIn[0] = False

        gold = pygame.Surface((size[0],size[1]))
        gold.fill((255,215,0))

        font = pygame.font.SysFont('', 155)

        title = font.render('2048', True, (255,255,255))
        gold.blit(title, (size[0]/2 - title.get_width()/2 ,60))

        font = pygame.font.SysFont('', 135)

        scoreText = font.render('Score: ' + str(int(score[0])), True, (255,255,255))
        gold.blit(scoreText, (size[0]/2 - scoreText.get_width()/2, 210))

        contB = extras.word('Continue',['center',360],cont,[],'',(255,255,255),(255,215,120),135)
        resetB = extras.word('Play Again',['center',490],reset,[],'',(255,255,255),(200,200,200),135)

        if fadeIn[0]:
            resetB.render(gold)
            contB.render(gold)

        resetB.isHovered(mouse)
        contB.isHovered(mouse)

        gold.set_alpha(fadeIn[1])
        screen.blit(gold, (0,0))

        if not fadeIn[0]:
            resetB.render(screen)
            contB.render(screen)
            screen.blit(scoreText, (size[0]/2 - scoreText.get_width()/2, 210))
            screen.blit(title, (size[0]/2 - title.get_width()/2 ,60))

            score[0] = score[1]

    pygame.display.flip()
    screen.fill((255,255,255))
    