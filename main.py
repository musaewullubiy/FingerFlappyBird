import cv2
import numpy as np
import mediapipe as mp
import random

import pygame
from sprites import PipeSprite, BirdSprite

WINDOW_SIZE = (800, 400)


def run_game(cap, hands):
    all_sprites = pygame.sprite.Group()
    pipes = pygame.sprite.Group()

    pipe_spawn_time = 3000
    pygame.time.set_timer(pygame.USEREVENT, pipe_spawn_time)

    bird_sprite = BirdSprite('img/bird.png', (50, 50))
    all_sprites.add(bird_sprite)

    clock = pygame.time.Clock()
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT and not game_over:
                gap_size = 150
                pipe_y_position = random.randint(50, WINDOW_SIZE[1] - gap_size - 50)

                top_pipe = PipeSprite('img/pipe.png', WINDOW_SIZE[0], pipe_y_position, is_top_pipe=True)
                all_sprites.add(top_pipe)
                pipes.add(top_pipe)

                bottom_pipe = PipeSprite('img/pipe.png', WINDOW_SIZE[0], pipe_y_position + gap_size)
                all_sprites.add(bottom_pipe)
                pipes.add(bottom_pipe)

        # Чтение кадра из камеры
        ret, frame = cap.read()
        if not ret:
            continue

        # Преобразование изображения в RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Обработка изображения с использованием MediaPipe
        results = hands.process(image_rgb)

        # Преобразование изображения для Pygame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = np.rot90(frame_rgb)  # Поворот изображения на 90 градусов
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        frame_surface = pygame.transform.flip(frame_surface, True, False)  # Перевернуть по горизонтали

        screen.fill((0, 0, 0))
        screen.blit(frame_surface, (0, 0))

        if results.multi_hand_landmarks and not game_over:
            for landmarks in results.multi_hand_landmarks:
                # Получение координат последней фаланги указательного пальца
                index_finger_tip = landmarks.landmark[8]  # Индекс 8 соответствует последней фаланге указательного пальца

                # Преобразование координат из нормализованных в пиксели
                x = int(index_finger_tip.x * WINDOW_SIZE[0])
                y = int(index_finger_tip.y * WINDOW_SIZE[1])

                # Обновление позиции птички
                bird_sprite.update_position(50, y)

        if not game_over:
            all_sprites.update()

            # Проверка столкновений птички с трубами
            if pygame.sprite.spritecollideany(bird_sprite, pipes):
                game_over = True

        all_sprites.draw(screen)

        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Finger Flappy Bird')

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_SIZE[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_SIZE[1])
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)

    run_game(cap, hands)

    cap.release()
    pygame.quit()
