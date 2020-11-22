import pygame
from numpy import cos


class GameObject:

    def __init__(self, image_path, x, y, width, height, sound_path=None):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))  # scale the image

        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        self.x_pos = x
        self.y_pos = y

        self.exists = 1
        self.width = width
        self.height = height
        self.index = 0

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

    def detect_collision(self, other_body) -> bool:
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        if self.x_pos + self.width < other_body.x_pos:
            return False
        elif self.x_pos > other_body.x_pos + other_body.width:
            return False

        return True


class PlayerCharacter(GameObject):
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, x_direction, y_direction, max_width, max_height):
        # X axis movement
        if x_direction > 0:
            self.x_pos += self.SPEED
        elif x_direction < 0:
            self.x_pos -= self.SPEED

        # Y axis movement
        if y_direction > 0:
            self.y_pos -= self.SPEED
        elif y_direction < 0:
            self.y_pos += self.SPEED

        # X movement limitations
        if self.x_pos >= max_width - 145:
            self.x_pos = max_width - 145
        elif self.x_pos <= 95:
            self.x_pos = 95

        # Y movement limitations
        if self.y_pos >= max_height - 70:
            self.y_pos = max_height - 70
        elif self.y_pos <= 20:
            self.y_pos = 20


class NonPlayerCharacter(GameObject):
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
        self.base_movement_line = y

    def move(self, max_width): # Straight Line Movement
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 70:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

    def alt_move(self, max_width): # Sinusoidal Movement
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 70:
            self.SPEED = -abs(self.SPEED)

        self.x_pos += self.SPEED
        self.y_pos = self.base_movement_line + self.SPEED*cos(0.04*abs(self.x_pos))

