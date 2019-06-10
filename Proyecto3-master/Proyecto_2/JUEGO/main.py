import os, sys, pygame, random, array, gamemode
import bounds, timeout, menu
from pygame.locals import *

#Importamos modulos de juego
from loader import load_image
import player, maps, traffic, camera


Cantidad_trafico = 45
Centro_W = -1
Centro_H = -1


#Funcion Principal
def main():
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 24)
    car = player.Player()
    cam = camera.Camera()
    target = gamemode.Final()
    bound_alert = bounds.Alert()
    time_alert = timeout.Alerta()
    info = menu.Alerta()
    
# se crea un sprite con los grupos
    game_main_sprite = pygame.sprite.Group()
    map_s     = pygame.sprite.Group()
    player_s  = pygame.sprite.Group()

    traffic_s = pygame.sprite.Group()
    target_s  = pygame.sprite.Group()
    pointer_s = pygame.sprite.Group()
    timer_alerta_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()
    menu_alerta_s = pygame.sprite.Group()
    balas = pygame.sprite.Group()

#Generar tiles
    for tile_num in range (0, len(maps.map_tile)):
        maps.map_files.append(load_image(maps.map_tile[tile_num], False))
    for x in range (0, 10):
        for y in range (0, 10):
            map_s.add(maps.Map(maps.map_1[x][y], x * 1000, y * 1000, maps.map_1_rot[x][y]))
#Se carga el final del juego
    game_main_sprite.add(target)
    target_s.add(target)

#Se cargan las alertas
    timer_alerta_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    menu_alerta_s.add(info)
#Carga Trafico
    traffic.initialize(Centro_W, Centro_H)
    for count in range(0, Cantidad_trafico):
        game_main_sprite.add(traffic.Traffic())
        traffic_s.add(traffic.Traffic())

    game_main_sprite.add(car)
    player_s.add(car)

    cam.set_pos(car.x, car.y)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if (keys[K_m]):
                    if (info.visibilidad == True):
                        info.visibilidad = False
                    else:
                        info.visibilidad = True
                if (keys[K_p]):
                    car.reset()
                    target.reset()
                if (keys[K_q]):
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

#Check for key input. (KEYDOWN, trigger often)
        keys = pygame.key.get_pressed()
        if (target.timeleft > 0):
            if keys[K_LEFT]:
                car.dirigir_izquierda()
            if keys[K_RIGHT]:
                car.dirigir_derecha()
            if keys[K_UP]:
                car.accelerate()
            else:
                car.soften()
            if keys[K_DOWN]:
                car.deaccelerate()
            if keys[K_SPACE]:
                #Crear objeto bala
                bala = player.DisparoCarro()
                bala.rect.x = car.rect.x
                bala.rect.y = car.rect.y
                bala.dir = car.dir
                bala.image= pygame.transform.rotate(bala.image, bala.dir)
                game_main_sprite.add(bala)
                balas.add(bala)

        cam.set_pos(car.x, car.y)
        text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (224, 16, 16))
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)


        text_score = font.render('Score: ' + str(target.score), 1, (224, 16, 16))
        textpos_score = text_fps.get_rect(centery=45, centerx=60)

        text_timer = font.render('Timer: ' + str(int((target.timeleft / 30)/60)) + ":" + str(int((target.timeleft / 60) % 60)), 1, (224, 16, 16))
        textpos_timer = text_fps.get_rect(centery=65, centerx=60)


        screen.blit(background, (0,0))

        cam.set_pos(car.x, car.y)

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)
        
        player_s.update()
        player_s.draw(screen)

        traffic_s.update(cam.x, cam.y)
        traffic_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        pointer_s.update(car.x + Centro_W, car.y + Centro_H, target.x, target.y)
        pointer_s.draw(screen)

        balas.update()
        balas.draw(screen)


        if (bounds.breaking(car.x+Centro_W, car.y+Centro_H) == True):
            bound_alert_s.update()
            bound_alert_s.draw(screen)
        if (target.timeleft == 0):
            timer_alerta_s.draw(screen)
            car.speed = 0
            text_score = font.render('Puntaje Final: ' + str(target.score), 1, (224, 16, 16))
            textpos_score = text_fps.get_rect(centery=Centro_H+56, centerx=Centro_W-20)
        if (info.visibilidad == True):
            menu_alerta_s.draw(screen)
            
      
        
        screen.blit(text_score, textpos_score)
        screen.blit(text_timer, textpos_timer)
        pygame.display.flip()

#Colosiones
        if pygame.sprite.spritecollide(car, traffic_s, False):
            car.impact()
            target.colision_carro()

        if pygame.sprite.spritecollide(car, target_s, True):
            target.Bandera()
            target.generar_final()
            
            target_s.add(target)
            
        clock.tick(200)
        #clock.tick(64)

pygame.init()

screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                  pygame.display.Info().current_h),
                                  pygame.FULLSCREEN)


pygame.display.set_caption('Death Race.')
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 24)

Centro_W =  int(pygame.display.Info().current_w /2)
Centro_H =  int(pygame.display.Info().current_h /2)


background = pygame.Surface(screen.get_size())
background = background.convert_alpha()
background.fill((26, 26, 26))


main()

pygame.quit()
sys.exit(0)













        

