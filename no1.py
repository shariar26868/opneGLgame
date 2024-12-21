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
bullet_speed = 15  # Increased speed for the projectiles

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
    to_remove = []  # List to store projectiles to remove
    for projectile in projectiles[:]:  # Iterate over a copy of the list
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

    display_buttons()
    glutSwapBuffers()

def display_buttons():
    """Draw the control buttons at the top."""
    # Draw Restart button (Left Arrow)
    draw_rectangle(50, 550, 150, 580, (0.5, 0.5, 0.5))  # Gray button
    display_text(70, 560, "Restart")

    # Draw Play/Pause button (Amber)
    draw_rectangle(200, 550, 300, 580, (1, 0.5, 0))  # Amber button
    display_text(210, 560, "Play/Pause")

    # Draw Close button (Red)
    draw_rectangle(350, 550, 450, 580, (1, 0, 0))  # Red button
    display_text(370, 560, "Close")

def handle_mouse_click(button, state, x, y):
    """Handle mouse clicks for control buttons."""
    global game_pause, game_over, score, speed
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 600 - y  # Invert the y-coordinate to match OpenGL's coordinate system
        if 50 <= x <= 150 and 550 <= y <= 580:  # Restart button
            game_over = False
            game_pause = False
            reset_game()  # Reset game state
        elif 200 <= x <= 300 and 550 <= y <= 580:  # Play/Pause button
            game_pause = not game_pause
            print("Game Paused" if game_pause else "Game Resumed")
        elif 350 <= x <= 450 and 550 <= y <= 580:  # Close button
            print("Goodbye")
            print(f"Final Score: {score}")
            glutLeaveMainLoop()  # Exit the GLUT main loop safely

def reset_game():
    """Reset the game state."""
    global falling_circles, projectiles, score, speed, game_pause
    falling_circles.clear()  # Remove any remaining falling circles
    projectiles.clear()  # Clear all projectiles
    score = 0  # Reset the score
    speed = 2  # Reset falling circle speed
    game_pause = False  # Reset the game pause state
    print("Starting Over")  # Print the message when the game restarts

# Main loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 600)
    glutCreateWindow(b"Space Shooter Game")
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMouseFunc(handle_mouse_click)
    
    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
