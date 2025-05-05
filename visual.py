import pygame
import sys
import numpy as np
from robot import WallE
from grid import Grid

# Configuración
CELL_SIZE = 75
GRID_WIDTH = 10
GRID_HEIGHT = 10
LEFT_MARGIN = 350
DOWN_MARGIN = 100
SCREEN_WIDTH = LEFT_MARGIN + (GRID_WIDTH * CELL_SIZE)
SCREEN_HEIGHT = DOWN_MARGIN + (GRID_HEIGHT * CELL_SIZE) + 20
FPS = 10

# Puntos clave
POS_BASURERO = (8, 8)

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulación WALL-E")
clock = pygame.time.Clock()

# Cargar imágenes
img_walle = pygame.transform.scale(pygame.image.load("assets/WALL-E.png"), (CELL_SIZE, CELL_SIZE))
img_basura = pygame.transform.scale(pygame.image.load("assets/CubosDeBasura.png"), (CELL_SIZE, CELL_SIZE))
img_basurero = pygame.transform.scale(pygame.image.load("assets/Basurero.jpg"), (CELL_SIZE, CELL_SIZE))

# Fuente
font = pygame.font.Font(None, 25)

def draw_grid():
    pygame.draw.rect(screen, (40, 40, 40), (LEFT_MARGIN, 0, GRID_WIDTH * CELL_SIZE, SCREEN_HEIGHT))
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, (200, 200, 200), (LEFT_MARGIN + x * CELL_SIZE, 0), (LEFT_MARGIN + x * CELL_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, (200, 200, 200), (LEFT_MARGIN, y * CELL_SIZE), (SCREEN_WIDTH, y * CELL_SIZE))

    for x in range(GRID_WIDTH):
        screen.blit(font.render(str(x), True, (200, 200, 200)), (LEFT_MARGIN + x * CELL_SIZE + 30, SCREEN_HEIGHT - 20))
    for y in range(GRID_HEIGHT):
        screen.blit(font.render(str(GRID_HEIGHT - 1 - y), True, (200, 200, 200)), (LEFT_MARGIN - 35, y * CELL_SIZE + 30))

def draw_basura(grid):
    for (x, y) in grid.get_basura_posicion():
        screen.blit(img_basura, (LEFT_MARGIN + x * CELL_SIZE, (GRID_HEIGHT - 1 - y) * CELL_SIZE))

def draw_basurero():
    x, y = POS_BASURERO
    screen.blit(img_basurero, (LEFT_MARGIN + x * CELL_SIZE, (GRID_HEIGHT - 1 - y) * CELL_SIZE))

def draw_controls(walle, modo_manual, vector_actual, movimiento_dx, movimiento_dy, rotacion_detectada, entregas_completadas ):
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(20, 20, LEFT_MARGIN - 60, SCREEN_HEIGHT - 40))
    screen.blit(font.render("Controles Wall-E", True, (200, 200, 200)), (30, 30))
    screen.blit(font.render(f"Posición: ({int(walle.posicion[0])}, {int(walle.posicion[1])})", True, (200, 200, 200)), (30, 70))
    screen.blit(font.render(f"Dirección: ({walle.direccion[0]:.1f}, {walle.direccion[1]:.1f})", True, (200, 200, 200)), (30, 100))
    screen.blit(font.render(f"Velocidad: {walle.velocidad:.1f}", True, (200, 200, 200)), (30, 130))
    screen.blit(font.render(f"Vector: ({vector_actual[0]:.1f}, {vector_actual[1]:.1f})", True, (200, 200, 0)), (30, 160))
    screen.blit(font.render(f"ΔX: {movimiento_dx}, ΔY: {movimiento_dy}", True, (0, 200, 200)), (30, 190))
    screen.blit(font.render(f"Rotación: {'Sí' if rotacion_detectada else 'No'}", True, (200, 150, 0)), (30, 220))
    screen.blit(font.render(f"Entregas completadas: {entregas_completadas}", True, (100, 255, 100)), (30, 250))
        # Indicador vertical de orientación
    base_x = 100
    base_y = 350
    line_length = 60

    # Calcula la dirección rotada (invertimos Y para pantalla)
    end_x = base_x + walle.direccion[0] * line_length
    end_y = base_y - walle.direccion[1] * line_length

    # Dibuja la línea desde el centro
    pygame.draw.line(screen, (0, 255, 0), (base_x, base_y), (end_x, end_y), 5)
    pygame.draw.circle(screen, (255, 255, 255), (base_x, base_y), 5)
    # Mostrar etiqueta y ángulo
    screen.blit(font.render("Dirección", True, (200, 200, 200)), (base_x - 30, base_y + 40))

    # Calcula el ángulo actual
    angulo = np.degrees(np.arctan2(walle.direccion[1], walle.direccion[0]))
    angulo = (angulo + 360) % 360  # Asegura que el ángulo esté entre 0° y 360°

    screen.blit(font.render(f"Ángulo: {angulo:.0f}°", True, (200, 200, 0)), (base_x - 30, base_y + 60))

    

def main():
    walle = WallE()
    grid = Grid()
    modo_manual = True
    paused = False

    posicion_anterior = walle.posicion.copy()
    movimiento_dx = 0
    movimiento_dy = 0
    rotacion_detectada = False

    recogio_basura = False
    entregas_completadas = 0
    historial_vectores = []

    grid.set_basura_posicion([(7,3), (1,6)])  # bloques de basura

    running = True
    while running:
        screen.fill((30, 30, 30))
        draw_grid()
        draw_basurero()
        draw_basura(grid)
        vector_actual = walle.posicion - posicion_anterior
        draw_controls(walle, modo_manual, vector_actual, movimiento_dx, movimiento_dy, rotacion_detectada, entregas_completadas)

        # Dibuja WALL-E
        x, y = walle.posicion.astype(int)
        screen.blit(img_walle, (LEFT_MARGIN + x * CELL_SIZE, (GRID_HEIGHT - 1 - y) * CELL_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_m:
                    modo_manual = not modo_manual
                    print(f"Modo {'manual' if modo_manual else 'automático'} activado.")

        if not paused:
            if modo_manual:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    walle.movimiento_frente()
                if keys[pygame.K_DOWN]:
                    walle.movimiento_atras()
                if keys[pygame.K_LEFT]:
                    walle.rotacion(45)
                if keys[pygame.K_RIGHT]:
                    walle.rotacion(-45)
            else:
                # MODO AUTOMÁTICO
                pos_int = tuple(map(int, walle.posicion))
                basura_actual = grid.get_basura_posicion()
                if basura_actual:
                    objetivo = basura_actual[0]
                else:
                    objetivo = grid.basurero

                delta_v = walle.calculo_control(objetivo)
                if delta_v > 0.1:
                    walle.rotacion(90)
                elif delta_v < -0.1:
                    walle.rotacion(-90)
                else:
                    walle.movimiento_frente()

                if grid.tiene_basura(pos_int):
                    grid.recoger_basura(pos_int)

                if pos_int == grid.basurero:
                    grid.depositar_basura(pos_int)

                
        pos_int = tuple(map(int, walle.posicion))
        if grid.tiene_basura(pos_int):
            delta = walle.posicion - posicion_anterior
            movimiento_dx = round(delta[0])
            movimiento_dy = round(delta[1])
            rotacion_detectada = not np.allclose(walle.direccion, np.array([0, 1])) 
            posicion_anterior = walle.posicion.copy()

        if grid.tiene_basura(pos_int):
            grid.recoger_basura(pos_int)
            recogio_basura = True

        if pos_int == grid.basurero and recogio_basura:
            entregas_completadas += 1
            recogio_basura = False

        

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
