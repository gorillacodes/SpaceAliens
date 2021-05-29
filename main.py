import pygame
import random
from pygame.constants import K_RETURN
pygame.font.init()

WIDTH, HEIGHT = 650, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Aliens By Talha")

RED_SPACE_SHIP = pygame.image.load("assets/pixel_ship_red_small.png")
GREEN_SPACE_SHIP = pygame.image.load("assets/pixel_ship_green_small.png")
BLUE_SPACE_SHIP = pygame.image.load("assets/pixel_ship_blue_small.png")

YELLOW_SPACE_SHIP = pygame.image.load("assets/pixel_ship_yellow.png")

RED_LASER = pygame.image.load("assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("assets/pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load("assets/pixel_laser_yellow.png")

BG = pygame.transform.scale(pygame.image.load(
    "assets/background-black.png"), (WIDTH, HEIGHT))

HS = open("Scores of Space Aliens.txt", "a+")


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100, score=0):
        self.x = x
        self.y = y
        self.health = health
        self.score = score
        self.ship_img = None
        self.bullet_img = None
        self.bullets = []
        self.cooldown_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

    def move_bullets(self, vel, obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)

    def shoot(self):
        if self.cooldown_counter == 0:
            bullet = Bullet(self.x, self.y, self.laser_img)
            self.bullets.append(bullet)
            self.cooldown_counter = 1

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def move_bullets(self, vel, objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        self.score += 10
                        objs.remove(obj)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                               self.ship_img.get_height()+10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height()+10,
                                               self.ship_img.get_width() * (self.health/self.max_health), 10))


class Alien(Ship):

    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),

    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cooldown_counter == 0:
            bullet = Bullet(self.x-20, self.y, self.laser_img)
            self.bullets.append(bullet)
            self.cooldown_counter = 1


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 60)
    score_font = pygame.font.SysFont("comicsans", 27)

    level = 0
    lives = 5

    enemies = []
    n_enemies = 5
    enemy_vel = 1

    bullet_vel = 5

    player = Player(300, 530)
    player_vel = 5

    lost = False
    lost_count = 0

    HS.seek(0)
    data = HS.readlines()
    newdata = []
    for score in data:
        s = score.rstrip("\n")
        i = int(s)
        newdata.append(i)
    hs = max(newdata)

    def redraw_window():
        WIN.blit(BG, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        score_label = score_font.render(
            f"Score: {player.score}", 1, (255, 255, 255))
        highscore_label = score_font.render(
            f"High Score: {hs}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (WIDTH - score_label.get_width() -
                               10, level_label.get_height() + 10))
        WIN.blit(highscore_label, (10, lives_label.get_height() + 10))

        if lost:
            lost_label = lost_font.render(
                "You're a loser LMAO!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2,
                                  HEIGHT/2 - lost_label.get_height()/2))

        player.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                HS.write(str(player.score)+"\n")
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            n_enemies += 1
            for i in range(n_enemies):
                enemy = Alien(random.randrange(
                    25, WIDTH-100), random.randrange(-1300, -100), random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x + player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x - player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y + player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y - player_vel + player.get_height()+25 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_bullets(bullet_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_bullets(-bullet_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render(
            "Summoner, Press ENTER to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width() /
                               2, HEIGHT/2 - title_label.get_height()/2))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                main()
            if event.type == pygame.QUIT:
                run = False
    HS.close()
    pygame.quit()


main_menu()
