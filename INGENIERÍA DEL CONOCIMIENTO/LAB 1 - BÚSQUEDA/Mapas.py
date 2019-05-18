import numpy as np
from pylab import *
from Algoritmos import Algoritmo_A_Estrella
from Algoritmos import Algoritmo_Avaro
from Algoritmos import Nodo
import matplotlib.pyplot as plt

class Mapa():

    def __init__(self, Fichero, Costes, ArbolTransitable, AguaAccesible, DistanciaDiagonal, PenalizarMovDiagonal):
        """
        Constructor. Carga un fichero con los datos relativos al mapa.
        :param Fichero: Dirección del fichero de localización.
        :param Costes: Array de costes de transición por cada tipo de celda [terreno, agua, pantano, árbol]
        :param ArbolTransitable: Indica si los árboles son transitables.
        :param AguaAccesible: Indica si el agua es accesible desde el terreno.
        :param DistanciaDiagonal: Distancia D2.
        :param PenalizarMovDiagonal: Indica si se van a penalizar, en cuanto al coste, si se va a tomar un camino en diagonal.
        """

        # Inicialización de arrays de datos que se van a obtener acerca de los algoritmos
        self.CostesAStar = []
        self.CostesAvara = []
        self.CostesOptimosFichero = []
        self.NumNodosExpAStar = []
        self.NumNodosExpAvara = []

        # Comprobaciones acerca de los parámetros de entrada
        if DistanciaDiagonal > 0:
            self.DistanciaDiagonal = DistanciaDiagonal
        else:
            print("La DistanciaDiagonal no puede ser negativa.")
            return None

        if isinstance(PenalizarMovDiagonal, bool) is True:
            self.PenalizarMovDiagonal = PenalizarMovDiagonal
        else:
            print("PenalizarMovDiagonal debe de ser de tipo boolean.")

        self.AguaAccesible = AguaAccesible

        if len(Costes) is 4:
            self.Costes = Costes
        else:
            print("El tamaño del array de costes no corresponde con el número de tipos de celdas transitables.")
            return None

        if self.Costes[0] < 1:
            print("El coste del paso por el terreno no puede ser negativo")
            return None

        if self.Costes[1] < 1:
            print("El coste del paso por el agua no puede ser negativo")
            return None

        if self.Costes[2] < 1:
            print("El coste del paso por el pantano no puede ser negativo")
            return None

        if ArbolTransitable is False:
            self.Costes[3] = -1
        elif ArbolTransitable is True and self.Costes[3] < 1:
            print("El coste del paso por el árbol no puede ser negativo")
            return None

        # Lectura del fichero de mapa
        with open(Fichero) as f:
            content = f.readlines()
            content = [x.strip() for x in content]

        # Inicialización de los mapas que se van a utilizar
        self.mapa = []
        self.mapa_objetos = []
        self.mapa_colores = []

        # Dimensiones del mapa
        self.largo = int(content[1].split()[1])
        self.ancho = int(content[2].split()[1])

        # Nombre del mapa
        self.nombreMapa = Fichero.split(sep='/')[-1]

        print("Cargando mapa de " + str(self.largo) + "x" + str(self.ancho) + ".")

        # Mapa costes
        for i in range(0, self.largo):
            linea = []
            for j in range(0, self.ancho):
                celda = content[4 + i][j]
                linea.append(self.__ParseoCelda(celda))
            self.mapa.append(linea)

        # Mapa de tipos de celda
        for i in range(0, self.largo):
            linea = []
            for j in range(0, self.ancho):
                celda = content[4 + i][j]
                linea.append(self.__ParseoCeldaPalabra(celda))
            self.mapa_objetos.append(linea)

        # Mapa de colores
        for i in range(0, self.largo):
            linea = []
            for j in range(0, self.ancho):
                celda = content[4 + i][j]
                linea.append(self.__ParseoCeldaColores(celda))
            self.mapa_colores.append(linea)

        # Se transforman los mapas a arrays de numpy
        self.mapa = np.array(self.mapa)
        self.mapa_objetos = np.array(self.mapa_objetos)
        self.mapa_colores = np.array(self.mapa_colores)
        self.mapa_imprimir = np.copy(self.mapa_colores)

        # Imprimimos el mapa cargado
        self.__ImprimirMapaColores()

    def __ParseoCelda(self, Caracter):
        """
        Función para parsear los tipos de celdas a los costes oportunos.
        :param Caracter: Caracter a parsear.
        :return: Devuelve el caracter parseado.
        """
        if Caracter == '.':
            return self.Costes[0]
        if Caracter == 'G':
            return self.Costes[0]
        if Caracter == '@':
            return -1
        if Caracter == 'O':
            return -1
        if Caracter == 'T':
            return self.Costes[3]
        if Caracter == 'S':
            return self.Costes[2]
        if Caracter == 'W':
            return self.Costes[1]

    def __ParseoCeldaColores(self, Caracter):
        """
        Función para parsear los tipos de celdas a los colores oportunos.
        :param Caracter: Caracter a parsear.
        :return: Devuelve el color parseado.
        """
        if Caracter == '.':
            return [255, 255, 255]
        if Caracter == 'G':
            return [255, 255, 255]
        if Caracter == '@':
            return [121, 85, 61]
        if Caracter == 'O':
            return [121, 85, 61]
        if Caracter == 'T':
            return [87, 166, 57]
        if Caracter == 'S':
            return [132, 195, 190]
        if Caracter == 'W':
            return [59, 131, 189]

    def __ParseoCeldaPalabra(self, Caracter):
        """
        Función para parsear los tipos de celdas al tipo de celda oportuno.
        :param Caracter: Caracter a parsear.
        :return: Devuelve la palabra parseada.
        """
        if Caracter == '.':
            return "Terreno"
        if Caracter == 'G':
            return "Terreno"
        if Caracter == '@':
            return "Muro"
        if Caracter == 'O':
            return "Muro"
        if Caracter == 'T':
            return "Arbol"
        if Caracter == 'S':
            return "Pantano"
        if Caracter == 'W':
            return "Agua"

    def __ImprimirMapaColores(self):
        """
        Función para mostrar el mapa de colores.
        :return: Muestra el mapa de colores.
        """
        fig, ax = subplots(figsize=(20, 10))
        im = plt.imshow(self.mapa_imprimir, interpolation='none', aspect='auto')

        plt.show()

    def __ImprimirGraficasCostes(self):
        """
        Función para mostrar la gráfica de costes.
        """

        self.CostesOptimosFichero = list(map(float, self.CostesOptimosFichero))

        fig, ax1 = subplots(figsize=(20, 10))

        ax1.plot(self.CostesAStar, label='Coste A*', color='c', marker='o')
        ax1.plot(self.CostesAvara, label='Coste Avara', color='g', marker='o')
        ax1.plot(self.CostesOptimosFichero, label='Coste Óptimo Fichero', color='r', marker='o')

        fig.suptitle('Costes por cada prueba y algoritmo', fontsize=20)
        plt.xlabel('Prueba')
        plt.ylabel("Coste")
        legend(loc='upper left')
        ax1.grid('on')

        plt.show()

        print("Costes A*", self.CostesAStar)
        print("Costes Avara", self.CostesAvara)
        print("Costes Óptimos fichero", self.CostesOptimosFichero)

    def __ImprimirGraficasNodosExpandidos(self):
        """
        Función para mostrar la gráfica de nodos expandidos.
        """
        fig, ax1 = subplots(figsize=(20, 10))

        ax1.plot(self.NumNodosExpAStar, label='Nodos expandidos A*', color='r', marker='o')
        ax1.plot(self.NumNodosExpAvara, label='Nodos expandidos Avara', color='g', marker='o')

        fig.suptitle('Nodos expendidos por cada prueba y algoritmo', fontsize=20)
        plt.xlabel('Prueba')
        plt.ylabel("Nodos expendidos")
        legend(loc='upper left')
        ax1.grid('on')

        plt.show()
        print("Nodos expandidos A*", self.NumNodosExpAStar)
        print("Nodos expandidos Avara", self.NumNodosExpAvara)

    def __Astar(self, Inicio, Fin, DistanciaComparada=None):

        """
        Función para ejecutar el algoritmo A* sobre el mapa dado un inicio y un fin. Devuelve el camino recorrido
        y los valores f, g y h para cada nodo.
        :param Inicio: Nodo inicial.
        :param Fin: Nodo final.
        :param DistanciaComparada: Distancia óptima precalculada.
        :return: Devuelve el camino recorrido y los valores f, g y h para cada nodo.
        """
        print("======================")

        print("Búsqueda A*")
        print("----------------------")

        print("Inicio: " + str(Inicio))
        print("Fin:    " + str(Fin))

        inalcanzable = False

        # Comprobamos que el nodo inicial es accesible
        if self.mapa[Inicio[0]][Inicio[1]] == -1:
            print("La posición inicial es: " + self.mapa_objetos[Inicio[0]][Inicio[1]])
            inalcanzable = True

        # Comprobamos que el nodo final es accesible
        if self.mapa[Fin[0]][Fin[1]] == -1:
            print("La posición final es: " + self.mapa_objetos[Fin[0]][Fin[1]])
            inalcanzable = True

        # Si el nodo inicial o el nodo final no son accesibles, terminamos el algoritmo
        if inalcanzable == True:
            return False, -1, -1, -1, -1

        # Ejecución del algoritmo A*
        camino, abiertos, cerrados = Algoritmo_A_Estrella(self.mapa, self.mapa_objetos, Inicio, Fin, self.DistanciaDiagonal, \
                                                          self.Costes, self.AguaAccesible, self.PenalizarMovDiagonal)

        # Creamos una copia del mapa de colores para imprimir el camino
        self.mapa_imprimir = np.copy(self.mapa_colores)

        print("----------------------")
        print("Coste total: " + str(camino[-1].G))

        # Imprimimos la comparación del coste calculado con el que figura en el fichero
        if DistanciaComparada is not None:
            print("Distancia óptima: " + str(DistanciaComparada))
            print("Distancia comparada: " + str(float(DistanciaComparada) - float(camino[-1].G)))

        # Pintamos los nodos cerrados en el mapa
        for nodo in cerrados:
            self.mapa_imprimir[nodo.Posicion[0]][nodo.Posicion[1]] = [128, 128, 128]

        # Pintamos los nodos abiertos en el mapa
        for nodo in abiertos:
            self.mapa_imprimir[nodo.Posicion[0]][nodo.Posicion[1]] = [255, 255, 0]

        # Pintamos el camino en el mapa
        for nodo in camino:
            print("Coordenadas: (" + str(nodo.Posicion[0]) + "," + str(nodo.Posicion[1]) + ")", end=", ")
            print("F: %.5f" % nodo.F, end=", ")
            print("G: %.5f" % nodo.G, end=", ")
            print("H: %.5f" % nodo.H, end="\n")
            self.mapa_imprimir[nodo.Posicion[0]][nodo.Posicion[1]] = [255, 0, 0]
        print("----------------------")

        return True, len(abiertos), len(abiertos), camino[-1].G, DistanciaComparada

    def __Greedy(self, Inicio, Fin, DistanciaComparada=None):
        """
        Función para ejecutar el algoritmo Avara sobre el mapa dado un inicio y un fin. Devuelve el camino recorrido
        y los valores f, g y h para cada nodo.
        :param Inicio: Nodo inicial.
        :param Fin: Nodo final.
        :param DistanciaComparada: Distancia óptima precalculada.
        :return: Devuelve el camino recorrido y los valores f, g y h para cada nodo.
        """
        print("=======================================================================================================")
        print("Búsqueda Avara")
        print("----------------------")
        print("Inicio: " + str(Inicio))
        print("Fin:    " + str(Fin))

        inalcanzable = False

        # Comprobamos que el nodo inicial es accesible
        if self.mapa[Inicio[0]][Inicio[1]] == -1:
            print("La posición inicial es: " + self.mapa_objetos[Inicio[0]][Inicio[1]])
            inalcanzable = True

        # Comprobamos que el nodo final es accesible
        if self.mapa[Fin[0]][Fin[1]] == -1:
            print("La posición final es: " + self.mapa_objetos[Fin[0]][Fin[1]])
            inalcanzable = True

        # Si el nodo inicial o el nodo final no son accesibles, terminamos el algoritmo
        if inalcanzable == True:
            return False, -1, -1, -1, -1

        # Ejecución del algoritmo Avaro
        camino, abiertos, cerrados = Algoritmo_Avaro(self.mapa, self.mapa_objetos, Inicio, Fin, self.DistanciaDiagonal,\
                                                     self.Costes, self.AguaAccesible, self.PenalizarMovDiagonal)

        # Creamos una copia del mapa de colores para imprimir el camino
        self.mapa_imprimir = np.copy(self.mapa_colores)

        print("----------------------")
        print("Coste total: " + str(camino[-1].G))

        if DistanciaComparada is not None:
            print("Distancia óptima: " + str(DistanciaComparada))
            print("Distancia comparada: " + str(float(DistanciaComparada) - float(camino[-1].G)))

        # Pintamos los nodos cerrados en el mapa
        for nodo in cerrados:
            self.mapa_imprimir[nodo.Posicion[0]][nodo.Posicion[1]] = [128, 128, 128]

        # Pintamos los nodos abiertos en el mapa
        for nodo in abiertos:
            self.mapa_imprimir[nodo.Posicion[0]][nodo.Posicion[1]] = [255, 255, 0]

        # Pintamos el camino en el mapa
        for nodo in camino:
            print("Coordenadas: (" + str(nodo.Posicion[0]) + "," + str(nodo.Posicion[1]) + ")", end=", ")
            print("F: %.5f" % nodo.F, end=", ")
            print("G: %.5f" % nodo.G, end=", ")
            print("H: %.5f" % nodo.H, end="\n")
            self.mapa_imprimir[nodo.Posicion[0]][nodo.Posicion[1]] = [255, 0, 0]
        print("----------------------")

        return True, len(abiertos), len(abiertos), camino[-1].G, DistanciaComparada

    def EjercutarFicheroPruebas(self, Fichero):
        """
        Función para ejecutar en cascada todas las búsquedas indicadas en un fichero .sce
        :param Inicio: Nodo inicial
        :param Fin: Nodo final
        :param DistanciaComparada: Distancia "óptima" indicada en el fichero.
        """
        # Lectura del fichero de pruebas
        with open(Fichero) as f:
            content = f.readlines()
            content = [x.strip() for x in content]

        indice = 1
        terminado = False

        # Iteramos sobre las filas del fichero
        while terminado is False:

            # Comprobamos que la línea a buscar no excede el número de líneas del fichero
            if indice < len(content):

                # Dividimos cada parámetro de la fila y los guardamos en un array
                linea = content[indice].split()

                # Para ser válido, necesitamos 9 parámetros
                if len(linea) == 9:

                    # Comprobamos que el nombre del mapa, su ancho y alto coinciden con el mapa cargado
                    if self.nombreMapa == linea[1] and self.ancho == int(linea[2]) and self.largo == int(linea[3]):

                        print("****************************************************************************************")
                        print("Búsqueda: " + str(indice))

                        posicionInicio = [int(linea[4]), int(linea[5])]
                        posicionFinal = [int(linea[6]), int(linea[7])]

                        ejecucion_Astar_terminada, abiertos, cerrados, coste, distanciaOptima = self.__Astar(posicionInicio, posicionFinal, linea[8])

                        if ejecucion_Astar_terminada:
                            self.CostesOptimosFichero.append(distanciaOptima)
                            self.__ImprimirMapaColores()
                            self.CostesAStar.append(coste)
                            self.NumNodosExpAStar.append(abiertos + cerrados)
                        else:
                            print("A*, Objetivo no alcanzado.")

                        ejecucion_Avara_terminada, abiertos, cerrados, coste, distanciaOptima = self.__Greedy(posicionInicio, posicionFinal, linea[8])

                        if ejecucion_Avara_terminada:
                            self.__ImprimirMapaColores()
                            self.CostesAvara.append(coste)
                            self.NumNodosExpAvara.append(abiertos + cerrados)
                        else:
                            print("Avara, Objetivo no alcanzado.")

                    else:
                        print("El nombre de mapa / ancho / alto no coincide.")
                else:
                    # Bucle terminado
                    terminado = True

                # Movemos el índice a la siguiente fila
                indice += 1

            else:
                # Bucle terminado
                terminado = True

        # Imprimimos las gráficas de información
        self.__ImprimirGraficasCostes()
        self.__ImprimirGraficasNodosExpandidos()