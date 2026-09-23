import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime

contador_citas = 1

def diagnosticar():
    global contador_citas
    try:
        nombre = entry_nombre.get()
        edad = entry_edad.get()
        temperatura = float(entry_temp.get())
        presion = entry_presion.get()
        oxigenacion = int(entry_oxi.get())
        frecuencia = int(entry_freq.get())

        fiebre = var_fiebre.get()
        tos = var_tos.get()
        dolor = var_dolor.get()

        p = oxigenacion < 90
        q = temperatura >= 39 and frecuencia > 110
        r = fiebre and tos and oxigenacion < 95
        s = tos and dolor
        t = fiebre

        if p:
            diagnostico = "ALERTA: Oxigenacion critica"
            regla = "Regla 1: p -> Alerta (Ox < 90)"
        elif q:
            diagnostico = "Fiebre alta con taquicardia"
            regla = "Regla 2: q -> Urgente"
        elif r:
            diagnostico = "Posible infeccion respiratoria"
            regla = "Regla 3: r -> Infeccion"
        elif s:
            diagnostico = "Posible faringitis"
            regla = "Regla 4: s -> Faringitis"
        elif t:
            diagnostico = "Valoracion por fiebre"
            regla = "Regla 5: t -> Valoracion"
        else:
            diagnostico = "Signos estables"
            regla = "Regla 6: Estable"

        folio = random.randint(1000, 9999)
        estado = "Estable" if oxigenacion >= 95 else "Requiere atencion"
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        resultado = f"CITA No. {contador_citas:04d}\nEXPEDIENTE: {nombre} | Edad: {edad}\nFolio: #{folio} | Fecha: {ahora}\nVitales: {temperatura}C | {presion} | {oxigenacion}% O2 | {frecuencia} lpm\n\nDiagnostico: {diagnostico}\nEstado: {estado}\nLogica: {regla}"

        label_resultado.config(text=resultado)
        contador_citas += 1
        label_cita.config(text=f"Proxima Cita No. {contador_citas:04d}")

    except ValueError:
        messagebox.showerror("Error", "Revisa numeros")

ventana = tk.Tk()
ventana.title("SISTEMA DIAGNOSTICO Doctor Simi")
ventana.geometry("420x650")

tk.Label(ventana, text="SISTEMA DE DIAGNOSTICO", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(ventana, text=datetime.now().strftime("%d/%m/%Y %H:%M"), font=("Arial", 9)).pack()

label_cita = tk.Label(ventana, text=f"Cita No. {contador_citas:04d}", font=("Arial", 11, "bold"), fg="blue")
label_cita.pack(pady=5)

tk.Label(ventana, text="Nombre:").pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

tk.Label(ventana, text="Edad:").pack()
entry_edad = tk.Entry(ventana)
entry_edad.pack()

tk.Label(ventana, text="--- Signos Vitales ---", font=("Arial", 10, "bold")).pack(pady=5)

tk.Label(ventana, text="Temperatura C:").pack()
entry_temp = tk.Entry(ventana)
entry_temp.insert(0, "36.5")
entry_temp.pack()

tk.Label(ventana, text="Presion (120/80):").pack()
entry_presion = tk.Entry(ventana)
entry_presion.insert(0, "120/80")
entry_presion.pack()

tk.Label(ventana, text="Oxigenacion %:").pack()
entry_oxi = tk.Entry(ventana)
entry_oxi.insert(0, "98")
entry_oxi.pack()

tk.Label(ventana, text="Frecuencia lpm:").pack()
entry_freq = tk.Entry(ventana)
entry_freq.insert(0, "75")
entry_freq.pack()

tk.Label(ventana, text="--- Sintomas ---", font=("Arial", 10, "bold")).pack(pady=5)
var_fiebre = tk.BooleanVar()
var_tos = tk.BooleanVar()
var_dolor = tk.BooleanVar()
tk.Checkbutton(ventana, text="Fiebre", variable=var_fiebre).pack()
tk.Checkbutton(ventana, text="Tos", variable=var_tos).pack()
tk.Checkbutton(ventana, text="Dolor de garganta", variable=var_dolor).pack()

tk.Button(ventana, text="DIAGNOSTICAR", bg="#4CAF50", fg="white", command=diagnosticar).pack(pady=15)

label_resultado = tk.Label(ventana, text="", justify="left", bg="#f0f0f0", font=("Arial", 10), wraplength=380)
label_resultado.pack(fill="both", padx=10, pady=10)

ventana.mainloop()