import pygame
import time
from sys import exit
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
    K_RIGHT,
    K_LEFT
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Dino Game') # donne un nom à la fenetre ouverte

clock=pygame.time.Clock() # gère la vitesse du jeu

# définition du sol
sol = pygame.image.load("Graphiques/Arrière_plan/Ground.png")
sol = pygame.transform.scale(sol, (1800,15))  # Applique la taille placée en parametre à l'image
sol_x = 0
sol_rect=sol.get_rect(center=(640,40))

# définition du bouton replay
replay_surf = pygame.image.load("Graphiques/Arrière_plan/replay_button.png")
replay_surf = pygame.transform.scale(replay_surf, (60,50)) # Applique la taille placée en parametre à l'image
replay_rect= replay_surf.get_rect(center=(400,150))

game_over_surf = pygame.image.load("Graphiques/Arrière_plan/game_over.png")
game_over_rect = replay_surf.get_rect(center=(250,100))

couronne_surf = pygame.image.load("Graphiques/Arrière_plan/couronne.png")
couronne_rect = couronne_surf.get_rect(midbottom=(30,320))

chapeau_surf = pygame.image.load("Graphiques/Arrière_plan/chapeau.png")
chapeau_surf = pygame.transform.scale(chapeau_surf,(30,30))
chapeau_rect = couronne_surf.get_rect(midbottom=(30,320))


#définit l'intervalle entre les obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,2200)
    
class Player():
    def __init__(self):
        '''Défini les divers paramètres de jeu : images, vitesse et gravité'''
        self.run1 = pygame.image.load("Graphiques/Dino/DinoRun1.png").convert_alpha()
        self.run2 = pygame.image.load("Graphiques/Dino/DinoRun2.png").convert_alpha()
        self.run = [self.run1,self.run2]
        self.index = 0
        self.jump = pygame.image.load("Graphiques/Dino/DinoJump.png").convert_alpha()
        self.duck1 = pygame.image.load("Graphiques/Dino/DinoDuck1.png").convert_alpha()
        self.duck2 = pygame.image.load("Graphiques/Dino/DinoDuck2.png").convert_alpha()
        self.dead = pygame.image.load("Graphiques/Dino/DinoDead.png").convert_alpha()
        self.duck = [self.duck1,self.duck2]
        self.surf = self.run[self.index]
        self.rect = self.surf.get_rect(midbottom = (80,320))
        
        self.run_crown1 = pygame.image.load("Graphiques/Dino_Crown/DinoRun1.png").convert_alpha()
        self.run_crown2 = pygame.image.load("Graphiques/Dino_Crown/DinoRun2.png").convert_alpha()
        self.run_crown = [self.run_crown1,self.run_crown2]
        self.jump_crown = pygame.image.load("Graphiques/Dino_Crown/DinoJump.png").convert_alpha()
        self.duck_crown1 = pygame.image.load("Graphiques/Dino_Crown/DinoDuck1.png").convert_alpha()
        self.duck_crown2 = pygame.image.load("Graphiques/Dino_Crown/DinoDuck2.png").convert_alpha()
        self.duck_crown = [self.duck_crown1,self.duck_crown2]
        
        self.run_red1 = pygame.image.load("Graphiques/Dino_Red/DinoRun1.png").convert_alpha()
        self.run_red2 = pygame.image.load("Graphiques/Dino_Red/DinoRun2.png").convert_alpha()
        self.run_red = [self.run_red1,self.run_red2]
        self.jump_red = pygame.image.load("Graphiques/Dino_Red/DinoJump.png").convert_alpha()
        self.duck_red1 = pygame.image.load("Graphiques/Dino_Red/DinoDuck1.png").convert_alpha()
        self.duck_red2 = pygame.image.load("Graphiques/Dino_Red/DinoDuck2.png").convert_alpha()
        self.duck_red = [self.duck_red1,self.duck_red2]
        self.dead_red = pygame.image.load("Graphiques/Dino_Red/DinoDead.png").convert_alpha()
        
        self.run_hat1 = pygame.image.load("Graphiques/Dino_Hat/DinoRun1.png").convert_alpha()
        self.run_hat2 = pygame.image.load("Graphiques/Dino_Hat/DinoRun2.png").convert_alpha()
        self.run_hat = [self.run_hat1,self.run_hat2]
        self.jump_hat = pygame.image.load("Graphiques/Dino_Hat/DinoJump.png").convert_alpha()
        self.duck_hat1 = pygame.image.load("Graphiques/Dino_Hat/DinoDuck1.png").convert_alpha()
        self.duck_hat2 = pygame.image.load("Graphiques/Dino_Hat/DinoDuck2.png").convert_alpha()
        self.duck_hat = [self.duck_hat1, self.duck_hat2]
        self.dead_hat = pygame.image.load("Graphiques/Dino_Hat/DinoDead.png").convert_alpha()
        
        
        self.gravity = 0
        self.vitesse = 0
        
    def update(self):
        '''Défini une hauteur par défaut pour le dinosaure afin que celui-ci court sur un sol
            et y raterrisse après avoir sauté'''
        if self.rect.bottom>=320: 
            self.rect.bottom=320 
            screen.blit(self.surf,self.rect)


    def player_animation(self, skin_jump, skin_run, skin_duck):
        '''Alterne entre 2 images stockées dans diverses listes, afin de permettre au dinosaure de courir, sauter et se baisser'''
        global pressed_keys, game_speed
        self.vitesse = (game_speed)/50
        
        # si le dinosaure est au dessus du sol, alors on change son image
        
        if self.rect.bottom<320 and not pressed_keys[K_DOWN]:
            self.surf=skin_jump
            self.surf.get_rect(midbottom = (80,320))
        else:
            # si le dinosaure est au sol, alors on le fait courir
            self.index += self.vitesse
            if self.index>len(skin_run):
                self.index=0
            self.surf=skin_run[int(self.index)]
            self.rect = self.surf.get_rect(midbottom = (80,320))
            
            # si on appuie sur la flèche du bas, alors le dinosaure se baisse
        if pressed_keys[K_DOWN]:
            self.index += self.vitesse
            if self.index>len(skin_duck):
                self.index=0
            self.surf=skin_duck[int(self.index)]
            self.rect=self.surf.get_rect(midbottom = (80,320))
        

class Oiseau():
    def __init__(self):
        '''Défini les images de l'oiseau'''
        self.fly1 = pygame.image.load("Graphiques/Oiseau/Bird1.png").convert_alpha()
        self.fly2 = pygame.image.load("Graphiques/Oiseau/Bird2.png").convert_alpha()
        self.fly1= pygame.transform.scale(self.fly1, (70,40))
        self.fly2= pygame.transform.scale(self.fly2, (70,40))
        self.fly = [self.fly1,self.fly2]
        self.index = 0
        self.hauteur=[140,220,220,290,290]
        self.surf = self.fly[self.index]
        self.rect = self.surf.get_rect(bottomright = (600,300))
        self.rect.y=random.choice(self.hauteur)
        
            
    def oiseau_animation(self):
        '''Alterne entre 2 images stockées dans la liste vol, afin de permettre à l'oiseau de voler'''
        global pressed_keys
        if self.rect.y in self.hauteur:
            self.index += 0.05
            if self.index>len(self.fly):
                self.index=0
            self.surf=self.fly[int(self.index)]
        
class Cactus() :
    def __init__(self):
        '''Défini les divers modèles de cactus'''
        self.small1 = pygame.image.load("Graphiques/Cactus/SmallCactus1.png").convert_alpha()
        self.small2 = pygame.image.load("Graphiques/Cactus/SmallCactus2.png").convert_alpha()
        self.small3 = pygame.image.load("Graphiques/Cactus/SmallCactus3.png").convert_alpha()
        self.large1 = pygame.image.load("Graphiques/Cactus/LargeCactus1.png").convert_alpha()
        self.large2 = pygame.image.load("Graphiques/Cactus/LargeCactus2.png").convert_alpha()
        self.large3 = pygame.image.load("Graphiques/Cactus/LargeCactus3.png").convert_alpha()
        self.cactus_small = [self.small1,self.small2,self.small3]
        self.cactus_large = [self.large1,self.large2,self.large3]
        self.surf = random.choice(self.cactus_small)
        self.rect = self.surf.get_rect(bottomright = (700,320))
        

    
class Nuage():
    def __init__(self):
        '''Défini les nuages'''
        self.x = SCREEN_WIDTH + random.randint(800,1000)
        self.y = random.randint(50,100)
        self.surf = pygame.image.load("Graphiques/Arrière_plan/Cloud.png").convert_alpha()
        self.width = self.surf.get_width()
        
    def update(self):
        '''Fait apparaitre un nouveau nuage si celui ci quitte l'écran'''
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(800,1000)
            self.y = random.randint(50,100)
    
    def draw(self,screen):
        '''Fait apparaitre les nuages à l'écran'''
        screen.blit(self.surf,(self.x,self.y))
               
class Confettis():
    def __init__(self):
        '''initialisation des images qui constituent le gif'''
        self.image1 = pygame.image.load("Graphiques/Confettis/frame-01.jpg").convert_alpha()
        self.image2 = pygame.image.load("Graphiques/Confettis/frame-02.jpg").convert_alpha()
        self.image3 = pygame.image.load("Graphiques/Confettis/frame-03.jpg").convert_alpha()
        self.image4 = pygame.image.load("Graphiques/Confettis/frame-04.jpg").convert_alpha()
        self.image5 = pygame.image.load("Graphiques/Confettis/frame-05.jpg").convert_alpha()
        self.image6 = pygame.image.load("Graphiques/Confettis/frame-06.jpg").convert_alpha()
        self.image7 = pygame.image.load("Graphiques/Confettis/frame-07.jpg").convert_alpha()
        self.image8 = pygame.image.load("Graphiques/Confettis/frame-08.jpg").convert_alpha()
        self.image9 = pygame.image.load("Graphiques/Confettis/frame-09.jpg").convert_alpha()
        self.image10 = pygame.image.load("Graphiques/Confettis/frame-10.jpg").convert_alpha()
        self.image11 = pygame.image.load("Graphiques/Confettis/frame-11.jpg").convert_alpha()
        self.image12 = pygame.image.load("Graphiques/Confettis/frame-12.jpg").convert_alpha()
        self.image13 = pygame.image.load("Graphiques/Confettis/frame-13.jpg").convert_alpha()
        self.image14 = pygame.image.load("Graphiques/Confettis/frame-14.jpg").convert_alpha()
        self.image15 = pygame.image.load("Graphiques/Confettis/frame-15.jpg").convert_alpha()
        self.image16 = pygame.image.load("Graphiques/Confettis/frame-16.jpg").convert_alpha()
        self.image17 = pygame.image.load("Graphiques/Confettis/frame-17.jpg").convert_alpha()
        self.image18 = pygame.image.load("Graphiques/Confettis/frame-18.jpg").convert_alpha()
        self.image19 = pygame.image.load("Graphiques/Confettis/frame-19.jpg").convert_alpha()
        self.image20 = pygame.image.load("Graphiques/Confettis/frame-20.jpg").convert_alpha()
        self.image21 = pygame.image.load("Graphiques/Confettis/frame-21.jpg").convert_alpha()
        self.image22 = pygame.image.load("Graphiques/Confettis/frame-22.jpg").convert_alpha()
        self.image23 = pygame.image.load("Graphiques/Confettis/frame-23.jpg").convert_alpha()
        self.image24 = pygame.image.load("Graphiques/Confettis/frame-24.jpg").convert_alpha()
        self.image25 = pygame.image.load("Graphiques/Confettis/frame-25.jpg").convert_alpha()
        self.image26 = pygame.image.load("Graphiques/Confettis/frame-26.jpg").convert_alpha()
        self.image27 = pygame.image.load("Graphiques/Confettis/frame-27.jpg").convert_alpha()
        self.image28 = pygame.image.load("Graphiques/Confettis/frame-28.jpg").convert_alpha()
        self.image29 = pygame.image.load("Graphiques/Confettis/frame-29.jpg").convert_alpha()
        self.image30 = pygame.image.load("Graphiques/Confettis/frame-30.jpg").convert_alpha()
        self.confettis = [self.image1,self.image2,self.image3,self.image4,self.image5,self.image6,self.image7,self.image8,self.image9,self.image10,self.image11,self.image12,self.image13,self.image14,self.image15,self.image16,self.image17,self.image18,self.image19,self.image20,self.image21,self.image22,self.image23,self.image24,self.image25,self.image26,self.image27,self.image28,self.image29,self.image30]
        self.index = 0
        self.surf = self.confettis[self.index]
        self.surf = pygame.transform.scale(self.surf, (1000,1000))
        self.rect = self.surf.get_rect(midtop = (600,0))
        
        
    def confettis_animation(self):
        '''Fait défiler les images définies plus tôt pour faire apparaitre des confettis
            ( pygame ne prenant pas en charge les gif ) '''
        for i in range(700):
            self.index += 0.0008
            if self.index>len(self.confettis):
                self.index=0
            self.surf = self.confettis[int(self.index)]

def display_score():
    '''Affiche le score'''
    current_time = (pygame.time.get_ticks() - start_time)//100
    test_font = pygame.font.SysFont( "Lobster" ,  48 )
    score_surf = test_font.render(f'{current_time}',True,(64,64,64))
    score_rect = score_surf.get_rect(center = (750,25))
    screen.blit(score_surf,score_rect)
    return current_time


def highest_score(last_score, Hi):
    '''Affiche le meilleur score'''
    if last_score > Hi : Hi = last_score 
    test_font = pygame.font.SysFont( "Lobster" ,  48 )
    hi_score_surf = test_font.render(f'HI : {Hi}',True,(64,64,64))
    hi_score_rect = hi_score_surf.get_rect(center = (70,25))
    screen.blit(hi_score_surf,hi_score_rect)
    return Hi
            
def background():
    '''Donne l'impression que le sol avance'''
    global sol_x
    screen.blit(sol,(sol_x,300))
    screen.blit(sol,(sol_x+ 1800,300))
    if sol_x<=-1800:
        screen.blit(sol,(sol_x+ 1800,300))
        sol_x=0
    sol_x-=game_speed

def restart(obstacle_list,surf,draw_cactus):
    '''Relance le jeu en remettant tous les décors en place'''
    screen.fill((255,255,255))
    player_rect = surf.get_rect(midbottom = (80,300))
    if surf == player.dead:
        player_rect = surf.get_rect(midbottom = (80,320))
    screen.blit(sol,(0,300))
    for obstacle_rect in obstacle_list:
        if obstacle_rect.bottom==320:
            screen.blit(cactus.surf,obstacle_rect)
        else:
            screen.blit(oiseau.surf,obstacle_rect)
        
        if draw_cactus == False :
            obstacle_rect.left=900
        game_speed=10
        pygame.display.update()
    
    
def obstacle_movement(obstacle_list):
    ''' Fait bouger les obstacles'''
    global game_speed, taille_cactus
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= game_speed # Fait avancer les obstacles
            if obstacle_rect.bottom == 320: # si le bas de l'image est défini à 320, on dessine un cactus
                screen.blit(cactus.surf,obstacle_rect)
            else: # sinon, on dessine un oiseau
                screen.blit(oiseau.surf,obstacle_rect)
        # Fait apparaitre un nouveau taille_cactus de cactus au hasard, sois un grand sois un petit en fonction de 'taille_cactus'   
            for obstacle in obstacle_list :
                if obstacle.x < -100:
                    if taille_cactus == 0 :
                        cactus.surf=random.choice(cactus.cactus_large)
                    if taille_cactus == 1 :
                        cactus.surf=random.choice(cactus.cactus_small)
        
        # si les images sont à l'écran ont les dessine et les Fait bouger, sinon on les supprime
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list    
    else:
        return []

def collisions(player,obstacles):
    '''Détecte les colisions entre le dinosaure et les obstacles'''
    if obstacles:
        for obstacle_rect in obstacles:
            # Si le dinosaure rentre avec n'importe quel obstacle présent dans la liste 'obstacle', alors le dinosaure meurt et le joueur perd
            if player.colliderect(obstacle_rect): 
                return False
    return True

    
player = Player()
oiseau = Oiseau()
cactus = Cactus()
nuage = Nuage()
confettis = Confettis()

start_game = 0 
run = False
start_time = 0 
game_speed = 12 
taille_cactus = random.randint(0,1) # choisit si la partie sera faite de petit ou de grands cactus
nb_partie = 0
Hi = 0
last_score = 0

obstacle_rect_list = []
screen.fill((255,255,255))
screen.blit(sol,(0,300))
screen.blit(player.jump,player.rect)
count = 0
null = True

while True :
    pressed_keys = pygame.key.get_pressed()             

    # menu de début de partie
    if start_game==0:
        for event in pygame.event.get():
            start_time = pygame.time.get_ticks()
            player.gravity=-20
            if event.type==pygame.QUIT:
                exit()
            
            if null :  
                skin_jump = player.jump
                skin_run = player.run
                skin_duck = player.duck
                skin_dead = player.dead
                
            
            if event.type == pygame.KEYUP:
                if event.key==K_RIGHT:
                    count+=1
                    if count == 0:
                        screen.fill((255,255,255))
                        screen.blit(sol,(0,300))
                        screen.blit(player.jump,(35,225))
                    if count == 1 :
                        null=False
                        skin_jump = player.jump_crown
                        skin_run = player.run_crown
                        skin_duck = player.duck_crown
                        skin_dead = player.dead
                        screen.blit(player.jump_crown,(35,215))
                
                elif event.key==K_LEFT:
                    count -=1
                    if count == 0:
                        screen.fill((255,255,255))
                        screen.blit(sol,(0,300))
                        screen.blit(player.jump,(35,225))
                        skin_jump = player.jump
                        skin_run = player.run
                        skin_duck = player.duck
                        skin_dead = player.dead
                    elif count ==-1 :
                        null = False
                        skin_jump = player.jump_red
                        skin_run = player.run_red
                        skin_duck = player.duck_red
                        skin_dead = player.dead_red
                        screen.blit(player.jump_red,(35,225))
            if event.type == pygame.KEYDOWN:
               if (event.key == K_SPACE): run = True
                
        
        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key==K_ESCAPE:
                exit()
        if run :
            if event.type == KEYDOWN:
                # si le joueur appuie sur la barre espace et que le dino n'est pas déja en l'air, alors le dinosaure saute
                if (event.key == K_UP or event.key== K_SPACE) and player.rect.bottom==320 : 
                    player.gravity=-20
                    
                    
        else :
            
            # si on appuie sur la barre espace, la partie recommence
            if event.type == KEYDOWN and(event.key == K_UP or event.key== K_SPACE):
                start_time = pygame.time.get_ticks()
                restart(obstacle_rect_list,skin_jump,False) # relance le jeu
                if event.type == KEYDOWN and(event.key == K_UP or event.key== K_SPACE):
                    restart(obstacle_rect_list,skin_jump,False)
                    player.rect = player.surf.get_rect(midbottom = (80,320))
                    screen.blit(player.surf,player.rect)
                    run = True
           
           # si on appuie sur bouton replay, la partie recommence
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(event.pos):
                     start_time = pygame.time.get_ticks()
                     restart(obstacle_rect_list,player.jump,False)
                     player.rect = player.surf.get_rect(midbottom = (80,320))
                     screen.blit(player.surf,player.rect)
                     run = True
        
        # Fait apparaitre un oiseau ou un cactus
        if event.type == obstacle_timer and run:
             a = random.randint(0,2)
             if a == 0 or a == 1: # plus de chance d'avoir un cactus que un oiseau
                obstacle_rect_list.append(cactus.surf.get_rect(midbottom = (random.randint(1500,1800),320)))
             elif a == 2 :
                 obstacle_rect_list.append(oiseau.surf.get_rect(bottomright = (random.randint(1500,1700),random.choice(oiseau.hauteur))))
            
                
        
    if run :
        
                        
        screen.fill((255, 255, 255)) # initialise le fond en blanc
        background() # fait bouger le sol
        start_game+=1
        
        # plus le joueur va vite, plus la gravité augmente
        player.gravity+=1    
        player.rect.y+=player.gravity
        player.update()
        
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
                
        # anime les oiseaux et le dinosaure
        player.player_animation(skin_jump, skin_run, skin_duck)
        oiseau.oiseau_animation()
        
        # fait apparaitre les nuages et les fait avancer    
        nuage.draw(screen)
        nuage.update()
        
        screen.blit(player.surf,player.rect)
        
        
        if (display_score()>=500 and display_score()<=515) or (display_score()>=1000 and display_score()<=1015):
            confettis.confettis_animation()
            screen.blit(confettis.surf,confettis.rect)
        if display_score()>=1000:
            skin_jump = player.jump_hat
            skin_run = player.run_hat
            skin_duck = player.duck_hat
            skin_dead = player.dead_hat
            

        display_score() # fait apparaitre le score
        if nb_partie >= 1 : highest_score(last_score,Hi) # affiche le meilleur score
        game_speed+=0.001 # augmente la vitesse du jeu
        
        run = collisions(player.rect,obstacle_rect_list)
        if not run:
            # change le dinosaure en fontion si il est en vie ou non
            if pressed_keys[K_DOWN]:
                player.rect = player.surf.get_rect(midbottom = (80,300))
            elif skin_dead == player.dead_hat:
                player.rect = player.surf.get_rect(midbottom = (80,340))
                screen.blit(skin_dead,player.rect)
                skin_jump = player.jump
                skin_run = player.run
                skin_duck = player.duck
                skin_dead = player.dead
            else :
                screen.blit(skin_dead,player.rect)
            # menu de fin de partie
            if player.rect.bottom==320:
                player.rect = player.surf.get_rect(midbottom = (80,330))
            restart(obstacle_rect_list,skin_dead,True)    
            screen.blit(skin_dead,player.rect)
            nb_partie += 1
            last_score = display_score()
            
            if skin_jump == player.jump_crown :
                screen.blit(couronne_surf,couronne_rect)
            if display_score()>= 1000 :
                screen.blit(chapeau_surf,chapeau_rect)
            screen.blit(replay_surf,replay_rect)
            screen.blit (game_over_surf, game_over_rect)
            pygame.display.update()
            display_score()
            if nb_partie >= 1 : highest_score(last_score,Hi)

            
            if nb_partie >= 1 and last_score > Hi:
                Hi = last_score
            
            run = False

    
    pygame.display.update()
    clock.tick(game_speed+30)

    
pygame.quit()
quit()

