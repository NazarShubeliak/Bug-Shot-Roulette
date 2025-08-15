import pygame
import sys
import random

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

# --------------------
# ДОДАНО: Початок ігрової логіки
# --------------------

# Класи та функції гри (скопійовано та адаптовано)

class Shotgun:
    def __init__(self):
        self.damage = 1
        self.rounds = []

    def doubleDamage(self):
        self.damage = 2

    def resetDamage(self):
        self.damage = 1

    def addRounds(self, live=0, blank=0):
        self.rounds = [True]*live + [False]*blank
        random.shuffle(self.rounds)

    def pickRound(self):
        if not self.rounds:
            return None
        return self.rounds.pop()

class Player:
    def __init__(self, name, health=4):
        self.name = name
        self.health = health
        self.items = []
        self.turnsWaiting = 0

    def takeDamage(self, dmg):
        self.health -= dmg
        return self.health <= 0

    def addHealth(self, h=1):
        self.health = min(self.health + h, 5)

    def useItem(self, item, shotgun, enemy):
        if item not in self.items:
            return "Немає такого предмета"
        self.items.remove(item)
        if item == "🚬":
            self.addHealth(1)
            return "Викурено сигарету. +1 HP"
        elif item == "🍺":
            if shotgun.rounds:
                shotgun.rounds.pop()
                return "Відкинуто 1 набій"
            return "Немає набоїв"
        elif item == "🔪":
            shotgun.doubleDamage()
            return "Подвоєно шкоду!"
        elif item == "🔍":
            if not shotgun.rounds:
                return "Немає набоїв"
            return "Наступний набій: БОЙОВИЙ" if shotgun.rounds[-1] else "Наступний набій: ХОЛОСТИЙ"
        elif item == "⛓":
            enemy.turnsWaiting = 1
            return f"{enemy.name} зв'язаний і пропускає хід"
        elif item == "📱":
            enemy.turnsWaiting = 1
            return f"{enemy.name} пропускає хід через дзвінок"
        elif item == "🔧":
            if shotgun.rounds:
                shotgun.rounds[-1] = not shotgun.rounds[-1]
                new_type = "БОЙОВИЙ" if shotgun.rounds[-1] else "ХОЛОСТИЙ"
                return f"Наступний патрон тепер {new_type}"
            else:
                return "Немає патронів для конвертора"
        return "Нічого не відбулося"

# Ініціалізація гравців та дробовика
player = Player("Гравець")
dealer = Player("Дилер")
player.items = ["🚬", "🍺", "🔍", "📱", "🔧"]
dealer.items = ["🔪", "⛓"]
shotgun = Shotgun()
shotgun.addRounds(2, 4)

message = "Вітаємо в грі!"
turn = "player"

# Кнопки для дій гравця
class Button:
    def __init__(self, text, x, y, w=150, h=60):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, (200, 0, 0), self.rect)
        font = pygame.font.SysFont('consolas', 30)
        txt = font.render(self.text, True, (255, 255, 255))
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

spin_btn = Button("ЗАРЯДИТИ", 50, screen_height - 100)
shoot_btn = Button("СТРІЛЯТИ", 250, screen_height - 100)
radio_btn = Button("🎵 РАДІО", 450, screen_height - 100)

# Кнопки для предметів гравця (створюватимемо динамічно)
item_buttons = []

def update_item_buttons():
    item_buttons.clear()
    x = 650
    y = screen_height - 100
    for item in player.items:
        btn = Button(item, x, y, 50, 50)
        item_buttons.append(btn)
        x += 60

update_item_buttons()

def reset_game():
    global player, dealer, shotgun, turn, message
    player = Player("Гравець")
    dealer = Player("Дилер")
    player.items = ["🚬", "🍺", "🔍", "📱", "🔧"]
    dealer.items = ["🔪", "⛓"]
    shotgun = Shotgun()
    shotgun.addRounds(2, 4)
    turn = "player"
    message = "Гра почалась! Ваш хід."
    update_item_buttons()

def shoot():
    global message, turn
    bullet = shotgun.pickRound()
    if bullet is None:
        message = "Немає набоїв! Натисніть ЗАРЯДИТИ."
        return

    if turn == "player":
        if bullet:
            dead = dealer.takeDamage(shotgun.damage)
            message = "Ви влучили в ДИЛЕРА!"
            if dead:
                message = "ВИ ПЕРЕМОГЛИ!"
        else:
            message = "Ви промахнулись. Хід Дилера."
            turn = "dealer"
    elif turn == "dealer":
        if dealer.turnsWaiting:
            dealer.turnsWaiting -= 1
            message = "Дилер пропускає хід!"
            turn = "player"
            return
        if bullet:
            dead = player.takeDamage(shotgun.damage)
            message = "Дилер влучив у ВАС!"
            if dead:
                message = "ВИ ПОМЕРЛИ!"
        else:
            message = "Дилер промахнувся. Ваш хід."
            turn = "player"
    shotgun.resetDamage()

def spin():
    shotgun.addRounds(2, 4)
    global message
    message = "Заряджено!"

# --------------------
# ДОДАНО: Кінець ігрової логіки
# --------------------

# Змінна, що визначає чи гра запущена
game_started = False

# Головний ігровий цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обробка кліків миші
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Ліва кнопка миші
            mouse_x, mouse_y = event.pos

            if not game_started:
                # Меню: перевірка кнопок
                if play_button_rect.collidepoint(mouse_x, mouse_y) and show_buttons:
                    # Стартуємо гру
                    background = pygame.image.load("./img/bg_game.png")  # Завантажуємо новий фон
                    background = pygame.transform.scale(background, (screen_width, screen_height))
                    show_dictator = True
                    show_buttons = False
                    game_started = True
                    reset_game()

                elif options_button_rect.collidepoint(mouse_x, mouse_y) and show_buttons:
                    print("Options button clicked!")
                    # Тут можна додати опції

                elif exit_button_rect.collidepoint(mouse_x, mouse_y) and show_buttons:
                    running = False
            else:
                # Якщо гра запущена — обробляємо кнопки дій
                if spin_btn.is_clicked((mouse_x, mouse_y)):
                    spin()
                elif shoot_btn.is_clicked((mouse_x, mouse_y)):
                    shoot()
                elif radio_btn.is_clicked((mouse_x, mouse_y)):
                    # Можна додати музику, поки просто повідомлення
                    message = "Радіо переключено"
                else:
                    # Клік по предметах гравця
                    for btn in item_buttons:
                        if btn.is_clicked((mouse_x, mouse_y)):
                            result = player.useItem(btn.text, shotgun, dealer)
                            message = result
                            update_item_buttons()
                            break

    # Отримуємо поточні координати миші
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Зміна курсора
    if (play_button_rect.collidepoint(mouse_x, mouse_y) or
        options_button_rect.collidepoint(mouse_x, mouse_y) or
        exit_button_rect.collidepoint(mouse_x, mouse_y)) and show_buttons:
        pygame.mouse.set_cursor(*hand_cursor)  # Змінюємо курсор на руку
    else:
        pygame.mouse.set_cursor(*default_cursor)  # Повертаємо стандартний курсор

    # Додамо анімацію для кнопок (тільки в меню)
    play_button_offset = 0
    options_button_offset = 0
    exit_button_offset = 0

    if not game_started:
        if play_button_rect.collidepoint(mouse_x, mouse_y):
            play_button_offset = 10
        if options_button_rect.collidepoint(mouse_x, mouse_y):
            options_button_offset = 10
        if exit_button_rect.collidepoint(mouse_x, mouse_y):
            exit_button_offset = 10

    # Малюємо фон
    screen.blit(background, (0, 0))

    # Малюємо кнопки меню, якщо вони показані
    if show_buttons:
        screen.blit(play_button, play_button_rect.move(0, play_button_offset))
        screen.blit(options_button, options_button_rect.move(0, options_button_offset))
        screen.blit(exit_button, exit_button_rect.move(0, exit_button_offset))

    # Малюємо диктора, якщо потрібно
    if show_dictator:
        screen.blit(dictator_image, dictator_rect)

    # Якщо гра запущена — малюємо UI гри
    if game_started:
        # Малюємо кнопки дій
        spin_btn.draw()
        shoot_btn.draw()
        radio_btn.draw()

        # Малюємо здоров'я гравця і дилера
        font = pygame.font.SysFont('consolas', 40)
        player_health_text = font.render(f"Гравець HP: {player.health}", True, (255, 255, 255))
        dealer_health_text = font.render(f"Дилер HP: {dealer.health}", True, (255, 255, 255))
        screen.blit(player_health_text, (50, 50))
        screen.blit(dealer_health_text, (50, 100))

        # Малюємо повідомлення
        msg_font = pygame.font.SysFont('consolas', 30)
        msg_surface = msg_font.render(message, True, (255, 255, 0))
        screen.blit(msg_surface, (50, 150))

        # Малюємо кнопки предметів гравця
        for btn in item_buttons:
            btn.draw()

    # Оновлюємо екран
    pygame.display.update()

# Завершуємо роботу Pygame
pygame.quit()
sys.exit()

