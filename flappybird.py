import pygame
from sys import exit
import random
import math  # 用於計算上下移動的數學函數

#game variables
GAME_WIDTH = 360
GAME_HEIGHT = 640

#bird class
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 34
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

#pipe class
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64 
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False
        self.original_y = pipe_y  # 記錄水管生成的原始高度

#game images
background_image = pygame.image.load("flappybirdbg.jpeg")
background_image = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))

bird_image = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load("toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load("bottompipe.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))

# === 載入 Game Over 圖片 ===
game_over_image = pygame.image.load("gameover.png")  
game_over_width = 320
game_over_height = int(game_over_image.get_height() * (game_over_width / game_over_image.get_width()))
game_over_image = pygame.transform.scale(game_over_image, (game_over_width, game_over_height))

# === 音樂初始化與播放 ===
pygame.mixer.init()
pygame.mixer.music.load("sasageyo.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#game logic
bird = Bird(bird_image)
pipes = []
base_velocity_x = -2 
velocity_x = base_velocity_x 
velocity_y = 0 
gravity = 0.4      
score = 0
game_over = False

def draw():
    window.blit(background_image, (0, 0))
    window.blit(bird.img, bird)

    for pipe in pipes:
        window.blit(pipe.img, pipe)
    
    # === 套用自訂字型 (如果找不到會自動退回預設字型) ===
    try:
        text_font = pygame.font.Font("BLACEB__.TTF", 45) # 如果你的檔案有副檔名請改為 "Blacklettersh.ttf"
    except:
        text_font = pygame.font.SysFont("Arial.ttf", 45)
    
    if game_over:
        go_x = (GAME_WIDTH - game_over_width) // 2
        go_y = (GAME_HEIGHT - game_over_height) // 2 - 30
        window.blit(game_over_image, (go_x, go_y))
        
        score_text = text_font.render(f"Score: {int(score)}", True, "white")
        score_rect = score_text.get_rect(center=(GAME_WIDTH // 2, go_y + game_over_height + 40))
        window.blit(score_text, score_rect)
    else:
        text_str = str(int(score))
        text_render = text_font.render(text_str, True, "white")
        window.blit(text_render, (5, 0))

def move():
    global velocity_y, score, game_over, velocity_x
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > GAME_HEIGHT:
        game_over = True
        pygame.mixer.music.stop()
        return

    # 每得 10 分增加速度
    speed_level = int(score) // 10
    velocity_x = base_velocity_x - (speed_level * 0.5)

    for pipe in pipes:
        pipe.x += velocity_x

        # === 30分之後，拳頭與巨人會上下移動 ===
        if score >= 0:
            offset = math.sin(pipe.x * 0.05) * 45
            pipe.y = pipe.original_y + offset

        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5
            pipe.passed = True
        
        bird_hitbox = bird.inflate(-14, -14)   
        pipe_hitbox = pipe.inflate(-14, -14)

        if bird_hitbox.colliderect(pipe_hitbox):
            game_over = True
            pygame.mixer.music.stop()
            return
            
    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)

def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2)
    opening_space = GAME_HEIGHT / 4  

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    top_pipe.original_y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    bottom_pipe.original_y = bottom_pipe.y
    pipes.append(bottom_pipe)

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird - Attack on Titan Edition")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500) 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == create_pipes_timer and not game_over:
            create_pipes()
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                velocity_y = -6

                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    velocity_x = base_velocity_x 
                    game_over = False
                    pygame.mixer.music.play(-1)
    
    if not game_over:
        move()
    
    draw()
    pygame.display.update()
    clock.tick(60)