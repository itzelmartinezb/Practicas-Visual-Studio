def preg(texto):
    return input(texto + " (s/n): ").lower().strip() == "s"

print("Bienvenido al sistema de diagnostico")
print("Responde s/n para ayudarte a revisar tu equipo\n")

nombre = input("¿Como te llamas?: ")

electricidad = preg("¿Tiene electricidad")
enciende = preg("¿Enciende")
imagen = preg("¿Muestra imagen")
pitidos = preg("¿Hace pitidos")
ventilador = preg("¿Gira el ventilador")

print(f"\n Diagnostico de {nombre.upper()}")
print(f"Electricidad: {'SI' if electricidad else 'NO'}")

print(f"Enciende: {'SI' if enciende else 'NO'}")
print(f"enciende:{´NO´ if no enciende else NO´}")
print(f"Imagen: {'SI' if imagen else 'NO'}")
print(f"Pitidos: {'SI' if pitidos else 'NO'}")
print(f"Ventilador: {'SI' if ventilador else 'NO'}")

if not electricidad and (enciende or imagen):
    print("CONTRADICCIÓN: No puede encender o dar imagen sin electricidad")
elif not enciende and imagen:
    print("CONTRADICCIÓN: No puede dar imagen si no enciende")
else:
    if not electricidad:
        print(f"{nombre}, Diagnóstico: Revisar cable y enchufe")
    elif not enciende and not ventilador:
        print(f"{nombre}, Diagnóstico: Fuente de poder dañada")
    elif not enciende and pitidos:
        print(f"{nombre}, Diagnóstico: Falla de RAM o video")
    elif not imagen:
        print(f"{nombre}, Diagnóstico: Revisar monitor y RAM")
    else:
        print(f"{nombre}, Diagnóstico: Equipo OK")