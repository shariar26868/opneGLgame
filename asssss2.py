from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Variables for game state
game_pause = False
game_over = False
catcher_x = 200
bullets = []  # List of active bullets
falling_circles = []  # List of falling circles
score = 0
missed_circles = 0
misfires = 0
speed = 2  # Falling speed of circles

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
BULLET_SPEED = 5
MAX_MISSES = 3
MAX_MISFIRES = 3

# Function to draw a circle
def draw_circle(cx, cy, r, color=(1, 1, 1)):
    glColor3f(*color)
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

# Function to draw the spaceship shooter
def draw_shooter():
    glColor3f(0, 0, 1)  # Blue
    glBegin(GL_QUADS)
    glVertex2f(catcher_x, 50)
    glVertex2f(catcher_x + 100, 50)
    glVertex2f(catcher_x + 100, 100)
    glVertex2f(catcher_x, 100)
    glEnd()

# Function to update bullets
def update_bullets():
    global misfires
    for bullet in bullets[:]:
        bullet[1] += BULLET_SPEED  # Move bullet upwards
        if bullet[1] > WINDOW_HEIGHT:  # Check if bullet goes off-screen
            bullets.remove(bullet)
            misfires += 1

# Function to update falling circles
def update_circles():
    global falling_circles, score, missed_circles, game_over
    for circle in falling_circles[:]:
        circle[1] -= speed  # Move circle downwards

        # Check collision with shooter
        if 50 <= circle[1] <= 100 and catcher_x <= circle[0] <= catcher_x + 100:
            game_over = True

        # Check if circle is hit by a bullet
        for bullet in bullets[:]:
            if math.sqrt((circle[0] - bullet[0]) ** 2 + (circle[1] - bullet[1]) ** 2) < 20:
                score += 1
                falling_circles.remove(circle)
                bullets.remove(bullet)
                break

        # Check if circle falls off-screen
        if circle[1] < 0:
            missed_circles += 1
            falling_circles.remove(circle)

        if missed_circles >= MAX_MISSES:
            game_over = True

# Function to draw falling circles
def draw_circles():
    for circle in falling_circles:
        draw_circle(circle[0], circle[1], 20, color=(1, 0, 0))

# Function to draw bullets
def draw_bullets():
    for bullet in bullets:
        draw_circle(bullet[0], bullet[1], 5, color=(0, 1, 0))

# Function to display text
def display_text(x, y, text):
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Display function
def display():
    global score, game_over, misfires
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    if not game_over:
        draw_shooter()
        draw_bullets()
        draw_circles()

        # Update game elements
        update_bullets()
        update_circles()

        # Display score and stats
        display_text(10, 550, f"Score: {score}")
        display_text(10, 520, f"Missed: {missed_circles}/{MAX_MISSES}")
        display_text(10, 490, f"Misfires: {misfires}/{MAX_MISFIRES}")

        if misfires >= MAX_MISFIRES:
            game_over = True
    else:
        display_text(200, 300, "GAME OVER!")
        display_text(180, 260, f"Final Score: {score}")
        display_text(150, 220, "Press 'R' to Restart")

    glutSwapBuffers()

# Keyboard input function
def keyboard(key, x, y):
    global catcher_x, game_pause, game_over, bullets, score, missed_circles, misfires, speed

    if key == b'a' and catcher_x > 0:  # Move left
        catcher_x -= 20
    elif key == b'd' and catcher_x < WINDOW_WIDTH - 100:  # Move right
        catcher_x += 20
    elif key == b' ':  # Shoot
        if not game_over and not game_pause:
            bullets.append([catcher_x + 50, 100])
    elif key == b'p':  # Pause game
        game_pause = not game_pause
    elif key == b'r':  # Restart game
        game_over = False
        game_pause = False
        score = 0
        missed_circles = 0
        misfires = 0
        speed = 2
        bullets = []
        falling_circles = []

    glutPostRedisplay()

# Timer function to spawn circles and refresh display
def timer(value):
    if not game_pause and not game_over:
        if random.random() < 0.03:  # Spawn a new circle with a small probability
            falling_circles.append([random.randint(20, WINDOW_WIDTH - 20), WINDOW_HEIGHT])
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # ~60 FPS

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Shooter Game")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, timer, 0)  # Start timer
    glutMainLoop()

if __name__ == "__main__":
    main()
