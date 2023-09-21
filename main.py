import pygame, sys, os, random

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
    

football = pygame.transform.scale(pygame.image.load("Penalty/assets/football.png"), (64, 64)).convert_alpha()
target = pygame.transform.scale(pygame.image.load("Penalty/assets/target.png"), (64, 64))
BG = pygame.image.load("Penalty/assets/goal.png").convert_alpha()
option_store = None
ball_rect = football.get_rect()
BajaBlast = pygame.transform.scale(pygame.image.load("Penalty/scoreboard/BajaBlast_scoreboard.png"), (238, 114)).convert_alpha()
MugRootBeer = pygame.transform.scale(pygame.image.load("Penalty/scoreboard/MugRootBeer_scoreboard.png"), (238, 114)).convert_alpha()
goal = pygame.transform.scale(pygame.image.load("Penalty/scoreboard/score_scoreboard.png"), (24, 24)).convert_alpha()
miss = pygame.transform.scale(pygame.image.load("Penalty/scoreboard/miss_scoreboard.png"), (24, 24)).convert_alpha()


KEEPER = {
    "BL": pygame.transform.scale(pygame.image.load(os.path.join('Penalty/keeper', 'keeper_BL.png')), (304, 384)).convert_alpha(),
    "BR" : pygame.transform.scale(pygame.image.load(os.path.join('Penalty/keeper', 'keeper_BR.png')), (304, 384)).convert_alpha(),
    "idle" : pygame.transform.scale(pygame.image.load(os.path.join('Penalty/keeper', 'keeper_idle.png')), (163, 315)).convert_alpha(),
    "M" : pygame.transform.scale(pygame.image.load(os.path.join('Penalty/keeper', 'keeper_T.png')), (304, 384)).convert_alpha(),
    "TL" : pygame.transform.scale(pygame.image.load(os.path.join('Penalty/keeper', 'keeper_TL.png')), (304, 384)).convert_alpha(),
    "TR" : pygame.transform.scale(pygame.image.load(os.path.join('Penalty/keeper', 'keeper_TR.png')), (304, 384)).convert_alpha()
}

KEEPER_POS = {
    "BL": (293, 78),
    "BR" : (617, 95),
    "M" : (445, 78),
    "TL" : (223, 50),
    "TR" : (694, 65),
}

SCORE_POS = {
    (300, 290): "BL",
    (770, 290): "BR" ,
    (530, 100): "M",
    (300, 100): "TL",
    (770, 100): "TR"
}

clock = pygame.time.Clock()
FPS = 120

options = ["TL","BL","M","TR","BR"]

def score_board(p_score):
    screen.blit(MugRootBeer, (0, 0))

    for score, type in enumerate(p_score):
        if type:
            screen.blit(goal, (44 + (score) * 32,  67))
        else:
            screen.blit(miss, (44 + (score) * 32,  67))
            
def comp_option(target, level):
    global option_store
    weight = (level + 1) / 2

    if not option_store:
        weighted_list = [1 if option != SCORE_POS[target[0]] else weight for option in options]
        option_store = random.choices(options, weights=(weighted_list))[0]

    return option_store

def get_quadrant():
    mx, my = pygame.mouse.get_pos()

    quadrants = [(530, 100), (300, 100), (770, 100), (770, 290), (300, 290)]
    pos = 0

    for quad in quadrants:
        if mx in range(quad[0]-50, quad[0]+150) and my in range(quad[1]-50, quad[1]+150):
            pos = quad

    return (pos, True) if pos else ((mx-32, my-32), False)

      
def keeper(computer_option):
    screen.blit(KEEPER[computer_option], KEEPER_POS[computer_option])

def main():
    global option_store
    level = 1
    shot = False
    ball_x, ball_y = 567, 671
    p_score = []

    while True:
        pygame.mouse.set_visible(False)
        if not shot:
            target_pos = get_quadrant() 
            
        screen.blit(BG, (0, 0))
        score_board(p_score)
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                shot = True
        
        if shot and target_pos[1]:
            keeper(comp_option(target_pos, level))
            ball_x -= (ball_x - (target_pos[0][0]) - 36) / 4
            ball_y -= (ball_y - (target_pos[0][1]) - 36) / 4
        else:
            screen.blit(KEEPER["idle"], (509, 135))
            screen.blit(pygame.transform.scale(target, ((128, 128) if target_pos[1] else (64, 64))), (target_pos[0]))
            shot = False

        if ball_rect.collidepoint(target_pos[0][0] + 36, target_pos[0][1] + 36) and target_pos[1]:
            if len(p_score) < 5:
                if SCORE_POS[target_pos[0]] == option_store:
                    p_score.append(False)
                else:
                    p_score.append(True)
    
            target_pos = get_quadrant()
            shot = False
            ball_x, ball_y = 567, 671
            option_store = None

        ball_rect.x, ball_rect.y = ball_x, ball_y
        screen.blit(football, (ball_x, ball_y))
        
        pygame.display.update()
        pygame.display.set_caption(f"fps: {int(clock.get_fps())}")
        clock.tick(FPS)
main()