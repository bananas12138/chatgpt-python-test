import pygame
import random
import sys
import os


sys.setrecursionlimit(10000)

# 初始化 Pygame
pygame.init()

# 设置游戏窗口大小和标题
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("原批入侵地球")

# 加载游戏资源
#background_image = pygame.image.load("b.jpg")
player_image = pygame.image.load("player.png")
alien_image = pygame.image.load("alien.png")
bullet_image = pygame.image.load("bullet.png")
#explosion_sound = pygame.mixer.Sound("bgm.mp3")
#pygame.mixer.music.load("bgm.mp3")
#pygame.mixer.music.play(-1)

# 设置游戏元素初始位置和速度
player_x = screen_width / 2
player_y = screen_height - player_image.get_height() - 10
player_speed = 20
alien_list = []
for i in range(10):
    alien_x = random.randint(0, screen_width - alien_image.get_width())
    alien_y = random.randint(-500, -50)
    alien_speed = random.randint(1, 3)
    alien_list.append([alien_x, alien_y, alien_speed])

bullet_list = []
bullet_speed = 7
fire_rate = 2  # 表示每秒可以射出的子弹数量
last_fire_time = pygame.time.get_ticks()  # 上一次射击的时间

# 设置游戏暂停状态的变量
paused = False

# 设置游戏循环
clock = pygame.time.Clock()  # 设置游戏帧率
score = 0  # 初始化得分
font = pygame.font.Font(None, 30)  # 设置字体和大小
game_over = False  # 游戏是否结束的标志
lives = 3  # 玩家生命数
invincible = False  # 玩家是否处于无敌状态
invincible_start_time = 0  # 无敌状态开始的时间戳
restart_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 50, 200, 50)  # 重新开始按钮
start_time = pygame.time.get_ticks()  # 游戏开始的时间戳
while not game_over:


    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_x += player_speed
            elif event.key == pygame.K_UP:
                player_y -= player_speed
            elif event.key == pygame.K_DOWN:
                player_y += player_speed
            elif event.key == pygame.K_SPACE:
                if not game_over:  # 如果游戏已经结束，按空格键不会发射子弹
                    current_time = pygame.time.get_ticks()
                    if current_time - last_fire_time > 1000 / fire_rate:
                        bullet_x = player_x + player_image.get_width() / 2 - bullet_image.get_width() / 2
                        bullet_y = player_y - bullet_image.get_height()
                        bullet_list.append([bullet_x, bullet_y])
                        last_fire_time = current_time

    # 更新游戏元素位置
    for i in range(len(alien_list)):
        alien_list[i][1] += alien_list[i][2]  # 更新外星人的纵坐标
        if alien_list[i][1] > screen_height:  # 如果外星人跑出屏幕了
            alien_list[i][0] = random.randint(0, screen_width - alien_image.get_width())  # 随机生成新的横坐标
            alien_list[i][1] = random.randint(-500, -50)  # 随机生成新的纵坐标
            alien_list[i][2] = random.randint(1, 4)  # 随机生成新的速度
        for j in range(len(bullet_list)):
            if bullet_list[j][0] + bullet_image.get_width() > alien_list[i][0] and \
                    bullet_list[j][0] < alien_list[i][0] + alien_image.get_width() and \
                    bullet_list[j][1] < alien_list[i][1] + alien_image.get_height() and \
                    bullet_list[j][1] + bullet_image.get_height() > alien_list[i][1]:  # 检测子弹是否击中外星人
                score += 5  # 击中外星人加 5 分
                del bullet_list[j]
                alien_list[i][0] = random.randint(0, screen_width - alien_image.get_width())
                alien_list[i][1] = random.randint(-500, -50)
                alien_list[i][2] = random.randint(1, 4)
                break
    for i in range(len(bullet_list)):
        bullet_list[i][1] -= bullet_speed
        if bullet_list[i][1] + bullet_image.get_height() < 0:
            del bullet_list[i]
            break

    # 绘制游戏元素
    # screen.blit(background_image, (0, 0))
    screen.blit(player_image, (player_x, player_y))
    for alien in alien_list:
        screen.blit(alien_image, (alien[0], alien[1]))
    score_text = font.render("Score: " + str(score), True, (0, 255, 0))
    screen.blit(score_text, (10, 10))

    # 检测外星人和玩家之间是否发生了碰撞
    if not invincible:  # 如果玩家处于无敌状态，不会被外星人撞到
        player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
        for alien in alien_list:
            alien_rect = pygame.Rect(alien[0], alien[1], alien_image.get_width(), alien_image.get_height())
            if player_rect.colliderect(alien_rect):
                lives -= 1
                if lives > 0:  # 如果玩家还有生命数，重新生成玩家和外星人
                    player_x = screen_width / 2
                    player_y = screen_height - player_image.get_height() - 10
                    alien_list.clear()
                    for i in range(10):
                        alien_x = random.randint(0, screen_width - alien_image.get_width())
                        alien_y = random.randint(-500, -50)
                        alien_speed = random.randint(1, 4)
                        alien_list.append([alien_x, alien_y, alien_speed])
                    invincible = True
                    invincible_start_time = pygame.time.get_ticks()
                else:  # 如果玩家已经没有生命数，游戏结束
                    game_over = True

    # 检测无敌状态是否结束
    if invincible:
        current_time = pygame.time.get_ticks()
        if current_time - invincible_start_time > 3000:
            invincible = False

    # 检测游戏是否失败
    if game_over:
        font = pygame.font.Font(None, 60)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (
            screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2 - game_over_text.get_height() / 2))
        pygame.draw.rect(screen, (0, 0, 0), restart_button)
        restart_text = font.render("Restart", True, (255, 255, 255))
        screen.blit(restart_text, (screen_width / 2 - restart_text.get_width() / 2, screen_height / 2 + 60))
        pygame.display.update()



    # 等待用户点击重新开始按钮
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(mouse_x, mouse_y):
            game_over = False
            score = 0
            lives = 3
            player_x = screen_width / 2
            player_y = screen_height - player_image.get_height() - 10
            alien_list.clear()
            for i in range(10):
                alien_x = random.randint(0, screen_width - alien_image.get_width())
                alien_y = random.randint(-500, -50)
                alien_speed = random.randint(1, 4)
                alien_list.append([alien_x, alien_y, alien_speed])
            invincible = True
            invincible_start_time = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    # 更新游戏窗口
    pygame.display.update()

    # 控制游戏帧率
    clock.tick(60)

    # 绘制游戏背景
    screen.fill((255, 255, 255))


# 退出 Pygame
pygame.quit()
sys.exit()
