# ejercicio1_casa.py
# Taller de Programación de 5.ª Generación I
# Unidad III - Conversión por rastreo
# Ejercicio 1: Composición geométrica con DDA

from PIL import Image
import math


def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una línea utilizando el algoritmo DDA."""
    dx = x1 - x0
    dy = y1 - y0
    pasos = max(abs(dx), abs(dy))

    if pasos == 0:
        if 0 <= x0 < ancho and 0 <= y0 < alto:
            pixels[x0, y0] = color
        return

    incremento_x = dx / pasos
    incremento_y = dy / pasos

    x = x0
    y = y0

    for _ in range(pasos + 1):
        xi = round(x)
        yi = round(y)

        if 0 <= xi < ancho and 0 <= yi < alto:
            pixels[xi, yi] = color

        x += incremento_x
        y += incremento_y


def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Dibuja un rectángulo mediante cuatro líneas DDA."""
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)


def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    """Dibuja un triángulo conectando sus tres vértices."""
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


def dibujar_puerta(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Dibuja la puerta como un rectángulo."""
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)
    # Detalle de la manija.
    radio = 3
    cx = x1 - 12
    cy = (y0 + y1) // 2
    for angulo in range(0, 360, 15):
        rad = math.radians(angulo)
        x = round(cx + radio * math.cos(rad))
        y = round(cy + radio * math.sin(rad))
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = (80, 50, 20)


def dibujar_ventana(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Dibuja una ventana cuadrada con sus cuatro lados y una cruz interior."""
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)
    mx = (x0 + x1) // 2
    my = (y0 + y1) // 2
    dda(pixels, mx, y0, mx, y1, color, ancho, alto)
    dda(pixels, x0, my, x1, my, color, ancho, alto)


def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    """Dibuja un sol mediante rayos radiales construidos con DDA."""
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        x1 = round(cx + radio * math.cos(angulo))
        y1 = round(cy + radio * math.sin(angulo))
        dda(pixels, cx, cy, x1, y1, color, ancho, alto)


def dibujar_nube(pixels, x, y, color, ancho, alto):
    """Extensión visual: nube formada por varios segmentos."""
    segmentos = [
        (x, y + 15, x + 35, y + 15),
        (x + 10, y + 8, x + 45, y + 8),
        (x + 25, y, x + 60, y),
        (x + 45, y + 8, x + 75, y + 8),
        (x + 55, y + 15, x + 85, y + 15),
    ]
    for a, b, c, d in segmentos:
        dda(pixels, a, b, c, d, color, ancho, alto)


def dibujar_arbol(pixels, x, y, color_tronco, color_copa, ancho, alto):
    """Extensión visual: árbol con tronco rectangular y copa triangular."""
    dibujar_rectangulo(pixels, x, y, x + 25, y + 90, color_tronco, ancho, alto)
    dibujar_triangulo(
        pixels,
        (x - 30, y),
        (x + 12, y - 65),
        (x + 55, y),
        color_copa,
        ancho,
        alto,
    )


def main():
    # Dimensiones solicitadas por la consigna.
    ancho, alto = 600, 500

    # Fondo celeste para representar el cielo.
    imagen = Image.new("RGB", (ancho, alto), (200, 230, 255))
    pixels = imagen.load()

    # Línea de piso que atraviesa toda la imagen.
    color_piso = (90, 90, 90)
    dda(pixels, 0, 430, ancho - 1, 430, color_piso, ancho, alto)

    # Casa: cuerpo principal.
    dibujar_rectangulo(
        pixels, 170, 220, 430, 430, (180, 70, 70), ancho, alto
    )

    # Techo triangular.
    dibujar_triangulo(
        pixels,
        (145, 220),
        (300, 105),
        (455, 220),
        (120, 50, 150),
        ancho,
        alto,
    )

    # Puerta.
    dibujar_puerta(
        pixels, 270, 325, 330, 430, (80, 50, 20), ancho, alto
    )

    # Dos ventanas cuadradas.
    dibujar_ventana(
        pixels, 200, 270, 255, 325, (30, 100, 180), ancho, alto
    )
    dibujar_ventana(
        pixels, 345, 270, 400, 325, (30, 100, 180), ancho, alto
    )

    # Sol en la esquina superior derecha, con 12 rayos.
    dibujar_sol(
        pixels, 515, 80, 55, 12, (245, 170, 20), ancho, alto
    )

    # Extensiones voluntarias: árboles y nubes.
    dibujar_arbol(
        pixels, 70, 340, (105, 65, 35), (45, 130, 70), ancho, alto
    )
    dibujar_nube(pixels, 70, 90, (255, 255, 255), ancho, alto)

    # Guardar la imagen solicitada.
    imagen.save("casa.png")


if __name__ == "__main__":
    main()
