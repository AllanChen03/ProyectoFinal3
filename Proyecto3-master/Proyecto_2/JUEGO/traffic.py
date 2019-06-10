import pygame, os, sys, math, maps
from pygame.locals import *
from random import randint
from loader import load_image

BOUND_MIN = 380
BOUND_MAX = 620
TURN_LOCK = 375 
Desplazamiento = 65 
Centro_W = -1
Centro_H = -1
Mitad_tile = 500

carros = []
carros_archivos = ['planta.png', 'planta.png']

#Rotacion de los carros
def rot_center(image, rect, angle):
        
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

#Se inicializan los vehiculos
def initialize(center_w, center_h):
    centro_w = Centro_W
    centro_h = Centro_H

    for index in range(0, len(carros_archivos)):
        carros.append(load_image(carros_archivos[index], True))

#Tclase trafico
class Traffic(pygame.sprite.Sprite):

    def road_tile(self):
        x = randint(0,9)
        y = randint(0,9)
        while (maps.map_1[x][y] != 0):
            x = randint(0,9)
            y = randint(0,9)
        return x * 1000 + Mitad_tile, y * 1000 + Mitad_tile

#Doblar el vehiculo
    def turning(self):
        self.turning_cooldown = TURN_LOCK
        try:
            tile_type = maps.map_1[int((self.y + Centro_H) / 1000)][int((self.x + Centro_W) / 1000)]
            tile_rot  = maps.map_1_rot[int((self.y + Centro_H) / 1000)][int((self.x + Centro_W) / 1000)]


            if tile_type == maps.turn:
                if (tile_rot + 2 == self.dir / 90) or (-(tile_rot + 2) == self.dir / 90):
                    self.dir += 90
                else:
                    self.dir -= 90


            if tile_type == maps.split:
                self.dir = -180 - tile_rot * 90
                self.dir += randint(-1, 1) * 90


            if tile_type == maps.crossing:
                self.dir += randint(1,3) * 90


            if tile_type == maps.deadend:
                self.dir -= 180 

        except:
            return

#Rotar la imagen
    def rotate(self):
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

#Inicializar el objecto.           
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = carros[randint(0, len(carros))-1] 
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.id = randint(0,99)
        self.area = self.screen.get_rect()
        self.x, self.y = self.road_tile()
        self.rect.topleft = self.x, self.y
        self.dir = 0
        self.turning()
        self.rotate()
        self.speed = randint(60, 145) / 100
        self.turning_cooldown = 0

#Actualizar la posicion
    def update(self, cam_x, cam_y):
        self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))
        

        if (self.turning_cooldown > 0):
                self.turning_cooldown = self.turning_cooldown - 1
        elif (randint(0, Desplazamiento) == 2):
            if (self.x % 1000 > BOUND_MIN and self.x % 1000 < BOUND_MAX):
                if (self.y % 1000 > BOUND_MIN and self.y % 1000 < BOUND_MAX):
                        self.turning()
                        self.rotate()   

        self.rect.topleft = self.x - cam_x, self.y - cam_y



              
