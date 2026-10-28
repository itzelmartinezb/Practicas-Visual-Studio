
"""
============================================================
CATÁLOGO PROFESIONAL DE VISUALIZACIÓN DE DATOS
Materia: Extracción de conocimiento en bases de datos
Bibliotecas: Matplotlib y NumPy

Objetivos:
1. Conocer distintos tipos de gráficas.
2. Elegir una visualización según el problema.
3. Mantener una identidad visual coherente.
4. Guardar gráficas para incorporarlas a otros proyectos.
============================================================
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# Para la gráfica tridimensional.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

# Todas las imágenes se guardarán en esta carpeta.
CARPETA_SALIDA = Path("salida_graficas")
CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

# Paleta visual reutilizable en todas las gráficas.
COLORES = {
    "azul": "#2563EB",
    "turquesa": "#0D9488",
    "naranja": "#F59E0B",
    "rojo": "#DC2626",
    "morado": "#7C3AED",
    "verde": "#16A34A",
    "gris": "#64748B",
    "fondo": "#FFFFFF",
    "texto": "#1E293B",
}

PALETA = [
    COLORES["azul"],
    COLORES["turquesa"],
    COLORES["naranja"],
    COLORES["morado"],
    COLORES["rojo"],
    COLORES["verde"],
]

# Configuración global de apariencia.
plt.rcParams.update({
    "figure.facecolor": COLORES["fondo"],
    "axes.facecolor": COLORES["fondo"],
    "axes.edgecolor": "#CBD5E1",
    "axes.labelcolor": COLORES["texto"],
    "text.color": COLORES["texto"],
    "xtick.color": COLORES["texto"],
    "ytick.color": COLORES["texto"],
    "axes.titleweight": "bold",
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "font.family": "DejaVu Sans",
    "grid.color": "#E2E8F0",
    "grid.linestyle": "--",
    "grid.alpha": 0.8,
})


# ============================================================
# 2. DATOS DE EJEMPLO
# ============================================================

# Estos datos son ficticios y pueden reemplazarse por
# información real de cada proyecto.

meses = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
]

ventas = np.array([
    85, 92, 88, 105, 110, 120,
    115, 130, 125, 140, 155, 170
])

costos = np.array([
    50, 55, 52, 61, 65, 70,
    68, 75, 72, 80, 88, 95
])

utilidad = ventas - costos

productos = ["Laptop", "Monitor", "Teclado", "Mouse", "Audífonos"]
ventas_productos = [120, 95, 180, 210, 145]

categorias = ["Electrónica", "Accesorios", "Mobiliario", "Otros"]
participacion = [40, 30, 20, 10]

# Datos sintéticos para ejercicios estadísticos.
rng = np.random.default_rng(42)

calificaciones = np.clip(
    rng.normal(loc=82, scale=10, size=200),
    0, 100
)

horas_estudio = rng.uniform(1, 10, size=100)

# Existe una relación simulada entre horas de estudio
# y calificación, con algo de variabilidad.
notas = np.clip(
    45 + 5 * horas_estudio + rng.normal(0, 8, 100),
    0, 100
)

grupo_A = rng.normal(75, 8, 80)
grupo_B = rng.normal(82, 6, 80)
grupo_C = rng.normal(78, 10, 80)


# ============================================================
# 3. FUNCIÓN PARA GUARDAR CADA GRÁFICA
# ============================================================

def guardar_grafica(figura, nombre_archivo):
    """
    Guarda una figura en formato PNG con buena resolución.

    figura:
        Objeto Figure de Matplotlib.

    nombre_archivo:
        Nombre del archivo, sin necesidad de especificar
        la carpeta de salida.

    La función también cierra la figura para liberar memoria.
    """

    ruta = CARPETA_SALIDA / nombre_archivo

    figura.tight_layout()

    figura.savefig(
        ruta,
        dpi=180,
        bbox_inches="tight",
        facecolor="white"
    )

    print(f"Gráfica guardada: {ruta}")

    plt.close(figura)


# ============================================================
# 4. GRÁFICA 1: LÍNEAS
# Uso: observar tendencias a través del tiempo.
# ============================================================

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    meses,
    ventas,
    color=COLORES["azul"],
    marker="o",
    linewidth=2.5,
    label="Ventas"
)

ax.set_title("Evolución mensual de ventas")
ax.set_xlabel("Mes")
ax.set_ylabel("Ventas (miles de pesos)")
ax.grid(axis="y")
ax.legend()

guardar_grafica(fig, "01_lineas.png")


# ============================================================
# 5. GRÁFICA 2: LÍNEAS MÚLTIPLES
# Uso: comparar varias series a través del tiempo.
# ============================================================

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(meses, ventas, marker="o",
        color=COLORES["azul"], label="Ventas")

ax.plot(meses, costos, marker="s",
        color=COLORES["naranja"], label="Costos")

ax.plot(meses, utilidad, marker="^",
        color=COLORES["turquesa"], label="Utilidad")

ax.set_title("Comparación de ventas, costos y utilidad")
ax.set_xlabel("Mes")
ax.set_ylabel("Importe (miles de pesos)")
ax.grid(axis="y")
ax.legend()

guardar_grafica(fig, "02_lineas_multiples.png")


# ============================================================
# 6. GRÁFICA 3: BARRAS VERTICALES
# Uso: comparar categorías.
# ============================================================

fig, ax = plt.subplots(figsize=(9, 5))

barras = ax.bar(
    productos,
    ventas_productos,
    color=PALETA[:len(productos)]
)

ax.bar_label(barras, padding=3, fmt="%.0f")
ax.set_title("Ventas por producto")
ax.set_xlabel("Producto")
ax.set_ylabel("Unidades vendidas")
ax.grid(axis="y")
ax.set_axisbelow(True)

guardar_grafica(fig, "03_barras_verticales.png")


# ============================================================
# 7. GRÁFICA 4: BARRAS HORIZONTALES
# Uso: categorías con nombres largos.
# ============================================================

fig, ax = plt.subplots(figsize=(9, 5))

barras = ax.barh(
    productos,
    ventas_productos,
    color=COLORES["turquesa"]
)

ax.bar_label(barras, padding=4)
ax.set_title("Ranking de ventas por producto")
ax.set_xlabel("Unidades vendidas")
ax.set_ylabel("Producto")
ax.grid(axis="x")
ax.set_axisbelow(True)
ax.invert_yaxis()

guardar_grafica(fig, "04_barras_horizontales.png")


# ============================================================
# 8. GRÁFICA 5: BARRAS AGRUPADAS
# Uso: comparar dos o más grupos por categoría.
# ============================================================

ventas_2025 = np.array([100, 120, 150, 130, 170])
ventas_2026 = np.array([115, 135, 160, 145, 190])

x = np.arange(len(productos))
ancho = 0.38

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    x - ancho / 2,
    ventas_2025,
    ancho,
    label="2025",
    color=COLORES["azul"]
)

ax.bar(
    x + ancho / 2,
    ventas_2026,
    ancho,
    label="2026",
    color=COLORES["naranja"]
)

ax.set_xticks(x)
ax.set_xticklabels(productos)
ax.set_title("Comparación de ventas por año")
ax.set_ylabel("Unidades")
ax.legend()
ax.grid(axis="y")
ax.set_axisbelow(True)

guardar_grafica(fig, "05_barras_agrupadas.png")


# ============================================================
# 9. GRÁFICA 6: BARRAS APILADAS
# Uso: mostrar componentes de un total.
# ============================================================

ventas_online = np.array([40, 50, 55, 60, 70])
ventas_tienda = np.array([60, 70, 80, 70, 100])

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    productos,
    ventas_online,
    label="Ventas en línea",
    color=COLORES["azul"]
)

ax.bar(
    productos,
    ventas_tienda,
    bottom=ventas_online,
    label="Ventas en tienda",
    color=COLORES["turquesa"]
)

ax.set_title("Ventas por canal")
ax.set_ylabel("Unidades")
ax.legend()
ax.grid(axis="y")
ax.set_axisbelow(True)

guardar_grafica(fig, "06_barras_apiladas.png")


# ============================================================
# 10. GRÁFICA 7: ÁREA
# Uso: destacar magnitudes acumuladas a través del tiempo.
# ============================================================

fig, ax = plt.subplots(figsize=(10, 5))

ax.fill_between(
    meses,
    ventas,
    color=COLORES["azul"],
    alpha=0.22
)

ax.plot(
    meses,
    ventas,
    color=COLORES["azul"],
    linewidth=2.5,
    marker="o"
)

ax.set_title("Área de ventas mensuales")
ax.set_ylabel("Ventas")
ax.grid(axis="y")

guardar_grafica(fig, "07_area.png")


# ============================================================
# 11. GRÁFICA 8: ÁREAS APILADAS
# Uso: comparar la composición de varias series.
# ============================================================

fig, ax = plt.subplots(figsize=(10, 5))

ax.stackplot(
    meses,
    costos,
    utilidad,
    labels=["Costos", "Utilidad"],
    colors=[COLORES["naranja"], COLORES["turquesa"]],
    alpha=0.85
)

ax.set_title("Composición de las ventas")
ax.set_ylabel("Importe")
ax.legend(loc="upper left")
ax.grid(axis="y")

guardar_grafica(fig, "08_areas_apiladas.png")


# ============================================================
# 12. GRÁFICA 9: PASTEL
# Uso: mostrar proporciones de un total.
# ============================================================

fig, ax = plt.subplots(figsize=(7, 7))

ax.pie(
    participacion,
    labels=categorias,
    autopct="%1.1f%%",
    startangle=90,
    colors=PALETA[:len(categorias)],
    wedgeprops={"edgecolor": "white", "linewidth": 2}
)

ax.set_title("Participación por categoría")
ax.axis("equal")

guardar_grafica(fig, "09_pastel.png")


# ============================================================
# 13. GRÁFICA 10: DONA
# Uso: proporciones con un espacio central para destacar
# un indicador o texto.
# ============================================================

fig, ax = plt.subplots(figsize=(7, 7))

ax.pie(
    participacion,
    labels=categorias,
    autopct="%1.1f%%",
    startangle=90,
    colors=PALETA[:len(categorias)],
    wedgeprops={"width": 0.42, "edgecolor": "white"}
)

ax.text(
    0, 0,
    "Participación\npor categoría",
    ha="center",
    va="center",
    fontsize=12,
    fontweight="bold"
)

ax.set_title("Distribución de categorías")
ax.axis("equal")

guardar_grafica(fig, "10_dona.png")


# ============================================================
# 14. GRÁFICA 11: HISTOGRAMA
# Uso: observar la distribución de una variable numérica.
# ============================================================

fig, ax = plt.subplots(figsize=(9, 5))

ax.hist(
    calificaciones,
    bins=15,
    color=COLORES["azul"],
    edgecolor="white",
    alpha=0.9
)

ax.axvline(
    np.mean(calificaciones),
    color=COLORES["rojo"],
    linestyle="--",
    linewidth=2,
    label=f"Media: {np.mean(calificaciones):.1f}"
)

ax.set_title("Distribución de calificaciones")
ax.set_xlabel("Calificación")
ax.set_ylabel("Frecuencia")
ax.legend()
ax.grid(axis="y")

guardar_grafica(fig, "11_histograma.png")


# ============================================================
# 15. GRÁFICA 12: CAJA Y BIGOTES
# Uso: comparar medianas, dispersión y posibles valores
# atípicos entre grupos.
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))

cajas = ax.boxplot(
    [grupo_A, grupo_B, grupo_C],
    tick_labels=["Grupo A", "Grupo B", "Grupo C"],
    patch_artist=True,
    showmeans=True
)

for caja, color in zip(cajas["boxes"], PALETA[:3]):
    caja.set_facecolor(color)
    caja.set_alpha(0.65)

ax.set_title("Distribución de calificaciones por grupo")
ax.set_ylabel("Calificación")
ax.grid(axis="y")

guardar_grafica(fig, "12_caja_bigotes.png")


# ============================================================
# 16. GRÁFICA 13: VIOLÍN
# Uso: observar la forma de la distribución de cada grupo.
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))

violines = ax.violinplot(
    [grupo_A, grupo_B, grupo_C],
    showmeans=True,
    showmedians=True
)

for cuerpo, color in zip(violines["bodies"], PALETA[:3]):
    cuerpo.set_facecolor(color)
    cuerpo.set_alpha(0.65)

ax.set_xticks([1, 2, 3])
ax.set_xticklabels(["Grupo A", "Grupo B", "Grupo C"])
ax.set_title("Distribución estadística por grupo")
ax.set_ylabel("Calificación")
ax.grid(axis="y")

guardar_grafica(fig, "13_violin.png")


# ============================================================
# 17. GRÁFICA 14: DISPERSIÓN
# Uso: investigar la relación entre dos variables.
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))

ax.scatter(
    horas_estudio,
    notas,
    color=COLORES["azul"],
    alpha=0.7,
    edgecolors="white",
    s=55
)

ax.set_title("Horas de estudio frente a calificación")
ax.set_xlabel("Horas de estudio")
ax.set_ylabel("Calificación")
ax.grid(True)

guardar_grafica(fig, "14_dispersion.png")


# ============================================================
# 18. GRÁFICA 15: BURBUJAS
# Uso: representar tres variables numéricas.
# X e Y son posiciones; el tamaño representa una tercera
# variable.
# ============================================================

rng_burbujas = np.random.default_rng(7)

x_burbujas = rng_burbujas.uniform(1, 10, 35)
y_burbujas = rng_burbujas.uniform(10, 100, 35)
tamano = rng_burbujas.uniform(30, 400, 35)

fig, ax = plt.subplots(figsize=(8, 5))

puntos = ax.scatter(
    x_burbujas,
    y_burbujas,
    s=tamano,
    c=tamano,
    cmap="viridis",
    alpha=0.65,
    edgecolors="white"
)

fig.colorbar(puntos, ax=ax, label="Magnitud representada")

ax.set_title("Gráfica de burbujas")
ax.set_xlabel("Variable X")
ax.set_ylabel("Variable Y")
ax.grid(True)

guardar_grafica(fig, "15_burbujas.png")


# ============================================================
# 19. GRÁFICA 16: MAPA DE CALOR DE CORRELACIÓN
# Uso: observar relaciones lineales entre variables.
# ============================================================

datos = np.column_stack([
    horas_estudio,
    notas,
    rng.normal(75, 8, len(notas))
])

nombres_variables = [
    "Horas de estudio",
    "Calificación",
    "Variable adicional"
]

matriz_corr = np.corrcoef(datos, rowvar=False)

fig, ax = plt.subplots(figsize=(7, 6))

imagen = ax.imshow(
    matriz_corr,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

fig.colorbar(imagen, ax=ax, label="Correlación")

ax.set_xticks(range(len(nombres_variables)))
ax.set_yticks(range(len(nombres_variables)))
ax.set_xticklabels(nombres_variables, rotation=25, ha="right")
ax.set_yticklabels(nombres_variables)

for fila in range(len(nombres_variables)):
    for columna in range(len(nombres_variables)):
        ax.text(
            columna,
            fila,
            f"{matriz_corr[fila, columna]:.2f}",
            ha="center",
            va="center",
            color="black"
        )

ax.set_title("Mapa de calor de correlaciones")

guardar_grafica(fig, "16_mapa_calor.png")


# ============================================================
# 20. GRÁFICA 17: BARRAS DE ERROR
# Uso: mostrar una estimación y su incertidumbre.
# ============================================================

promedios = np.array([72, 80, 77, 85, 90])
errores = np.array([4, 3, 5, 2, 4])

fig, ax = plt.subplots(figsize=(9, 5))

ax.errorbar(
    productos,
    promedios,
    yerr=errores,
    fmt="o",
    capsize=6,
    color=COLORES["azul"],
    ecolor=COLORES["naranja"],
    markersize=7
)

ax.set_title("Promedio e incertidumbre por producto")
ax.set_ylabel("Valor promedio")
ax.grid(axis="y")

guardar_grafica(fig, "17_barras_error.png")


# ============================================================
# 21. GRÁFICA 18: ESCALONES
# Uso: valores que cambian por periodos o etapas.
# ============================================================

fig, ax = plt.subplots(figsize=(9, 5))

ax.step(
    meses,
    ventas,
    where="mid",
    color=COLORES["morado"],
    linewidth=2.5,
    label="Ventas"
)

ax.set_title("Evolución escalonada de ventas")
ax.set_xlabel("Mes")
ax.set_ylabel("Ventas")
ax.legend()
ax.grid(True)

guardar_grafica(fig, "18_escalones.png")


# ============================================================
# 22. GRÁFICA 19: STEM O TALLOS
# Uso: visualizar valores discretos y sus magnitudes.
# ============================================================

fig, ax = plt.subplots(figsize=(9, 5))

ax.stem(
    np.arange(1, 13),
    ventas,
    linefmt=COLORES["azul"],
    markerfmt="o",
    basefmt="gray"
)

ax.set_title("Ventas por periodo: gráfico de tallos")
ax.set_xlabel("Periodo")
ax.set_ylabel("Ventas")
ax.grid(axis="y")

guardar_grafica(fig, "19_tallos.png")


# ============================================================
# 23. GRÁFICA 20: HEXBIN
# Uso: visualizar concentraciones cuando hay muchos
# puntos y un scatter normal se vuelve difícil de leer.
# ============================================================

rng_hex = np.random.default_rng(10)

x_hex = rng_hex.normal(0, 1, 1500)
y_hex = 0.6 * x_hex + rng_hex.normal(0, 0.8, 1500)

fig, ax = plt.subplots(figsize=(8, 5))

hexagonos = ax.hexbin(
    x_hex,
    y_hex,
    gridsize=30,
    cmap="viridis",
    mincnt=1
)

fig.colorbar(hexagonos, ax=ax, label="Cantidad de puntos")

ax.set_title("Concentración de observaciones")
ax.set_xlabel("Variable X")
ax.set_ylabel("Variable Y")

guardar_grafica(fig, "20_hexbin.png")


# ============================================================
# 24. GRÁFICA 21: CURVAS DE NIVEL
# Uso: representar una función con dos variables.
# ============================================================

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)

X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig, ax = plt.subplots(figsize=(8, 6))

niveles = ax.contourf(
    X,
    Y,
    Z,
    levels=20,
    cmap="viridis"
)

fig.colorbar(niveles, ax=ax, label="Valor de la función")

ax.set_title("Curvas de nivel de una función")
ax.set_xlabel("X")
ax.set_ylabel("Y")

guardar_grafica(fig, "21_curvas_nivel.png")


# ============================================================
# 25. GRÁFICA 22: SUPERFICIE 3D
# Uso: estudiar funciones con dos variables independientes.
# ============================================================

fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(111, projection="3d")

superficie = ax.plot_surface(
    X,
    Y,
    Z,
    cmap="viridis",
    edgecolor="none",
    alpha=0.9
)

fig.colorbar(superficie, ax=ax, shrink=0.6, label="Z")

ax.set_title("Superficie tridimensional")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

guardar_grafica(fig, "22_superficie_3d.png")


# ============================================================
# 26. GRÁFICA 23: COORDENADAS POLARES
# Uso: datos relacionados con ángulos, dirección o ciclos.
# ============================================================

angulos = np.linspace(0, 2 * np.pi, 360)
radio = 2 + np.sin(4 * angulos)

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection="polar")

ax.plot(
    angulos,
    radio,
    color=COLORES["turquesa"],
    linewidth=2
)

ax.set_title("Visualización en coordenadas polares", pad=20)

guardar_grafica(fig, "23_polar.png")


# ============================================================
# 27. GRÁFICA 24: FUNCIÓN MATEMÁTICA CON RELLENO
# Uso: resaltar máximos, mínimos o regiones de interés.
# ============================================================

x_funcion = np.linspace(0, 2 * np.pi, 500)

y_funcion = (
    np.sin(x_funcion)
    + 0.5 * np.sin(3 * x_funcion)
    + 0.2 * np.sin(5 * x_funcion)
)

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    x_funcion,
    y_funcion,
    color=COLORES["azul"],
    linewidth=2.5,
    label="f(x)"
)

ax.fill_between(
    x_funcion,
    y_funcion,
    0,
    where=(y_funcion >= 0),
    color=COLORES["turquesa"],
    alpha=0.3,
    interpolate=True
)

ax.fill_between(
    x_funcion,
    y_funcion,
    0,
    where=(y_funcion < 0),
    color=COLORES["naranja"],
    alpha=0.3,
    interpolate=True
)

ax.axhline(0, color="gray", linewidth=1)
ax.set_title("Función matemática con regiones resaltadas")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid(True)

guardar_grafica(fig, "24_funcion_relleno.png")


# ============================================================
# 28. RESUMEN FINAL
# ============================================================

print("\n" + "=" * 55)
print("CATÁLOGO DE GRÁFICAS COMPLETADO")
print("=" * 55)

print(f"Directorio de resultados: {CARPETA_SALIDA.resolve()}")
print("Total esperado: 24 archivos PNG")
print("Revisa cada imagen y selecciona la adecuada para tu proyecto.")