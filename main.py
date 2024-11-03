import pygame
import random
import sys

# Ініціалізація Pygame
pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Налаштування гравця
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Налаштування ворога
enemy_size = 50
enemy_speed = 3
enemy_list = []

# Налаштування снаряда
bullet_size = 5
bullet_speed = 10
bullets = []
bullet_cooldown = 500  # Затримка між пострілами (в мілісекундах)
last_bullet_time = 0

# Лічильник знищених ворогів
score = 0
font = pygame.font.Font(None, 36)

# Функція для початку нової гри
def reset_game():
    global player_x, player_y, enemy_list, bullets, score, enemy_speed, last_bullet_time
    player_x = WIDTH // 2
    player_y = HEIGHT - player_size - 10
    enemy_list = []
    bullets = []
    score = 0
    enemy_speed = 3  # Початкова швидкість ворогів
    last_bullet_time = 0  # Останній час пострілу

# Основні функції
def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_size)
    y = -enemy_size
    enemy_list.append([x, y])

def draw_enemies():
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

def update_enemies():
    for enemy in enemy_list:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemy_list.remove(enemy)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_size, bullet_size))

def update_bullets():
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

def detect_collisions():
    global score, enemy_speed
    for enemy in enemy_list:
        for bullet in bullets:
            if (enemy[0] < bullet[0] < enemy[0] + enemy_size and
                enemy[1] < bullet[1] < enemy[1] + enemy_size):
                bullets.remove(bullet)
                enemy_list.remove(enemy)
                score += 1  # Оновлюємо лічильник
                # Збільшуємо швидкість ворогів щоразу після 5 знищених
                if score % 5 == 0:
                    enemy_speed += 1
                break

def detect_player_collision():
    for enemy in enemy_list:
        if (enemy[0] < player_x < enemy[0] + enemy_size or
            enemy[0] < player_x + player_size < enemy[0] + enemy_size):
            if (enemy[1] < player_y < enemy[1] + player_size or
                enemy[1] < player_y + player_size < enemy[1] + player_size):
                return True
    return False

def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def display_game_over():
    game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(final_score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 40))

# Головний цикл гри
running = True
game_over = False
clock = pygame.time.Clock()

reset_game()

while running:
    screen.fill(BLACK)
    
    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Перевірка на натискання клавіші R для перезапуску гри
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_over = False
            reset_game()

    if not game_over:
        # Управління гравцем
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_bullet_time > bullet_cooldown:
                bullets.append([player_x + player_size // 2, player_y])
                last_bullet_time = current_time  # Оновлюємо час останнього пострілу

        # Спавн ворогів
        if random.randint(1, 30) == 1:
            spawn_enemy()

        # Оновлення положення ворогів і снарядів
        update_enemies()
        update_bullets()

        # Відображення ворогів, гравця та снарядів
        draw_enemies()
        draw_bullets()
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

        # Перевірка зіткнень
        detect_collisions()

        # Перевірка зіткнення з гравцем
        if detect_player_collision():
            game_over = True

        # Відображення рахунку
        display_score()
    else:
        # Відображення повідомлення про програш
        display_game_over()

    pygame.display.flip()
    clock.tick(30)

# Завершення гри
pygame.quit()
sys.exit()