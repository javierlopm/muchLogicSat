#sudo apt-get install python-pygame
import pygame, sys
from pygame.locals import *

def draw(N,M,xlines,ylines):
    pygame.init()
    X=N+1
    Y=M+1
    
    infoObject = pygame.display.Info()
    XRES=min(infoObject.current_w/4*3,infoObject.current_h/4*3)
    YRES=XRES
    DISPLAY=pygame.display.set_mode((XRES,YRES))

    WHITE=(255,255,255)
    blue=(0,0,255)
    black = (0,0,0)

    DISPLAY.fill(WHITE)

    myfont = pygame.font.SysFont("monospace", 15)


    RADIUS=(XRES^2+YRES^2)
    #pygame.draw.rect(DISPLAY,blue,(200,150,100,50))
    dist=RADIUS*3
    xdesp=XRES/(X+1)
    ydesp=YRES/(Y+1)

    #MATRIX
    for i in range(1,X+1):
        label = myfont.render(repr(i), 0, black)
        if i<X:
            DISPLAY.blit(label, (ydesp/4*1,i*ydesp+ydesp/2))
            DISPLAY.blit(label, (i*xdesp+xdesp/2,(Y+1)*ydesp-ydesp/4*2))
        for j in range(1,Y+1):
            pygame.draw.circle(DISPLAY, black, (i*xdesp,j*ydesp), RADIUS, 0)
    #LINES X
    acc=0
    print(xlines)
    for j in range(N+1):
        for i in range(N):
            if xlines[j][i]=='1':
                pygame.draw.rect(DISPLAY,blue,(i*xdesp+xdesp,(j+1)*ydesp,xdesp,3))

    #LINES Y
    acc=0
    print(ylines)
    for i in range(N):
        for j in range(N+1):
            if ylines[i][j]=='1':
                pygame.draw.rect(DISPLAY,blue,(j*xdesp+xdesp,(i+1)*ydesp,3,xdesp))

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def main():
    for line in sys.stdin:
        line=sys.stdin.next().split()
        N = int(line[0])
        M = int(line[1])
        text=iter(line[2:])
        print(N)
        print(M)
        xlines=[]
        ylines=[]
        i=0
        for e in text:
            i=i+1
            xlines.append(e)
            if i<N+1:
                e=text.next()
                ylines.append(e)
        draw(N,M,xlines,ylines)
        #print(all((len(x)==M+1) for x in ylines))
main()