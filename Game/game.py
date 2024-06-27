# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Load player model
sprite = pygame.image.load("phantom.png")
player = pygame.transform.scale(sprite, (200, 200))
player_flipped = pygame.transform.flip(player, True, False)  # Pre-flip the player image horizontally

# Load fireball
fireball_image = pygame.image.load("fireball.png")  # Load your fireball image
fireball_image = pygame.transform.scale(fireball_image, (50, 50))  # Scale the fireball image
fireball_image_flipped = pygame.transform.flip(fireball_image, True, False)  # Pre-flip the fireball image horizontally

# Define initial player position variables
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_direction = "left"  # Keep track of the player direction

# List to store fireballs
fireballs = []

class Fireball:
    def __init__(self, x, y, direction):
        self.image = fireball_image if direction == "right" else fireball_image_flipped
        self.pos = pygame.Vector2(x, y)
        self.direction = direction
        self.speed = 500

    def update(self, dt):
        if self.direction == "right":
            self.pos.x += self.speed * dt
        else:
            self.pos.x -= self.speed * dt

    def draw(self, screen):
        screen.blit(self.image, self.pos)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Shoots fireball upon Left Mouse Button Click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                new_fireball = Fireball(player_pos.x + 100, player_pos.y + 75, player_direction)  # Adjust positions as needed
                fireballs.append(new_fireball)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # Determine which sprite to draw based on player direction
    if player_direction == 'left':
        screen.blit(player, player_pos)
    else:
        screen.blit(player_flipped, player_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
        player_direction = 'left'
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
        player_direction = 'right'

    # Update and draw fireballs
    for fireball in fireballs:
        fireball.update(dt)
        fireball.draw(screen)

    # Remove fireballs that have moved off-screen
    fireballs = [fireball for fireball in fireballs if fireball.pos.x < screen.get_width() and fireball.pos.x > 0]

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
