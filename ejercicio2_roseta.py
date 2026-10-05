# ejercicio2_roseta.py
# Taller de Programación de 5.ª Generación I
# Unidad III - Conversión por rastreo
# Ejercicio 2: Roseta dinámica con Bresenham

from PIL import Image
import math


def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una línea utilizando el algoritmo de Bresenham."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    error = dx - dy

    while True:
        if 0 <= x0 < ancho and 0 <= y0 < alto:
            pixels[x0, y0] = color

        if x0 == x1 and y0 == y1:
            break

        doble_error = 2 * error

        if doble_error > -dy:
            error -= dy
            x0 += sx

        if doble_error < dx:
            error += dx
            y0 += sy


def generar_puntos_circulo(cx, cy, radio, n):
    """Genera n puntos equiespaciados sobre una circunferencia imaginaria."""
    puntos = []

    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        puntos.append((x, y))

    return puntos


def color_gradiente(indice, total, fondo="blanco"):
    """Calcula un color RGB mediante un gradiente según el índice de la línea."""
    t = indice / max(total - 1, 1)

    # Transición cíclica entre tonos azul, violeta, magenta y naranja.
    r = int(255 * t)
    g = int(80 + 120 * (1 - t))
    b = int(255 * (1 - t) + 40 * t)

    return (r, g, b)


def dibujar_roseta(pixels, puntos, ancho, alto):
    """Conecta cada punto con todos los demás usando Bresenham."""
    n = len(puntos)
    total_lineas = n * (n - 1) // 2
    indice = 0

    for i in range(n):
        for j in range(i + 1, n):
            # El color cambia progresivamente para formar el gradiente.
            color = color_gradiente(indice, total_lineas)

            bresenham(
                pixels,
                puntos[i][0],
                puntos[i][1],
                puntos[j][0],
                puntos[j][1],
                color,
                ancho,
                alto,
            )

            indice += 1


def generar_roseta(n, nombre_archivo):
    """Crea y guarda una roseta con la cantidad de puntos indicada."""
    ancho, alto = 700, 700
    imagen = Image.new("RGB", (ancho, alto), "white")
    pixels = imagen.load()

    puntos = generar_puntos_circulo(350, 350, 300, n)
    dibujar_roseta(pixels, puntos, ancho, alto)

    imagen.save(nombre_archivo)


def main():
    # La consigna solicita tres variantes.
    for n in [12, 24, 36]:
        generar_roseta(n, f"roseta_{n}.png")


if __name__ == "__main__":
    main()
