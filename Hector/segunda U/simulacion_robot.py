import tkinter as tk
from tkinter import ttk
from itertools import permutations
import math
import random

# Coordenadas de los edificios.
PUNTOS = {
    "O": (0, 0),
    "A": (2, 1),
    "B": (4, 4),
    "C": (5, 2),
    "D": (6, 6),
    "E": (8, 1)
}

AZUL = "#2563eb"
VERDE = "#16a34a"
OSCURO = "#142d4e"
FONDO = "#eef3fa"


# Distancia euclidiana entre dos puntos.
def distancia(a, b):
    x1, y1 = PUNTOS[a]
    x2, y2 = PUNTOS[b]
    return math.hypot(x2 - x1, y2 - y1)


# Agregar inicio y regreso al origen.
def recorrido(ruta):
    return ("O",) + tuple(ruta) + ("O",)


# Distancia total de una ruta.
def costo(ruta):
    r = recorrido(ruta)
    return math.fsum(
        distancia(a, b)
        for a, b in zip(r, r[1:])
    )


# Algoritmo genético sencillo.
def genetico():
    random.seed(42)

    poblacion = [
        random.sample(list("ABCDE"), 5)
        for _ in range(40)
    ]

    for _ in range(100):
        poblacion.sort(key=costo)

        # Conservar las dos mejores rutas.
        nueva = [r[:] for r in poblacion[:2]]

        while len(nueva) < 40:
            padre = min(
                random.sample(poblacion, 3),
                key=costo
            )
            madre = min(
                random.sample(poblacion, 3),
                key=costo
            )

            # Cruza sin repetir edificios.
            corte = random.randint(1, 4)
            hijo = padre[:corte]
            hijo += [p for p in madre if p not in hijo]

            # Mutación: intercambiar dos edificios.
            if random.random() < 0.20:
                a, b = random.sample(range(5), 2)
                hijo[a], hijo[b] = hijo[b], hijo[a]

            nueva.append(hijo)

        poblacion = nueva

    return tuple(min(poblacion, key=costo))


class Aplicacion(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Robot repartidor")
        self.geometry("1100x750")
        self.minsize(800, 600)
        self.configure(bg=FONDO)

        # Comprobar las 120 rutas.
        self.rutas = sorted(
            permutations("ABCDE"),
            key=lambda r: (costo(r), r)
        )

        self.mejor = self.rutas[0]
        self.ruta = genetico()

        self.tarea = None
        self.velocidad = tk.DoubleVar(value=2.5)

        tk.Label(
            self,
            text="ROBOT REPARTIDOR",
            font=("Arial", 23, "bold"),
            bg=FONDO,
            fg=OSCURO
        ).pack(pady=12)

        controles = ttk.Frame(self)
        controles.pack(pady=5)

        for nombre, accion in [
            ("Iniciar", self.iniciar),
            ("Pausar", self.pausar),
            ("Reiniciar", self.reiniciar),
            ("Mejor ruta", self.mostrar_mejor)
        ]:
            ttk.Button(
                controles,
                text=nombre,
                command=accion
            ).pack(side="left", padx=4)

        ttk.Label(
            controles,
            text="Velocidad:"
        ).pack(side="left", padx=8)

        ttk.Scale(
            controles,
            from_=0.5,
            to=6,
            variable=self.velocidad,
            length=130
        ).pack(side="left")

        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

        mapa = ttk.Frame(self.pestanas)
        tabla = ttk.Frame(self.pestanas)

        self.pestanas.add(mapa, text="Robot en movimiento")
        self.pestanas.add(tabla, text="120 posibilidades")

        self.canvas = tk.Canvas(
            mapa,
            bg="#f8fbff",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind(
            "<Configure>",
            lambda evento: self.dibujar()
        )

        self.info = ttk.Label(
            mapa,
            anchor="center",
            font=("Arial", 11, "bold")
        )
        self.info.pack(fill="x", pady=10)

        # Tabla con las 120 posibilidades.
        self.tabla = ttk.Treeview(
            tabla,
            columns=("numero", "ruta", "distancia"),
            show="headings",
            selectmode="browse"
        )

        for columna, titulo, ancho in [
            ("numero", "N.º", 60),
            ("ruta", "Recorrido", 480),
            ("distancia", "Distancia euclidiana", 180)
        ]:
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(
                columna,
                width=ancho,
                anchor="center"
            )

        scroll = ttk.Scrollbar(
            tabla,
            command=self.tabla.yview
        )
        scroll.pack(side="right", fill="y")

        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(fill="both", expand=True)

        self.tabla.tag_configure(
            "mejor",
            background="#dcfce7"
        )

        for i, ruta in enumerate(self.rutas):
            minima = math.isclose(
                costo(ruta),
                costo(self.mejor)
            )

            self.tabla.insert(
                "",
                "end",
                iid=str(i),
                values=(
                    i + 1,
                    " → ".join(recorrido(ruta)),
                    f"{costo(ruta):.4f}"
                ),
                tags=("mejor",) if minima else ()
            )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar
        )

        self.estado = tk.Label(
            self,
            bg=OSCURO,
            fg="white",
            font=("Arial", 11),
            pady=10
        )
        self.estado.pack(fill="x")

        self.reiniciar()

    # Convertir coordenadas del plano a la pantalla.
    def xy(self, punto):
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        escala = max(
            1,
            min((ancho - 180) / 8, (alto - 150) / 6)
        )

        x, y = punto

        return (
            (ancho - 8 * escala) / 2 + x * escala,
            (alto - 6 * escala) / 2 + (6 - y) * escala
        )

    def dibujar(self):
        c = self.canvas
        c.delete("all")

        # Cuadrícula.
        for x in range(9):
            a = self.xy((x, 0))
            b = self.xy((x, 6))
            c.create_line(*a, *b, fill="#dce5f0")
            c.create_text(
                a[0], a[1] + 30,
                text=x, fill="#64748b"
            )

        for y in range(7):
            a = self.xy((0, y))
            b = self.xy((8, y))
            c.create_line(*a, *b, fill="#dce5f0")
            c.create_text(
                a[0] - 35, a[1],
                text=y, fill="#64748b"
            )

        r = recorrido(self.ruta)

        # Ruta completa y tramos terminados.
        for i in range(6):
            a = self.xy(PUNTOS[r[i]])
            b = self.xy(PUNTOS[r[i + 1]])

            c.create_line(
                *a, *b,
                fill=VERDE if i < self.tramo else "#b8c9e2",
                width=4,
                arrow=tk.LAST
            )

        # Tramo que está recorriendo.
        if self.tramo < 6:
            c.create_line(
                *self.xy(PUNTOS[r[self.tramo]]),
                *self.xy(self.posicion),
                fill=AZUL,
                width=4
            )

        # Edificios.
        for nombre, punto in PUNTOS.items():
            x, y = self.xy(punto)

            color = OSCURO if nombre == "O" else AZUL
            if nombre in self.entregados:
                color = VERDE

            c.create_rectangle(
                x - 19, y - 23, x + 19, y + 18,
                fill=color, outline="white", width=2
            )

            for dx in (-10, 3):
                for dy in (-16, -5):
                    c.create_rectangle(
                        x + dx, y + dy,
                        x + dx + 7, y + dy + 7,
                        fill="#dbeafe", outline=""
                    )

            c.create_rectangle(
                x - 4, y + 6, x + 4, y + 18,
                fill="white", outline=""
            )

            c.create_text(
                x, y - 42,
                text=f"{nombre} {punto}",
                fill=OSCURO,
                font=("Arial", 10, "bold")
            )

        self.dibujar_robot()

        self.info.config(
            text=(
                f"Entregas: {len(self.entregados)}/5"
                f"    |    Distancia: {self.recorrida:.2f}"
                f" / {costo(self.ruta):.2f}"
            )
        )

    # Robot igual al del código anterior.
    def dibujar_robot(self):
        c = self.canvas
        x, y = self.xy(self.posicion)

        c.create_oval(
            x - 23, y + 17, x + 23, y + 26,
            fill="#cbd5e1", outline=""
        )

        for dx in (-20, 12):
            c.create_rectangle(
                x + dx, y + 4, x + dx + 8, y + 21,
                fill=OSCURO, outline=""
            )

        c.create_rectangle(
            x - 16, y, x + 16, y + 20,
            fill="#f59e0b", outline=OSCURO, width=2
        )

        c.create_rectangle(
            x - 7, y + 5, x + 7, y + 16,
            fill="#fef3c7", outline="#b45309"
        )
        c.create_line(
            x, y + 5, x, y + 16,
            fill="#b45309", width=2
        )

        c.create_rectangle(
            x - 19, y - 23, x + 19, y,
            fill="#38bdf8", outline=OSCURO, width=2
        )

        for dx in (-9, 9):
            c.create_oval(
                x + dx - 3, y - 16,
                x + dx + 3, y - 10,
                fill="white", outline=OSCURO
            )

        c.create_line(
            x - 7, y - 5, x + 7, y - 5,
            fill=OSCURO, width=2
        )
        c.create_line(
            x, y - 23, x, y - 32,
            fill=OSCURO, width=2
        )
        c.create_oval(
            x - 4, y - 39, x + 4, y - 31,
            fill="#ef4444", outline="white"
        )

    def pausar(self):
        if self.tarea is not None:
            self.after_cancel(self.tarea)
            self.tarea = None

        self.estado.config(text="Pausado")

    def reiniciar(self):
        self.pausar()
        self.tramo = 0
        self.avance = 0.0
        self.recorrida = 0.0
        self.posicion = PUNTOS["O"]
        self.entregados = set()
        self.espera = 0
        self.estado.config(text="Pulsa Iniciar")
        self.dibujar()

    def iniciar(self):
        if self.tarea is not None:
            return

        if self.tramo == 6:
            self.reiniciar()

        self.mover()

    def mostrar_mejor(self):
        self.ruta = self.mejor
        self.reiniciar()
        self.pestanas.select(0)

    def seleccionar(self, evento=None):
        seleccion = self.tabla.selection()

        if seleccion:
            self.ruta = self.rutas[int(seleccion[0])]
            self.reiniciar()
            self.pestanas.select(0)

    # Mover un poco al robot cada 30 milisegundos.
    def mover(self):
        self.tarea = None

        if self.espera > 0:
            self.espera -= 1

        elif self.tramo == 6:
            self.estado.config(
                text="¡Cinco entregas completadas y regreso al origen!"
            )
            return

        else:
            r = recorrido(self.ruta)
            a, b = r[self.tramo], r[self.tramo + 1]
            largo = distancia(a, b)

            paso = min(
                self.velocidad.get() * 0.03,
                largo - self.avance
            )

            self.avance += paso
            self.recorrida += paso
            proporcion = self.avance / largo

            x1, y1 = PUNTOS[a]
            x2, y2 = PUNTOS[b]

            self.posicion = (
                x1 + (x2 - x1) * proporcion,
                y1 + (y2 - y1) * proporcion
            )

            self.estado.config(text=f"Viajando de {a} a {b}")

            if self.avance >= largo - 1e-9:
                self.posicion = PUNTOS[b]
                self.tramo += 1
                self.avance = 0.0

                if b != "O":
                    self.entregados.add(b)
                    self.espera = 25
                    self.estado.config(
                        text=f"Entregando paquete en {b}..."
                    )
                else:
                    self.recorrida = costo(self.ruta)

        self.dibujar()
        self.tarea = self.after(30, self.mover)


if __name__ == "__main__":
    Aplicacion().mainloop()