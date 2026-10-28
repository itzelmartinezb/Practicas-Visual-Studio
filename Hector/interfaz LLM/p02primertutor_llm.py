# ============================================================
# PRACTICA 2
# TUTOR INTELIGENTE CON LLM
# ============================================================

import ollama
import tkinter as tk
from tkinter import scrolledtext, messagebox


# ============================================================
# CONFIGURACION DEL MODELO
# ============================================================

MODELO = "llama3.2:latest"

mensaje_sistema = """
Eres un tutor especializado en programación con Python.

Tu función es ayudar a estudiantes universitarios.

Debes:
1. Explicar Python de manera sencilla y clara.
2. Utilizar ejemplos fáciles de entender.
3. Explicar los procedimientos paso a paso.
4. Evitar términos demasiado técnicos cuando sea posible.
5. Mostrar ejemplos de código en Python.
6. Explicar los errores que pueda cometer el estudiante.
7. No proporcionar solamente la respuesta final.
8. Explicar los conceptos necesarios para comprender
   cada problema.
9. Motivar al estudiante a continuar aprendiendo.
"""


mensajes = [
    {
        "role": "system",
        "content": mensaje_sistema
    }
]


# ============================================================
# FUNCION HISTORIA
# ============================================================

def mostrar_historia():

    historia = """
HISTORIA DE LOS LLM

Los modelos de lenguaje son sistemas de inteligencia
artificial capaces de trabajar con texto y generar
respuestas.

Sus primeros desarrollos utilizaban reglas y métodos
estadísticos.

Con el avance del aprendizaje automático surgieron
modelos capaces de analizar grandes cantidades de
información.

Posteriormente aparecieron las redes neuronales y los
modelos Transformer, que mejoraron la comprensión y
generación de texto.

Actualmente existen los LLM (Large Language Models),
que pueden utilizarse para conversar, explicar temas,
generar código y ayudar en diferentes actividades.

En esta práctica utilizamos Ollama para ejecutar
localmente el modelo llama3.2.
"""

    messagebox.showinfo(
        "Historia de los LLM",
        historia
    )


# ============================================================
# FUNCION ENVIAR
# ============================================================

def enviar_pregunta():

    pregunta = entrada.get("1.0", tk.END).strip()

    if pregunta == "":
        messagebox.showwarning(
            "Aviso",
            "Escribe una pregunta antes de enviar."
        )
        return

    if pregunta.lower() == "salir":
        ventana.destroy()
        return

    chat.insert(
        tk.END,
        "\nEstudiante\n",
        "titulo_estudiante"
    )

    chat.insert(
        tk.END,
        pregunta + "\n\n",
        "pregunta"
    )

    mensajes.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    entrada.delete("1.0", tk.END)

    chat.insert(
        tk.END,
        "Tutor: pensando...\n\n",
        "titulo_tutor"
    )

    chat.see(tk.END)
    ventana.update()

    try:

        respuesta = ollama.chat(
            model=MODELO,
            messages=mensajes
        )

        contenido = respuesta["message"]["content"]

    except Exception as error:

        chat.insert(
            tk.END,
            "No se pudo conectar con Ollama.\n\n",
            "error"
        )

        chat.insert(
            tk.END,
            str(error) + "\n\n",
            "error"
        )

        mensajes.pop()
        chat.see(tk.END)
        return

    mensajes.append(
        {
            "role": "assistant",
            "content": contenido
        }
    )

    chat.insert(
        tk.END,
        "Tutor\n",
        "titulo_tutor"
    )

    chat.insert(
        tk.END,
        contenido + "\n",
        "respuesta"
    )

    chat.insert(
        tk.END,
        "\n" + "-" * 70 + "\n",
        "separador"
    )

    chat.see(tk.END)


# ============================================================
# FUNCION LIMPIAR
# ============================================================

def limpiar_chat():

    global mensajes

    mensajes = [
        {
            "role": "system",
            "content": mensaje_sistema
        }
    ]

    chat.delete(
        "1.0",
        tk.END
    )

    chat.insert(
        tk.END,
        "¡Chat limpiado!\n\n",
        "bienvenida"
    )

    chat.insert(
        tk.END,
        "Puedes comenzar una nueva conversación.\n",
        "respuesta"
    )


# ============================================================
# VENTANA
# ============================================================

ventana = tk.Tk()

ventana.title(
    "Tutor Inteligente con LLM"
)

ventana.geometry(
    "900x650"
)

ventana.minsize(
    750,
    550
)

ventana.configure(
    bg="#F8EAF2"
)


# ============================================================
# ENCABEZADO
# ============================================================

encabezado = tk.Frame(
    ventana,
    bg="#E8B7D0",
    height=85
)

encabezado.pack(
    fill=tk.X
)

encabezado.pack_propagate(False)


titulo = tk.Label(
    encabezado,
    text="TUTOR INTELIGENTE",
    font=("Arial", 22, "bold"),
    bg="#E8B7D0",
    fg="#6B3152"
)

titulo.pack(
    pady=(13, 0)
)


subtitulo = tk.Label(
    encabezado,
    text="Asistente de programación",
    font=("Arial", 10),
    bg="#E8B7D0",
    fg="#704F62"
)

subtitulo.pack(
    pady=3
)


# ============================================================
# BOTONES ARRIBA
# ============================================================

marco_botones = tk.Frame(
    ventana,
    bg="#F8EAF2"
)

marco_botones.pack(
    pady=12
)


boton_enviar = tk.Button(
    marco_botones,
    text="Enviar",
    command=enviar_pregunta,
    width=14,
    font=("Arial", 10, "bold"),
    bg="#C76B99",
    fg="white",
    activebackground="#B65A87",
    activeforeground="white",
    relief=tk.FLAT,
    cursor="hand2"
)

boton_enviar.grid(
    row=0,
    column=0,
    padx=5
)


boton_historia = tk.Button(
    marco_botones,
    text="Historia de LLM",
    command=mostrar_historia,
    width=14,
    font=("Arial", 10, "bold"),
    bg="#9B82B5",
    fg="white",
    activebackground="#896FA5",
    activeforeground="white",
    relief=tk.FLAT,
    cursor="hand2"
)

boton_historia.grid(
    row=0,
    column=1,
    padx=5
)


boton_limpiar = tk.Button(
    marco_botones,
    text="Limpiar",
    command=limpiar_chat,
    width=14,
    font=("Arial", 10, "bold"),
    bg="#D29AB7",
    fg="white",
    activebackground="#C287A5",
    activeforeground="white",
    relief=tk.FLAT,
    cursor="hand2"
)

boton_limpiar.grid(
    row=0,
    column=2,
    padx=5
)


boton_salir = tk.Button(
    marco_botones,
    text="Salir",
    command=ventana.destroy,
    width=14,
    font=("Arial", 10, "bold"),
    bg="#8D657E",
    fg="white",
    activebackground="#79556B",
    activeforeground="white",
    relief=tk.FLAT,
    cursor="hand2"
)

boton_salir.grid(
    row=0,
    column=3,
    padx=5
)


# ============================================================
# CONTENEDOR DEL CHAT
# ============================================================

marco_chat = tk.Frame(
    ventana,
    bg="#F8EAF2"
)

marco_chat.pack(
    fill=tk.BOTH,
    expand=True,
    padx=25,
    pady=(5, 8)
)


chat = scrolledtext.ScrolledText(
    marco_chat,
    font=("Arial", 10),
    wrap=tk.WORD,
    bg="#FFFFFF",
    fg="#443843",
    relief=tk.FLAT,
    borderwidth=0,
    padx=15,
    pady=15
)

chat.pack(
    fill=tk.BOTH,
    expand=True
)


# ============================================================
# ESTILOS DEL CHAT
# ============================================================

chat.tag_config(
    "bienvenida",
    foreground="#A24D78",
    font=("Arial", 13, "bold")
)

chat.tag_config(
    "titulo_estudiante",
    foreground="#B24F82",
    font=("Arial", 11, "bold")
)

chat.tag_config(
    "titulo_tutor",
    foreground="#79589A",
    font=("Arial", 11, "bold")
)

chat.tag_config(
    "pregunta",
    foreground="#4B4048",
    font=("Arial", 10)
)

chat.tag_config(
    "respuesta",
    foreground="#443843",
    font=("Arial", 10)
)

chat.tag_config(
    "error",
    foreground="#B33E4D",
    font=("Arial", 10, "bold")
)

chat.tag_config(
    "separador",
    foreground="#D9A6BF"
)


# ============================================================
# MENSAJE INICIAL
# ============================================================

chat.insert(
    tk.END,
    "Bienvenida al Tutor Inteligente\n\n",
    "bienvenida"
)

chat.insert(
    tk.END,
    "Soy un asistente especializado en programación "
    "con Python.\n\n",
    "respuesta"
)

chat.insert(
    tk.END,
    "Puedes preguntarme, por ejemplo:\n\n",
    "titulo_tutor"
)

chat.insert(
    tk.END,
    "• ¿Qué es una variable?\n"
    "• ¿Cómo funciona un ciclo for?\n"
    "• ¿Qué es una función?\n"
    "• ¿Cómo se crea una lista?\n\n",
    "respuesta"
)

chat.insert(
    tk.END,
    "-" * 70 + "\n",
    "separador"
)


# ============================================================
# AREA PARA ESCRIBIR
# ============================================================

etiqueta = tk.Label(
    ventana,
    text="Escribe tu pregunta",
    font=("Arial", 10, "bold"),
    bg="#F8EAF2",
    fg="#6B3152"
)

etiqueta.pack(
    anchor="w",
    padx=25
)


entrada = tk.Text(
    ventana,
    height=3,
    font=("Arial", 10),
    wrap=tk.WORD,
    bg="#FFFFFF",
    fg="#443843",
    insertbackground="#A24D78",
    relief=tk.FLAT,
    padx=10,
    pady=8
)

entrada.pack(
    fill=tk.X,
    padx=25,
    pady=6
)


# ============================================================
# INICIAR
# ============================================================

ventana.mainloop()
