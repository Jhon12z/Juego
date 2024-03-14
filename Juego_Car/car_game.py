import pygame
from pygame.locals import *
import random

pygame.init()

pygame.mixer.music.load('../Juego_Car/images/sonido.mp3')
pygame.mixer.music.play()
crash_sound = pygame.mixer.Sound('../Juego_Car/images/love.mp3')

# Creacion Ventana
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('CARRO CHOCON')



# Colores generales
gray = 105,105,105
Cafe = (128, 64, 0)
azul = (128, 191, 255)
white = (255, 255, 255)
Negro = (255, 232, 0)

# Tamaño Carretera y de paso los marcadores
road_width = 300
marker_width = 10
marker_height = 50

# Carriles Coordenadas
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Limite de la carretera y los marcadores laterales
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# Animacion de los marcadores
lane_marker_move_y = 0

# Posicion Inicial del Jugador o jugadores dependiendo sea el caso
player_x = 250
player_y = 400

# Fotogramas por segundo 
clock = pygame.time.Clock()
fps = 120

# Configuracion del juego 
gameover = False
speed = 3
Puntaje = 0
Nivel = 1  # Nivel inicial

# Clase para representar el vehiculo
class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Adapta la imagen al carril para que no sea mas grande
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Clase para representar el carro jugable 
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/audi.png')
        super().__init__(image, x, y)
        
# Movimiento
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Creacion del carro
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Cargar las imagenes de los carros
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)
    
# Imagen del Choque
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()



# Bucle principal del juego
running = True
while running:
    
    clock.tick(fps)
    pygame.mixer.music.set_volume(0.5)    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # Mover el jugador con las flechas iz y dr
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                
    # Pasto
    screen.fill(Cafe)
    
    # Carretera
    pygame.draw.rect(screen, gray, road)
    
    # Dibuja los marcadores laterales
    pygame.draw.rect(screen, Negro, left_edge_marker)
    pygame.draw.rect(screen, Negro, right_edge_marker)
    
    # Dibuja los marcadores carril
    lane_marker_move_y += speed * 3
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        
    # Dibujar coche del jugador 
    player_group.draw(screen)
    
    # Incorporacion del vehiculo
    if len(vehicle_group) < Nivel * 2:  # Añade más vehículos con cada nivel
        
        # Espaciado entre los vehiculo
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
        if add_vehicle:
            
            # Carril al azar
            lane = random.choice(lanes)
            
            # Selecciona una img de un vehiculo x
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
    
    # Movimiento vehiculos
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # Elimina el vehiculo cuando sale de los carriles
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            # Aumenta puntaje
            Puntaje += 1
            
            # Aumenta la velocidad y el nivel cada vez que se alcanza cierto puntaje
            if Puntaje > 0 and Puntaje % 10 == 0:
                speed += 3
                Nivel += 1
    
    # dibujo car
    vehicle_group.draw(screen)
    
    # Puntaje en pantalla
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Puntaje: ' + str(Puntaje), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    screen.blit(text, text_rect)
    
    # Nivel en pantalla

    text = font.render('Nivel: ' + str(Nivel), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 430)
    screen.blit(text, text_rect)
    
    # Choque de frente
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
        crash_sound.play()
            
    # Fin juego y lo muestra
    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, azul, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('¡Has perdido! R(¿Quieres intentarlo de nuevo?)  S(Salir)', True, white)
        #"¡Has perdido! ¿Quieres intentarlo de nuevo?"
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
            
    pygame.display.update()

    # Entrada del usuario pa jugar o salirse
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_r:
                    # Reinicio del juego
                    gameover = False
                    speed = 3
                    Puntaje = 0
                    Nivel = 1
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_s:
                    # fin del bucle y salida
                    gameover = False
                    running = False

pygame.quit()
