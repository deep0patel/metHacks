import time
import pygame
import random
from pygame import mixer

pygame.init()

# Set up the display
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ECOsort")
# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
key = 0
high_score = 0
# Set up the fonts
FONT_SMALL = pygame.font.Font(None, 24)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_LARGE = pygame.font.Font(None, 48)
lockscreen = pygame.image.load('lockscreen.png')

# Sound effect
intake_sound = mixer.Sound("sound/intake.wav")


TRASH_TYPES = ["blue", "black", "green"]

TRASH_IMAGES = {
    "blue": [pygame.image.load("park/plastic.png"), pygame.image.load("park/juice_box.png"),
             pygame.image.load("park/magazine.png"),
             pygame.image.load("park/newspaper.png")],
    "black": [pygame.image.load("park/paper_nap.png")],
    "green": [pygame.image.load("park/paper_nap.png"), pygame.image.load("park/broken_rose.png")
        , pygame.image.load("park/banana_Peel.png"), pygame.image.load("park/animal_waste.png"),
              pygame.image.load("park/apple.png"), ]
}


def scale_image(img, factor):
    new_size = (int(img.get_width() * factor), int(img.get_height() * factor))
    return pygame.transform.scale(img, new_size)


# Set up trash object
class Trash:
    def __init__(self):
        self.trash_type = random.choice(TRASH_TYPES)
        self.image_list = TRASH_IMAGES[self.trash_type]
        self.image = scale_image(random.choice(self.image_list), 0.1)
        self.width, self.height = self.image.get_size()
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(-SCREEN_HEIGHT, -self.height)

    def intersects(self, bin_rect):
        return bin_rect.colliderect(pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()))

    def in_bin(self, bin_rect):
        if self.trash_type == "blue" and bin_rect == BINS[0]:
            return True
        elif self.trash_type == "black" and bin_rect == BINS[1]:
            return True
        elif self.trash_type == "green" and bin_rect == BINS[2]:
            return True
        else:
            return False


green_bin = scale_image(pygame.image.load("green.png"), 0.65)
black_bin = scale_image(pygame.image.load("black.png"), 0.65)
blue_bin = scale_image(pygame.image.load("blue.png"), 0.65)

BIN_WIDTH = green_bin.get_width()
BIN_HEIGHT = green_bin.get_height()

GREEN_BIN_RECT = pygame.Rect(69, SCREEN_HEIGHT - BIN_HEIGHT, BIN_WIDTH, 50)
BLACK_BIN_RECT = pygame.Rect(469, SCREEN_HEIGHT - BIN_HEIGHT, BIN_WIDTH, 50)
BLUE_BIN_RECT = pygame.Rect(269, SCREEN_HEIGHT - BIN_HEIGHT, BIN_WIDTH, 50)

BOTTOM_RECT = pygame.Rect(0,SCREEN_HEIGHT,SCREEN_WIDTH,0)

BINS = [
    BLUE_BIN_RECT, BLACK_BIN_RECT, GREEN_BIN_RECT
]

# Defines general colours
SKY = (150, 240, 255)
GRASS = (126, 200, 80)
IVORY = (250, 250, 235)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the game clock
CLOCK = pygame.time.Clock()

# Set up the game variables
score = 0
done = False
game_over = False
image_created = False
chance = 3
start = 0
pause = False

# -------Title Screen-------
while not done and start == 0:

    # Tracks user events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User has quit the game.")
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = 1
                paused = 1
                # Gameplay music
                mixer.music.load('sound/game music.mp3')
                pygame.mixer.music.set_volume(1)
                mixer.music.play(-1)

    # Displays graphics
    SCREEN.fill((255, 255, 255))
    Welcome = FONT_MEDIUM.render(f'ENTER TO START ...', True, BLACK)
    SCREEN.blit(lockscreen, (
        SCREEN_WIDTH // 2 - lockscreen.get_width() // 2,
        SCREEN_HEIGHT // 2 - lockscreen.get_height() // 2))
    SCREEN.blit(Welcome, (
        SCREEN_WIDTH // 2 - Welcome.get_width() // 2,
        SCREEN_HEIGHT // 2 - Welcome.get_height() // 2 + lockscreen.get_height()))
    pygame.display.flip()
    CLOCK.tick(60)

# Game loop
while not game_over and chance > 0 and start == 1:

    if pause:
        pass
    # drawing basics
    SCREEN.fill(SKY)
    pygame.draw.rect(SCREEN, GRASS, (0, 490, 960, 50), 0)
    SCREEN.blit(green_bin, (69, 478))
    SCREEN.blit(blue_bin, (269, 478))
    SCREEN.blit(black_bin, (469, 478))

    if not image_created:
        trash = Trash()
        image = trash.image
        image_rect = image.get_rect()
        image_rect.x = random.randint(0, SCREEN_WIDTH - image.get_width())
        image_rect.y = 0
        image_created = True

    trashvelocityx = 0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User has quit the game.")
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = True
            if event.key == pygame.K_RETURN:
                pause = False
            if event.key == pygame.K_LEFT:  # Bin movement controls
                key = "Left"
            if event.key == pygame.K_RIGHT:
                key = "Right"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:  # Bin movement controls
                if key == "Left":
                    key = 0
            if event.key == pygame.K_RIGHT:
                if key == "Right":
                    key = 0

    # Bin movement ---
    if key == "Left":  # Adds velocity leftward, normal speed
        trashvelocityx += -3
        image_rect.move_ip(trashvelocityx, 0)
    if key == "Right":  # Adds velocity rightward, normal speed
        trashvelocityx += 3
        image_rect.move_ip(trashvelocityx, 0)

    if trashvelocityx > 6:  # Sets a cap on rightward velocity at 2.4 while succing
        trashvelocityx = 5
    if trashvelocityx < -6:  # Sets a cap on leftward velocity at 2.4 while succing
        trashvelocityx = -5

    # Move the object downwards
    image_rect.move_ip(0, 2)

    for bin_rect in [GREEN_BIN_RECT, BLACK_BIN_RECT, BLUE_BIN_RECT]:
        if image_rect.colliderect(bin_rect):
            # trash has collided with bin_rect, do something
            if trash.in_bin(bin_rect):
                score += 1
                intake_sound.play(0)
            else:
                intake_sound.play(0)
                chance -= 1
            image_created = False

    if image_rect.bottom >= SCREEN_HEIGHT:
        intake_sound.play(0)
        chance -= 1
        image_created = False

    SCREEN.blit(image, image_rect)

    # Draw the score
    score_text = FONT_MEDIUM.render(f'score: {score}', True, BLACK)
    SCREEN.blit(score_text, (10, 10))

    # High Score
    high_score_text = FONT_MEDIUM.render(f'High Score: {high_score}', True, BLACK)
    if high_score < score:
        high_score_text = FONT_MEDIUM.render(f'High Score: {high_score}', True, BLACK)
        high_score = score

    # Draw lives
    live_text = FONT_MEDIUM.render(f'lives: {chance}', True, BLACK)
    SCREEN.blit(live_text, (600, 10))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    CLOCK.tick(60)

    if chance <= 0:
        game_over = True

    if game_over:
        while game_over:
            # game_over = True
            game_over_text = FONT_LARGE.render('Game Over', True, BLACK)
            SCREEN.blit(game_over_text, (
                SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            score_text = FONT_MEDIUM.render(f'Final Score: {score}', True, BLACK)
            SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + game_over_text.get_height()))
            SCREEN.blit(high_score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + game_over_text.get_height() + score_text.get_height()))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Quit
                        game_over = True
                    elif event.key == pygame.K_RETURN:
                        game_over = False
                        chance = 3

        pygame.quit()

        # Update the display
        pygame.display.flip()
