import pygame
import constants as const
from utilities import scale_img, load_character_animations, handle_keyboard_event
from character import Character
from weapon import Weapon

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
pygame.display.set_caption(const.GAME_TITLE)
# Create clock for maintaining frame rate
clock = pygame.time.Clock()
# Load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png"),const.SCALE).convert_alpha()
# Load character animations
character_animations = load_character_animations()
# Create the player character
player = Character(100, 100, 0, character_animations)
# Create player's weapon
bow = Weapon(bow_image)

# Define player movement variables
movement_flags = {
    "up": False,
    "down": False,
    "left": False,
    "right": False
}

# Main game loop
running = True
while running:

    # Limit the frame rate
    clock.tick(const.FPS)

    # Fill screen with background color
    screen.fill(const.BG)

    # Calculate player movement
    dx, dy = 0, 0
    if movement_flags["up"]:
        dy -= const.PLAYER_SPEED
    if movement_flags["down"]:
        dy += const.PLAYER_SPEED
    if movement_flags["left"]:
        dx -= const.PLAYER_SPEED
    if movement_flags["right"]:
        dx += const.PLAYER_SPEED

    # Move player
    player.move(dx, dy)
    # Update player
    player.update()
    bow.update(player)
    # Draw player character on screen
    player.draw(screen)
    bow.draw(screen)

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_keyboard_event(event, movement_flags, True)
        elif event.type == pygame.KEYUP:
            handle_keyboard_event(event, movement_flags, False)

    # Update Display
    pygame.display.update()

pygame.quit()