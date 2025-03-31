import pygame
import random

# 初始化 pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打飞机游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 飞机设置
plane_width, plane_height = 50, 50
plane_x, plane_y = WIDTH // 2, HEIGHT - 100
plane_speed = 5

# 子弹设置
bullets = []
bullet_width, bullet_height = 5, 10
bullet_speed = 7

# 障碍物设置
obstacles = []
obstacle_width, obstacle_height = 50, 50
obstacle_speed = 3
spawn_interval = 30  # 每隔多少帧生成一个障碍物

# 游戏时钟
clock = pygame.time.Clock()

def draw_plane(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, plane_width, plane_height))

def draw_bullet(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, obstacle)

def main():
    global plane_x, plane_y
    running = True
    frame_count = 0

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 飞机移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and plane_x > 0:
            plane_x -= plane_speed
        if keys[pygame.K_RIGHT] and plane_x < WIDTH - plane_width:
            plane_x += plane_speed
        if keys[pygame.K_UP] and plane_y > 0:
            plane_y -= plane_speed
        if keys[pygame.K_DOWN] and plane_y < HEIGHT - plane_height:
            plane_y += plane_speed

        # 自动发射子弹
        if frame_count % 10 == 0:  # 每 10 帧发射一颗子弹
            bullets.append(pygame.Rect(plane_x + plane_width // 2 - bullet_width // 2, plane_y, bullet_width, bullet_height))

        # 更新子弹位置
        bullets[:] = [bullet for bullet in bullets if bullet.y > 0]
        for bullet in bullets:
            bullet.y -= bullet_speed

        # 生成障碍物
        if frame_count % spawn_interval == 0:
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacles.append(pygame.Rect(obstacle_x, 0, obstacle_width, obstacle_height))

        # 更新障碍物位置
        obstacles[:] = [obstacle for obstacle in obstacles if obstacle.y < HEIGHT]
        for obstacle in obstacles:
            obstacle.y += obstacle_speed

        # 检测子弹与障碍物碰撞
        for bullet in bullets[:]:
            for obstacle in obstacles[:]:
                if bullet.colliderect(obstacle):
                    bullets.remove(bullet)
                    obstacles.remove(obstacle)
                    break

        # 检测飞机与障碍物碰撞
        for obstacle in obstacles:
            if pygame.Rect(plane_x, plane_y, plane_width, plane_height).colliderect(obstacle):
                print("游戏结束！")
                running = False

        # 绘制元素
        draw_plane(plane_x, plane_y)
        draw_bullet(bullets)
        draw_obstacles(obstacles)

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    pygame.quit()

if __name__ == "__main__":
    main()
