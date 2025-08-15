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

# Завантажуємо початковий фон і кнопки
background = pygame.image.load("./img/bg.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Завантаження кнопок
play_button = pygame.image.load("./img/start_button.png")
options_button = pygame.image.load("./img/options_button.png")
exit_button = pygame.image.load("./img/exit_button.png")

# Масштабуємо кнопки під нові розміри (в два рази більші)
button_width, button_height = 300, 100  # Тепер кнопки в два рази більші
play_button = pygame.transform.scale(play_button, (button_width, button_height))
options_button = pygame.transform.scale(options_button, (button_width, button_height))
exit_button = pygame.transform.scale(exit_button, (button_width, button_height))

# Встановлюємо позиції кнопок
play_button_rect = play_button.get_rect(center=(screen_width // 2, screen_height // 3))
options_button_rect = options_button.get_rect(center=(screen_width // 2, screen_height // 2))
exit_button_rect = exit_button.get_rect(center=(screen_width // 2, screen_height * 2 // 3))

# Завантаження картинки диктора
dictator_image = pygame.image.load("./img/dictator.png")
dictator_image = pygame.transform.scale(dictator_image, (900, 524))  # Масштабуємо картинку диктора
dictator_rect = dictator_image.get_rect(center=(screen_width // 2, 570))  # Центруємо картинку

# Змінний курсор
default_cursor = pygame.cursors.arrow
hand_cursor = pygame.cursors.diamond

# Змінна для відображення диктора
show_dictator = False
show_buttons = True  # Флаг для відображення кнопок

# Головний ігровий цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обробка кліків миші
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Ліва кнопка миші
            mouse_x, mouse_y = event.pos

            # Перевіряємо, чи натиснута кнопка Play
            if play_button_rect.collidepoint(mouse_x, mouse_y) and show_buttons:
                print("Play button clicked!")
                # Зміна фону та показ диктора
                background = pygame.image.load("./img/bg_game.png")  # Завантажуємо новий фон
                background = pygame.transform.scale(background, (screen_width, screen_height))
                show_dictator = True  # Показуємо диктора
                show_buttons = False  # Ховаємо кнопки

            # Перевіряємо, чи натиснута кнопка Options
            elif options_button_rect.collidepoint(mouse_x, mouse_y) and show_buttons:
                print("Options button clicked!")
                # Код для відкриття налаштувань гри
            # Перевіряємо, чи натиснута кнопка Exit
            elif exit_button_rect.collidepoint(mouse_x, mouse_y) and show_buttons:
                print("Exit button clicked!")
                running = False

    # Отримуємо поточні координати миші
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Зміна курсора
    if (play_button_rect.collidepoint(mouse_x, mouse_y) or
        options_button_rect.collidepoint(mouse_x, mouse_y) or
        exit_button_rect.collidepoint(mouse_x, mouse_y)) and show_buttons:
        pygame.mouse.set_cursor(*hand_cursor)  # Змінюємо курсор на руку
    else:
        pygame.mouse.set_cursor(*default_cursor)  # Повертаємо стандартний курсор

    # Додамо анімацію для кнопок
    play_button_offset = 0
    options_button_offset = 0
    exit_button_offset = 0

    # Перевіряємо, чи курсор на кнопці Play
    if play_button_rect.collidepoint(mouse_x, mouse_y):
        play_button_offset = 10  # Опускаємо на 10 пікселів

    # Перевіряємо, чи курсор на кнопці Options
    if options_button_rect.collidepoint(mouse_x, mouse_y):
        options_button_offset = 10  # Опускаємо на 10 пікселів

    # Перевіряємо, чи курсор на кнопці Exit
    if exit_button_rect.collidepoint(mouse_x, mouse_y):
        exit_button_offset = 10  # Опускаємо на 10 пікселів

    # Малюємо фон
    screen.blit(background, (0, 0))

    # Малюємо кнопки на екрані з анімацією, якщо кнопки ще не приховані
    if show_buttons:
        screen.blit(play_button, play_button_rect.move(0, play_button_offset))
        screen.blit(options_button, options_button_rect.move(0, options_button_offset))
        screen.blit(exit_button, exit_button_rect.move(0, exit_button_offset))

    # Якщо потрібно, малюємо картинку диктора
    if show_dictator:
        screen.blit(dictator_image, dictator_rect)

    # Оновлюємо екран
    pygame.display.update()

# Завершуємо роботу Pygame
pygame.quit()
sys.exit()

