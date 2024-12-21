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

def drawline(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_circle(cx, cy, r):
    num_segments = 100
    theta = 2 * math.pi / num_segments
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    x = r
    y = 0

    glBegin(GL_POLYGON)
    for _ in range(num_segments):
        glVertex2f(x + cx, y + cy)
        t = x
        x = cos_theta * x - sin_theta * y
        y = sin_theta * t + cos_theta * y
    glEnd()

def draw_catcher():
    glColor3f(0, 0, 1)  # Blue
    glBegin(GL_QUADS)
    glVertex2f(catcher_x, 50)
    glVertex2f(catcher_x + 100, 50)
    glVertex2f(catcher_x + 100, 100)
    glVertex2f(catcher_x, 100)
    glEnd()

def draw_diamond():
    glColor3f(1, 1, 0)  # Yellow
    glBegin(GL_QUADS)
    glVertex2f(diamond_x - 10, diamond_y)
    glVertex2f(diamond_x + 10, diamond_y)
    glVertex2f(diamond_x + 10, diamond_y - 20)
    glVertex2f(diamond_x - 10, diamond_y - 20)
    glEnd()

def draw_rocket():
    # Rocket body
    glColor3f(1, 1, 1)  # White
    drawline(catcher_x + 10, 60, catcher_x + 90, 60)  # Bottom of the rocket
    drawline(catcher_x + 10, 60, catcher_x + 10, 140)  # Left side
    drawline(catcher_x + 90, 60, catcher_x + 90, 140)  # Right side

    # Rocket tip (nose cone)
    glColor3f(1, 0, 0)  # Red
    drawline(catcher_x + 10, 140, catcher_x + 50, 180)  # Left slant
    drawline(catcher_x + 90, 140, catcher_x + 50, 180)  # Right slant

    # Circular windows
    glColor3f(0, 0, 1)  # Blue
    draw_circle(catcher_x + 50, 100, 10)  # Middle window
    draw_circle(catcher_x + 50, 120, 10)  # Upper window
    draw_circle(catcher_x + 50, 80, 10)   # Lower window

def update_diamond():
    global diamond_y, diamond_x, catcher_x, game_over, score, speed
    if game_pause or game_over:
        return

    # Move the diamond downward
    diamond_y -= speed

    # Check if the diamond is caught by the catcher
    if 50 <= diamond_y <= 100 and catcher_x <= diamond_x <= catcher_x + 100:
        score += 1
        reset_diamond()

    # Check if the diamond falls out of bounds
    if diamond_y < 0:
        game_over = True

def reset_diamond():
    global diamond_y, diamond_x, speed
    diamond_y = 500
    diamond_x = random.randint(50, 450)
    speed += 0.2  # Increase speed more slowly for a gradual difficulty increase

def display_text(x, y, text):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display():
    global score
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 600)

    # Draw game elements
    if not game_over:
        draw_catcher()
        draw_diamond()
        draw_rocket()
        update_diamond()

        # Display score
        display_text(10, 550, f"Score: {score}")
    else:
        display_text(200, 300, "GAME OVER!")
        display_text(180, 260, f"Final Score: {score}")
        display_text(150, 220, "Press 'R' to Restart")

    glutSwapBuffers()

def keyboard(key, x, y):
    global catcher_x, game_pause, game_over, score, speed
    if key == b'a':  # Move left
        if not game_pause and not game_over and catcher_x > 0:
            catcher_x -= 20
    elif key == b'd':  # Move right
        if not game_pause and not game_over and catcher_x < 400:
            catcher_x += 20
    elif key == b'p':  # Pause game
        game_pause = not game_pause
    elif key == b'r':  # Restart game
        game_over = False
        game_pause = False
        score = 0
        speed = 2  # Reset speed to initial value
        reset_diamond()
    glutPostRedisplay()

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # ~60 FPS

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Dynamic Rocket Game with Slower Bullet")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, timer, 0)  # Start timer
    glutMainLoop()

if __name__ == "__main__":
    main()
