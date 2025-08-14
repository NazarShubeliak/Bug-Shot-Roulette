import pygame
import sys

# Ініціалізація Pygame
pygame.init()

# Отримуємо роздільну здатність екрану
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# Налаштовуємо вікно на весь екран
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Встановлюємо назву вікна
pygame.display.set_caption("Bug Shot Roulette (Parody)")

# Завантажуємо фон
background = pygame.image.load("./img/bg.png")  # Переконайся, що шлях до файлу правильний

# Масштабуємо фон під роздільну здатність екрану
background = pygame.transform.scale(background, (screen_width, screen_height))

# Головний ігровий цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    
    # Малюємо фон
    screen.blit(background, (0, 0))

    # Оновлюємо екран
    pygame.display.update()

# Завершуємо роботу Pygame
pygame.quit()
sys.exit()

