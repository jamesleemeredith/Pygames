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

# Load Health Bar Images
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png"),const.UI_SCALE).convert_alpha()
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png"),const.UI_SCALE).convert_alpha()
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png"),const.UI_SCALE).convert_alpha()


# Load character animations
character_animations = load_character_animations()
# Load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png"),const.WEAPON_SCALE).convert_alpha()
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png"),const.WEAPON_SCALE).convert_alpha()

# Function for displaying game info:
def draw_ui():
    pygame.draw.rect(screen, const.PANEL, (0, 0, const.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, const.WHITE, (0,50), (const.SCREEN_WIDTH, 50))
    # draw lives
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20) > 0 and half_heart_drawn == False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))

# Define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)
# Damage Text Class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # Make damage text float up
        self.rect.y -= 1
        # delete the counter after a few seconds
        self.counter += 1
        if self.counter > 50:
            self.kill()


# Create the player character
player = Character(100, 100, 100, 'player', character_animations)
# Create player's weapon
bow = Weapon(bow_image, arrow_image)
# Create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
# Create enemy
enemy = Character(200, 300, 100, 'ghost', character_animations)
# Create enemy_list
enemy_list = []
enemy_list.append(enemy)

# Define player movement variables
movement_flags = {
    "up": False,
    "down": False,
    "left": False,
    "right": False
}

# Main game loop ###########################################
running = True
while running:

    # Limit the frame rate
    clock.tick(const.FPS)

    # Fill screen with background color
    screen.fill(const.BG)

    # Calculate player movement
    dx, dy = 0, 0
    if movement_flags["up"]:
        dy -= player.speed
    if movement_flags["down"]:
        dy += player.speed
    if movement_flags["left"]:
        dx -= player.speed
    if movement_flags["right"]:
        dx += player.speed

    # Move the player
    player.move(dx, dy)

    # Updates game objects
    for enemy in enemy_list:
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), const.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()

    # Draw game objects
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    draw_ui()

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_keyboard_event(event, movement_flags, True)
        elif event.type == pygame.KEYUP:
            handle_keyboard_event(event, movement_flags, False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.attack()

    # Update Display
    pygame.display.update()

pygame.quit()