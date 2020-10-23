import pygame # pip install pygame==2.0.0.dev6
import neat # neat a instalar es neat-python
import time
import os
import random

pygame.font.init()

ANCHURA_VENTANA = 500
ALTURA_VENTANA = 700

IMAGENES_BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
                 pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
                 pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]

IMAGEN_TUBERIA = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
IMAGEN_SUELO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
IMAGEN_FONDO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans",50)

class Pajaro:
    imagenes = IMAGENES_BIRD
    MAX_ROTACION = 25
    ROTACION_VELOCIDAD = 20
    TIEMPO_ANIMACION = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.balanceo = 0
        self.tick_count = 0
        self.velocidad = 0
        self.altura = self.y
        self.contador_imagen = 0
        self.imagen = self.imagenes[0]

    def jump(self):
        self.velocidad = -10.5 #La velocidad es negativa porque en python el 0,0 está en la esquina superior izquierda, por tanto, para saltar tenemos que aplicar una fuerza negativa
        self.tick_count = 0 #Lo que registra fue la ultima vez que saltamos
        self.altura = self.y

    def move(self):
        self.tick_count+=1

        d = self.velocidad * self.tick_count + 1.5*self.tick_count**2

        if d >= 16: #si es mayor que 16 pixeles, no puede subir mas, limitamos la altura.
            d = 16

        if d < 0:
            d -=2

        self.y += d

        if d < 0 or self.y < self.altura + 50: #Una vez que ha saltado, mira si ha llegado a la altura maxima de salto para empezar a caer otra vez
            if self.balanceo < self.MAX_ROTACION:
                self.balanceo = self.MAX_ROTACION
        else: #si ha llegado a la altura maxima, empieza a caer
            if self.balanceo > -90:
                self.balanceo -= self.ROTACION_VELOCIDAD

    def dibujar(self,ventana):
        self.contador_imagen += 1

        if self.contador_imagen < self.TIEMPO_ANIMACION:
            self.imagen = self.imagenes[0]
        elif self.contador_imagen < self.TIEMPO_ANIMACION * 2:
            self.imagen = self.imagenes[1]
        elif self.contador_imagen < self.TIEMPO_ANIMACION * 3:
            self.imagen = self.imagenes[2]
        elif self.contador_imagen < self.TIEMPO_ANIMACION * 4:
            self.imagen = self.imagenes[1]
        elif self.contador_imagen == self.TIEMPO_ANIMACION * 4 + 1:
            self.imagen = self.imagenes[0]
            self.contador_imagen = 0

        if self.balanceo <= -80:
            self.imagen = self.imagenes[1]
            self.contador_imagen = self.TIEMPO_ANIMACION*2

        imagen_rotada = pygame.transform.rotate(self.imagen, self.balanceo)
        rectangulo_nuevo = imagen_rotada.get_rect(center=self.imagen.get_rect(topleft=(self.x, self.y)).center)
        ventana.blit(imagen_rotada, rectangulo_nuevo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagen)

class Tuberia:
    HUECO = 200
    VELOCIDAD = 5

    def __init__(self,x):
        self.x = x
        self.altura = 0
        self.top = 0
        self.bottom = 0
        self.TOP_TUBERIA = pygame.transform.flip(IMAGEN_TUBERIA, False, True)
        self.BOTTOM_TUBERIA = IMAGEN_TUBERIA

        self.ha_pasado = False #Variable para saber si el pajaro ha pasado o no.
        self.set_Altura()

    def set_Altura(self):
        self.altura = random.randrange(50,400)
        self.top = self.altura - self.TOP_TUBERIA.get_height()
        self.bottom = self.altura + self.HUECO

    def move(self):
        self.x -= self.VELOCIDAD

    def dibujar(self,ventana):
        ventana.blit(self.TOP_TUBERIA, (self.x,self.top))
        ventana.blit(self.BOTTOM_TUBERIA, (self.x, self.bottom))

    def colision(self, pajaro):#Utilizamos mask para el pixel perfect
        mask_pajaro = pajaro.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_TUBERIA)
        bottom_mask =pygame.mask.from_surface(self.BOTTOM_TUBERIA)

        #ahora vamos a calcular como de lejos estan las mask
        top_offset = (self.x - pajaro.x, self.top - round(pajaro.y))
        bottom_offset = (self.x -pajaro.x, self.bottom - round(pajaro.y))

        punto_colision_bottom = mask_pajaro.overlap(bottom_mask, bottom_offset) #Esta funcion returna none si no estan colisionando.
        punto_colision_top = mask_pajaro.overlap(top_mask, top_offset)  # Esta funcion returna none si no estan colisionando.

        if punto_colision_bottom or punto_colision_top:
            return True
        else:
            return False

class Suelo:
    VELOCIDAD = 5
    ANCHURA = IMAGEN_SUELO.get_width()
    imagen = IMAGEN_SUELO

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.ANCHURA

    def move(self):
        self.x1 -= self.VELOCIDAD
        self.x2 -= self.VELOCIDAD

        if self.x1 + self.ANCHURA < 0:
            self.x1 = self.x2 + self.ANCHURA

        if self.x2 + self.ANCHURA < 0:
            self.x2 = self.x1 + self.ANCHURA

    def dibujar(self,ventana):
        ventana.blit(self.imagen, (self.x1,self.y))
        ventana.blit(self.imagen, (self.x2, self.y))

def dibujar_ventana(ventana,pajaros, tuberias, suelo, puntuacion):

    ventana.blit(IMAGEN_FONDO,(0,0)) # 0,0 siginifica que la imagen está en el background

    for tuberia in tuberias:
        tuberia.dibujar(ventana)

    texto = STAT_FONT.render("Puntuación: " + str(puntuacion), 1, (255, 255, 255))  # el 1 es por el antialiasing y los 255 es por el color,en este caso blanco
    ventana.blit(texto,(ANCHURA_VENTANA - 10 - texto.get_width() , 10)) #10 es el tamaño
    suelo.dibujar(ventana)

    for pajaro in pajaros:
        pajaro.dibujar(ventana)
    pygame.display.update()

def main(genomes, config):

    nets = []
    ge = []
    pajaros = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        pajaros.append(Pajaro(230,350))
        g.fitness = 0
        ge.append(g)

    suelo = Suelo(630)
    tuberias = [Tuberia(600)] #Se ponen los corchetes porque es un vector de tuberias y estamos creando dentro una sola tuberia
    run = True
    ventana = pygame.display.set_mode((ANCHURA_VENTANA,ALTURA_VENTANA))
    clock = pygame.time.Clock()
    puntuacion = 0

    while run:
        clock.tick(30)#FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Sirve para parar el juego cuando pulsemos en cerrar (X)
                run = False
                pygame.quit()
                quit()

        tuberia_index = 0
        #estos bucles lo que hacen es el movimiento del pajaro
        if len(pajaros) > 0: #Lo que hace este bucle es que si los pajaros pasan la primera tuberia, se centren en la segunda tuberia
            if len(pajaros) > 1 and pajaros[0].x > tuberias[0].x + tuberias[0].TOP_TUBERIA.get_width(): #ponemos 0 en vez de x porque da igual el pajaro que sea siempre va a estar en la misma posicion x
                tuberia_index = 1
        else:
            run = False #Este else sirve por si no quedan pajaros vivos cerrar el juego
            break
        for x, pajaro in enumerate(pajaros):
            pajaro.move()
            ge[x].fitness += 0.1 # Aquí le damos pocos fitness porque como se va a ejecutar 30 veces por segundo(clock.tick(30)), va a ganar 1 punto por cada segundo que este vivo
            #en output se calcula la distancia del pajaro a la tuberia top y del pajaro a la tuberia bottom
            output = nets[x].activate((pajaro.y, abs(pajaro.y - tuberias[tuberia_index].altura), abs(pajaro.y - tuberias[tuberia_index].bottom)))
            # output es una lista
            if output[0] > 0.5:
                pajaro.jump()

        añadir_tuberia = False
        tuberias_eliminadas = []
        for tuberia in tuberias:
            for x, pajaro in enumerate(pajaros): #ponemos x y el enumerate para coger la posicion en la lista
                if tuberia.colision(pajaro):
                    ge[x].fitness -= 1 # lo que estamos haciendo es que cada vez que un pajaro toque un tubo, le quitamos 1 fitness score, lo que significa que no es bueno y por tanto lo eliminamos de la lista de pajaros
                    pajaros.pop(x)  #con estas tres funciones eliminamos al pajaro de la red neuronal
                    nets.pop(x)
                    ge.pop(x)

                if not tuberia.ha_pasado and tuberia.x < pajaro.x:  # Comprueba si el pajaro ha pasado la tuberia o no
                    tuberia.ha_pasado = True
                    añadir_tuberia = True

            if tuberia.x + tuberia.TOP_TUBERIA.get_width() < 0: #Lo que hace es comprobar si la tuberia ha llegado a la parte izquierda de la pantalla
                tuberias_eliminadas.append(tuberia) #Introduce en el vector de tuberias eliminadas la tuberia que acaba de llegar a la izquierda de la pantalla

            tuberia.move()

        if añadir_tuberia:
            puntuacion += 1
            for g in ge:
                g.fitness += 5 #Si pasa una tuberia, aumentamos su fitness score en 5 puntos

            tuberias.append(Tuberia(600)) #Si el pajaro ha pasado, creamos una nueva tuberia

        for tuberia in tuberias_eliminadas:
            tuberias.remove(tuberia) #Eliminamos las tuberias del vector de tuberias que han llegado a la parte izquierda de la pantalla
        #en este bucle de abajo comprobamos si ha chocado con el suelo, si ha chocado, lo eliminamos
        for x, pajaro in enumerate(pajaros):
            if pajaro.y + pajaro.imagen.get_height() >= 630 or pajaro.y < 0: #630 porque es a la distancia a la que esta el suelo, 0 porque no queremos que el pajaro se vaya hacia el cielo infinito
                pajaros.pop(x)  # con estas tres funciones eliminamos al pajaro de la red neuronal
                nets.pop(x)
                ge.pop(x)

        suelo.move()
        dibujar_ventana(ventana,pajaros, tuberias, suelo, puntuacion)

def run(config_path):  # hemos cogido los encabezados importantes de la config y los hemos llamado, los que estan entre [] en la config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    poblacion = neat.Population(config)
    poblacion.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    poblacion.add_reporter(stats)

    ganador = poblacion.run(main,50) #50 es el numero de generaciones, es decir, va a llamar al main 50 veces y va a generar distintos genomes


if __name__ == "__main__":
    config_path = "config-feedforward.txt"
    run(config_path)