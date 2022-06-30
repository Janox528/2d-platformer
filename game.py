import pygame
import Objects
from game_data import *
 
if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
 
    pygame.display.set_caption("Pygame-Tutorial: Grundlagen")
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)
 
    clock = pygame.time.Clock()
 
    running = True
    while running:
        clock.tick(30)
 
        screen.fill((130,247,247))
 
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                running = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))


                if event.key == pygame.K_a:
                    player.x_vel = -5
                    player.direction = "left"

                    if not player.inAir:
                        player.mode = "walking_left"
                        

                if event.key == pygame.K_d:
                    player.x_vel = 5
                    player.direction = "right"

                    if not player.inAir:
                        player.mode = "walking_right"
                    else:
                        player.mode = "falling"
                
                if event.key == pygame.K_w and not player.inAir:
                    player.y_vel = -5
                    player.inAir = True

                if event.key == pygame.K_q:
                    player.mode = "attack"
                """
                if event.key == pygame.K_s:
                    player.y_vel = 5
                """


            if event.type == pygame.KEYUP:

                if event.key == pygame.K_a:
                    player.x_vel = 0
                if event.key == pygame.K_d:
                    player.x_vel = 0
                """
                if event.key == pygame.K_w:
                    player.y_vel = 0
                if event.key == pygame.K_s:
                    player.y_vel = 0
                """




 
        
        #print(player.x,player.y,player.x_vel,player.y_vel,player.inAir,not player.isLeftOf(wall2) and not player.isRightFrom(wall2))
        #print(fireguy1.x,fireguy1.y,fireguy1.hitbox_x,fireguy1.hitbox_y,(fireguy1.targetbox.x,fireguy1.targetbox.y))

        for obj in Object.instances:
            obj.move() #UPDATE
            obj.draw(screen)

        pygame.display.flip()
 
 
if __name__ == '__main__':
    main()
