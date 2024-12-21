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
bullet_speed = 50  # Increased speed for the projectiles

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

def draw_rocket():
    """Draws a realistic rocket shape."""
    # Rocket body
    draw_ellipse(catcher_x + 25, 100, 20, 60, (0.8, 0, 0))  # Red rocket body (ellipse)

    # Rocket nose (cone shape)
    draw_triangle(catcher_x + 10, 160, catcher_x + 40, 160, catcher_x + 25, 200, (1, 0.7, 0))  # Yellow cone

    # Rocket fins (triangle shapes)
    draw_triangle(catcher_x + 5, 60, catcher_x + 25, 30, catcher_x + 45, 60, (0, 0, 0))  # Left fin (black)
    draw_triangle(catcher_x + 25, 60, catcher_x + 45, 60, catcher_x + 25, 30, (0, 0, 0))  # Right fin (black)

    # Rocket flame (yellow)
    draw_triangle(catcher_x + 15, 10, catcher_x + 35, 10, catcher_x + 25, -20, (1, 1, 0))  # Flame

def draw_ellipse(cx, cy, rx, ry, color):
    """Draws an ellipse with center (cx, cy), x radius (rx), and y radius (ry)."""
    num_segments = 100
    theta = 2 * math.pi / num_segments
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    x = rx
    y = 0

    glColor3f(*color)
    glBegin(GL_POLYGON)
    for _ in range(num_segments):
        glVertex2f(x + cx, y + cy)
        t = x
        x = cos_theta * x - sin_theta * y
        y = sin_theta * t + cos_theta * y
    glEnd()

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
    to_remove = []  # List to store projectiles to remove
    for projectile in projectiles:
        projectile[1] += bullet_speed  # Move the projectile upwards (increased speed)
        if projectile[1] > 600:  # Remove projectiles that go off-screen
            to_remove.append(projectile)
        else:
            for circle in falling_circles[:]:
                if check_collision(projectile, circle):  # Check for collision with each falling circle
                    to_remove.append(projectile)  # Add to remove list
                    falling_circles.remove(circle)  # Remove the falling circle
                    score += 1  # Increase score
                    print(f"Score: {score}")  # Print score to console
    
    # Now remove all projectiles that need to be removed
    for projectile in to_remove:
        projectiles.remove(projectile)

def display():
    """Render the entire game scene."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)  # Set background color
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 600)

    if not game_over:
        draw_rocket()
        update_falling_circles()  # Update falling circles
        update_projectiles()  # Update projectiles
        
        # Draw falling circles
        for circle in falling_circles:
            draw_falling_circle(circle[0], circle[1])

        # Draw projectiles
        for projectile in projectiles:
            draw_projectile(projectile[0], projectile[1])

    else:
        display_text(200, 300, "GAME OVER!")
        display_text(180, 260, f"Final Score: {score}")

    display_buttons()
    glutSwapBuffers()

def display_buttons():
    """Draw the control buttons without a background."""
    # Draw Restart button (Left arrow)
    display_text(110, 560, "<----")

    # Draw Pause button (Audio pause "| |")
    display_text(220, 560, "| |")

    # Draw Close button (X shape)
    display_text(370, 560, "X")

def handle_mouse_click(button, state, x, y):
    """Handle mouse clicks for control buttons."""
    global game_pause, game_over, score, speed
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 600 - y  # Invert the y-coordinate to match OpenGL's coordinate system
        if 50 <= x <= 150 and 550 <= y <= 580:  # Restart button
            game_over = False
            game_pause = False
            score = 0
            speed = 2
            print("Starting Over")
            reset_game()
        elif 200 <= x <= 300 and 550 <= y <= 580:  # Pause button
            game_pause = not game_pause
            print("Game Paused" if game_pause else "Game Resumed")
        elif 350 <= x <= 450 and 550 <= y <= 580:  # Close button
            print("Goodbye")
            print(f"Final Score: {score}")
            glutLeaveMainLoop()  # Exit the GLUT main loop safely

def reset_game():
    """Reset the game state."""
    global falling_circles
    falling_circles.clear()  # Remove any remaining falling circles

def keyboard(key, x, y):
    """Handle keyboard input for controlling the shooter and firing projectiles."""
    global catcher_x
    if key == b'a' and catcher_x > 0:
        catcher_x -= 20  # Move shooter left
    elif key == b'd' and catcher_x < 450:
        catcher_x += 20  # Move shooter right
    elif key == b' ' and not game_over and not game_pause:  # Spacebar to fire
        if len(projectiles) < 3:  # Limit the number of projectiles on screen
            projectiles.append([catcher_x + 25, 100])  # Add projectile at shooter's position
            print("Fired a projectile!")
    glutPostRedisplay()

def timer(value):
    """Update the game state periodically."""
    if not game_pause and not game_over:
        spawn_falling_circle()  # Spawn a new falling circle periodically
    glutPostRedisplay()
    glutTimerFunc(1000, timer, 0)  # Call this function again in 1 second

def spawn_falling_circle():
    """Spawn a new falling circle."""
    global falling_circles
    x = random.randint(50, 450)
    falling_circles.append([x, 500])  # Add a new falling circle at random x position

def main():
    """Initialize and run the game."""
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Spaceship Shooter Game")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(handle_mouse_click)
    glutTimerFunc(1000, timer, 0)  # Start the falling circle spawn timer
    glutMainLoop()

if __name__ == "__main__":
    main()
