import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("❤️ Petualangan Cinta Lukman & Salawa ❤️")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)

# Load Aset
bg_default = pygame.image.load("assets/images/bg1.jpg")
bg_love = pygame.image.load("assets/images/bg2.jpg")
bg = bg_default

h1_img = pygame.transform.scale(pygame.image.load("assets/images/h1.png"), (60, 80))
h2_img = pygame.transform.scale(pygame.image.load("assets/images/h2.png"), (50, 70))

monster_paths = [
    "assets/images/monster.png",
    "assets/images/monster1.png",
    "assets/images/monster2.png",
    "assets/images/orc.png",
    "assets/images/monster3.png"
]
monster_imgs = [pygame.transform.scale(pygame.image.load(p), (60, 60)) for p in monster_paths]

heart_img = pygame.transform.scale(pygame.image.load("assets/images/heart.png"), (30, 30))

# Musik
try:
    pygame.mixer.music.load("assets/sounds/romantis.mp3")
    pygame.mixer.music.play(-1)
except:
    print("⚠️ Musik gagal dimuat.")

# Karakter
h1 = pygame.Rect(100, 500, 60, 80)
h2 = pygame.Rect(-100, 500, 50, 70)

# Game elements
monsters, monster_moves = [], []
hearts, bullets = [], []

monster_names = ["Ego", "Curiga", "Ekonomi", "Cemburu", "Takut", "Bosan"]
monster_index, spawn_counter = 0, 0

h1_vel_y = 0
is_jumping = False
health = 3

font = pygame.font.SysFont("comicsansms", 20)
big_font = pygame.font.SysFont("comicsansms", 36)

story_texts = [
    "Dunia penuh rintangan...",
    "Namun cinta Lukman untuk Salawa tak goyah!",
    "Kini, dia harus menyelamatkan sang putri...",
    "Meski Ego, Cemburu, dan Curiga menghadang...",
]
current_story, story_timer = 0, pygame.time.get_ticks()
salawa_muncul = False
ending = False

# Dialog & cutscene
dialogues = [
    "Salawa: Aku percaya kamu akan datang...",
    "Lukman: Aku lewati rintangan demi kamu.",
    "Salawa: Maaf ya, aku sempat ragu...",
    "Lukman: Sekarang aku akan terus jaga kamu ❤️"
]
dialogue_index, dialogue_timer = 0, 0
cutscene = False
walk_together = False
hearts_floating = []
hearts_rain = []

# Gambar & Teks
def draw():
    screen.blit(bg, (0, 0))
    screen.blit(h1_img, h1)
    screen.blit(font.render("Lukman", True, WHITE), (h1.x, h1.y - 20))
    if salawa_muncul:
        screen.blit(h2_img, h2)
        screen.blit(font.render("Salawa", True, WHITE), (h2.x, h2.y - 20))
    for i, m in enumerate(monsters):
        screen.blit(monster_imgs[i % len(monster_imgs)], m)
        screen.blit(font.render(monster_names[i % len(monster_names)], True, RED), (m.x, m.y - 20))
    for h in hearts:
        screen.blit(heart_img, h)
    for b in bullets:
        pygame.draw.rect(screen, RED, b)
    for hf in hearts_floating:
        pygame.draw.circle(screen, PINK, (hf[0], hf[1]), 6)
    for hr in hearts_rain:
        pygame.draw.circle(screen, (255, 105, 180), (hr[0], hr[1]), 4)
    screen.blit(font.render(f"❤️ Nyawa: {health}", True, RED), (10, 10))
    if current_story < len(story_texts):
        text = big_font.render(story_texts[current_story], True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 50))
    pygame.display.flip()

running = True
while running:
    screen.fill((0, 0, 0))
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if ending:
        bg = bg_love
        if cutscene:
            if dialogue_index < len(dialogues) and pygame.time.get_ticks() - dialogue_timer > 4000:
                screen.fill((0, 0, 0))
                text = font.render(dialogues[dialogue_index], True, WHITE)
                screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
                pygame.display.flip()
                dialogue_index += 1
                dialogue_timer = pygame.time.get_ticks()
            elif dialogue_index >= len(dialogues):
                walk_together = True
                cutscene = False
        elif walk_together:
            if h1.x < WIDTH:
                h1.x += 2
                h2.x = h1.x + 10
                hearts_floating.append([h1.x + 30, h1.y - 10])
                if random.random() < 0.3:
                    hearts_rain.append([random.randint(0, WIDTH), 0])
            else:
                screen.fill((0, 0, 0))
                text = big_font.render("💞 Cinta sejati tak bisa dipenjara 💞", True, WHITE)
                screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
                pygame.display.flip()
                pygame.time.wait(6000)
                running = False
        for hf in hearts_floating[:]:
            hf[1] -= 1
            if hf[1] < 0:
                hearts_floating.remove(hf)
        for hr in hearts_rain[:]:
            hr[1] += 3
            if hr[1] > HEIGHT:
                hearts_rain.remove(hr)
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and h1.x > 0:
        h1.x -= 5
    if keys[pygame.K_RIGHT] and h1.x < WIDTH - h1.width:
        h1.x += 5
    if keys[pygame.K_SPACE] and len(bullets) < 5:
        bullets.append(pygame.Rect(h1.centerx, h1.y + 20, 10, 5))
    if keys[pygame.K_UP] and not is_jumping:
        h1_vel_y = -20
        is_jumping = True

    h1.y += h1_vel_y
    h1_vel_y += 1
    if h1.y >= 500:
        h1.y = 500
        is_jumping = False

    for b in bullets[:]:
        b.x += 10
        if b.x > WIDTH:
            bullets.remove(b)
        for i, m in enumerate(monsters):
            if b.colliderect(m):
                bullets.remove(b)
                monsters.remove(m)
                monster_moves.pop(i)
                break

    if spawn_counter >= 60 and monster_index < len(monster_names):
        m = pygame.Rect(WIDTH, 500, 60, 60)
        monsters.append(m)
        monster_moves.append(random.choice([-1, 1]))
        monster_index += 1
        spawn_counter = 0
    else:
        spawn_counter += 1

    for i, m in enumerate(monsters[:] ):
        m.x -= 2
        m.y += monster_moves[i]
        if m.y <= 450 or m.y >= 520:
            monster_moves[i] *= -1
        if m.colliderect(h1):
            health -= 1
            monsters.remove(m)
            monster_moves.pop(i)

    if random.randint(0, 100) < 2:
        hearts.append(pygame.Rect(random.randint(100, 700), 500, 30, 30))
    for h in hearts[:]:
        if h1.colliderect(h):
            health += 1
            hearts.remove(h)

    if current_story < len(story_texts) and pygame.time.get_ticks() - story_timer > 4000:
        current_story += 1
        story_timer = pygame.time.get_ticks()

    if health <= 0:
        screen.fill((0, 0, 0))
        text = big_font.render("😭 Lukman gagal menyelamatkan Salawa!", True, RED)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(4000)
        break

    if monster_index == len(monster_names) and len(monsters) == 0:
        if not salawa_muncul:
            salawa_muncul = True
            h2.x = h1.x + 60
        elif h2.x > h1.x + 10:
            h2.x -= 2
        else:
            ending = True
            cutscene = True
            dialogue_timer = pygame.time.get_ticks()

    clock.tick(60)

pygame.quit()
sys.exit()
