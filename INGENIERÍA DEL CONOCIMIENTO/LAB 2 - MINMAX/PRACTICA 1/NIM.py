import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.ticker as plticker
from pylab import *

class Nodo():
    """
    Clase que representa un nodo del Espacio del Estados.
    """
    def __init__(self, Padre, Tipo, FichasRestantes, Movimiento):
        """
        Constructor de clase.
        :param Padre: Nodo padre del nodo actual.
        :param Tipo: Tipo de nodo (MIN-MAX).
        :param FichasRestantes: Número de fichas del juego.
        :param Movimiento: Movimiento efectuado para llegar a este estado.
        """
        self.Padre = Padre
        self.Ganador = 0
        self.Tipo = Tipo
        self.FichasRestantes = FichasRestantes

        if Padre == None:
            self.Profundidad = 0
        else:
            self.Profundidad = self.Padre.Profundidad + 1

        if Movimiento == None:
            self.Movimiento = -1
        else:
            self.Movimiento = Movimiento

    def __str__(self):
        """
        Método sobrescrito para imprimir los atributos del objeto.
        """
        return "Profundidad: " + str(self.Profundidad) + ", Ganador: " + str(self.Ganador) + ", Tipo: " \
               + str(self.Tipo) + ", FichasRestantes: " + str(self.FichasRestantes) + ", Movimiento: " + str(
            self.Movimiento)

class Nim():
    """
    Clase que representa el juego Nim.
    """
    def __init__(self, Ayuda=True, Profundidad_K=None):
        """
        Constructor de clase.
        :param Profundidad_K: Variable para calcular la profundidad máxima el árbol MIN-MAX.
        :param Ayuda: Indica si se le va dando consejos al jugador humano.
        """
        self.__Nodos = []
        self.__Movimientos = [1, 2, 3]
        self.__TiemposDeCalculoMax = []
        self.__TiemposDeCalculoMin = []
        self.__TiempoInicio = 0
        self.__Ayuda = Ayuda
        self.__ProfundidadArbol = 0

        # Si no se indica profundidad, ésta es infinito.
        if Profundidad_K is None:
            self.__K = 500000
        else:
            self.__K = Profundidad_K

        if self.__K > 10:
            print("\033[93m" + "¡¡¡ATENCIÓN, CON VALORES DE K MAYORES QUE 10 Y NÚMERO ALTO DE FICHAS, " 
                + "LOS CÁLCULOS RALENTIZAN MUCHO EL JUEGO!!!" + "\033[0m")

    def __EmpezarContarTiempo(self):
        """
        Función para poner en marcha el cronómetro de tiempo.
        """
        self.__TiempoInicio = time.time()

    def __PararContarTiempo(self, Jugador):
        """
        Función para parar el cronómetro y añadir el tiempo calculado a la lista de tiempos MAX o MIN.
        :param MinMax: Tiempo calculado para MIN o MAX.
        """
        tiempoPasado = time.time() - self.__TiempoInicio

        if Jugador == "H":
            self.__TiemposDeCalculoMax.append(tiempoPasado)
        else:
            self.__TiemposDeCalculoMin.append(tiempoPasado)

        self.__TiempoInicio = 0

        if Jugador != "H" or self.__Ayuda:
            print("Se ha calculado la mejor jugada en:", "\033[1m", tiempoPasado, "\033[0m", "s.")

    def EstadisticasTiemposDeCalculo(self):
        """
        Función para mostrar la gráfica de cálculos de tiempos de creación y análisis del árbol MIN-MAX.
        """
        fig, ax1 = subplots(figsize=(20, 10))
        if self.__Ayuda:
            ax1.plot(self.__TiemposDeCalculoMax, color='c', marker='o', label="Tiempos Jugador Humano")
        ax1.plot(self.__TiemposDeCalculoMin, color='r', marker='o', label="Tiempos Jugador Máquina")
        loc = plticker.MultipleLocator(base=1)
        ax1.xaxis.set_major_locator(loc)
        fig.suptitle('Tiempo de cálculo por turno', fontsize=20)
        plt.xlabel('Turno')
        plt.ylabel("Tiempo de cálculo")
        plt.legend(loc='upper left')
        ax1.grid(True)
        plt.show()

    def __GetParametros(self):
        """
        Función para obtener los parámetros del juego:
            - Número de fichas.
            - Primer Jugador.
        """
        # Pide al usuario el número de fichas del juego, hasta que el número indicado es correcto (>1).
        while True:
            numFichasTemp = -1
            try:
                numFichasTemp = int(input("Introduzca número de fichas: "))
            except:
                print("Error")

            if numFichasTemp < 1:
                print("Error")
            else:
                self.__NumFichas = int(numFichasTemp)
                self.__NumFichasRestantes = self.__NumFichas
                break

        # Pide al usuario el primer jugador del juego, hasta que el primer jugador indicado es correcto (H/M).
        while True:
            primerJugadorTemp = -1
            try:
                primerJugadorTemp = input("Introduzca el primer jugador, Humano (H), Máquina (M): ")
            except:
                print("Error")

            if primerJugadorTemp != "H" and primerJugadorTemp != "M":
                print("Error")
            else:
                self.__PrimerJugador = primerJugadorTemp
                self.__JugadorActual = self.__PrimerJugador
                break

        # Creamos el primer nodo raíz.
        if self.__PrimerJugador == 'H':
            self.__Raiz = Nodo(Padre=None, Tipo="MAX", FichasRestantes=self.__NumFichas, Movimiento=None)
        else:
            self.__Raiz = Nodo(Padre=None, Tipo="MIN", FichasRestantes=self.__NumFichas, Movimiento=None)
        self.__Nodos.append(self.__Raiz)

    def __GetNodosNivel(self, Nivel):
        """
        Función que devuelve todos los nodos de un nivel.
        :param Nivel: Profundidad del árbol.
        :return: Devuelve una lista de nodos que pertenecen al nivel indicado.
        """
        return [x for x in self.__Nodos if x.Profundidad == Nivel]

    def __GetMinMaxNivelPadre(self, Nivel, Padre, MinMax, Echo=False):
        """
        Función que devuelve el valor MIN o MAX que el nodo padre tomará de sus nodos hijos.
        :param Nivel: Profundidad de los hijos.
        :param Padre: Nodo padre.
        :param MinMax: Tipo de nodo (MIN o MAX).
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        :return: Devuelve el valor MIN o MAX tomado por el nodo padre.
        """
        minMax = []
        # Recupera todos los nodos hijos del nodo padre indicado.
        nodos = [x for x in self.__Nodos if x.Profundidad == Nivel and x.Padre == Padre]

        # Extraemos todos los valores MIN-MAX.
        for nodo in nodos:
            minMax.append(nodo.Ganador)

        if Echo:
            print("-----")
            print("Nivel", Nivel)
            print("MinMax", MinMax)
            print("MinMaxArray", minMax)
            print("")

        # Devuelve el valor mínimo o máximo, dependiendo del tipo de nodo que sea el nodo padre (MIN o MAX).
        if MinMax == "MAX":
            return max(minMax)
        else:
            return min(minMax)

    def __CalcularGanador(self, Fichas, Tipo):
        """
        Función para calcular si el jugador actual va a ganar dado un número de fichas.
        :param Fichas: Número de fichas.
        :param Tipo: Tipo de nodo MIN o MAX.
        :return: Devuelve si el jugador va a ganar.
        """
        if Fichas % 4 == 1:
            if Tipo == "MAX":
                return -1 # Gana MIN
            else:
                return 1 # Gana MAX
        else: 
            if Tipo == "MAX":
                return 1 # Gana MAX
            else:
                return -1 # Gana MIN

    def __CrearArbol(self, Jugador, Echo=False):
        """
        Función para crear el árbol MIN-MAX.
        :param Jugador: Jugador del cual se va a crear el árbol MIN-MAX.
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        """
        # Cálculo de la profundidad máxima del árbol.
        if Jugador == "H":
            tipoActual = "MAX"
            profundidadMax = self.__K * 2
        else:
            tipoActual = "MIN"
            profundidadMax = (self.__K * 2) - 1

        # Iteración hasta llegar a la profundidad máxima o hasta que se haya creado el árbol entero.
        for nivelActual in range(0, profundidadMax + 1):

            # Tipo de nodo
            if tipoActual == "MAX":
                tipoActual = "MIN"
            else:
                tipoActual = "MAX"

            if Echo:
                print("Creando Nivel", nivelActual)

            # Recuperamos todos los nodos de un nivel.
            nodosNivel = self.__GetNodosNivel(nivelActual)

            if len(nodosNivel) > 0:
                # Hay hijos en el nivel actual.
                for nodoActual in nodosNivel:
                    for movimiento in self.__Movimientos:
                        # Generemos los hijos de los nodos del nivel actual.
                        fichasRestantes = nodoActual.FichasRestantes - movimiento
                        if fichasRestantes >= 0:
                            # Descartarmos los hijos cuyas fichas restantes sean menores que 0 pues no puede existir un estado con 
                            # número de fichas restantes negativo.
                            nodo_temp = Nodo(Padre=nodoActual, Tipo=tipoActual, FichasRestantes=fichasRestantes, Movimiento=movimiento)
                            self.__Nodos.append(nodo_temp)

                self.__ProfundidadArbol = nivelActual
            else:
                # Si ya hay nodos en el nivel actual, significa que el árbol ya se ha generado completamente y no hay que seguir iterando.
                break

    def __CalculaMinMax(self, Jugador, Echo=False):
        """
        Función para propagar desde los nodos hoja hasta el raíz, el valor MIN-MAX.
        :param Jugador:
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        """
        # Iteración desde los nodos de mayor profundidad hasta el raíz.
        for nivelActual in range(self.__ProfundidadArbol, -1, -1):
            if Echo:
                print("Explorando Nivel", nivelActual)

            # Recuperamos los nodos del nivel actual.
            nodosNivel = self.__GetNodosNivel(nivelActual)

            # Iteración de cada nodo del nivel actual.
            for nodoActual in nodosNivel:
                if nodoActual.FichasRestantes == 0:
                    # Nodos hojas por terminación del juego.
                    if Echo:
                        print("Hoja en nivel", nivelActual)
                    # Calculamos el ganador
                    if nodoActual.Tipo == "MAX":
                        if Echo:
                            print("Hoja MAX")
                        nodoActual.Ganador = 1
                    else:
                        if Echo:
                            print("Hoja MIN")
                        nodoActual.Ganador = -1
                elif nivelActual == self.__ProfundidadArbol:
                    # Nodos hojas por profundidad máxima del árbol.
                    if Echo:
                        print("Nivel Máximo alcanzado")
                    # Calculamos el ganador.
                    nodoActual.Ganador = self.__CalcularGanador(nodoActual.FichasRestantes, nodoActual.Tipo)
                else:
                    # No son hojas hay que seleccionar el valor MIN-MAX del padre, del valor MIN-MAX de los hijos del nodo actual.
                    if Echo:
                        print("nodoActual.Tipo", nodoActual.Tipo)
                    # Propagamos el valor MIN-MAX.
                    nodoActual.Ganador = self.__GetMinMaxNivelPadre(nivelActual + 1, nodoActual, nodoActual.Tipo)

    def __CambioDeTurno(self):
        """
        Función para cambiar de turno.
        """
        self.__Raiz = None
        self.__Nodos = []

        # Cambia el jugador actual y crea el número nodo raíz del árbol MIN-MAX.
        if self.__JugadorActual == "H":
            self.__JugadorActual = "M"
            self.__Raiz = Nodo(Padre=None, Tipo="MIN", FichasRestantes=self.__NumFichasRestantes, Movimiento=None)
        else:
            self.__JugadorActual = "H"
            self.__Raiz = Nodo(Padre=None, Tipo="MAX", FichasRestantes=self.__NumFichasRestantes, Movimiento=None)

        self.__Nodos.append(self.__Raiz)

    def __SeleccionarMovimiento(self, MinMax, Echo=False):
        """
        Función para elegir el mejor movimiento posible de un jugador.
        :param MinMax: MIN o MAX a buscar (el jugador actual).
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        :return: Devuelve el mejor número de fichas que un jugador puede tomar.
        """
        minMax = []
        # Recupera todos los nodos hijos del nodo raíz.
        nodos = [x for x in self.__Nodos if x.Profundidad == 1]

        if Echo:
            print("---")
            print("Nodos hijos:")

        # Añade a una lista los valores de los nodos hijos del raíz.
        for nodo in nodos:
            if Echo:
                print(nodo)
            minMax.append(nodo.Ganador)

        if Echo:
            print("La Raiz es:", MinMax)

        # Selecciona el nodo con mayor valor o menor, dependiendo de si buscamos MIN o MAX.
        if MinMax == "MAX":
            nodoEleccion = nodos[minMax.index(max(minMax))]
        else:
            nodoEleccion = nodos[minMax.index(min(minMax))]

        if Echo:
            print("---")

        # Devuelve el mejor movimiento.
        return nodoEleccion.Movimiento

    def Jugar(self):
        """
        Función con el flujo principal del juego.
        """
        # Obtención de los parámetros del juego (nº de fichas y primer jugador).
        self.__GetParametros()
        ganador = False

        print("")
        print("---------------------")
        print("| COMIENZA EL JUEGO |")
        print("---------------------")
        print("")

        # Bucle del juego.
        while ganador is False:
            print("Quedan:", "\033[1m", self.__NumFichasRestantes, "FICHAS.", "\033[0m")
            print("Turno del jugador:", "\033[1m", "\033[0m", self.__JugadorActual)

            if self.__NumFichasRestantes == 0:
                # Fin del juego.
                print("")
                print("----------------------------")
                print("| \033[1m" + "HA GANADO EL JUGADOR, ", self.__JugadorActual, " |")
                print("----------------------------", "\033[0m")
                ganador = True
            else:
                # El juego continúa.

                # Cálculo de la mejor jugada y almacenamiento del tiempo requerido.
                if self.__JugadorActual == "M" or self.__Ayuda:
                    self.__EmpezarContarTiempo()
                    self.__CrearArbol(Jugador=self.__JugadorActual)
                    self.__CalculaMinMax(Jugador=self.__JugadorActual)
                    movimientoRecomendado = self.__SeleccionarMovimiento(self.__Raiz.Tipo)
                    self.__PararContarTiempo(Jugador=self.__JugadorActual)

                if self.__JugadorActual == "H":
                    # Turno del jugador humano.

                    if self.__Ayuda:
                        # Si está en el modo ayuda, imprimimos el mejor movimiento calculado.
                        print("El movimiento recomendado para el jugador es tomar:", "\033[1m", movimientoRecomendado,
                        " FICHAS.", "\033[0m")

                    # El programe solicita al usuario, el número de fichas que desea retirar hasta que el número indicado sea válido.
                    while True:
                        movimientoTemp = -1
                        try:
                            movimientoTemp = int(input("¿Cuántas fichas tomas?: "))
                        except:
                            print("Error")

                        if movimientoTemp < 1 or movimientoTemp > 3 or movimientoTemp > self.__NumFichasRestantes:
                            print("Error")
                        else:
                            movimientoRecomendado = movimientoTemp
                            break
                else:
                    # Turno de la máquina
                    print("La máquina toma:", "\033[1m", movimientoRecomendado, "FICHAS.", "\033[0m")

                # Cálculo del número de fichas restantes después del turno y cambio de turno.
                self.__NumFichasRestantes = self.__NumFichasRestantes - movimientoRecomendado
                self.__CambioDeTurno()
                print("")
                print("------------")
                print("")