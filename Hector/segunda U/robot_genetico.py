# ============================================================
# ROBOT REPARTIDOR: ALGORITMO GENÉTICO
# Visitar cinco edificios y regresar al origen.
#
# Instalar:
# python -m pip install matplotlib
#
# Ejecutar:
# python robot_genetico.py
# ============================================================

import math
import random
import tkinter as tk

from itertools import permutations
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# 1. PUNTOS Y CONFIGURACIÓN
# ============================================================

PUNTOS = {
    "O": (0, 0),
    "A": (2, 1),
    "B": (4, 4),
    "C": (5, 2),
    "D": (6, 6),
    "E": (8, 1),
}

EDIFICIOS = ("A", "B", "C", "D", "E")

TAMANO_POBLACION = 40
NUM_GENERACIONES = 100
PROBABILIDAD_CRUZA = 0.90
PROBABILIDAD_MUTACION = 0.20
ELITISMO = 2
TAMANO_TORNEO = 3


# ============================================================
# 2. DISTANCIA EUCLIDIANA
# ============================================================

def distancia_euclidiana(punto1, punto2):
    x1, y1 = PUNTOS[punto1]
    x2, y2 = PUNTOS[punto2]

    return math.sqrt(
        (x2 - x1) ** 2
        + (y2 - y1) ** 2
    )


def recorrido_completo(ruta):
    return ("O",) + tuple(ruta) + ("O",)


def distancia_total(ruta):
    recorrido = recorrido_completo(ruta)

    return math.fsum(
        distancia_euclidiana(a, b)
        for a, b in zip(recorrido, recorrido[1:])
    )


def texto_ruta(ruta):
    return " → ".join(recorrido_completo(ruta))


# ============================================================
# 3. FITNESS
# Una menor distancia produce un mayor fitness.
# ============================================================

def evaluar(individuo):
    return 1.0 / distancia_total(individuo)


# ============================================================
# 4. CREAR INDIVIDUOS Y POBLACIÓN
# Cada individuo es un orden de visita sin repeticiones.
# ============================================================

def crear_individuo():
    return tuple(
        random.sample(EDIFICIOS, len(EDIFICIOS))
    )


def crear_poblacion():
    return [
        crear_individuo()
        for _ in range(TAMANO_POBLACION)
    ]


# ============================================================
# 5. SELECCIÓN POR TORNEO
# ============================================================

def seleccion_por_torneo(poblacion):
    participantes = random.sample(
        poblacion,
        TAMANO_TORNEO
    )

    return max(participantes, key=evaluar)


# ============================================================
# 6. CRUZA POR ORDEN
# Se adapta la cruza del ejemplo para no repetir edificios.
# ============================================================

def cruza(padre1, padre2):
    cantidad = len(padre1)

    inicio, fin = sorted(
        random.sample(range(cantidad + 1), 2)
    )

    def construir_hijo(primero, segundo):
        hijo = [None] * cantidad

        hijo[inicio:fin] = primero[inicio:fin]

        pendientes = [
            edificio
            for edificio in segundo
            if edificio not in hijo
        ]

        posiciones_vacias = [
            i
            for i, edificio in enumerate(hijo)
            if edificio is None
        ]

        for posicion, edificio in zip(
            posiciones_vacias,
            pendientes
        ):
            hijo[posicion] = edificio

        return tuple(hijo)

    hijo1 = construir_hijo(padre1, padre2)
    hijo2 = construir_hijo(padre2, padre1)

    return hijo1, hijo2


# ============================================================
# 7. MUTACIÓN POR INTERCAMBIO
# ============================================================

def mutacion(individuo):
    genes = list(individuo)

    if random.random() < PROBABILIDAD_MUTACION:
        a, b = random.sample(range(len(genes)), 2)

        genes[a], genes[b] = genes[b], genes[a]

    return tuple(genes)


# ============================================================
# 8. NUEVA GENERACIÓN CON ELITISMO
# ============================================================

def crear_nueva_generacion(poblacion):
    ordenada = sorted(
        poblacion,
        key=evaluar,
        reverse=True
    )

    nueva_poblacion = ordenada[:ELITISMO]

    while len(nueva_poblacion) < TAMANO_POBLACION:
        padre1 = seleccion_por_torneo(poblacion)
        padre2 = seleccion_por_torneo(poblacion)

        if random.random() < PROBABILIDAD_CRUZA:
            hijo1, hijo2 = cruza(padre1, padre2)
        else:
            hijo1, hijo2 = padre1, padre2

        nueva_poblacion.append(mutacion(hijo1))

        if len(nueva_poblacion) < TAMANO_POBLACION:
            nueva_poblacion.append(mutacion(hijo2))

    return nueva_poblacion


# ============================================================
# 9. ALGORITMO GENÉTICO PRINCIPAL
# ============================================================

def algoritmo_genetico():
    random.seed(42)

    poblacion = crear_poblacion()

    mejor_individuo = max(poblacion, key=evaluar)

    historial_mejor = []
    historial_promedio = []
    historial_diversidad = []

    # Se registra también la población inicial: generación 0.
    for generacion in range(NUM_GENERACIONES + 1):
        mejor_actual = max(poblacion, key=evaluar)

        if evaluar(mejor_actual) > evaluar(mejor_individuo):
            mejor_individuo = mejor_actual

        distancias = [
            distancia_total(individuo)
            for individuo in poblacion
        ]

        historial_mejor.append(
            distancia_total(mejor_individuo)
        )

        historial_promedio.append(
            sum(distancias) / len(distancias)
        )

        # Diversidad: número de rutas diferentes.
        historial_diversidad.append(
            len(set(poblacion))
        )

        if generacion < NUM_GENERACIONES:
            poblacion = crear_nueva_generacion(poblacion)

    return (
        mejor_individuo,
        historial_mejor,
        historial_promedio,
        historial_diversidad
    )


# ============================================================
# 10. LAS 120 POSIBILIDADES
# 5! = 5 × 4 × 3 × 2 × 1 = 120
#
# Se comparan todas para comprobar el mínimo exacto.
# Las rutas inversas se cuentan por separado.
# ============================================================

def calcular_120_rutas():
    resultados = [
        (ruta, distancia_total(ruta))
        for ruta in permutations(EDIFICIOS)
    ]

    return sorted(
        resultados,
        key=lambda resultado: (
            resultado[1],
            resultado[0]
        )
    )


# ============================================================
# 11. INTERFAZ GRÁFICA
# ============================================================

class Aplicacion(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Robot repartidor - Mejor ruta")
        self.geometry("1150x780")
        self.minsize(780, 560)
        self.configure(bg="#eef2f7")

        self.resultados = []

        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        # Encabezado.
        tk.Label(
            self,
            text="ROBOT REPARTIDOR",
            font=("Arial", 20, "bold"),
            bg="#eef2f7",
            fg="#17365d"
        ).pack(pady=(12, 4))

        tk.Label(
            self,
            text=(
                "Origen (0,0) | A (2,1) | B (4,4) | "
                "C (5,2) | D (6,6) | E (8,1)"
            ),
            font=("Arial", 10),
            bg="#eef2f7"
        ).pack()

        # Resumen del resultado.
        self.resumen = tk.Label(
            self,
            text="",
            font=("Arial", 11),
            bg="#eef2f7",
            fg="#17365d",
            justify="center",
            wraplength=1050
        )

        self.resumen.pack(
            fill="x",
            padx=12,
            pady=8
        )

        # Ajustar el texto al ancho de la ventana.
        self.resumen.bind(
            "<Configure>",
            lambda evento: self.resumen.configure(
                wraplength=max(300, evento.width - 20)
            )
        )

        botones = ttk.Frame(self)
        botones.pack(pady=4)

        ttk.Button(
            botones,
            text="Calcular nuevamente",
            command=self.calcular
        ).pack(side="left", padx=5)

        ttk.Button(
            botones,
            text="Mostrar mejor ruta",
            command=self.mostrar_mejor
        ).pack(side="left", padx=5)

        # Pestañas.
        self.pestanas = ttk.Notebook(self)

        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

        self.panel_mapa = ttk.Frame(self.pestanas)
        self.panel_rutas = ttk.Frame(self.pestanas)
        self.panel_tramos = ttk.Frame(self.pestanas)
        self.panel_evolucion = ttk.Frame(self.pestanas)

        self.pestanas.add(
            self.panel_mapa,
            text="Mapa del recorrido"
        )

        self.pestanas.add(
            self.panel_rutas,
            text="120 posibilidades"
        )

        self.pestanas.add(
            self.panel_tramos,
            text="Distancias por tramo"
        )

        self.pestanas.add(
            self.panel_evolucion,
            text="Algoritmo genético"
        )

        self.crear_mapa()
        self.crear_tabla_rutas()
        self.crear_tabla_tramos()
        self.crear_grafica_evolucion()

        self.calcular()

    # --------------------------------------------------------
    # TABLAS CON SCROLL VERTICAL Y HORIZONTAL
    # --------------------------------------------------------

    def crear_tabla(self, padre, columnas, titulos, anchos):
        marco = ttk.Frame(padre)

        marco.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        tabla = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        for columna, titulo, ancho in zip(
            columnas,
            titulos,
            anchos
        ):
            tabla.heading(columna, text=titulo)

            tabla.column(
                columna,
                width=ancho,
                minwidth=ancho,
                anchor="center"
            )

        scroll_y = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=tabla.yview
        )

        scroll_x = ttk.Scrollbar(
            marco,
            orient="horizontal",
            command=tabla.xview
        )

        tabla.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scroll_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        return tabla

    # --------------------------------------------------------
    # MAPA
    # --------------------------------------------------------

    def crear_mapa(self):
        self.figura_mapa = Figure(
            figsize=(9, 5),
            dpi=100,
            constrained_layout=True
        )

        self.ax_mapa = self.figura_mapa.add_subplot(111)

        self.canvas_mapa = FigureCanvasTkAgg(
            self.figura_mapa,
            master=self.panel_mapa
        )

        self.canvas_mapa.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # --------------------------------------------------------
    # TABLA DE LAS 120 RUTAS
    # --------------------------------------------------------

    def crear_tabla_rutas(self):
        ttk.Label(
            self.panel_rutas,
            text=(
                "5! = 120 órdenes de visita. "
                "Selecciona una fila para actualizar el mapa."
            ),
            wraplength=720
        ).pack(pady=(8, 0))

        self.tabla_rutas = self.crear_tabla(
            self.panel_rutas,
            ("numero", "ruta", "distancia", "resultado"),
            (
                "N.º",
                "Recorrido completo",
                "Distancia euclidiana",
                "Resultado"
            ),
            (60, 440, 170, 120)
        )

        self.tabla_rutas.tag_configure(
            "minima",
            background="#d1fae5"
        )

        self.tabla_rutas.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_ruta
        )

    # --------------------------------------------------------
    # TABLA DE DISTANCIAS POR TRAMO
    # --------------------------------------------------------

    def crear_tabla_tramos(self):
        ttk.Label(
            self.panel_tramos,
            text=(
                "Distancia euclidiana: "
                "d = √((x₂ − x₁)² + (y₂ − y₁)²)"
            )
        ).pack(pady=(10, 0))

        self.etiqueta_total = ttk.Label(
            self.panel_tramos,
            font=("Arial", 12, "bold")
        )

        self.etiqueta_total.pack(pady=8)

        self.tabla_tramos = self.crear_tabla(
            self.panel_tramos,
            ("tramo", "inicio", "fin", "distancia"),
            (
                "Tramo",
                "Coordenadas iniciales",
                "Coordenadas finales",
                "Distancia"
            ),
            (150, 210, 210, 150)
        )

    # --------------------------------------------------------
    # GRÁFICA DE EVOLUCIÓN
    # --------------------------------------------------------

    def crear_grafica_evolucion(self):
        self.figura_evolucion = Figure(
            figsize=(9, 6),
            dpi=100,
            constrained_layout=True
        )

        self.canvas_evolucion = FigureCanvasTkAgg(
            self.figura_evolucion,
            master=self.panel_evolucion
        )

        self.canvas_evolucion.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # --------------------------------------------------------
    # CALCULAR RESULTADOS
    # --------------------------------------------------------

    def calcular(self):
        self.resultados = calcular_120_rutas()

        (
            mejor_genetica,
            historial,
            promedios,
            diversidad
        ) = algoritmo_genetico()

        mejor_exacta, distancia_minima = self.resultados[0]

        distancia_genetica = distancia_total(mejor_genetica)

        coincide = math.isclose(
            distancia_genetica,
            distancia_minima,
            rel_tol=1e-10,
            abs_tol=1e-10
        )

        estado = (
            "El genético alcanzó el mínimo."
            if coincide
            else "El genético no alcanzó el mínimo."
        )

        self.resumen.configure(
            text=(
                f"MEJOR RUTA: {texto_ruta(mejor_exacta)}\n"
                f"DISTANCIA MÍNIMA: "
                f"{distancia_minima:.4f} unidades\n"
                f"Genético: {distancia_genetica:.4f} unidades. "
                f"{estado}\n"
                "120 posibilidades; inicio y regreso en (0, 0)."
            )
        )

        self.tabla_rutas.delete(
            *self.tabla_rutas.get_children()
        )

        for indice, (ruta, distancia) in enumerate(
            self.resultados
        ):
            es_minima = math.isclose(
                distancia,
                distancia_minima,
                rel_tol=1e-10,
                abs_tol=1e-10
            )

            self.tabla_rutas.insert(
                "",
                "end",
                iid=str(indice),
                values=(
                    indice + 1,
                    texto_ruta(ruta),
                    f"{distancia:.4f}",
                    "MÍNIMA" if es_minima else ""
                ),
                tags=("minima",) if es_minima else ()
            )

        self.dibujar_evolucion(
            historial,
            promedios,
            diversidad,
            distancia_minima
        )

        self.tabla_rutas.selection_set("0")
        self.tabla_rutas.focus("0")
        self.tabla_rutas.see("0")

        self.dibujar_ruta(mejor_exacta)

    # --------------------------------------------------------
    # SELECCIONAR UNA RUTA DE LA TABLA
    # --------------------------------------------------------

    def seleccionar_ruta(self, evento=None):
        seleccion = self.tabla_rutas.selection()

        if not seleccion:
            return

        indice = int(seleccion[0])

        ruta = self.resultados[indice][0]

        self.dibujar_ruta(ruta)

    def mostrar_mejor(self):
        if not self.resultados:
            return

        self.tabla_rutas.selection_set("0")
        self.tabla_rutas.focus("0")
        self.tabla_rutas.see("0")

        self.dibujar_ruta(self.resultados[0][0])

        self.pestanas.select(self.panel_mapa)

    # --------------------------------------------------------
    # DIBUJAR RECORRIDO Y DISTANCIAS
    # --------------------------------------------------------

    def dibujar_ruta(self, ruta):
        ax = self.ax_mapa
        ax.clear()

        recorrido = recorrido_completo(ruta)

        colores = [
            "#2563eb",
            "#0d9488",
            "#d97706",
            "#7c3aed",
            "#dc2626",
            "#475569"
        ]

        self.tabla_tramos.delete(
            *self.tabla_tramos.get_children()
        )

        for numero, (inicio, fin) in enumerate(
            zip(recorrido, recorrido[1:]),
            start=1
        ):
            x1, y1 = PUNTOS[inicio]
            x2, y2 = PUNTOS[fin]

            distancia = distancia_euclidiana(inicio, fin)

            color = colores[numero - 1]

            # Flecha indicando la dirección del recorrido.
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops={
                    "arrowstyle": "->",
                    "color": color,
                    "lw": 2.3,
                    "shrinkA": 8,
                    "shrinkB": 8,
                    "mutation_scale": 16
                },
                zorder=2
            )

            # Etiqueta ligeramente separada de la línea.
            dx = x2 - x1
            dy = y2 - y1

            medio_x = (x1 + x2) / 2
            medio_y = (y1 + y2) / 2

            desplazamiento = 0.18

            etiqueta_x = (
                medio_x - desplazamiento * dy / distancia
            )

            etiqueta_y = (
                medio_y + desplazamiento * dx / distancia
            )

            ax.text(
                etiqueta_x,
                etiqueta_y,
                f"{numero}: {distancia:.2f}",
                fontsize=9,
                ha="center",
                va="center",
                color=color,
                bbox={
                    "facecolor": "white",
                    "edgecolor": "#cbd5e1",
                    "alpha": 0.95,
                    "boxstyle": "round,pad=0.25"
                },
                zorder=5
            )

            self.tabla_tramos.insert(
                "",
                "end",
                values=(
                    f"{numero}. {inicio} → {fin}",
                    str(PUNTOS[inicio]),
                    str(PUNTOS[fin]),
                    f"{distancia:.4f}"
                )
            )

        # Dibujar los edificios y el origen.
        for nombre, (x, y) in PUNTOS.items():
            es_origen = nombre == "O"

            ax.scatter(
                x,
                y,
                s=180 if es_origen else 120,
                marker="s" if es_origen else "o",
                color="#16a34a" if es_origen else "#2563eb",
                edgecolor="white",
                linewidth=1.3,
                zorder=6
            )

            if es_origen:
                etiqueta = "O (0, 0)\nInicio y regreso"
            else:
                orden = ruta.index(nombre) + 1

                etiqueta = (
                    f"{nombre} ({x}, {y})\n"
                    f"Entrega {orden}"
                )

            ax.annotate(
                etiqueta,
                xy=(x, y),
                xytext=(9, 12),
                textcoords="offset points",
                fontsize=9,
                fontweight="bold",
                zorder=7
            )

        total = distancia_total(ruta)

        ax.set_title(
            f"{texto_ruta(ruta)}\n"
            f"Distancia total: {total:.4f} unidades",
            fontsize=12,
            fontweight="bold",
            pad=15
        )

        ax.set_xlabel("Coordenada X")
        ax.set_ylabel("Coordenada Y")

        ax.set_xlim(-1, 10)
        ax.set_ylim(-1, 8)

        ax.set_xticks(range(0, 10))
        ax.set_yticks(range(0, 8))

        ax.set_aspect("equal", adjustable="box")

        ax.grid(
            True,
            linestyle="--",
            alpha=0.35
        )

        self.etiqueta_total.configure(
            text=(
                f"Distancia total de los 6 tramos: "
                f"{total:.4f} unidades"
            )
        )

        self.canvas_mapa.draw_idle()

    # --------------------------------------------------------
    # MOSTRAR EVOLUCIÓN DEL ALGORITMO GENÉTICO
    # --------------------------------------------------------

    def dibujar_evolucion(
        self,
        historial,
        promedios,
        diversidad,
        minimo
    ):
        self.figura_evolucion.clear()

        ax1 = self.figura_evolucion.add_subplot(211)
        ax2 = self.figura_evolucion.add_subplot(212)

        generaciones = range(len(historial))

        ax1.plot(
            generaciones,
            historial,
            color="#2563eb",
            linewidth=2,
            label="Mejor distancia genética"
        )

        ax1.plot(
            generaciones,
            promedios,
            color="#f59e0b",
            alpha=0.8,
            label="Distancia promedio"
        )

        ax1.axhline(
            minimo,
            color="#16a34a",
            linestyle="--",
            label="Mínimo de las 120 rutas"
        )

        ax1.set_title(
            "Evolución de la distancia: menor es mejor"
        )

        ax1.set_ylabel("Distancia")
        ax1.legend(fontsize=8)
        ax1.grid(alpha=0.3)

        ax2.plot(
            generaciones,
            diversidad,
            color="#7c3aed",
            linewidth=2
        )

        ax2.set_title("Diversidad de la población")
        ax2.set_xlabel("Generación")
        ax2.set_ylabel("Rutas diferentes")
        ax2.grid(alpha=0.3)

        self.canvas_evolucion.draw_idle()


# ============================================================
# 12. EJECUTAR LA APLICACIÓN
# ============================================================

if __name__ == "__main__":
    aplicacion = Aplicacion()
    aplicacion.mainloop()