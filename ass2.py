#import Lab2_task1
import random
import time
#from Lab2_task1 import*
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

w=500
h=600

def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx >= 0 and dy >= 0:
        if abs(dx) >= abs(dy):
            return 0
        else:
            return 1
    elif dx < 0 and dy >= 0:
        if abs(dx) >= abs(dy):
            return 3
        else:
            return 2
    elif dx < 0 and dy < 0:
        if abs(dx) >= abs(dy):
            return 4
        else:
            return 5
    elif dx >= 0 and dy < 0:
        if abs(dx) >= abs(dy):
            return 7
        else:
            return 6
    
    

def convertTozero(X, Y, z):
    if z == 0:
        return X, Y
    elif z == 1:
        return Y, X
    elif z == 2:
        return Y, -X
    elif z == 3:
        return -X, Y
    elif z == 4:
        return -X, -Y
    elif z == 5:
        return -Y, -X
    elif z == 6:
        return -Y, X
    elif z == 7:
        return X, -Y



def originalzone(X,Y,z):
    if z == 0:
        return X, Y
    elif z == 1:
        return Y, X
    elif z == 2:
        return -Y, X
    elif z == 3:
        return -X, Y
    elif z == 4:
        return -X, -Y
    elif z == 5:
        return -Y, -X
    elif z == 6:
        return Y, -X
    elif z == 7:
        return X, -Y


def midpoint(a,b,z):
    x1,y1=a[0],a[1]
    x2,y2=b[0],b[1]

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)



    X = x1
    Y = y1
    
    glBegin(GL_POINTS)
    while X <= x2:
        x_t,y_t=originalzone(X,Y,z)
        glVertex2f(x_t, y_t)


        if d > 0:
            d += incNE
            Y += 1 if y2 > y1 else -1
        else:
            d += incE

        X += 1

    glEnd()



        
def drawline(x1,y1,x2,y2):
    
    z=findzone(x1,y1,x2,y2)
    a=convertTozero(x1,y1,z)
    b=convertTozero(x2,y2,z)
    midpoint(a,b,z)

game_pause=False


catcher_x1=200
catcher_x2=300



def generate_random_color():
    red = random.random() 
    green = random.random() 
    blue = random.random() 
    return red,green,blue
color=generate_random_color()

diamond_x = random.randint(10, 490)
diamond_y = 520
last_time = time.time()
score = 0
game_over = False




def draw_left_arrow():
    glColor3f(0, 128, 128)
    drawline(15, 550, 45, 550)
    drawline(15, 550, 35, 560)
    drawline(15, 550, 35, 540)
    
def draw_play_button():

    glColor3f(255, 191, 0)
    drawline(245, 540, 245, 560)
    drawline(255, 540, 255, 560)

def draw_pause_button():
    glColor3f(255, 191, 0)
    drawline(240, 540, 240, 560)
    drawline(240, 560, 260, 550)
    drawline(240, 540, 260, 550)

def draw_cross_button():
    glColor3f(255, 0, 0)
    drawline(485, 560, 455, 540)
    drawline(455, 560, 485, 540)

def draw_catcher():
    global catcher_x1, catcher_x2

    drawline(catcher_x1,10,catcher_x2,10)
    drawline(catcher_x1,10,catcher_x1-10,20)
    drawline(catcher_x2,10,catcher_x2+10,20)
    drawline(catcher_x1-10,20,catcher_x2+10,20)

class BoundingBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def has_collided(box1, box2):
    return (
        box1.x < box2.x + box2.width and
        box1.x + box1.width > box2.x and
        box1.y < box2.y + box2.height and
        box1.y + box1.height > box2.y
    )

def draw_diamond():
    global diamond_x,diamond_y,color
    
    glColor3f(color[0],color[1],color[2])
    drawline(diamond_x,diamond_y,diamond_x-10,diamond_y-15)
    drawline(diamond_x,diamond_y,diamond_x+10,diamond_y-15)
    drawline(diamond_x-10,diamond_y-15,diamond_x,diamond_y-30)
    drawline(diamond_x+10,diamond_y-15,diamond_x,diamond_y-30)

def update_diamonds():
    global diamond_y, diamond_x, score, game_over, last_time,catcher_x1,catcher_x2,color,game_pause

    
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    if game_over==False and game_pause==False:
        
        speed=delta_time*100
        diamond_y-=speed

        diamond_box = BoundingBox(diamond_x - 10, diamond_y - 30, 20, 30)
        catcher_box = BoundingBox(catcher_x1, 10, catcher_x2 - catcher_x1, 20)

        if diamond_box.y <= 19:
            if has_collided(catcher_box, diamond_box)==True:
                score += 1
                speed*=2
                color=generate_random_color()
                print(f"Score: {score}")
                
                diamond_x = random.randint(10, 490)
                diamond_y = 520
            else:
                game_over = True
                game_pause=True
                print(f"Game Over! Final Score: {score}")

def mouselistener(button, state, x, y):
    global color, game_pause,catcher_x1, catcher_x2, score, diamond_x, diamond_y,game_over

    c_y=h-y
    if button == GLUT_LEFT_BUTTON:
        
        
        if state == GLUT_DOWN:
            
            if 245<= x <=255 and 540<=c_y<=560:
                if game_pause==True:
                    game_pause=False
                    print("Game resumed")
                else:
                    game_pause=True
                    print("Game paused")
                if game_over==True:
                    game_over=False
                    catcher_x1=200
                    catcher_x2=300
                    score=0
                    diamond_x=random.randint(10, 490)
                    diamond_y=520
                    print("Starting over!")   
            if 15<=x<=45 and 540<=c_y<=560:
                catcher_x1=200
                catcher_x2=300
                score=0
                diamond_x=random.randint(10, 490)
                diamond_y=520
                if game_pause==True:
                    game_pause=False
                if game_over==True:
                    game_over=False
                color=generate_random_color()
                print("Starting over!")
            if 455<=x<485 and 540<=c_y<=560:
                print(f"Goodbye!Final Score: {score}")
                glutLeaveMainLoop()


    glutPostRedisplay()


def special_keys(key,x,y):
    global catcher_x1, catcher_x2, game_pause, last_time


    step=5

    if key==GLUT_KEY_LEFT:

        if catcher_x1-step>=10 and game_pause==False:
            catcher_x1-=step
            catcher_x2-=step

    if key==GLUT_KEY_RIGHT:

        if catcher_x2+step<=490 and game_pause==False:
            catcher_x1+=step
            catcher_x2+=step
    glutPostRedisplay()


    
def display():
    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 600)

    glMatrixMode(GL_MODELVIEW)

    draw_left_arrow()
    global game_pause,game_over
    if game_pause==False :
        draw_play_button()

    if game_pause==True:
        draw_pause_button()

    draw_cross_button()
    
    if game_over==False:
        glColor3f(1,1,1)
        draw_catcher()
    elif game_over==True:
        glColor3f(255,0,0)
        draw_catcher()

    
    if game_over==False:

        
        draw_diamond()
        update_diamonds()


    

    glutSwapBuffers()

def animate():
    global game_over,game_pause
    if game_pause==False:
        if game_over==False:
            
            draw_diamond()
            update_diamonds()
        glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(w, h)
glutInitWindowPosition(900, 250)
glutCreateWindow(b"Catch the diamonds!")
glClearColor(0.0, 0.0, 0.0, 1.0)
glutDisplayFunc(display)
glutIdleFunc(animate)
glutMouseFunc(mouselistener)
glutSpecialFunc(special_keys)
glutMainLoop()

