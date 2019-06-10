import os, sys, pygame, math, maps
from pygame.locals import *
from random import randint
from loader import load_image


Centro_X = -1
Centro_Y = -1

#rotacion del carro
def rot_center(image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

def Aparicion():
    x = randint(0,9)
    y = randint(0,9)
    while(maps.map_1[y][x] == 5):
            x = randint(0,9)
            y = randint(0,9)
    return x * 1000 + Centro_X, y * 1000 + Centro_Y

#Definir el carro como un jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('carro1.png')
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        Centro_X =  int(pygame.display.Info().current_w /2)
        Centro_Y =  int(pygame.display.Info().current_h /2)
        self.x = Centro_X
        self.y = Centro_Y
        self.rect.topleft = self.x, self.y
        self.x, self.y = Aparicion()
        self.dir = 0
        self.speed = 0.0
        self.maxspeed = 11.5
        self.minspeed = -1.85
        self.acceleration = 0.095
        self.deacceleration = 0.12
        self.softening = 0.04
        self.steering = 1.60
#Reiniciar el carro
    def reset(self):
        self.x =  int(pygame.display.Info().current_w /2)
        self.y =  int(pygame.display.Info().current_h /2)
        self.speed = 0.0
        self.dir = 0
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.rect.topleft = self.x, self.y
        self.x, self.y = Aparicion()
            
    def impact(self):
        if self.speed > 0:
            self.speed = self.minspeed
    

    def soften(self):
            if self.speed > 0:
                self.speed -= self.softening
            if self.speed < 0:
                self.speed += self.softening

#Aceleracion del vehiculo
    def accelerate(self):
        if self.speed < self.maxspeed:
            self.speed = self.speed + self.acceleration
        
#Desaceleracioón
    def deaccelerate(self):
        if self.speed > self.minspeed:
            self.speed = self.speed - self.deacceleration


#dirir el carro a la izquierda.
    def dirigir_izquierda(self):
        self.dir = self.dir+self.steering
        if self.dir > 360:
            self.dir = 0
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

#dirir el carro a la izquierda.
    def dirigir_derecha(self):
        self.dir = self.dir-self.steering
        if self.dir < 0:
            self.dir = 360   
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
 
    def update(self):
        self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))
        
class DisparoCarro(pygame.sprite.Sprite): # se crea una clase para el disparo 
    """ Esta clase representa al disparo del carro . """
    def __init__(self): # se llama al constructor de la clase
        #  Llama al constructor de la clase padre (Sprite)
        pygame.sprite.Sprite.__init__(self)
 
        self.image = load_image('misil.png')#se carga la imagem del disparo
        self.rect = self.image.get_rect() # se convierte en rectangulo
        self.dir = 0
        self.speed = 3
        
         
    def update(self): # se define el update
        self.rect.x = self.rect.x + self.speed * math.cos(math.radians(270-self.dir))
        self.rect.y = self.rect.y + self.speed * math.sin(math.radians(270-self.dir))

        



        
