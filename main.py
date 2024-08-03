
import pygame
from sys import exit
from random import choice, randint
import time

class Caracter (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        caract_walk_r_1=pygame.image.load('graphics/WalkingR1.png')
        caract_walk_r_2 = pygame.image.load('graphics/WalkingR.png')
        caract_walk_l_1 = pygame.image.load('graphics/WalkingL1.png')
        caract_walk_l_2 = pygame.image.load('graphics/WalkingL.png')
        caract_still=pygame.image.load('graphics/Still.png')

        walk_right=[caract_walk_r_1,caract_walk_r_2]
        walk_left=[caract_walk_l_1,caract_walk_l_2]
        self.animation=[walk_left,walk_right,caract_still]
        self.index=0

        self.image=self.animation[2]
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(350, 470))



    def player_input(self):
        keys=pygame.key.get_pressed()
        if self.rect.x > 0 and self.rect.x < 600:
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
                self.index+=0.2
                if self.index >= len(self.animation[0]):
                    self.index=0
                self.image= self.animation[0][int(self.index)]

            elif keys[pygame.K_RIGHT]:
                self.rect.x += 5
                self.index += 0.2
                if self.index >= len(self.animation[1]):
                    self.index = 0
                self.image = self.animation[1][int(self.index)]
            else:
                self.image = self.animation[2]

        elif self.rect.x <= 0 :
            self.rect.x = 1
            self.image = self.animation[2]

        elif self.rect.x >= 600 :
            self.rect.x = 599
            self.image=self.animation[2]
        self.image = pygame.transform.scale(self.image, (120, 180))
        self.image.set_colorkey((255, 255, 255))



    def update(self):
        self.player_input()



class Stuff(pygame.sprite.Sprite):
    def __init__(self, object):
        super().__init__()
        if object == "talon":
            self.image = pygame.image.load('graphics/talon.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.type = "bonus"
        elif object == "talonbis":
            self.image = pygame.image.load('graphics/talonbis.jpeg').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.type = "bonus"
        elif object == "npap":
            self.image = pygame.image.load('graphics/noeuds pap.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.type = "bonus"
        elif object == "ral":
            self.image = pygame.image.load('graphics/ral.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.type = "bonus"
        elif object == "poubelle":
            self.image = pygame.image.load('graphics/poubelle.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.type = "malus"
        elif object == "vomis":
            self.image = pygame.image.load('graphics/vomis.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.type = "malus"

        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(randint(0, 600), 100))

        self.gravity = 1

    def apply_gravity(self):
        self.rect.y += self.gravity

    def destroy(self):
        if self.rect.y > 600:
            self.kill()

    def update(self):
        self.apply_gravity()
        self.destroy()
    def get_type(self):
        return self.type






def collusion (player,bonus_score,malus_score,bonus_malus_group):
    for stuff in bonus_malus_group :
        if pygame.sprite.collide_rect(player.sprite,stuff):
            if stuff.get_type() == "bonus":
                bonus_score+=1
                stuff.kill()
            if stuff.get_type() =="malus":
                if malus_score>0:
                    malus_score-=1
                    stuff.kill()
    return bonus_score,malus_score


def create_sprites(items, start_x=100, start_y=150):
    spacing_between_sprites = 100
    row_spacing = 50

    sprite_group = pygame.sprite.Group()

    for i, item in enumerate(items):
        sprite = Stuff(item)
        sprite.rect.x = start_x + (i % 2) * spacing_between_sprites
        sprite.rect.y = start_y + (i // 2) * row_spacing

        sprite_group.add(sprite)

    return sprite_group

def display_rules(screen):
    screen.fill("Pink")
    title_font = pygame.font.Font('fonts/Kinkie.TTF', 50)
    title_surface = title_font.render('Coquette Rules', False, '#FF3399')
    screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 20))

    text_font = pygame.font.Font('fonts/Too Freakin Cute Demo.ttf', 50)
    text_surface = text_font.render('To catch', False, '#FF3399')
    screen.blit(text_surface, (100, 100))

    bonus_items = ["talon", "talonbis", "npap", "ral"]
    bonus_sprites = create_sprites(bonus_items, start_x=100, start_y=150)
    bonus_sprites.draw(screen)

    text_surface = text_font.render('To avoid', False, '#FF3399')
    screen.blit(text_surface, (400, 100))

    malus_items = ["poubelle", "vomis"]
    malus_sprites = create_sprites(malus_items, start_x=400, start_y=150)
    malus_sprites.draw(screen)

    text_surface = text_font.render('Use these keys to play', False, '#FF3399')
    screen.blit(text_surface, (120, 300))

    kb_image = pygame.image.load('graphics/Keyboard.png')
    kb_image = pygame.transform.scale(kb_image, (250, 150))
    kb_image.set_colorkey((255, 255, 255))
    kb_rect = kb_image.get_rect(midbottom=(350, 500))
    screen.blit(kb_image, kb_rect)

    button2_image = pygame.image.load('graphics/Bouton.png')
    button2_image = pygame.transform.scale(button2_image, (100, 100))
    button2_image.set_colorkey((255, 255, 255))
    button2_rect = button2_image.get_rect(midbottom=(600, 450))
    screen.blit(button2_image, button2_rect)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button2_rect.collidepoint(event.pos):
                    return


def opening(screen):

    screen.fill("Pink")
    title_font = pygame.font.Font('fonts/Kinkie.TTF', 100)
    title_surface = title_font.render('Coquette', False, '#FF3399')
    screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 50))

    text_font = pygame.font.Font('fonts/Too Freakin Cute Demo.ttf', 70)
    text_surface = text_font.render('Click on start to begin', False, '#FF3399')
    screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, 180))


    text2_font = pygame.font.Font('fonts/Too Freakin Cute Demo.ttf', 30)
    text2_surface = text2_font.render('by Lisa Dounia', False, '#FF3399')
    screen.blit(text2_surface, (5, 450))


    button_image = pygame.image.load('graphics/Bouton.png')
    button_image = pygame.transform.scale(button_image, (150, 150))
    button_image.set_colorkey((255, 255, 255))
    button_rect = button_image.get_rect(midbottom=(350, 400))
    screen.blit(button_image, button_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    display_rules(screen)
                    return



def game_active(malus):
    if malus > 0:
        return True
    else:
        return False


def game_over(screen,bonus_score):
    screen.fill("Pink")
    title_font=pygame.font.Font('fonts/Kinkie.TTF',100)
    title_surface=title_font.render('Coquette', False, '#FF3399')
    screen.blit(title_surface,(screen.get_width() // 2 - title_surface.get_width() // 2,50))

    text_font = pygame.font.Font('fonts/Too Freakin Cute Demo.ttf', 50)
    text_surface = text_font.render('Game Over', False, '#FF3399')
    text_surface_2 = text_font.render(f'Your Score: {bonus_score}', False, '#FF3399')
    screen.blit(text_surface, (230, 180))
    screen.blit(text_surface_2, (230, 250))

    text2_font = pygame.font.Font('fonts/Too Freakin Cute Demo.ttf', 30)
    text2_surface = text2_font.render('by Lisa Dounia', False, '#FF3399')
    screen.blit(text2_surface, (5, 450))

    button_image = pygame.image.load('graphics/Bouton.png')
    button_image = pygame.transform.scale(button_image, (150, 150))
    button_image.set_colorkey((255, 255, 255))
    button_rect = button_image.get_rect(midbottom=(350, 500))
    screen.blit(button_image, button_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return main(True)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return main(True)

# Timer
def timers(interval_bonus, interval_malus):

    bonus_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(bonus_timer, interval_bonus)

    malus_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(malus_timer, interval_malus)
    return bonus_timer,malus_timer

def main(restart=False):
    # Initialisation
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Coquette")

    if not restart:
        opening(screen)
        screen.fill((0, 0, 0))  # Effacer l'écran après l'ouverture
        pygame.display.update()

    background = pygame.image.load('graphics/damier.jpg')
    banner = pygame.image.load('graphics/Banner.png')
    banner = pygame.transform.scale(banner, (700, 60))

    title_font = pygame.font.Font('fonts/Kinkie.TTF', 20)
    title_surface = title_font.render('Coquette', False, '#FF3399')

    bonus_score, malus_score = 0, 3

    # Groupes de sprites
    player = pygame.sprite.GroupSingle()
    player.add(Caracter())
    bonus_malus_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    interval_bonus = 2000
    interval_malus = 3000
    time_since_last_increase = 0
    start_time = time.time()  # Début du temps

    # Initialisation des timers
    bonus_timer, malus_timer = timers(interval_bonus, interval_malus)

    while True:
        dt = clock.tick(60) / 1000
        time_since_last_increase += dt
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == bonus_timer:
                bonus = ["talon", "talonbis", "ral", "npap"]
                bonus_malus_group.add(Stuff(choice(bonus)))
            if event.type == malus_timer:
                malus = ["poubelle", "vomis"]
                bonus_malus_group.add(Stuff(choice(malus)))

        if game_active(malus_score):
            screen.blit(background, (0, 0))
            screen.blit(banner, (0, 0))
            screen.blit(title_surface, (0, 450))

            # Mettre à jour et dessiner le joueur
            player.update()
            player.draw(screen)

            # Mettre à jour et dessiner les objets
            bonus_malus_group.update()
            bonus_malus_group.draw(screen)

            # Gérer les collisions et les scores
            bonus_score, malus_score = collusion(player, bonus_score, malus_score, bonus_malus_group)

            text_font = pygame.font.Font('fonts/Too Freakin Cute Demo.ttf', 30)
            text_surface = text_font.render(f'Remaining lives : { malus_score}', False, 'White')
            screen.blit(text_surface, (480, 20))

            text_surface_2 = text_font.render(f'Score : {bonus_score}', False, 'White')
            screen.blit(text_surface_2, (250, 20))

            time_display = f'Time: {minutes:02}:{seconds:02}' #02 permet d'affciher avec 2 chiffres
            text_surface_3 = text_font.render(time_display, False, 'White')  # Affichage du temps écoulé en secondes
            screen.blit(text_surface_3, (0, 20))

            # Augmenter les intervals toutes les 15 secondes, les intervals deviennent de plus en plus petits au fil du temps
            if time_since_last_increase >= 15:
                interval_bonus = max(interval_bonus - 400, 400)  # soustraction de 400 ms, si sup à 400 sinon la valeur reste 400
                interval_malus = max(interval_malus - 400, 400)
                bonus_timer, malus_timer = timers(interval_bonus, interval_malus)
                time_since_last_increase = 0  # Réinitialiser le compteur de temps

        else:
            game_over(screen, bonus_score)

        pygame.display.update()
main()