import numpy as np
import math

class Nodo():

    def __init__(self, Padre=None, Posicion=None, G=None):
        """
        Constructor de la clase Nodo.
        :param Padre: Nodo padre.
        :param Posicion: Posición de de la casilla.
        :param G: Coste acumulado para llegar al nodo.
        """

        # Referencia al nodo padre
        self.Padre = Padre

        # Posición del nodo
        self.Posicion = Posicion

        # Funcion de evaluación
        self.F = 0

        # Coste acumulado, si es nulo, es 0
        if G is not None:
            self.G = G
        else:
            self.G = 0

        # Valor de la heurística
        self.H = 0

    def __eq__(self, NodoComparado):
        """
        Función para comparar 2 objetos del tipo Nodo.
        :param NodoComparado:
        :return: Devuelve true si las posiciones son iguales, false si son distintas.
        """
        return self.Posicion[0] == NodoComparado.Posicion[0] and self.Posicion[1] == NodoComparado.Posicion[1]

def Algoritmo_Avaro(Mapa, Mapa_Objetos, PosicionInicial, PosicionFinal, DistanciaDiagonal, Costes, AguaAccesible, PenalizarMovDiagonal, Echo = False):
    """
    :param Mapa: Mapa de costes y transitabilidad (-1 no transitable).
    :param Mapa_Objetos: Mapa que indica que tipo de celda es.
    :param PosicionInicial: Posición de inicio.
    :param PosicionFinal: Posición final.
    :param DistanciaDiagonal: Valor de D2.
    :param Costes: Costes según cada tipo de celda [terreno, agua, pantano, árbol].
    :param AguaAccesible: Indica si el agua es accesible desde el terreno.
    :param PenalizarMovDiagonal: Indica si se penaliza el tomar un camino en diagonal.
    :param Echo: Indica si se imprimen comentarios por consola durante el proceso de búsqueda.
    """
    # Movimientos posibles (Arriba, Abajo, Izquierda, Derecha y diagonales)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]

    # Inicialización nodo inicial
    nodo_Inicio = Nodo(Posicion=PosicionInicial)
    nodo_Inicio.G = 0
    nodo_Inicio.H = heuristica(PosicionInicial, PosicionFinal, nodo_Inicio.G, DistanciaDiagonal)
    nodo_Inicio.F = nodo_Inicio.G + nodo_Inicio.H

    # Inicialización nodo final
    nodo_Final = Nodo(Posicion=PosicionFinal)

    # Inicializacion listas de nodos abiertos y cerrados
    nodos_Abiertos = []
    nodos_Cerrados = []

    # Añadimos el primer nodo a la lista de abiertos
    nodos_Abiertos.append(nodo_Inicio)

    # Iteramos sobre los nodos abiertos hasta encontrar la solución o haber recorrido todos los nodos abiertos.
    while len(nodos_Abiertos) > 0:

        # Como estamos en Avara, ordenamos por H
        nodos_Abiertos.sort(key=lambda x: x.H, reverse=False)

        # Sacamos el siguiente nodo
        nodo_Actual = nodos_Abiertos[0]
        indice_Actual = 0
        nodos_hijos = []
        nodos_Abiertos.pop(indice_Actual)
        nodos_Cerrados.append(nodo_Actual)

        if Echo == True:
            print(nodo_Actual.Posicion)
            print("+------------------+")
            print("| G: actual: " + str(nodo_Actual.G) + " |")
            print("| F: actual: " + str(nodo_Actual.F) + " |")
            print("+------------------+")

        # Solución encontrada
        if nodo_Actual == nodo_Final:
            path = []
            current = nodo_Actual
            while current is not None:
                path.append(current)
                current = current.Padre
            return path[::-1], nodos_Abiertos, nodos_Cerrados

        # Obtenemos el tipo de celda actual
        tipo_celda_actual = Mapa_Objetos[nodo_Actual.Posicion[0]][nodo_Actual.Posicion[1]]

        # Generamos los nodos según los operadores
        for movimiento in movimientos:

            # Obtenemos la nueva posición
            nuevaPosicion = (nodo_Actual.Posicion[0] + movimiento[0], nodo_Actual.Posicion[1] + movimiento[1])

            # Está dentro del rango
            if nuevaPosicion[0] > (len(Mapa) - 1) or nuevaPosicion[0] < 0 or nuevaPosicion[1] > (
                    len(Mapa[len(Mapa) - 1]) - 1) or nuevaPosicion[1] < 0:
                continue

            # Se puede andar
            if Mapa[nuevaPosicion[0]][nuevaPosicion[1]] == -1:
                continue

            # Obtenemos el tipo de la celda hijo
            tipo_celda_siguiente = Mapa_Objetos[nuevaPosicion[0]][nuevaPosicion[1]]

            # Comprobamos las restricciones de accesibilidad
            if tipo_celda_actual == "Terreno" and tipo_celda_siguiente == "Agua" and AguaAccesible is False:
                continue

            if tipo_celda_actual == "Agua" and tipo_celda_siguiente == "Terreno" and AguaAccesible is False:
                continue

            # Calculamos los costes según el tipo de celda [Terreno, Agua, Pantano, Arbol]
            if tipo_celda_actual == "Terreno":
                coste_temp = Costes[0]
            elif tipo_celda_actual == "Agua":
                coste_temp = Costes[1]
            elif tipo_celda_actual == "Pantano":
                coste_temp = Costes[2]
            elif tipo_celda_actual == "Arbol":
                coste_temp = Costes[3]

            # Penalizamos el movimiento en diagonal si así está indicado
            if movimiento[0] is not 0 and movimiento[1] is not 0 and PenalizarMovDiagonal is True:
                coste_temp = math.sqrt((coste_temp**2) + (coste_temp**2))

            # Creamos el objeto nodo hijo y lo introducimos en la lista de hijos a evaluar.
            nodo_hijo = Nodo(nodo_Actual, nuevaPosicion, G=coste_temp)
            nodos_hijos.append(nodo_hijo)

        # Iteramos sobre los hijos generados
        for hijo in nodos_hijos:

            # Calculamos f, g y h
            hijo.H = heuristica(hijo.Posicion, PosicionFinal, hijo.G, DistanciaDiagonal)
            hijo.G += nodo_Actual.G
            hijo.F = hijo.H

            # Gestionamos las listas de abiertos y cerrados
            if hijo not in nodos_Abiertos and hijo not in nodos_Cerrados:
                nodos_Abiertos.append(hijo)

def Algoritmo_A_Estrella(Mapa, Mapa_Objetos, PosicionInicial, PosicionFinal, DistanciaDiagonal, Costes, AguaAccesible, PenalizarMovDiagonal, Echo = False):
    """
    :param Mapa: Mapa de costes y transitabilidad (-1 no transitable).
    :param Mapa_Objetos: Mapa que indica que tipo de celda es.
    :param PosicionInicial: Posición de inicio.
    :param PosicionFinal: Posición final.
    :param DistanciaDiagonal: Valor de D2.
    :param Costes: Costes según cada tipo de celda [terreno, agua, pantano, árbol].
    :param AguaAccesible: Indica si el agua es accesible desde el terreno.
    :param PenalizarMovDiagonal: Indica si se penaliza el tomar un camino en diagonal.
    :param Echo: Indica si se imprimen comentarios por consola durante el proceso de búsqueda.
    :return:
    """
    # Movimientos posibles (Arriba, Abajo, Izquierda, Derecha y diagonales)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]

    # Inicialización nodo inicial
    nodo_Inicio = Nodo(Posicion=PosicionInicial)
    nodo_Inicio.G = 0
    nodo_Inicio.H = heuristica(PosicionInicial, PosicionFinal, nodo_Inicio.G, DistanciaDiagonal)
    nodo_Inicio.F = nodo_Inicio.G + nodo_Inicio.H

    # Inicialización nodo final
    nodo_Final = Nodo(Posicion=PosicionFinal)

    # Inicializacion listas de nodos abiertos y cerrados
    nodos_Abiertos = []
    nodos_Cerrados = []

    # Añadimos el primer nodo a la lista de abiertos
    nodos_Abiertos.append(nodo_Inicio)

    # Iteramos sobre los nodos abiertos hasta encontrar la solución o haber recorrido todos los nodos abiertos.
    while len(nodos_Abiertos) > 0:

        # Como estamos en Avara, ordenamos por F
        nodos_Abiertos.sort(key=lambda x: x.F, reverse=False)

        # Sacamos el siguiente nodo
        nodo_Actual = nodos_Abiertos[0]
        indice_Actual = 0
        nodos_hijos = []
        nodos_Abiertos.pop(indice_Actual)
        nodos_Cerrados.append(nodo_Actual)

        if Echo == True:
            print(nodo_Actual.Posicion)
            print("+------------------+")
            print("| G: actual: " + str(nodo_Actual.G) + " |")
            print("| F: actual: " + str(nodo_Actual.F) + " |")
            print("+------------------+")

        # Solución encontrada
        if nodo_Actual == nodo_Final:
            path = []
            current = nodo_Actual
            while current is not None:
                path.append(current)
                current = current.Padre
            return path[::-1], nodos_Abiertos, nodos_Cerrados

        # Obtenemos el tipo de celda actual
        tipo_celda_actual = Mapa_Objetos[nodo_Actual.Posicion[0]][nodo_Actual.Posicion[1]]

        # Generamos los nodos según los operadores
        for movimiento in movimientos:

            # Obtenemos la nueva posición
            nuevaPosicion = (nodo_Actual.Posicion[0] + movimiento[0], nodo_Actual.Posicion[1] + movimiento[1])

            # Está dentro del rango
            if nuevaPosicion[0] > (len(Mapa) - 1) or nuevaPosicion[0] < 0 or nuevaPosicion[1] > (
                    len(Mapa[len(Mapa) - 1]) - 1) or nuevaPosicion[1] < 0:
                continue

            # Se puede andar
            if Mapa[nuevaPosicion[0]][nuevaPosicion[1]] == -1:
                continue

            # Obtenemos el tipo de la celda hijo
            tipo_celda_siguiente = Mapa_Objetos[nuevaPosicion[0]][nuevaPosicion[1]]

            # Comprobamos las restricciones de accesibilidad
            if tipo_celda_actual == "Terreno" and tipo_celda_siguiente == "Agua" and AguaAccesible is False:
                continue

            if tipo_celda_actual == "Agua" and tipo_celda_siguiente == "Terreno" and AguaAccesible is False:
                continue

            # Calculamos los costes según el tipo de celda [Terreno, Agua, Pantano, Arbol]
            if tipo_celda_actual == "Terreno":
                coste_temp = Costes[0]
            elif tipo_celda_actual == "Agua":
                coste_temp = Costes[1]
            elif tipo_celda_actual == "Pantano":
                coste_temp = Costes[2]
            elif tipo_celda_actual == "Arbol":
                coste_temp = Costes[3]

            # Penalizamos el movimiento en diagonal si así está indicado
            if movimiento[0] is not 0 and movimiento[1] is not 0 and PenalizarMovDiagonal is True:
                coste_temp = math.sqrt((coste_temp**2) + (coste_temp**2))

            # Creamos el objeto nodo hijo y lo introducimos en la lista de hijos a evaluar.
            nodo_hijo = Nodo(nodo_Actual, nuevaPosicion, G=coste_temp)
            nodos_hijos.append(nodo_hijo)

        # Iteramos sobre los hijos generados
        for hijo in nodos_hijos:

            # Calculamos f, g y h
            hijo.H = heuristica(hijo.Posicion, PosicionFinal, hijo.G, DistanciaDiagonal)
            hijo.G += nodo_Actual.G
            hijo.F = hijo.G + hijo.H

            # Gestionamos las listas de abiertos y cerrados
            if hijo in nodos_Abiertos:
                for nodoAbierto in nodos_Abiertos:
                    if nodoAbierto == hijo:
                        if hijo.G < nodoAbierto.G:
                            nodos_Abiertos.remove(nodoAbierto)
                            nodos_Abiertos.append(hijo)
                            break
            elif hijo in nodos_Cerrados:
                for nodoCerrado in nodos_Cerrados:
                    if nodoCerrado == hijo:
                        if hijo.G < nodoCerrado.G:
                            nodos_Cerrados.remove(nodoCerrado)
                            nodos_Abiertos.append(hijo)
                            break
            else:
                nodos_Abiertos.append(hijo)

def heuristica(Posicion, PosicionFinal, Coste, DistanciaDiagonal):
    """
    Función para el cálculo de la heurística de una celda.
    :param Posicion: Posición actual.
    :param PosicionFinal: Posición objetivo.
    :param Coste: Coste de la celda.
    :param DistanciaDiagonal: Valor de D2.
    :return:
    """
    D = 1 * Coste
    D2 = DistanciaDiagonal * Coste
    dx = abs(Posicion[0] - PosicionFinal[0])
    dy = abs(Posicion[1] - PosicionFinal[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
