def preg(t):
    return input(t+" (si/no): ").lower()=="si"

print("BIENVENIDO AL SISTEMA DE DIAGNOSTICO\n")
nombre = input("¿Como te llamas?: ")

electricidad = preg("¿Tiene electricidad")
if not electricidad:
    enciende = False
    imagen = False
    pitidos = False
    ventilador = False
else:
    enciende = preg("¿Enciende")
    if not enciende:
        ventilador = preg("¿Gira el ventilador")
        pitidos = preg("¿Hace pitidos")
        imagen = False
    else:
        imagen = preg("¿Muestra imagen")
        pitidos = preg("¿Hace pitidos") if not imagen else False
        ventilador = True

print(f"\nresumen de{nombre.upper()}")
print(f"Electricidad: {'SI' if electricidad else 'NO'}")
print(f"Enciende: {'SI' if enciende else 'NO'}")
print(f"Imagen: {'SI' if imagen else 'NO'}")
print(f"Pitidos: {'SI' if pitidos else 'NO'}")
print(f"Ventilador: {'SI' if ventilador else 'NO'}")

if not electricidad:
    print(f"{nombre}, Diagnóstico: Revisar cable y enchufe")
elif not enciende and not ventilador:
    print(f"{nombre}, Diagnóstico: Fuente de poder dañada")
elif not enciende and pitidos:
    print(f"{nombre}, Diagnóstico: Falla de RAM o video")
elif not enciende:
    print(f"{nombre}, Diagnóstico: Revisar fuente y botón")
elif not imagen:
    print(f"{nombre}, Diagnóstico: Revisar monitor y RAM")
else:
    print(f"{nombre}, Diagnóstico: Equipo OK")

# --- MEJORA 4: Mensaje final ---
print("\n--- REPORTE FINAL ---")
if not electricidad or (not enciende and not ventilador):
    print(f"{nombre}, tu equipo tiene una falla GRAVE. Se recomienda llevarlo con un técnico, no intentes abrir la fuente.")
elif not imagen or pitidos:
    print(f"{nombre}, es una falla MEDIA. Puedes intentar limpiar la RAM y revisar cables. Si no queda, llevar a técnico.")
else:
    print(f"{nombre}, tu equipo está bien. Si presenta lentitud, es problema de software.")
print(f"Fin del diagnóstico. Gracias por usar el sistema de {nombre.upper()}.")