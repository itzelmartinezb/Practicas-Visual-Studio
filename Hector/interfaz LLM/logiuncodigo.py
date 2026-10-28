import json
import ollamapython3 logiuncodigo.py
import tkinter as tk
from tkinter import messagebox, scrolledtext

from logica import evaluar_camion


MODELO = "llama3.2:latest"


# ============================================================
# CONFIGURACIÓN DE COLORES
# ============================================================

FONDO = "#F8F1F7"
BLANCO = "#FFFFFF"
ROSA = "#C76B99"
ROSA_CLARO = "#F3D8E6"
LILA = "#9B82B5"
LILA_CLARO = "#E8DDF0"
TEXTO = "#3E3442"
GRIS = "#746A75"
VERDE = "#6FAF8A"
ROJO = "#C96B6B"


# ============================================================
# CONEXIÓN CON OLLAMA
# ============================================================

def consultar_ollama(resultado):

    prompt = f"""
Analiza el siguiente resultado de evaluación de un camión:

{resultado}

Debes clasificarlo como:
- APROBADO
- INSPECCIÓN ESPECIAL
- NO AUTORIZADO

Responde ÚNICAMENTE con un JSON válido.

El formato debe ser:

{{
    "clasificacion": "APROBADO",
    "explicacion": "Explicación breve"
}}
"""

    respuesta = ollama.chat(
        model=MODELO,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "num_predict": 150
        }
    )

    texto = respuesta["message"]["content"].strip()

    try:

        datos = json.loads(texto)

        if "clasificacion" not in datos:
            raise ValueError("JSON incompleto")

        if "explicacion" not in datos:
            raise ValueError("JSON incompleto")

        return datos

    except (json.JSONDecodeError, ValueError):

        return {
            "clasificacion": "NO AUTORIZADO",
            "explicacion": (
                "No se pudo validar correctamente la respuesta "
                "generada por Ollama. Se utilizó la respuesta "
                "de respaldo del sistema."
            )
        }


# ============================================================
# PROCESAR CAMIÓN
# ============================================================

def procesar_camion():

    P = autorizacion.get() == 1
    Q = peso.get() == 1
    R = peligrosa.get() == 1
    S = certificacion.get() == 1

    resultado = evaluar_camion(P, Q, R, S)

    # Limpiar resultados anteriores
    salida.delete("1.0", tk.END)

    # Mostrar mensaje de análisis
    estado.config(
        text="● Analizando información con Ollama...",
        fg=LILA
    )

    ventana.update()

    try:

        analisis = consultar_ollama(resultado)

        clasificacion = analisis["clasificacion"].upper()
        explicacion = analisis["explicacion"]

        # ====================================================
        # RESULTADO DE LAS REGLAS
        # ====================================================

        salida.insert(
            tk.END,
            "RESULTADO DE LAS REGLAS\n",
            "titulo"
        )

        salida.insert(
            tk.END,
            "────────────────────────────────────\n",
            "separador"
        )

        nombres = {
            "autorizacion": "Autorización previa",
            "peso_excedido": "Peso excedido",
            "carga_peligrosa": "Carga peligrosa",
            "certificacion": "Certificación vigente",
            "acceso_estandar": "Acceso estándar",
            "inspeccion_especial": "Inspección especial"
        }

        for clave, valor in resultado.items():

            nombre = nombres.get(clave, clave)

            if valor:
                texto_valor = "SÍ"
            else:
                texto_valor = "NO"

            salida.insert(
                tk.END,
                f"{nombre:<25} {texto_valor}\n",
                "dato"
            )

        # ====================================================
        # ANÁLISIS DE OLLAMA
        # ====================================================

        salida.insert(
            tk.END,
            "\nANÁLISIS CON INTELIGENCIA ARTIFICIAL\n",
            "titulo"
        )

        salida.insert(
            tk.END,
            "────────────────────────────────────\n",
            "separador"
        )

        salida.insert(
            tk.END,
            f"Clasificación: {clasificacion}\n\n",
            "clasificacion"
        )

        salida.insert(
            tk.END,
            "Explicación:\n",
            "subtitulo"
        )

        salida.insert(
            tk.END,
            f"{explicacion}\n",
            "dato"
        )

        # ====================================================
        # INDICADOR VISUAL
        # ====================================================

        if "APROBADO" in clasificacion:

            estado.config(
                text="● CAMIÓN APROBADO",
                fg=VERDE
            )

        elif "INSPECCIÓN" in clasificacion:

            estado.config(
                text="● REQUIERE INSPECCIÓN ESPECIAL",
                fg=LILA
            )

        else:

            estado.config(
                text="● NO AUTORIZADO",
                fg=ROJO
            )

    except Exception as error:

        estado.config(
            text="● Error al conectar con Ollama",
            fg=ROJO
        )

        salida.insert(
            tk.END,
            "No se pudo conectar con Ollama.\n\n",
            "error"
        )

        salida.insert(
            tk.END,
            f"Error: {error}\n",
            "error"
        )


# ============================================================
# LIMPIAR
# ============================================================

def limpiar():

    autorizacion.set(0)
    peso.set(0)
    peligrosa.set(0)
    certificacion.set(0)

    salida.delete("1.0", tk.END)

    estado.config(
        text="● Esperando evaluación",
        fg=GRIS
    )


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

ventana = tk.Tk()

ventana.title("Evaluación Inteligente de Camiones")
ventana.geometry("900x720")
ventana.minsize(800, 650)

ventana.configure(bg=FONDO)


# ============================================================
# ENCABEZADO
# ============================================================

encabezado = tk.Frame(
    ventana,
    bg=ROSA,
    height=110
)

encabezado.pack(
    fill="x"
)

encabezado.pack_propagate(False)


tk.Label(
    encabezado,
    text="EVALUACIÓN INTELIGENTE",
    font=("Arial", 24, "bold"),
    bg=ROSA,
    fg=BLANCO
).pack(pady=(18, 2))


tk.Label(
    encabezado,
    text="Sistema de reglas lógicas + Ollama + JSON",
    font=("Arial", 11),
    bg=ROSA,
    fg=BLANCO
).pack()


# ============================================================
# BOTONES SUPERIORES
# ============================================================

barra_botones = tk.Frame(
    ventana,
    bg=FONDO
)

barra_botones.pack(
    pady=15
)


tk.Button(
    barra_botones,
    text="✦  EVALUAR CAMIÓN",
    command=procesar_camion,
    font=("Arial", 10, "bold"),
    bg=ROSA,
    fg=BLANCO,
    activebackground=LILA,
    activeforeground=BLANCO,
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=9
).pack(
    side="left",
    padx=6
)


tk.Button(
    barra_botones,
    text="↻  LIMPIAR",
    command=limpiar,
    font=("Arial", 10, "bold"),
    bg=LILA,
    fg=BLANCO,
    activebackground=ROSA,
    activeforeground=BLANCO,
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=9
).pack(
    side="left",
    padx=6
)


# ============================================================
# ESTADO
# ============================================================

estado = tk.Label(
    ventana,
    text="● Esperando evaluación",
    font=("Arial", 10, "bold"),
    bg=FONDO,
    fg=GRIS
)

estado.pack(
    pady=(0, 8)
)


# ============================================================
# PANEL DE DATOS
# ============================================================

panel = tk.Frame(
    ventana,
    bg=BLANCO,
    highlightbackground=ROSA_CLARO,
    highlightthickness=2
)

panel.pack(
    padx=35,
    pady=5,
    fill="x"
)


tk.Label(
    panel,
    text="DATOS DEL CAMIÓN",
    font=("Arial", 13, "bold"),
    bg=BLANCO,
    fg=TEXTO
).pack(
    pady=(12, 8)
)


autorizacion = tk.IntVar()
peso = tk.IntVar()
peligrosa = tk.IntVar()
certificacion = tk.IntVar()


marco_checks = tk.Frame(
    panel,
    bg=BLANCO
)

marco_checks.pack(
    padx=25,
    pady=(0, 15),
    fill="x"
)


def crear_check(texto, variable):

    return tk.Checkbutton(
        marco_checks,
        text=texto,
        variable=variable,
        font=("Arial", 10),
        bg=BLANCO,
        fg=TEXTO,
        activebackground=BLANCO,
        activeforeground=TEXTO,
        selectcolor=ROSA_CLARO,
        anchor="w",
        cursor="hand2"
    )


crear_check(
    "Tiene autorización previa",
    autorizacion
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=10,
    pady=4
)


crear_check(
    "Tiene el peso excedido",
    peso
).grid(
    row=0,
    column=1,
    sticky="w",
    padx=10,
    pady=4
)


crear_check(
    "Transporta materiales peligrosos",
    peligrosa
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=10,
    pady=4
)


crear_check(
    "Tiene certificación vigente",
    certificacion
).grid(
    row=1,
    column=1,
    sticky="w",
    padx=10,
    pady=4
)


marco_checks.columnconfigure(0, weight=1)
marco_checks.columnconfigure(1, weight=1)


# ============================================================
# ÁREA DE RESULTADOS
# ============================================================

tk.Label(
    ventana,
    text="RESULTADOS",
    font=("Arial", 13, "bold"),
    bg=FONDO,
    fg=TEXTO
).pack(
    pady=(15, 5)
)


salida = scrolledtext.ScrolledText(
    ventana,
    width=90,
    height=17,
    font=("Consolas", 10),
    bg=BLANCO,
    fg=TEXTO,
    insertbackground=TEXTO,
    relief="flat",
    padx=15,
    pady=12
)

salida.pack(
    padx=35,
    pady=(0, 20),
    fill="both",
    expand=True
)


# ============================================================
# ESTILOS DEL TEXTO
# ============================================================

salida.tag_config(
    "titulo",
    font=("Arial", 12, "bold"),
    foreground=ROSA
)

salida.tag_config(
    "subtitulo",
    font=("Arial", 10, "bold"),
    foreground=LILA
)

salida.tag_config(
    "clasificacion",
    font=("Arial", 13, "bold"),
    foreground=VERDE
)

salida.tag_config(
    "dato",
    font=("Consolas", 10),
    foreground=TEXTO
)

salida.tag_config(
    "separador",
    foreground=ROSA_CLARO
)

salida.tag_config(
    "error",
    font=("Arial", 10, "bold"),
    foreground=ROJO
)


# ============================================================
# INICIO
# ============================================================

ventana.mainloop()