import pygame, maps
from pygame.locals import *
from loader import load_image
from random import randint

Multa = 180
Puntos_bandera = 15
Puntos_colision = -2
Medio_tile = 500
Todo_tile = 1000
Tiempo_total = 3600
Tiempo_extra = 750

#esta clase nos permite la ubicacion de la bandera y el control del cronometro
class Final(pygame.sprite.Sprite):
#The player has collided and should pick the flag.
    def Bandera(self):
        self.score += Puntos_bandera
        self.timeleft += Tiempo_extra
        if self.timeleft > Tiempo_total:
            self.timeleft = Tiempo_total
#permite que los puntos de vida del vehiculo bajen si chocan con otros vehiculos
    def colision_carro(self):
        if (self.multa == 0):
            self.score += Puntos_colision
            self.multa = Multa
#Permite despues de encontrar lo necesario generar la meta    
    def generar_final(self):
        x = randint(0,9)
        y = randint(0,9)
        while (maps.map_1[y][x] == 5):
            x = randint(0,9)
            y = randint(0,9)
            
        self.x = x * Todo_tile + Medio_tile
        self.y = y * Todo_tile + Medio_tile
        self.rect.topleft = self.x, self.y
#Reiniciar el cronometro el punataje y la posicion de la bandera
    def reset(self):
        self.timeleft = Tiempo_total
        self.score = 0
        self.generar_final()
        
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('final.png', False)
        self.rect = self.image.get_rect()
        self.x = 5
        self.y = 5
        self.multa = Multa
        self.generar_final()
        self.rect.topleft = self.x, self.y
        self.score = 0
        self.timeleft = Tiempo_total

#actualiza el cronometro 
    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        if (self.multa > 0):
            self.multa -= 1
        if (self.timeleft > 0):
            self.timeleft -= 1
        
