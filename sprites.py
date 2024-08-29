import pygame


# Создание класса спрайтов для птички
class BirdSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale_size):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, scale_size)
        self.rect = self.image.get_rect()

    def update_position(self, x, y):
        self.rect.center = (x, y)

class PipeSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, is_top_pipe=False):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5  # Скорость движения труб
        self.is_top_pipe = is_top_pipe

        if self.is_top_pipe:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()