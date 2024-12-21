from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
game_over = False
game_pause = False
catcher_x = 200  
projectiles = []  
falling_circles = []  
score = 0
speed = 2 
bullet_speed = 25  
def draw_rectangle(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_circle(cx, cy, r, color):
    num_segments = 100
    theta = 2 * math.pi / num_segments
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    x = r
    y = 0

    glColor3f(*color)
    glBegin(GL_POLYGON)
    for _ in range(num_segments):
        glVertex2f(x + cx, y + cy)
        t = x
        x = cos_theta * x - sin_theta * y
        y = sin_theta * t + cos_theta * y
    glEnd()

def draw_shooter():
    draw_rectangle(catcher_x + 15, 50, catcher_x + 35, 130, (1, 1, 1))  
    draw_circle(catcher_x + 25, 115, 5, (1, 0, 0))  
    draw_circle(catcher_x + 25, 95, 5, (0, 0, 1))  
    draw_circle(catcher_x + 25, 75, 5, (1, 0, 0))  
    draw_triangle(catcher_x + 15, 130, catcher_x + 35, 130, catcher_x + 25, 150, (1, 0, 0))  
    draw_triangle(catcher_x + 15, 50, catcher_x + 5, 80, catcher_x + 15, 80, (0, 0, 1))  
    draw_triangle(catcher_x + 35, 50, catcher_x + 45, 80, catcher_x + 35, 80, (0, 0, 1)) 
    draw_triangle(catcher_x + 5, 50, catcher_x + 15, 50, catcher_x + 10, 40, (1, 0, 0)) 
    draw_triangle(catcher_x + 45, 50, catcher_x + 35, 50, catcher_x + 40, 40, (1, 0, 0))  

def draw_triangle(x1, y1, x2, y2, x3, y3, color):
    glColor3f(*color)
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def draw_projectile(x, y):
    draw_circle(x, y, 5, (1, 1, 1))  # White circle as the projectile

def draw_falling_circle(x, y):
    draw_circle(x, y, 10, (1, 1, 0))  # Yellow circle

def display_text(x, y, text):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def update_falling_circles():
    global falling_circles, score
    for circle in falling_circles[:]:
        circle[1] -= speed  
        if circle[1] < 0:  
            falling_circles.remove(circle)
        elif catcher_x <= circle[0] <= catcher_x + 50 and 50 <= circle[1] <= 100:
            falling_circles.remove(circle)
            score += 1 
            print(f"Score: {score}")  

def check_collision(projectile, circle):
    distance = math.sqrt((projectile[0] - circle[0])**2 + (projectile[1] - circle[1])**2)
    if distance <= 15:
        return True
    return False

def update_projectiles():
    global projectiles, falling_circles, score
    to_remove = set()  
    for projectile in projectiles:
        projectile[1] += bullet_speed
        if projectile[1] > 600:  
            to_remove.add(tuple(projectile))
        else:
            for circle in falling_circles[:]:
                if check_collision(projectile, circle): 
                    to_remove.add(tuple(projectile))
                    falling_circles.remove(circle)
                    score += 1 
                    print(f"Score: {score}")
    projectiles = [proj for proj in projectiles if tuple(proj) not in to_remove]


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0) 
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 600)

    if not game_over:
        draw_shooter()
        update_falling_circles() 
        update_projectiles() 
        for circle in falling_circles:
            draw_falling_circle(circle[0], circle[1])
        for projectile in projectiles:
            draw_projectile(projectile[0], projectile[1])
        display_text(10, 520, f"Your Score is: {score}")
    else:
        display_text(200, 300, "GAME IS OVER!")
        display_text(180, 260, f"Your Final Score is: {score}")

    display_buttons()
    glutSwapBuffers()

def display_buttons():
    draw_rectangle(50, 550, 150, 580, (0.5, 0.5, 0.5))  
    display_text(70, 560, "Restart")
    draw_rectangle(200, 550, 300, 580, (1, 0.5, 0))  
    display_text(210, 560, "Play/Pause")
    draw_rectangle(350, 550, 450, 580, (1, 0, 0))  
    display_text(370, 560, "Close")

def handle_mouse_click(button, state, x, y):
    global game_pause, game_over, score, speed
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 600 - y  
        if 50 <= x <= 150 and 550 <= y <= 580: 
            game_over = False
            game_pause = False
            score = 0
            speed = 2
            print("Starting Over")
            reset_game()
        elif 200 <= x <= 300 and 550 <= y <= 580:  
            game_pause = not game_pause
            print("Game Paused" if game_pause else "Game Resumed")
        elif 350 <= x <= 450 and 550 <= y <= 580:  
            print("Goodbye")
            print(f"Your Final Score is: {score}")
            glutLeaveMainLoop()  

def reset_game():
    global falling_circles
    falling_circles.clear()  

def keyboard(key, x, y):
    global catcher_x
    if key == b'a' and catcher_x > 0:
        catcher_x -= 20  
    elif key == b'd' and catcher_x < 450:
        catcher_x += 20  
    elif key == b' ' and not game_over and not game_pause:  
        projectiles.append([catcher_x + 25, 100])  
    glutPostRedisplay()

def timer(value):
    if not game_pause and not game_over:
        spawn_falling_circle()  
    glutPostRedisplay()
    glutTimerFunc(1000, timer, 0) 

def spawn_falling_circle():
    global falling_circles
    x = random.randint(50, 450)
    falling_circles.append([x, 500])  

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Rocket Shooter Game")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(handle_mouse_click)
    glutTimerFunc(1000, timer, 0) 
    glutMainLoop()  


if __name__ == "__main__":
    main()
 