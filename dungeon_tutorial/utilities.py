import pygame
from pathlib import Path
import constants as const

# Helper function to scale images
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w  * scale, h * scale))

# Define a function to load character images
def load_character_animations():
    character_animations = []
    character_types = ['player', 'ghost']
    animation_types = ['idle', 'run', 'shoot']

    for character in character_types:
        # Load images for each character into an animation list
        animation_list = []
        for animation in animation_types:
            try:
                img_list = []
                file_path = Path(f"{const.IMAGE_FILEPATH}{character}/{animation}")
                for img_file in file_path.glob("*.png"):
                    img = pygame.image.load(str(img_file)).convert_alpha()
                    img = scale_img(img, const.SCALE)
                    img_list.append(img)
                animation_list.append(img_list)
            except FileNotFoundError as e:
                print(f"Error: {e}")
                continue
            except pygame.error as e:
                print(f"Pygame error: {e}")
                continue
        character_animations.append(animation_list)
    return character_animations

# Define a keyboard event handler
def handle_keyboard_event(event, movement_flags, state):
    if event.key == pygame.K_w:
        movement_flags["up"] = state
    elif event.key == pygame.K_s:
        movement_flags["down"] = state
    elif event.key == pygame.K_a:
        movement_flags["left"] = state
    elif event.key == pygame.K_d:
        movement_flags["right"] = state