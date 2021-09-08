import pygame
import sys
import time
import random

def draw_floor(): # creating floor
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos + 288,450))

def create_pipe(): # creating pipes
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos - 125))
    return bottom_pipe,top_pipe

def move_pipes(pipes): # moving pipes
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes): # showing pipes
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes): # collisioncheck for pipes/floor
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -20 or bird_rect.bottom >= 450:
        return False
    return True

def rotate_bird(bird): # rotate on movement
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 4,1)
    return new_bird

def bird_animation(): # animate da birb
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state): # displays scores
    if game_state == "main_game":
        score_surface = game_font.render(f"Score: {int(score)}",True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}",True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f"High score: {int(high_score)}",True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,420))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score): # updates scores
    if score > high_score:
        high_score = score
    return high_score

# start
# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
pygame.display.set_caption('Flappy Bird Remake')
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.ttf",20)

# physics
gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0

# background
bg_surface = pygame.image.load("assets/background-day.png").convert()
floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_pos = 0

# birb
bird_upflap = pygame.image.load("assets/yellowbird-upflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_downflap = pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()
bird_frames = [bird_upflap,bird_midflap,bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,300)

# pipe
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [200,250,300,350]

# game over
game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))

# sounds
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
swoosh_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Ended")
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True: # normal-movement
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False: # restart
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                bird_movement -= 5
                gravity = 0.25
                score = 0
                score_sound_countdown = 100
                swoosh_sound.play()
        if event.type == SPAWNPIPE: # spawning pipes
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP: # animate bird
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()
    
    screen.blit(bg_surface,(0,0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")

    floor_x_pos -= 2
    draw_floor()
    if floor_x_pos <= -288: # moving floor
        floor_x_pos = 0
    


    
    pygame.display.update()
    clock.tick(60)