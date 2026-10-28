
# ============================================================
# PRACTICA 13: ALGORITMOS GENETICOS

# Es un método de optimización inspirado en la selección natural 
# de Darwin, busca la mejor solución a un problema haciendo evolucionar
# un conjunto de soluciones candidatas a lo largo del tiempo.
#
# Problema:
# Encontrar un valor de x que maximice:
#
# f(x) = sin(x) + 0.5*sin(3*x) + 0.2*sin(5*x)
#
# Restriccion:
# 0 <= x <= 10
#
# Factorial 
# 5! (5*4*3*2*1) = 120 posibilidades.
#
# Conceptos:
# - Poblacion: es el conjunto total de soluciones candidatas (individuos) en una generación determinada
    # ejemplo: Si buscas la configuración óptima de un motor, 
        # o los pesos de una red, la población es el grupo de 50 o 100 
        # configuraciones distintas que evalúas al mismo tiempo.

# - Cromosoma: Es la representación codificada de una solución individual.
    # ejemplo: Un vector o lista de valores (pueden ser bits [1,0,1], 
        # números enteros o números reales [2.5, -0.8, 14.1]) 
        # donde cada posición (gen) representa una variable o parámetro del problema.

# - Fitness (función de aptitud): Es la métrica o puntuación que evalúa qué tan "buena" 
    # es la solución representada por un cromosoma. 
    # ejemplo: Es la función de costo u optimización. 
        # A mayor fitness, mejor adaptado está el individuo para resolver el problema 
        # y mayor será su probabilidad de reproducirse.

# - Seleccion por torneo: Mecanismo para elegir los individuos que serán padres de la siguiente generación.
    # ejemplo: Se toman k individuos al azar de la población 
    # (por ejemplo, k=3) y compiten entre sí. 
    # El que tenga el mejor fitness gana el torneo y es seleccionado. 
    # Es rápido, no requiere ordenar toda la población y 
    # permite controlar la presión selectiva ajustando el tamaño del torneo k.

# - Cruza aritmetica (arithmetic crossover) operador de reproduccción diseñado para cromosomas con representación
    # de números reales
    # ejemplo: genera descendientes combinando linealmente los genes de los padres (p1 y p2) 
    # mediante un factor alpha E [0, 1]
                # Hijo_1 = alpha P1 + (1 - alpha) P_2
                # Hijo_2 = (1 - alpha) P_1 + alpha P_2


# - Mutacion gaussiana Operador de variación que altera levemente los genes de un 
    # individuo agregando un valor aleatorio extraído de una distribución normal (gaussiana) 
    # con media 0 y desviación estándar sigma

# - Elitismo Estrategia de conservación que copia directamente a los N mejores individuos 
    # de la generación actual a la siguiente generación, sin aplicarles cruza ni mutación.

# - Evolucion por generaciones
    # Es el ciclo iterativo global del algoritmo genético:

    # Se evalúa la Población actual con la función de Fitness.

    # Se aplica Elitismo para proteger a los mejores.

    #Se eligen padres mediante Selección por torneo.

    #Se aplican Cruza aritmética y Mutación gaussiana para crear la nueva descendencia.

    #Se reemplaza la población anterior y se repite el proceso hasta cumplir un criterio de paro (máximo de generaciones o convergencia).


# ============================================================


# ------------------------------------------------------------
# 1. IMPORTAR LIBRERIAS
# ------------------------------------------------------------

import math
import random
import numpy as np
import matplotlib.pyplot as plt


# Fijamos una semilla para repetir el experimento.
# Si cambiamos esta semilla, puede cambiar el resultado.
random.seed(42)
np.random.seed(42)


# ------------------------------------------------------------
# 2. CONFIGURACION DEL ALGORITMO
# ------------------------------------------------------------

# Limites permitidos para nuestro cromosoma x.
X_MIN = 0.0
X_MAX = 10.0

# Numero de soluciones que forman cada generacion.
TAMANO_POBLACION = 40

# Numero maximo de generaciones.
NUM_GENERACIONES = 100

# Probabilidad de realizar una cruza.
PROBABILIDAD_CRUZA = 0.90

# Probabilidad de mutar un hijo.
PROBABILIDAD_MUTACION = 0.20

# Desviacion de la mutacion gaussiana.
# Un valor mayor permite cambios mas grandes.
DESVIACION_MUTACION = 0.35

# Numero de mejores individuos que pasan directamente
# a la siguiente generacion.
ELITISMO = 2

# Numero de individuos que compiten en cada torneo.
TAMANO_TORNEO = 3


# ------------------------------------------------------------
# 3. FUNCION OBJETIVO
# ------------------------------------------------------------

def funcion_objetivo(x):
    """
    Calcula el fitness de una solucion.

    Como estamos maximizando, cuanto mayor sea el
    resultado, mejor sera el individuo.
    """

    return (
        math.sin(x)
        + 0.5 * math.sin(3 * x)
        + 0.2 * math.sin(5 * x)
    )


# ------------------------------------------------------------
# 4. CREAR UN INDIVIDUO
# ------------------------------------------------------------

def crear_individuo():
    """
    Un individuo es una solucion candidata.

    En este ejercicio el cromosoma tiene un solo gen:
    el numero real x.

    Ejemplo:
        individuo = 4.725

    Esto significa que la solucion candidata
    consiste en evaluar f(4.725).
    """

    return random.uniform(X_MIN, X_MAX)


# ------------------------------------------------------------
# 5. CREAR LA POBLACION INICIAL
# ------------------------------------------------------------

def crear_poblacion():
    """
    Genera muchas soluciones aleatorias.

    La poblacion inicial permite explorar distintas
    regiones del espacio de busqueda.
    """

    poblacion = []

    for _ in range(TAMANO_POBLACION):

        individuo = crear_individuo()

        poblacion.append(individuo)

    return poblacion


# ------------------------------------------------------------
# 6. EVALUAR UN INDIVIDUO
# ------------------------------------------------------------

def evaluar(individuo):
    """
    Calcula la aptitud del individuo.

    En nuestro caso:
        fitness = f(x)

    La funcion objetivo y el fitness coinciden porque
    el problema consiste directamente en maximizar f(x).
    """

    return funcion_objetivo(individuo)


# ------------------------------------------------------------
# 7. SELECCION POR TORNEO
# ------------------------------------------------------------

def seleccion_por_torneo(poblacion):
    """
    Selecciona un padre mediante un torneo.

    Pasos:
    1. Elegir varios individuos al azar.
    2. Comparar su fitness.
    3. Devolver el mejor del grupo.

    La seleccion favorece a los individuos buenos,
    pero permite que otros tambien sean seleccionados.
    """

    participantes = random.sample(
        poblacion,
        TAMANO_TORNEO
    )

    # max() selecciona al individuo con mayor fitness.
    ganador = max(
        participantes,
        key=evaluar
    )

    return ganador


# ------------------------------------------------------------
# 8. CRUZA ARITMETICA
# ------------------------------------------------------------

def cruza(padre1, padre2):
    """
    Combina dos padres para producir dos hijos.

    Como los cromosomas son numeros reales,
    usamos una combinacion ponderada.

    alpha es un numero aleatorio entre 0 y 1.

    Hijo 1:
        alpha * padre1 + (1-alpha) * padre2

    Hijo 2:
        alpha * padre2 + (1-alpha) * padre1

    Los hijos combinan informacion de ambos padres.
    """

    alpha = random.random()

    hijo1 = (
        alpha * padre1
        + (1 - alpha) * padre2
    )

    hijo2 = (
        alpha * padre2
        + (1 - alpha) * padre1
    )

    return hijo1, hijo2


# ------------------------------------------------------------
# 9. MUTACION GAUSSIANA
# ------------------------------------------------------------

def mutacion(individuo):
    """
    Modifica aleatoriamente un individuo.

    La mutacion se aplica con una probabilidad definida.

    Si ocurre:
        nuevo_x = x + ruido aleatorio

    El ruido procede de una distribucion gaussiana.

    Finalmente, limitamos el valor al dominio permitido.
    """

    # Decidimos si ocurre la mutacion.
    if random.random() < PROBABILIDAD_MUTACION:

        # Generamos un cambio aleatorio.
        cambio = random.gauss(
            0,
            DESVIACION_MUTACION
        )

        # Aplicamos el cambio al cromosoma.
        individuo = individuo + cambio

    # Impedimos que el cromosoma salga del dominio.
    individuo = max(
        X_MIN,
        min(X_MAX, individuo)
    )

    return individuo


# ------------------------------------------------------------
# 10. CREAR UNA NUEVA GENERACION
# ------------------------------------------------------------

def crear_nueva_generacion(poblacion):
    """
    Construye una nueva poblacion a partir de la actual.

    Incluye:
    - Elitismo
    - Seleccion
    - Cruza
    - Mutacion
    """

    nueva_poblacion = []

    # --------------------------------------------------------
    # A. ELITISMO
    # --------------------------------------------------------

    # Ordenamos los individuos desde el mejor al peor.
    poblacion_ordenada = sorted(
        poblacion,
        key=evaluar,
        reverse=True
    )

    # Copiamos los mejores individuos sin modificarlos.
    # Asi evitamos perder las mejores soluciones conocidas.
    mejores = poblacion_ordenada[:ELITISMO]

    nueva_poblacion.extend(mejores)

    # --------------------------------------------------------
    # B. GENERAR LOS DEMAS DESCENDIENTES
    # --------------------------------------------------------

    while len(nueva_poblacion) < TAMANO_POBLACION:

        # Elegimos dos padres.
        padre1 = seleccion_por_torneo(poblacion)
        padre2 = seleccion_por_torneo(poblacion)

        # ----------------------------------------------------
        # C. CRUZA
        # ----------------------------------------------------

        if random.random() < PROBABILIDAD_CRUZA:

            hijo1, hijo2 = cruza(
                padre1,
                padre2
            )

        else:
            # Si no hay cruza, los hijos son copias.
            hijo1 = padre1
            hijo2 = padre2

        # ----------------------------------------------------
        # D. MUTACION
        # ----------------------------------------------------

        hijo1 = mutacion(hijo1)
        hijo2 = mutacion(hijo2)

        # Agregamos el primer hijo si hay espacio.
        nueva_poblacion.append(hijo1)

        # Agregamos el segundo hijo si todavia hay espacio.
        if len(nueva_poblacion) < TAMANO_POBLACION:
            nueva_poblacion.append(hijo2)

    return nueva_poblacion


# ------------------------------------------------------------
# 11. ALGORITMO GENETICO PRINCIPAL
# ------------------------------------------------------------

def algoritmo_genetico():
    """
    Coordina todas las etapas del algoritmo genetico.

    Devuelve:
        mejor_individuo
        mejor_fitness
        historial_fitness
        historial_promedio
        historial_diversidad
    """

    # Generamos la primera poblacion.
    poblacion = crear_poblacion()

    # Aqui guardamos el mejor fitness de cada generacion.
    historial_fitness = []

    # Aqui guardamos el fitness promedio.
    historial_promedio = []

    # Aqui guardamos la diversidad de la poblacion.
    historial_diversidad = []

    # Mejor solucion conocida desde el inicio.
    mejor_individuo = max(
        poblacion,
        key=evaluar
    )

    mejor_fitness = evaluar(mejor_individuo)

    # --------------------------------------------------------
    # EVOLUCION POR GENERACIONES
    # --------------------------------------------------------

    for generacion in range(NUM_GENERACIONES):

        # Evaluamos a toda la poblacion.
        fitness_poblacion = [
            evaluar(individuo)
            for individuo in poblacion
        ]

        # Mejor individuo de la generacion actual.
        indice_mejor = fitness_poblacion.index(
            max(fitness_poblacion)
        )

        mejor_actual = poblacion[indice_mejor]
        fitness_mejor_actual = fitness_poblacion[indice_mejor]

        # Actualizamos el mejor global si encontramos
        # una solucion superior.
        if fitness_mejor_actual > mejor_fitness:

            mejor_individuo = mejor_actual
            mejor_fitness = fitness_mejor_actual

        # Guardamos el mejor valor global.
        historial_fitness.append(mejor_fitness)

        # Calculamos y guardamos el promedio.
        promedio = sum(fitness_poblacion) / len(
            fitness_poblacion
        )

        historial_promedio.append(promedio)

        # La desviacion estandar permite observar
        # que tan dispersos estan los individuos.
        diversidad = float(
            np.std(poblacion)
        )

        historial_diversidad.append(diversidad)

        # Mostramos informacion cada 10 generaciones.
        if generacion % 10 == 0:

            print(
                f"Generacion {generacion:03d} | "
                f"Mejor x = {mejor_individuo:.5f} | "
                f"Mejor fitness = {mejor_fitness:.6f} | "
                f"Promedio = {promedio:.6f} | "
                f"Diversidad = {diversidad:.5f}"
            )

        # Construimos la siguiente generacion.
        poblacion = crear_nueva_generacion(
            poblacion
        )

    return (
        mejor_individuo,
        mejor_fitness,
        historial_fitness,
        historial_promedio,
        historial_diversidad
    )


# ------------------------------------------------------------
# 12. EJECUCION PRINCIPAL
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("PRACTICA 13: ALGORITMO GENETICO")
    print("=" * 70)

    # Ejecutamos el algoritmo.
    (
        mejor_x,
        mejor_fitness,
        historial_fitness,
        historial_promedio,
        historial_diversidad
    ) = algoritmo_genetico()

    # Mostramos la mejor solucion.
    print("\n" + "=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)

    print(f"Mejor x encontrado: {mejor_x:.6f}")
    print(f"Mejor f(x):         {mejor_fitness:.6f}")

    # --------------------------------------------------------
    # 13. GRAFICAR LA FUNCION Y LA MEJOR SOLUCION
    # --------------------------------------------------------

    xs = np.linspace(X_MIN, X_MAX, 1000)

    ys = [
        funcion_objetivo(x)
        for x in xs
    ]

    plt.figure(figsize=(10, 5))

    plt.plot(
        xs,
        ys,
        label="Funcion objetivo"
    )

    plt.scatter(
        mejor_x,
        mejor_fitness,
        marker="*",
        s=200,
        label="Mejor solucion genetica"
    )

    plt.title("Algoritmo genetico: mejor solucion")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # --------------------------------------------------------
    # 14. GRAFICAR LA EVOLUCION DEL FITNESS
    # --------------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        historial_fitness,
        label="Mejor fitness"
    )

    plt.plot(
        historial_promedio,
        label="Fitness promedio"
    )

    plt.title("Evolucion de la poblacion")
    plt.xlabel("Generacion")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # --------------------------------------------------------
    # 15. GRAFICAR LA DIVERSIDAD
    # --------------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        historial_diversidad,
        label="Desviacion estandar de x"
    )

    plt.title("Diversidad de la poblacion")
    plt.xlabel("Generacion")
    plt.ylabel("Diversidad")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Mostrar todas las figuras.
    plt.show()


    #El programa mostrará cada diez generaciones el mejor individuo, su aptitud, el promedio y la diversidad. 
    #Al terminar, abrirá tres gráficas.

    #Gráfica 1: la mejor solución
        #La estrella representa el mejor individuo que encontró el algoritmo genético.
        #No debemos afirmar que necesariamente encontró el máximo global. 
        #Un algoritmo genético es una búsqueda estocástica y el resultado depende de los parámetros, 
        #la población y la aleatoriedad.

    #Gráfica 2: evolución del fitness
        #Mejor fitness
        #El mejor valor encontrado hasta ese momento. 
        #Con elitismo y conservación del mejor global, esta curva no debería disminuir.
        #Fitness promedio Indica la calidad media de la población. 
        #Puede subir o bajar de una generación a otra.

    #Gráfica 3: diversidad
        #La diversidad mide cuánto varían los valores de \(x\) dentro de la población.
        #- Diversidad alta: hay soluciones distribuidas en diferentes regiones.
        #- Diversidad baja: muchos individuos tienen valores similares.
        #- Diversidad demasiado baja: la población podría perder capacidad de explorar.
        #La diversidad no es exactamente lo mismo que calidad: 
        #una población diversa no necesariamente es buena, y una población homogénea 
        #puede haber convergido a una buena solución o haberse estancado.

#Ejecutar el programa tres veces modificando los parámetros.
#  Experimento	Población	Generaciones	Mutación
#   A. Base	        40	        100	            0.20
#   B. Población 
    #pequeña	    10	        100	            0.20
#   C. Mutación 
    #alta	        40	        100	            0.50

#Para cada ejecución, deben registrar el mejor x, el fitness final, la evolución del promedio y la diversidad.

#Preguntas de análisis:
#1. ¿Qué ocurre cuando reducimos la población a 10 individuos?
#2. ¿Por qué una mutación más frecuente puede ayudar a explorar y también dificultar la convergencia?
#3. ¿Cuál es la función del elitismo?
#4. ¿Por qué no es suficiente comparar solamente una ejecución?
#5. ¿Qué parámetros probarían para mejorar los resultados?