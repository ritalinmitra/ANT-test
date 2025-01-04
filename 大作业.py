# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 13:32:16 2024

@author: HP
"""
import pygame
import random
import sys
import time

pygame.init()

# 全屏
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# 颜色和字体
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# 没用通用是因为不知道为什么用None,36就会乱码
font = pygame.font.Font("C:/Windows/Fonts/simsun.ttc", 36)

# 用于记录正式实验的正确次数、错误次数、反应时间列表
correct_count = 0
error_count = 0
reaction_times = []

# 呈现指导语
def instruction():
    instruction_text = [
        "欢迎参加本实验，",
        "请将你的左手和右手食指分别放在键盘的D和K键上。",
        "一会屏幕上会呈现一个注视点“+”，",
        "其上或下方会出现5个水平排列的箭头，",
        "请正确且迅速判断中央箭头的方向！",
        "看到“←”按 D 键, 看到“→”按 K 键，",
        "如果你已经明白规则，请按空格键开始练习。"
    ]
    # 计算文本总高度，使得文本能够垂直居中
    text_height = (len(instruction_text) * 40)
    y_start = SCREEN_HEIGHT // 2 - text_height // 2
    for line in instruction_text:
        text_surface = font.render(line, True, WHITE)
        x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
        screen.blit(text_surface, (x, y_start))
        y_start += 40
    pygame.display.flip()
    clear_instruction()

# 等待空格键按下并清除指导语的函数
def clear_instruction():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    clear_screen()
                    waiting = False

# 呈现注视点的函数
def point(duration):
    fixation_point = font.render("+", True, WHITE)
    x = SCREEN_WIDTH // 2 - fixation_point.get_width() // 2
    y = SCREEN_HEIGHT // 2 - fixation_point.get_height() // 2
    screen.blit(fixation_point, (x, y))
    pygame.display.flip()
    pygame.time.delay(duration)

# 生成箭头序列的函数(三种情况)
def biu():
    conditions = [
        ["→", "→", "→", "→", "→"],  # 同方向，有提示
        ["←", "→", "←", "→", "←"],  # 不同方向，有干扰
        ["—", "—", "→", "—", "—"]   # 没有方向
    ]
    return random.choice(conditions)

# 在指定位置显示箭头序列（上方或下方）的函数
def biu_set(biu_seq, position):
    biu_width = 30
    biu_height = 30
    x_start = (SCREEN_WIDTH - biu_width * 5) // 2
    if position == "above":
        y_start = SCREEN_HEIGHT // 2 - biu_height * 3
    else:
        y_start = SCREEN_HEIGHT // 2 + biu_height
    for i in range(5):
        biu_text = font.render(biu_seq[i], True, WHITE)
        screen.blit(biu_text, (x_start + i * biu_width, y_start))
    pygame.display.flip()

# 显示反馈文字的函数（练习阶段）
def feedback(is_correct):
    feedback_text = "恭喜回答正确！" if is_correct else "抱歉！回答错误！"
    color = GREEN if is_correct else RED
    text_surface = font.render(feedback_text, True, color)
    x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
    y = SCREEN_HEIGHT - 50
    screen.blit(text_surface, (x, y))
    pygame.display.flip()
    pygame.time.delay(500)
    clear_screen()

# 练习阶段
def practice():
    num_practice_trials = 6
    for _ in range(num_practice_trials):
        point(1500)
        biu_seq = biu()
        position = random.choice(["above", "below"])
        biu_set(biu_seq, position)
        correct_key = pygame.K_d if biu_seq[2] == "←" else pygame.K_k
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_d or event.key == pygame.K_k or event.key == pygame.K_SPACE:
                        if event.key == correct_key:
                            # 记录正确响应
                            feedback(True)
                            waiting = False
                        elif event.key == (pygame.K_d if correct_key == pygame.K_k else pygame.K_k):
                            # 记录错误响应
                            feedback(False)
                            waiting = False
                        elif event.key == pygame.K_SPACE:
                            pass

# 呈现正式实验指导语的函数
    show_instructions_formal()
def show_instructions_formal():
    instructions_text = [
        "接下来是正式实验，",
        "正式实验没有正确/错误的反馈，其他规则与练习相同，",
        "看到“←”按 D 键, 看到“→”按 K 键，",
        "请按空格键开始正式实验。"
    ]
    total_text_height = (len(instructions_text) * 40)
    y_start = SCREEN_HEIGHT // 2 - total_text_height // 2
    for line in instructions_text:
        text_surface = font.render(line, True, WHITE)
        x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
        screen.blit(text_surface, (x, y_start))
        y_start += 40
    pygame.display.flip()
    clear_instruction()

# 正式实验阶段，添加记录反应时间和正确/错误次数逻辑
def formal_phase():
    global correct_count, error_count, reaction_times
    num_formal_trials = 24
    left_count = 0
    right_count = 0
    above_count = 0
    below_count = 0
    for _ in range(num_formal_trials):
        # 控制方向和位置的平衡呈现
        while True:
            biu_seq = biu()
            position = random.choice(["above", "below"])
            if (biu_seq[2] == "←" and left_count < 12) or (biu_seq[2] == "→" and right_count < 12):
                if (position == "above" and above_count < 12) or (position == "below" and below_count < 12):
                    break
            if biu_seq[2] == "←":
                left_count += 1
            elif biu_seq[2] == "→":
                right_count += 1
            if position == "above":
                above_count += 1
            else:
                below_count += 1
        point(1500)
        start_time = time.time()  # 记录开始时间
        biu_set(biu_seq, position)
        correct_key = pygame.K_d if biu_seq[2] == "←" else pygame.K_k
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_d or event.key == pygame.K_k or event.key == pygame.K_SPACE:
                        end_time = time.time()  # 记录结束时间，即响应时间
                        reaction_time = (end_time - start_time) * 1000  # 换算成毫秒
                        if event.key == correct_key:
                            # 记录正确响应，增加正确次数，记录反应时间
                            correct_count += 1
                            reaction_times.append(reaction_time)
                            clear_screen()
                            waiting = False
                        elif event.key == (pygame.K_d if correct_key == pygame.K_k else pygame.K_k):
                            # 记录错误响应，增加错误次数
                            error_count += 1
                            clear_screen()
                            waiting = False

    point(3000)
    end_instruction()

# 呈现结束的指导语，并添加显示统计信息逻辑
def end_instruction():
    end_text = "感谢你完成本次实验！按esc键退出"
    text_surface = font.render(end_text, True, WHITE)
    x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
    y = SCREEN_HEIGHT // 2 - text_surface.get_height() // 2
    screen.blit(text_surface, (x, y))
    pygame.display.flip()
    # 计算正确率和平均反应时间，并显示统计信息
    if correct_count + error_count > 0:
        accuracy = correct_count / (correct_count + error_count)
        if correct_count > 0:
            avg_reaction_time = sum(reaction_times) / correct_count
        else:
            avg_reaction_time = 0
        stats_text = f"你的正确率为{accuracy:.2f}，平均反应时间为{avg_reaction_time:.2f}毫秒"
        stats_surface = font.render(stats_text, True, WHITE)
        x_stats = SCREEN_WIDTH // 2 - stats_surface.get_width() // 2
        y_stats = SCREEN_HEIGHT // 2 + 50
        screen.blit(stats_surface, (x_stats, y_stats))
        pygame.display.flip()
        pygame.time.delay(2000)  # 等待2000ms

# 加个黑屏，清空屏幕
def clear_screen():
    screen.fill(BLACK)
    pygame.display.flip()


def main():
    instruction()
    practice()
    formal_phase()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 按esc键退出
                    running = False
    pygame.quit()


if __name__ == "__main__":
    main()