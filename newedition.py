from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Game state variables
game_over = False
game_pause = False
catcher_x = 200  # Initial position of the shooter
projectiles = []  # List to store fired projectiles
falling_circles = []  # List to store falling circles
score = 0
speed = 2  # Speed of falling circles

# Draw functions
def draw_rectangle(x1, y1, x2, y2, color):
    """Draws a rectangle."""
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_circle(cx, cy, r, color):
    """Draws a circle with the center at (cx, cy) and radius r."""
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
    """Draws the shooter (spaceship) at its current position."""
    draw_rectangle(catcher_x, 50, catcher_x + 50, 100, (0, 0, 1))  # Spaceship body
    draw_triangle(catcher_x + 10, 100, catcher_x + 40, 100, catcher_x + 25, 130, (1, 0, 0))  # Spaceship nose

def draw_triangle(x1, y1, x2, y2, x3, y3, color):
    """Draws a triangle."""
    glColor3f(*color)
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def draw_projectile(x, y):
    """Draws a projectile (circle)."""
    draw_circle(x, y, 5, (1, 0, 0))  # Red circle as the projectile

def draw_falling_circle(x, y):
    """Draws a falling circle."""
    draw_circle(x, y, 10, (1, 1, 0))  # Yellow circle

def display_text(x, y, text):
    """Display text at a specific position."""
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def update_falling_circles():
    """Update the position of falling circles."""
    global falling_circles, score
    for circle in falling_circles[:]:
        circle[1] -= speed  # Move circle downwards
        if circle[1] < 0:  # Remove circles that go off-screen
            falling_circles.remove(circle)
        elif catcher_x <= circle[0] <= catcher_x + 50 and 50 <= circle[1] <= 100:
            # Check if the falling circle collides with the shooter
            falling_circles.remove(circle)
            score += 1  # Increase score
            print(f"Score: {score}")  # Print score to console

def check_collision(projectile, circle):
    """Check if a projectile collides with a falling circle."""
    # Calculate the distance between the centers of the two circles
    distance = math.sqrt((projectile[0] - circle[0])**2 + (projectile[1] - circle[1])**2)
    # Check if the distance is less than or equal to the sum of their radii (5 + 10 = 15)
    if distance <= 15:
        return True
    return False

def update_projectiles():
    """Update the position of projectiles."""
    global projectiles, falling_circles, score  # Declare score as global
    for projectile in projectiles[:]:
        projectile[1] += 5  # Move the projectile upwards
        if projectile[1] > 600:  # Remove projectiles that go off-screen
            projectiles.remove(projectile)
        else:
            for circle in falling_circles[:]:
                if check_collision(projectile, circle):  # Check for collision with each falling circle
                    projectiles.remove(projectile)  # Remove the projectile
                    falling_circles.remove(circle)  # Remove the falling circle
                    score += 1  # Increase score
                    print(f"Score: {score}")  # Print score to console

def display():
    """Render the entire game scene."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)  # Set background color
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 600)

    if not game_over:
        draw_shooter()
        update_falling_circles()  # Update falling circles
        update_projectiles()  # Update projectiles
        
        # Draw falling circles
        for circle in falling_circles:
            draw_falling_circle(circle[0], circle[1])

        # Draw projectiles
        for projectile in projectiles:
            draw_projectile(projectile[0], projectile[1])

        # Display the score on the screen
        display_text(10, 520, f"Score: {score}")
    else:
        display_text(200, 300, "GAME OVER!")
        display_text(180, 260, f"Final Score: {score}")

    glutSwapBuffers()

def keyboard(key, x, y):
    """Handle keyboard input for controlling the shooter and firing projectiles."""
    global catcher_x
    if key == b'a' and catcher_x > 0:
        catcher_x -= 20  # Move shooter left
    elif key == b'd' and catcher_x < 450:
        catcher_x += 20  # Move shooter right
    elif key == b' ' and not game_over:  # Spacebar to fire projectile
        fire_projectile()  # Fire a projectile
    glutPostRedisplay()

def fire_projectile():
    """Fire a projectile from the shooter's position."""
    projectiles.append([catcher_x + 25, 60])  # Fire projectile from the center of the shooter

def spawn_falling_circle():
    """Spawn a new falling circle at a random position."""
    x = random.randint(50, 450)  # Random horizontal position
    falling_circles.append([x, 500])  # Start at the top of the screen

def timer(value):
    """Timer function to periodically spawn falling circles and update the game state."""
    if not game_pause and not game_over:
        spawn_falling_circle()  # Spawn a new falling circle
    glutPostRedisplay()
    glutTimerFunc(1000, timer, 0)  # Call timer every 1000 ms

def handle_mouse_click(button, state, x, y):
    """Handle mouse clicks for any game-related actions (if needed)."""
    pass

def main():
    """Main function to initialize and run the game."""
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 600)
    glutCreateWindow(b"Shooter Game")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(handle_mouse_click)
    glutTimerFunc(1000, timer, 0)  # Start the falling circle spawn timer
    glutMainLoop()

if __name__ == "__main__":
    main()
