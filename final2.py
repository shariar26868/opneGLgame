from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Variables for game state
game_pause = False
game_over = False
catcher_x = 200
diamond_x = random.randint(50, 450)
diamond_y = 500
score = 0
speed = 2  # Start with a slower speed

# Draw functions
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

def draw_catcher():
    draw_rectangle(catcher_x, 50, catcher_x + 100, 100, (0, 0, 1))

def draw_diamond():
    draw_rectangle(diamond_x - 10, diamond_y, diamond_x + 10, diamond_y - 20, (1, 1, 0))

def draw_rocket():
    draw_rectangle(catcher_x + 10, 60, catcher_x + 90, 140, (1, 1, 1))  # Rocket body
    glColor3f(1, 0, 0)  # Rocket tip (nose cone)
    glBegin(GL_TRIANGLES)
    glVertex2f(catcher_x + 10, 140)
    glVertex2f(catcher_x + 90, 140)
    glVertex2f(catcher_x + 50, 180)
    glEnd()
    # Circular windows
    draw_circle(catcher_x + 50, 100, 10, (0, 0, 1))
    draw_circle(catcher_x + 50, 120, 10, (0, 0, 1))
    draw_circle(catcher_x + 50, 80, 10, (0, 0, 1))

def update_diamond():
    global diamond_y, diamond_x, catcher_x, game_over, score, speed
    if game_pause or game_over:
        return

    diamond_y -= speed
    if 50 <= diamond_y <= 100 and catcher_x <= diamond_x <= catcher_x + 100:
        score += 1
        print(f"Score: {score}")  # Show score in console like in Game 1
        reset_diamond()
    if diamond_y < 0:
        game_over = True

def reset_diamond():
    global diamond_y, diamond_x, speed
    diamond_y = 500
    diamond_x = random.randint(50, 450)
    speed += 0.2

def display_text(x, y, text):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display_buttons():
    # Draw Restart button
    draw_rectangle(50, 550, 150, 580, (0.5, 0.5, 0.5))
    display_text(70, 560, "Restart")

    # Draw Play/Pause button
    draw_rectangle(200, 550, 300, 580, (1, 0.5, 0))
    display_text(210, 560, "Play/Pause")

    # Draw Close button
    draw_rectangle(350, 550, 450, 580, (1, 0, 0))
    display_text(370, 560, "Close")

def handle_mouse_click(button, state, x, y):
    global game_pause, game_over, score, speed
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 600 - y  # Invert the y-coordinate
        if 50 <= x <= 150 and 550 <= y <= 580:  # Restart button
            game_over = False
            game_pause = False
            score = 0
            speed = 2
            reset_diamond()
        elif 200 <= x <= 300 and 550 <= y <= 580:  # Play/Pause button
            game_pause = not game_pause
        elif 350 <= x <= 450 and 550 <= y <= 580:  # Close button
            print("Goodbye")
            print(f"Final Score: {score}")
            glutLeaveMainLoop()  # Exit the GLUT main loop safely


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 600)

    if not game_over:
        draw_catcher()
        draw_diamond()
        draw_rocket()
        update_diamond()
        display_text(10, 520, f"Score: {score}")
    else:
        display_text(200, 300, "GAME OVER!")
        display_text(180, 260, f"Final Score: {score}")

    display_buttons()
    glutSwapBuffers()

def keyboard(key, x, y):
    global catcher_x
    if key == b'a' and catcher_x > 0:
        catcher_x -= 20
    elif key == b'd' and catcher_x < 400:
        catcher_x += 20
    glutPostRedisplay()

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Dynamic Rocket Game")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(handle_mouse_click)
    glutTimerFunc(16, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
