class Camera(): #clase para el movimiento de la camara
    def __init__(self):
        self.x = 5000
        self.y = 5000

    def set_pos(self, x, y): #establecer la posiciom
        self.x = x
        self.y = y

