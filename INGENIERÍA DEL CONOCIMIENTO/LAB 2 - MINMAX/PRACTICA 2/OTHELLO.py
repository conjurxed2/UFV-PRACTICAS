import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.ticker as plticker
import matplotlib.patches as patches
import collections
from pylab import *
import copy

#region - CONSTANTES -

CUADRO_BLANCO = [255, 255, 255]
CUADRO_ROJO_MAQUINA = [255, 80, 80]
CUADRO_AZUL_HUMANO = [51, 153, 255]

JUGADOR_HUMANO = 1
JUGADOR_MAQUINA = -1
SIN_ASIGNAR = 0

#endregion

class Nodo():
    """
    Clase que representa un nodo del Espacio del Estados.
    """
    def __init__(self, Padre, Cuadro, Movimiento):
        """
        Constructor de clase.
        :param Padre: Nodo padre del nodo actual.
        :param Cuadro: Estado del cuadro del juego para este nodo.
        :param Movimiento: Movimiento efectuado para llegar a este nodo
        """
        self.Padre = Padre
        self.Cuadro = copy.deepcopy(Cuadro)
        self.Hijos = []
        self.Valor = -1

        if Movimiento == None:
            self.Movimiento = [-1,-1]
        else:
            self.Movimiento = Movimiento

class Othello():
    """
    Clase que representa el juego Othello o Reversi.
    """
    def __init__(self, Profundidad_K= 2, Ayuda= True):
        """
        Constructor de clase.
        :param Profundidad_K: Variable para calcular la profundidad máxima el árbol MIN-MAX.
        :param Ayuda: Indica si se le va dando consejos al jugador humano.
        """
        self.__K = Profundidad_K
        self.__Nodos = []
        self.__TiemposDeCalculoMax = []
        self.__TiemposDeCalculoMin = []
        self.__TiempoInicio = 0
        self.__Ayuda = Ayuda

        self.__Cuadro = [[0,0, 0, 0,0,0],
                       [0,0, 0, 0,0,0],
                       [0,0, 1,-1,0,0],
                       [0,0,-1, 1,0,0],
                       [0,0, 0, 0,0,0],
                       [0,0, 0, 0,0,0]]

        self.__CuadroPuntuaciones = [[8,6,4,4,6,8],
                                   [6,4,2,2,4,6],
                                   [4,2,1,1,2,4],
                                   [4,2,1,1,2,4],
                                   [6,4,2,2,4,6],
                                   [8,6,4,4,6,8]]

        self.__CuadroImprimir = [[[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],
                               [[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],
                               [[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],
                               [[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],
                               [[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],
                               [[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]]]

        if self.__K > 10:
            print("\033[93m" + "¡¡¡ATENCIÓN, CON VALORES DE K MAYORES QUE 10 Y NÚMERO ALTO DE FICHAS, "
                               + "LOS CÁLCULOS RALENTIZAN MUCHO EL JUEGO!!!" + "\033[0m")
                               
    def __DentroLimitesCuadro(self, X, Y):
        """
        Función para comprobar si las coordenadas están dentro de los límites del cuadro.
        :param X: Coordenada X.
        :param Y: Coordenada Y.
        :return: Devuelve si las coordenadas están dentro de los límites del cuadro.
        """
        if X > -1 and X < 6 and Y > -1 and Y < 6:
            return True
        else:
            return False

    def __ColocarFicha(self, X, Y, Jugador, Cuadro, Echo=False):
        """
        Función para colocar una ficha en el cuadro de juego indicado.
        :param X: Coordenada X.
        :param Y: Coordenada Y.
        :param Jugador: Jugador del cual se va a colocar la ficha.
        :param Cuadro: Cuadro del juego sobre el que se va a colocar la ficha.
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        """
        Cuadro[Y][X] = Jugador
        if Echo:
            print("Colocando ficha en:", X, Y, "Jugador", Jugador)

    def __GetJugadorContrario(self, Jugador):
        """
        Función para dado un jugador, obtener el contrario.
        :param Jugador:
        :return: Devuelve el identificador del jugador contrario al dado
        """
        if Jugador == JUGADOR_HUMANO:
            return JUGADOR_MAQUINA
        elif Jugador == JUGADOR_MAQUINA:
            return JUGADOR_HUMANO
        else:
            return 0

    def ImprimirCuadroDeJuego(self):
        """
        Función para mostrar el cuadro del juego:
            - Rojo: Jugador máquina.
            - Azul: Jugador humano.
        """
        for y in range(0, 6):
            for x in range(0, 6):
                if self.__Cuadro[y][x] == SIN_ASIGNAR:
                    self.__CuadroImprimir[y][x] = CUADRO_BLANCO
                elif self.__Cuadro[y][x] == JUGADOR_MAQUINA:
                    self.__CuadroImprimir[y][x] = CUADRO_ROJO_MAQUINA
                elif self.__Cuadro[y][x] == JUGADOR_HUMANO:
                    self.__CuadroImprimir[y][x] = CUADRO_AZUL_HUMANO

        plt.imshow(self.__CuadroImprimir)

        ax = plt.gca()

        ax.set_xticks(np.arange(0, 6, 1))
        ax.set_yticks(np.arange(0, 6, 1))

        ax.set_xticklabels(np.arange(0, 6, 1))
        ax.set_yticklabels(np.arange(0, 6, 1))

        ax.set_xticks(np.arange(-.5, 5, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 5, 1), minor=True)

        ax.grid(which='minor', color='k', linestyle='-', linewidth=2)

        plt.show()

    def __ConvertirFichasVertical(self, X, Y, Jugador, Cuadro, Echo=False, ColocarFicha=False):
        """
        Función para comprobar si hay movimientos válidos en vertical y si, así se indica, colocar la ficha 
        y transformar aquellas que lo requieran.
        :param X: Coordenada X donde se coloca la ficha.
        :param Y: Coordenada Y donde se coloca la ficha.
        :param Jugador: Jugador el cual efectúa el movimiento.
        :param Cuadro: Cuadro del juego sobre el que se comprueba/ejecuta el movimiento.
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        :param ColocarFicha: Indica si se va a colocar la ficha en el cuadro de juego.
        :return: Devuelve True/False si el movimiento es válido, por arriba o por abajo.
        """
        # Obtenemos el jugador contrario al que va a colocar la ficha.
        jugadorContrario = self.__GetJugadorContrario(Jugador)

        #region - ARRIBA -

        posicionArribaFicha = -1
        fichaEnemigaEncontrada = False

        if Y - 1 > -1 and Cuadro[Y - 1][X] == Jugador:
            if Echo:
                print("Hay una ficha aliada pegada.")
        else:
            for fila in range(Y - 1, -1, -1):
                if Cuadro[fila][X] == Jugador:
                    if fichaEnemigaEncontrada:
                        posicionArribaFicha = fila
                        if Echo:
                            print("Fila aliada encontrada")
                        break
                    else:
                        if Echo:
                            print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                        break
                elif Cuadro[fila][X] == jugadorContrario:
                    fichaEnemigaEncontrada = True
                else:
                    if Echo:
                        print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                    break

        if posicionArribaFicha != -1 and ColocarFicha:
            self.__ColocarFicha(X, Y, Jugador, Cuadro)
            for fila in range(Y - 1, posicionArribaFicha, -1):
                self.__ColocarFicha(X, fila, Jugador, Cuadro)
        else:
            if Echo:
                print("Nada por arriba")

        #endregion

        #region - ABAJO -
        posicionAbajoFicha = -1
        fichaEnemigaEncontrada = False

        if Y + 1 < 6 and Cuadro[Y + 1][X] == Jugador:
            if Echo:
                print("Hay una ficha aliada pegada.")
        else:
            for fila in range(Y + 1, 6):
                if Cuadro[fila][X] == Jugador:
                    if fichaEnemigaEncontrada:
                        posicionAbajoFicha = fila
                        if Echo:
                            print("Fila aliada encontrada")
                        break
                    else:
                        if Echo:
                            print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                        break
                elif Cuadro[fila][X] == jugadorContrario:
                    fichaEnemigaEncontrada = True
                else:
                    if Echo:
                        print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                    break

        if posicionAbajoFicha != -1 and ColocarFicha:
            self.__ColocarFicha(X, Y, Jugador, Cuadro)
            for fila in range(Y + 1, posicionAbajoFicha):
                self.__ColocarFicha(X, fila, Jugador, Cuadro)
        else:
            if Echo:
                print("Nada por abajo")

        #endregion

        # Comprobamos si alguna de las opciones es un movimiento válido.
        if posicionAbajoFicha == -1 and posicionArribaFicha == -1:
            return False
        else:
            return True

    def __ConvertirFichasHorizontal(self, X, Y, Jugador, Cuadro, Echo=False, ColocarFicha=False):
        """
        Función para comprobar si hay movimientos válidos en horizontal y si, así se indica, colocar la ficha 
        y transformar aquellas que lo requieran.
        :param X: Coordenada X donde se coloca la ficha.
        :param Y: Coordenada Y donde se coloca la ficha.
        :param Jugador: Jugador el cual efectúa el movimiento.
        :param Cuadro: Cuadro del juego sobre el que se comprueba/ejecuta el movimiento.
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        :param ColocarFicha: Indica si se va a colocar la ficha en el cuadro de juego.
        :return: Devuelve True/False si el movimiento es válido, por izquierda o derecha.
        """
        jugadorContrario = self.__GetJugadorContrario(Jugador)

        #region - IZQUIERDA -

        posicionIzquierdaFicha = -1
        fichaEnemigaEncontrada = False

        if X - 1 > -1 and Cuadro[Y][X - 1] == Jugador:
            if Echo:
                print("Hay una ficha aliada pegada.")
        else:
            for columna in range(X - 1, -1, -1):
                if Cuadro[Y][columna] == Jugador:
                    if fichaEnemigaEncontrada:
                        posicionIzquierdaFicha = columna
                        if Echo:
                            print("Fila aliada encontrada")
                        break
                    else:
                        if Echo:
                            print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                        break
                elif Cuadro[Y][columna] == jugadorContrario:
                    fichaEnemigaEncontrada = True
                else:
                    if Echo:
                        print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                    break

        if posicionIzquierdaFicha != -1 and ColocarFicha:
            self.__ColocarFicha(X, Y, Jugador, Cuadro)
            for columna in range(X - 1, posicionIzquierdaFicha, -1):
                self.__ColocarFicha(columna, Y, Jugador, Cuadro)
        else:
            if Echo:
                print("Nada por izquierda")

        #endregion

        #region - DERECHA -

        posicionDerechaFicha = -1
        fichaEnemigaEncontrada = False

        if X + 1 < 6 and Cuadro[Y][X + 1] == Jugador:
            if Echo:
                print("Hay una ficha aliada pegada.")
        else:
            for columna in range(X + 1, 6):
                if Cuadro[Y][columna] == Jugador:
                    if fichaEnemigaEncontrada:
                        posicionDerechaFicha = columna
                        if Echo:
                            print("Fila aliada encontrada")
                        break
                    else:
                        if Echo:
                            print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                        break
                elif Cuadro[Y][columna] == jugadorContrario:
                    fichaEnemigaEncontrada = True
                else:
                    if Echo:
                        print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                    break

        if posicionDerechaFicha != -1 and ColocarFicha:
            self.__ColocarFicha(X, Y, Jugador, Cuadro)
            for columna in range(X + 1, posicionDerechaFicha):
                self.__ColocarFicha(columna, Y, Jugador, Cuadro)
        else:
            if Echo:
                print("Nada por derecha")

        #endregion

        # Comprobamos si alguna de las opciones es un movimiento válido.
        if posicionDerechaFicha == -1 and posicionIzquierdaFicha == -1:
            return False
        else:
            return True

    def __ConvertirFichasDiagonalPrincipal(self, X, Y, Jugador, Cuadro, Echo=False, ColocarFicha=False):
        """
        Función para comprobar si hay movimientos válidos en la diagonal principal y si, así se indica, colocar la ficha 
        y transformar aquellas que lo requieran.
        :param X: Coordenada X donde se coloca la ficha.
        :param Y: Coordenada Y donde se coloca la ficha.
        :param Jugador: Jugador el cual efectúa el movimiento.
        :param Cuadro: Cuadro del juego sobre el que se comprueba/ejecuta el movimiento.
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        :param ColocarFicha: Indica si se va a colocar la ficha en el cuadro de juego.
        :return: Devuelve True/False si el movimiento es válido, hacia arriba-izquierda o abajo-derecha.
        """
        jugadorContrario = self.__GetJugadorContrario(Jugador)

        # Arriba-Izquierda
        posicionArribaIzquierdaFicha = [-1, -1]
        fichaEnemigaEncontrada = False

        if self.__DentroLimitesCuadro(X - 1, Y - 1) is False:
            if Echo:
                print("Fuera de rango.")
        elif Cuadro[Y - 1][X - 1] == Jugador:
            if Echo:
                print("Hay una ficha aliada pegada.")
        else:
            terminado = False
            movX = X - 1
            movY = Y - 1
            while terminado is False:
                if Cuadro[movY][movX] == Jugador:
                    if fichaEnemigaEncontrada:
                        posicionArribaIzquierdaFicha = [movY, movX]
                        if Echo:
                            print("Fila aliada encontrada")
                        terminado = True
                    else:
                        if Echo:
                            print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                        terminado = True
                elif Cuadro[movY][movX] == jugadorContrario:
                    fichaEnemigaEncontrada = True
                else:
                    if Echo:
                        print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                    terminado = True

                movY -= 1
                movX -= 1

                if self.__DentroLimitesCuadro(movX, movY) is False:
                    terminado = True

        if posicionArribaIzquierdaFicha != [-1,-1] and ColocarFicha:
            self.__ColocarFicha(X, Y, Jugador, Cuadro)
            terminado = False
            movX = X
            movY = Y

            while terminado is False:
                self.__ColocarFicha(movX, movY, Jugador, Cuadro)
                movY -= 1
                movX -= 1

                if [movY, movX] == posicionArribaIzquierdaFicha:
                    terminado = True

        else:
            if Echo:
                print("Nada por Arriba-Izquierda")

        # Abajo-Derecha
        posicionAbajoDerechaFicha = [-1, -1]
        fichaEnemigaEncontrada = False

        if self.__DentroLimitesCuadro(X + 1, Y + 1) is False:
            if Echo:
                print("Fuera de rango.")
        elif Cuadro[Y + 1][X + 1] == Jugador:
            if Echo:
                print("Hay una ficha aliada pegada.")
        else:
            terminado = False
            movX = X + 1
            movY = Y + 1
            while terminado is False:
                if Cuadro[movY][movX] == Jugador:
                    if fichaEnemigaEncontrada:
                        posicionAbajoDerechaFicha = [movY, movX]
                        if Echo:
                            print("Fila aliada encontrada")
                        terminado = True
                    else:
                        if Echo:
                            print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                        terminado = True
                elif Cuadro[movY][movX] == jugadorContrario:
                    fichaEnemigaEncontrada = True
                else:
                    if Echo:
                        print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                    terminado = True

                movY += 1
                movX += 1

                if self.__DentroLimitesCuadro(movX, movY) is False:
                    terminado = True

        if posicionAbajoDerechaFicha != [-1,-1] and ColocarFicha:
            self.__ColocarFicha(X, Y, Jugador, Cuadro)
            terminado = False
            movX = X
            movY = Y

            while terminado is False:
                self.__ColocarFicha(movX, movY, Jugador, Cuadro)
                movY += 1
                movX += 1

                if [movY, movX] == posicionAbajoDerechaFicha:
                    terminado = True

        else:
            if Echo:
                print("Nada por Abajo-Derecha")

        # Comprobamos si alguna de las opciones es un movimiento válido.
        if posicionAbajoDerechaFicha == [-1,-1] and posicionArribaIzquierdaFicha == [-1,-1]:
            return False
        else:
            return True

    def __ConvertirFichasDiagonalInversa(self, X, Y, Jugador, Cuadro, Echo=False, ColocarFicha=False):
        """
        Función para comprobar si hay movimientos válidos en la diagonal inversa y si, así se indica, colocar la ficha 
        y transformar aquellas que lo requieran.
        :param X: Coordenada X donde se coloca la ficha.
        :param Y: Coordenada Y donde se coloca la ficha.
        :param Jugador: Jugador el cual efectúa el movimiento.
        :param Cuadro: Cuadro del juego sobre el que se comprueba/ejecuta el movimiento.
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        :param ColocarFicha: Indica si se va a colocar la ficha en el cuadro de juego.
        :return: Devuelve True/False si el movimiento es válido, hacia arriba-derecha o abajo-izquierda.
        """
        jugadorContrario = self.__GetJugadorContrario(Jugador)

        #region - ARRIBA-DERECHA -
        posicionArribaDerechaFicha = [-1, -1]
        fichaEnemigaEncontrada = False

        if self.__DentroLimitesCuadro(X + 1, Y - 1) is False:
            if Echo:
                if Echo:
                    print("Fuera de rango")
        elif Cuadro[Y - 1][X + 1] == Jugador:
            if Echo:
                if Echo:
                    print("Hay una ficha aliada pegada.")
        else:
            terminado = False
            movX = X + 1
            movY = Y - 1
            while terminado is False:
                if Cuadro[movY][movX] == Jugador:
                    if fichaEnemigaEncontrada:
                        posicionArribaDerechaFicha = [movY, movX]
                        if Echo:
                            print("Fila aliada encontrada")
                        terminado = True
                    else:
                        if Echo:
                            print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                        terminado = True
                elif Cuadro[movY][movX] == jugadorContrario:
                    fichaEnemigaEncontrada = True
                else:
                    if Echo:
                        print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                    terminado = True

                movY -= 1
                movX += 1

                if self.__DentroLimitesCuadro(movX, movY) is False:
                    terminado = True

        if posicionArribaDerechaFicha != [-1, -1] and ColocarFicha:
            self.__ColocarFicha(X, Y, Jugador, Cuadro)
            terminado = False
            movX = X
            movY = Y

            while terminado is False:
                self.__ColocarFicha(movX, movY, Jugador, Cuadro)
                movY -= 1
                movX += 1

                if [movY, movX] == posicionArribaDerechaFicha:
                    terminado = True

        else:
            if Echo:
                print("Nada por Arriba-Derecha")

        # Abajo-Izquierda
        posicionAbajoIzquierdaFicha = [-1, -1]
        fichaEnemigaEncontrada = False

        if self.__DentroLimitesCuadro(X - 1, Y + 1) is False:
            if Echo:
                print("Fuera de rango.")
        elif Cuadro[Y + 1][X - 1] == Jugador:
            if Echo:
                print("Hay una ficha aliada pegada.")
        else:
            terminado = False
            movX = X -1
            movY = Y + 1
            while terminado is False:
                if Cuadro[movY][movX] == Jugador:
                    if fichaEnemigaEncontrada:
                        posicionAbajoIzquierdaFicha = [movY, movX]
                        if Echo:
                            print("Fila aliada encontrada")
                        terminado = True
                    else:
                        if Echo:
                            print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                        terminado = True
                elif Cuadro[movY][movX] == jugadorContrario:
                    fichaEnemigaEncontrada = True
                else:
                    if Echo:
                        print("Hay una ficha incorrecta en el camino, no puede colocarse esa ficha")
                    terminado = True

                movY += 1
                movX -= 1

                if self.__DentroLimitesCuadro(movX, movY) is False:
                    terminado = True

        if posicionAbajoIzquierdaFicha != [-1,-1] and ColocarFicha:
            self.__ColocarFicha(X, Y, Jugador, Cuadro)
            terminado = False
            movX = X
            movY = Y

            while terminado is False:
                self.__ColocarFicha(movX, movY, Jugador, Cuadro)
                movY += 1
                movX -= 1

                if [movY, movX] == posicionAbajoIzquierdaFicha:
                    terminado = True

        else:
            if Echo:
                print("Nada por Abajo-Izquierda")

        if posicionAbajoIzquierdaFicha == [-1,-1] and posicionArribaDerechaFicha == [-1,-1]:
            return False
        else:
            return True

    def __SeleccionarPosicionFicha(self, X, Y, Jugador, Cuadro, Echo=False, ColocarFicha=False, Mute=False):
        """
        Función para comprobar si hay movimientos válidos y si, así se indica, colocar la ficha 
        y transformar aquellas que lo requieran.
        :param X: Coordenada X sobre la que se coloca la ficha.
        :param Y: Coordenada Y sobre la que se coloca la ficha.
        :param Jugador: Jugador el cual efectúa el movimiento.
        :param Cuadro: Cuadro del juego sobre el que se comprueba/ejecuta el movimiento.
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        :param ColocarFicha: Indica si se va a colocar la ficha en el cuadro de juego.
        :param Mute: Indica si se imprime por pantalla un mensaje con el resultado.
        :return: Devuelve True/False si el movimiento es válido, hacia arriba-izquierda o abajo-derecha.
        """
        if Cuadro[Y][X] == 0:
            # No existe una ficha en esa casilla.

            #region - VERTICAL -

            if Echo:
                print("")
                print("Movimientos en Vertical:")
                print("------------------------")

            movVertical = self.__ConvertirFichasVertical(X, Y, Jugador, Cuadro, ColocarFicha=ColocarFicha, Echo=Echo)

            #endregion

            #region - HORIZONTAL -

            if Echo:
                print("")
                print("Movimientos en Horizontal:")
                print("------------------------")

            movHorizontal = self.__ConvertirFichasHorizontal(X, Y, Jugador, Cuadro, ColocarFicha=ColocarFicha, Echo=Echo)

            #endregion

            #region - DIAGONAL INVERSA -

            if Echo:
                print("")
                print("Movimientos en Diagonal Inversa:")
                print("------------------------")

            movDiagonalInversa = self.__ConvertirFichasDiagonalInversa(X, Y, Jugador, Cuadro, ColocarFicha=ColocarFicha, Echo=Echo)

            #endregion

            #region - DIAGONAL PRINCIPAL -

            if Echo:
                print("")
                print("Movimientos en Diagonal Principal:")
                print("------------------------")

            movDiagonalPrincipal = self.__ConvertirFichasDiagonalPrincipal(X, Y, Jugador, Cuadro, ColocarFicha=ColocarFicha, Echo=Echo)

            #endregion

            # Comprobamos si alguno de los movimientos posibles es válido.
            if movVertical or movHorizontal or movDiagonalPrincipal or movDiagonalInversa:
                if Mute == False:
                    print("")
                    print("Movimiento VÁLIDO.")
                return True
            else:
                if Mute == False:
                    print("")   
                    print("Movimiento NO VÁLIDO.")
                return False
        else:
            # Ya existe una ficha en esa casilla.
            if Mute == False:
                print("")
                print("Ya hay una ficha en esa casilla.")
            return False

    def __GetNumFichasJugadores(self, Cuadro):
        """
        Función que devuelve el número de fichas en el cuadro de cada jugador.
        :param Cuadro: Tablero del juego.
        :return: Devuelve el número de fichas en el cuadro de cada jugador.
        """
        puntuacionHumano = 0
        puntuacionMaquina = 0
        for fila in range(0, 6):
            for columna in range(0, 6):
                if Cuadro[fila][columna] == 1:
                    puntuacionHumano += 1
                elif Cuadro[fila][columna] == -1:
                    puntuacionMaquina += 1
        return puntuacionHumano, puntuacionMaquina

    def __GetConteoFichasCuadro(self, Cuadro):
        """
        Función que devuelve el número de puntos debido a las fichas en el cuadro de cada jugador.
        :param Cuadro: Tablero del juego.
        :return: Devuelve el número de puntos debido a las fichas en el cuadro de cada jugador.
        """
        puntuacionHumano = 0
        puntuacionMaquina = 0
        for fila in range(0, 6):
            for columna in range(0, 6):
                if Cuadro[fila][columna] == 1:
                    puntuacionHumano += self.__CuadroPuntuaciones[fila][columna]
                elif Cuadro[fila][columna] == -1:
                    puntuacionMaquina += self.__CuadroPuntuaciones[fila][columna]
        return puntuacionHumano, puntuacionMaquina

    def __TieneJugada(self, Jugador, Cuadro, Echo=False):
        """
        Función para comprobar si el jugador indicado tiene movimientos posibles con la configuración del cuadro indicada.
        :param Jugador: Jugador actual.
        :param Cuadro: Tablero del juego.
        :param Echo: Indica si se van imprimiendo mensajes por pantalla acerca de la ejecución.
        :return: Devuelve True si el jugador tiene jugadas posibles, False si no.
        """
        for fila in range(0, 6):
            for columna in range(0, 6):
                if self.__SeleccionarPosicionFicha(X=columna, Y=fila, Jugador=Jugador, Cuadro=Cuadro, Echo=False, ColocarFicha=False, Mute=True):
                    return True
        if Echo:
            print("No tiene movimientos posibles")
        return False

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
        print("Se ha calculado la mejor jugada en:", "\033[1m", tiempoPasado, "\033[0m", "s.")

    def EstadisticasTiemposDeCalculo(self):
        """
        Función para mostrar la gráfica de cálculos de tiempos de creación y análisis del árbol MIN-MAX.
        """
        fig, ax1 = subplots(figsize=(20, 10))
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
            - Primer Jugador.
        """
        while True:
            primerJugadorTemp = -1
            try:
                primerJugadorTemp = input("Introduzca el primer jugador, Humano (H), Máquina (M): ")
            except:
                print("Error")

            if primerJugadorTemp != "H" and primerJugadorTemp != "M":
                print("Error")
            else:
                self.PrimerJugador = primerJugadorTemp
                self.JugadorActual = self.PrimerJugador
                break

    def __GetMovimiento(self):
        """
        Función para obtener los parámetros de una jugaba:
            - Coordenada X.
            - Coordenada Y.
        :return: Coordenadas para colocar una ficha.
        """
        # Coordenada X.
        while True:
            movimientoXTemp = -1
            try:
                movimientoXTemp = int(input("Posición X: "))

                if movimientoXTemp > 5 or movimientoXTemp < 0:
                    print("Error")
                else:
                    break
            except:
                print("Error")

        # Coordenada Y.
        while True:
            movimientoYTemp = -1
            try:
                movimientoYTemp = int(input("Posición Y: "))
                if movimientoYTemp > 5 or movimientoYTemp < 0:
                    print("Error")
                else:
                    break
            except:
                print("Error")

        return movimientoXTemp, movimientoYTemp

    def __GenerarHijosNodo(self, Padre, Jugador):
        """
        Función para generar los hijos dado un nodo padre.
        :param Padre: Nodo sobre el que generar los hijos.
        :param Jugador: Jugador actual.
        :return: Devuelve el nodo padre con su array de hijos actualizada.
        """
        for fila in range(0, 6):
            for columna in range(0, 6):
                if self.__SeleccionarPosicionFicha(columna, fila, Jugador, Padre.Cuadro, False, False, True):
                    cuadroTemp = copy.deepcopy(Padre.Cuadro)
                    self.__SeleccionarPosicionFicha(columna, fila, Jugador=Jugador, Cuadro=cuadroTemp, Echo=False, ColocarFicha=True, Mute=True)
                    hijo = Nodo(Padre=Padre, Cuadro=cuadroTemp, Movimiento=[columna, fila])
                    Padre.Hijos.append(hijo)
        return Padre

    def __AlfaBeta(self, Nodo, Profundidad, Alfa, Beta, Jugador):
        """
        Función para generar el árbol minimax, explorarlo y podarlo si es posible.
        :param Nodo: Nodo actual.
        :param Profundidad: Profundidad actual.
        :param Alfa: Valor actual de alfa.
        :param Beta: Valor actual de beta.
        :param Jugador: Jugador actual.
        :return:
        """
    
        # Fase de transición
        if Profundidad == 0 or self.__TieneJugada(Jugador, Nodo.Cuadro) == False:
            # Profundidad máxima alcanzada o nodo de finalización del juego.

            # Función de evaluación.
            puntuacionHumano, puntuacionMaquina = self.__GetConteoFichasCuadro(Nodo.Cuadro)
            return puntuacionHumano - puntuacionMaquina

        if Jugador == JUGADOR_HUMANO:
            # Jugador humano.
            temp = float("-inf")

            # Generación de los hijos.
            Nodo = self.__GenerarHijosNodo(Nodo, JUGADOR_HUMANO)

            # Llamada recursiva por cada hijo.
            for hijo in Nodo.Hijos:
                resultado = self.__AlfaBeta(hijo, Profundidad-1, Alfa, Beta, JUGADOR_MAQUINA)
                # Cálculo de alfa.
                temp = max(temp, resultado)
                Alfa = max(Alfa, temp)
                hijo.Valor = resultado
                # Comprobamos si hay posible poda beta.
                if Alfa >= Beta:
                    # Poda beta.
                    break
                
            return temp

        else:
            # Jugador máquina.
            temp = float("inf")

            # Generación de los hijos.
            Nodo = self.__GenerarHijosNodo(Nodo, JUGADOR_MAQUINA)

            # Llamada recursiva por cada hijo.
            for hijo in Nodo.Hijos:
                resultado = self.__AlfaBeta(hijo, Profundidad-1, Alfa, Beta, JUGADOR_HUMANO)
                # Cálculo de beta.
                temp = min(temp, resultado)
                Beta = min(Beta, temp)
                hijo.Valor = resultado
                # Comprobamos si hay posible poda alfa.
                if Alfa >= Beta:
                    # Poda alfa.
                    break
            return temp

    def __FinDelJuego(self):
        """
        Función para imprimir los resultados del juego, una vez ha terminado.
        """
        puntuacionHumano, puntuacionMaquina = self.__GetNumFichasJugadores(self.__Cuadro)

        print("Jugador humano:", puntuacionHumano, "Jugador máquina:", puntuacionMaquina)

        if puntuacionHumano - puntuacionMaquina > 0:
            print("")
            print("----------------------------")
            print("| \033[1m" + "HA GANADO EL JUGADOR HUMANO!!! |")
            print("----------------------------", "\033[0m")
        elif puntuacionHumano - puntuacionMaquina < 0:
            print("")
            print("----------------------------")
            print("| \033[1m" + "HA GANADO EL JUGADOR MÁQUINA!!! |")
            print("----------------------------", "\033[0m")
        else:
            print("")
            print("----------------------------")
            print("| \033[1m" + "EMPATE!!! |")
            print("----------------------------", "\033[0m")

    def Jugar(self):
        """
        Flujo principal del juego.
        """
        self.__GetParametros()
        ganador = False

        print("")
        print("---------------------")
        print("| COMIENZA EL JUEGO |")
        print("---------------------")
        print("")

        while ganador is False:
            print("Turno del jugador:", "\033[1m", "\033[0m", self.JugadorActual)
            self.ImprimirCuadroDeJuego()
            ptosHumano, ptosMaquina = self.__GetNumFichasJugadores(self.__Cuadro)
            puntuacion = ptosHumano - ptosMaquina
            print("La puntuación es: " + str(puntuacion))

            if self.__TieneJugada(JUGADOR_HUMANO, self.__Cuadro) == False and self.__TieneJugada(JUGADOR_MAQUINA, self.__Cuadro) == False:
                # FIN DEL JUEGO
                self.__FinDelJuego()
                ganador = True
            else:
                if self.JugadorActual == "H":
                    # Jugador humano.
                    if self.__TieneJugada(JUGADOR_HUMANO, self.__Cuadro):
                        # Tiene movimientos válidos.
                        if self.__Ayuda:
                            # Modo ayuda al jugador humano.

                            # Cálculo del mejor movimiento.
                            self.Raiz = Nodo(Padre=None, Cuadro=copy.deepcopy(self.__Cuadro), Movimiento=None)
                            
                            mejor_jugada = self.__AlfaBeta(self.Raiz, 2*self.__K, float("-inf"), float("inf"), JUGADOR_HUMANO)

                            self.Raiz.Valor = mejor_jugada

                            for hijo in self.Raiz.Hijos:
                                if hijo.Valor == mejor_jugada:
                                    print("Movimiento recomendado", hijo.Movimiento)
                                    break

                        # Solicita al jugador humano, un movimiento válido.
                        movValido = False
                        while movValido == False:
                            movX, movY = self.__GetMovimiento()
                            movValido = self.__SeleccionarPosicionFicha(X=movX, Y=movY, Jugador=1, Cuadro=self.__Cuadro, Echo=False, ColocarFicha=False, Mute=False)
                        self.__SeleccionarPosicionFicha(X=movX, Y=movY, Jugador=1,  Cuadro=self.__Cuadro, Echo=False, ColocarFicha=True, Mute=False)
                        
                    else:
                        # No tiene movimientos válidos.
                        print("No puedes jugar")

                    # Cambio de turno.
                    self.JugadorActual = "M"

                else:
                    # Jugador máquina
                    if self.__TieneJugada(JUGADOR_MAQUINA, self.__Cuadro):
                        # Tiene movimientos válidos.

                        # Cálculo del mejor movimiento.
                        self.Raiz = Nodo(Padre=None, Cuadro=copy.deepcopy(self.__Cuadro), Movimiento=None)

                        self.__EmpezarContarTiempo()
                        mejor_jugada = self.__AlfaBeta(self.Raiz, (2*self.__K) -1, float("-inf"), float("inf"), JUGADOR_MAQUINA)
                        self.__PararContarTiempo(Jugador=self.JugadorActual)

                        self.Raiz.Valor = mejor_jugada

                        for hijo in self.Raiz.Hijos:
                            if hijo.Valor == mejor_jugada:
                                print("La máquina coloca ficha en:", hijo.Movimiento)
                                self.__SeleccionarPosicionFicha(X=hijo.Movimiento[0], Y=hijo.Movimiento[1], Jugador=-1, Cuadro=self.__Cuadro, Echo=False, ColocarFicha=True, Mute=False)
                                break
                        else:
                            # No tiene movimientos válidos.
                            print("La máquina no puede jugar")

                    # Cambio de turno.
                    self.JugadorActual = "H"
                print("")
                print("------------")
                print("")