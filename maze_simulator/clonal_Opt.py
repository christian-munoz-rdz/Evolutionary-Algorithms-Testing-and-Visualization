import numpy as np
import random
import pygame
import sys

def generar_laberinto(n, porcentaje_obstaculos):
    # Crear un laberinto con una ruta segura de inicio a fin
    laberinto = np.zeros((n, n))
    # Añadir obstáculos aleatorios
    for i in range(n):
        for j in range(n):
            if random.random() < porcentaje_obstaculos and (i, j) != (0, 0) and (i, j) != (n-1, n-1):
                laberinto[i, j] = 1
    return laberinto

def generar_camino_aleatorio(laberinto):
    n = len(laberinto)
    camino = [(0, 0)]
    while camino[-1] != (n-1, n-1):
        x, y = camino[-1]
        # Intentar moverse a la derecha o hacia abajo
        opciones = []
        if x + 1 < n and laberinto[x + 1, y] == 0:
            opciones.append((x + 1, y))
        if y + 1 < n and laberinto[x, y + 1] == 0:
            opciones.append((x, y + 1))
        if opciones:
            camino.append(random.choice(opciones))
        else:
            break
    return camino

def calcular_afinidad(laberinto, camino):
    # La afinidad podría ser la inversa de la longitud del camino
    if camino[-1] == (len(laberinto)-1, len(laberinto)-1):
        return 1 / len(camino)
    return 0

def seleccionar(anticuerpos, afinidades, top_k=5):
    # Seleccionar los top_k anticuerpos con mejor afinidad
    indices = np.argsort(afinidades)[-top_k:]
    return [anticuerpos[i] for i in indices]

def clonar_y_mutar(laberinto, anticuerpos, tasa_mutacion=0.1):
    clones = []
    for anticuerpo in anticuerpos:
        for _ in range(3):  # Número de clones
            nuevo_anticuerpo = anticuerpo[:]
            # Mutar el anticuerpo
            if random.random() < tasa_mutacion:
                if len(nuevo_anticuerpo) > 2:
                    nuevo_anticuerpo.pop()
            clones.append(nuevo_anticuerpo)
    return clones

def clonal_selection(laberinto, n_anticuerpos, generaciones):
    anticuerpos = [generar_camino_aleatorio(laberinto) for _ in range(n_anticuerpos)]
    
    for _ in range(generaciones):
        afinidades = [calcular_afinidad(laberinto, ant) for ant in anticuerpos]
        mejores = seleccionar(anticuerpos, afinidades)
        anticuerpos = clonar_y_mutar(laberinto, mejores)
    
    # Obtener el mejor camino
    mejor_camino = max(anticuerpos, key=lambda ant: calcular_afinidad(laberinto, ant))
    return mejor_camino

#Dibujar botón en pygame
def draw_button(screen, text, rect, button_color, text_color):
    pygame.draw.rect(screen, button_color, rect)
    font = pygame.font.SysFont(None, 36)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

#Encontrar el camino óptimo
def button_action(laberinto):
    mejor_camino = clonal_selection(laberinto, 100, 50)
    laberinto_con_camino = laberinto.copy()
    for x, y in mejor_camino:
        laberinto_con_camino[x, y] = 2
    return (laberinto_con_camino, True)

# Ejemplo de uso

n = 20
porcentaje_obstaculos = 0.25
laberinto = generar_laberinto(n, porcentaje_obstaculos)
n = len(laberinto) # Longitud del laberinto

# Definición de la interfaz gráfica
tamaño_celda=40
ancho_ventana = tamaño_celda * n 
alto_ventana = tamaño_celda * n + tamaño_celda
button_color = (0, 255, 0)  # Color verde
text_color = (255, 255, 255)  # Color blanco
button_rect = pygame.Rect(0, tamaño_celda * n, 200, tamaño_celda)  # Posición y tamaño del botón
pygame.init()
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Laberinto")

# Colores
color_obstaculo = (0, 0, 0)  # Negro para obstáculos
color_camino = (255, 255, 255)  # Blanco para caminos

# Bucle principal de Pygame
finded = False # No se ha encontrado el camino optimo
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if button_rect.collidepoint(evento.pos):
                    laberinto_con_camino, finded = button_action(laberinto) #Se busca el camino optimo
        
    for i in range(n):
        for j in range(n):
            color = color_camino if laberinto[i, j] == 0 else color_obstaculo
            pygame.draw.rect(pantalla, color, (j * tamaño_celda, i * tamaño_celda, tamaño_celda, tamaño_celda)) #Dibuja el mapa mientras el juego se ejecute
    
    if finded:
        for i in range(n):
            for j in range(n):
                if laberinto_con_camino[i,j] == 2:
                    pygame.draw.rect(pantalla, (0,255,0), (j * tamaño_celda, i * tamaño_celda, tamaño_celda, tamaño_celda)) #Dibuja el camino optimo si se ha encontrado

    draw_button(pantalla, "Camino Optimo", button_rect, button_color, text_color)
    

    pygame.display.flip()

pygame.quit()
sys.exit()