import pandas as pd
import numpy as np

class APrioriSeq():
    """
    Clase con la funcionalidad para ejecutar el algoritmo apriori para hallar patrones de asociación.
    """
    def ExcelPrueba(self, Fichero):
        """
        Función para cargar el fichero de pruebas "dummy".
        :param Fichero: Ruta del fichero.
        """
        fichero_datos = pd.ExcelFile(Fichero)
        fichero_datos.sheet_names
        self.Datos = fichero_datos.parse("Hoja1")
        self.Datos = self.Datos.groupby('id_cliente')['itemcomprado'].apply(list)
        self.Datos = self.Datos.reset_index(drop=False)
        self.Datos["items"] = self.Datos['itemcomprado'].apply(lambda x: self.__UniquePrueba(x))

        self.Itemset = self.__CalcularItemsetPrueba(self.Datos['items'])
        self.Itemset = np.array(sorted(self.Itemset))

    def CargaDataframe(self, Datos, Columna):
        """
        Función para cargar un fichero de datos con los patrones ya agrupados.
        :param Datos: Ruta del fichero de datos.
        :param Columna: Columna donde se encuentran los datos.
        """
        self.Datos = Datos.copy()
        self.Datos["items"] = self.Datos[Columna].apply(lambda x: self.__Unique(x))
        display(self.Datos)
        self.Itemset = self.__CalcularItemset(self.Datos['items'])
        self.Itemset = np.array(sorted(self.Itemset))

    def __Combinaciones(self, Columna, K):
        """
        Función para calcular las combinaciones de los itemsets candidatos.
        :param Columna: Columna donde están los itemsets.
        :param K: Iteración.
        """
        combinaciones = []
        combinaciones_str = []

        for item in Columna:
            for item_2 in Columna:
                for elemento in item_2:
                    temp = item.copy()
                    temp.append(elemento)
                    if temp not in combinaciones:
                        if len(temp) == K:
                            combinaciones.append(temp)

        for item in Columna:
            for item_2 in Columna:
                if item is not item_2:
                    for elemento in item_2:
                        temp = item.copy()
                        temp.append(elemento)
                        temp = sorted(temp)
                        temp = "".join(str(x) for x in temp)
                        if temp not in combinaciones_str:
                            if len(temp) == K:
                                combinaciones_str.append(temp)
                                combinaciones.append([temp])

        return combinaciones

    def __UniquePrueba(self, Array):
        """
        Función para calcular el itemset de los ficheros de prueba.
        :param Array: Array de items.
        """
        items = []
        for transaccion in Array:
            items.append(transaccion)
        return items

    def __Unique(self, Array):
        """
        Función para calcular el itemset de los ficheros.
        :param Array: Array de items.
        """
        return np.unique(Array)

    def __CalcularFreqSoporteRefractor(self, Transaccion, Columna):
        """
        Función para calcular la frecuencia soporte.
        :param Item: Item sobre el que se va a calcular.
        :param Columna: Columna del dataset para calcular la frecuencia soporte.
        :return: Devuelve la frecuencia soporte.
        """
        count = 0
        for fila in Columna:
            len_Item = len(Transaccion)
            items_encontrados = 0
            indice_temp = 0
            for item in range(0, len(Transaccion)):
                for fila_actual_i in range(indice_temp, len(fila)):
                    if items_encontrados == len(Transaccion):
                        break
                    if Transaccion[item] in fila[fila_actual_i]:
                        indice_temp = fila_actual_i + 1
                        items_encontrados += 1
                        break

            if items_encontrados == len_Item:
                count += 1
        return count

    def __CalcularItemsetPrueba(self, Columna):
        """
        Función para calcular los itemsets del fichero de pruebas.
        :param Columna: Columna con las transacciones.
        :return: Devuelve la lista de itemsets.
        """
        lista_itemset = []
        for i in range(0, len(Columna)):
            for item in Columna[i]:
                for item_i in item:
                    if item_i not in lista_itemset:
                        lista_itemset.append(item_i)
        return lista_itemset

    def __CalcularItemset(self, Columna):
        """
        Función para calcular los itemsets.
        :param Columna: Columna con las transacciones.
        :return: Devuelve la lista de itemsets.
        """
        lista_itemset = []
        for i in range(0, len(Columna)):
            for item in Columna[i]:
                if isinstance(item, list):
                    for item_i in item:
                        if item_i not in lista_itemset:
                            lista_itemset.append(item_i)
                else:
                    if item not in lista_itemset:
                        lista_itemset.append(item)
        return lista_itemset

    def __BorrarUltimo(self, Transaccion):
        """
        Función para borrar el primer item.
        :param Transaccion: Transacción a la cual borrar.
        :return: Devuelve la transacción.
        """
        temp = Transaccion.copy()
        if len(Transaccion) > 1:
            del temp[0]
        else:
            temp = temp[0]
            temp = temp[1:]
        return temp

    def __BorrarPrimero(self, Transaccion):
        """
        Función para borrar el último item.
        :param Transaccion: Transacción a la cual borrar.
        :return: Devuelve la transacción.
        """
        temp = Transaccion.copy()
        if len(Transaccion) > 1:
            del temp[-1]
        else:
            temp = temp[0]
            temp = temp[:-1]
        return temp

    def __CombinacionesGSP(self, k):
        """
        Función para calcular las combinaciones según el algoritmo gsp.
        :param k: Iteración.
        """
        temp = []
        temp_st = []
        temp_last = []
        for index, row in self.Soporte.iterrows():
            item = self.Soporte.loc[index, "Item"]

            borrarUltimo = self.__BorrarUltimo(item)
            borrarPrimero = self.__BorrarPrimero(item)

            if len(item) == 1:
                temp_st.append([borrarUltimo])
                temp_last.append([borrarPrimero])

                data = {'Item': item, 'Frec. Soporte': self.Soporte.loc[index, "Frec. Soporte"],
                        'Soporte': self.Soporte.loc[index, "Soporte"], '-1st': [borrarPrimero], '-Last': [borrarUltimo]}
                temp.append(data)
            else:
                if k > 2:

                    if len(borrarUltimo[0]) > 1:

                        temp_c = borrarPrimero.copy()
                        temp_c.append(borrarUltimo[0][0])
                        temp_st.append(borrarUltimo)
                        temp_last.append(temp_c)

                        borrarPrimero.append(borrarUltimo[0][1])

                        data = {'Item': item, 'Frec. Soporte': self.Soporte.loc[index, "Frec. Soporte"],
                                'Soporte': self.Soporte.loc[index, "Soporte"], '-1st': borrarUltimo,
                                '-Last': borrarPrimero}

                        temp.append(data)
                    else:
                        temp_st.append(borrarUltimo)
                        temp_last.append(borrarPrimero)
                else:
                    temp_st.append(borrarUltimo)
                    temp_last.append(borrarPrimero)


        self.Soporte["-1st"] = temp_st
        self.Soporte["-Last"] = temp_last
        dataf = pd.DataFrame(temp, columns= ["Item", "Frec. Soporte", "Soporte", "-1st", "-Last"])
        self.Soporte = self.Soporte.append(dataf)

    def __CalcularItemSetsFrecuentes(self, Minimo, Echo=False):
        """
        Función para calcular los itemsets frecuentes.
        :param Minimo: Frecuencia soporte umbral.
        :param Echo: Indica si se imprime por pantalla el avance de la función.
        """
        print("")
        print("Iniciando algoritmo apriori para patrones de asociación...")
        print("")
        print("Itemset:")
        print("")

        display(pd.DataFrame(self.Itemset))

        print("")
        print("-------")
        print("")

        print("Probando k = 1")

        self.Soporte = pd.DataFrame()
        print("Calculando combinaciones")
        self.Soporte["Item"] = self.Itemset
        self.Soporte["Item"] = self.Soporte['Item'].apply(lambda x: [x])
        print("Calculando Frec.Soporte")
        self.Soporte["Frec. Soporte"] = self.Soporte['Item'].apply(lambda x: self.__CalcularFreqSoporteRefractor(x, self.Datos["items"]))
        print("Calculando Soporte")
        self.Soporte["Soporte"] = self.Soporte["Frec. Soporte"] / len(self.Datos)
        self.Soporte = self.Soporte[self.Soporte["Frec. Soporte"] >= Minimo]

        End = False
        k = 2

        display(self.Soporte)

        print("")
        print("-------")
        print("")

        while End is False:
            print("Probando k = " + str(k))

            Soporte_bk = self.Soporte.copy()
            Dataframe_temp = pd.DataFrame()
            print("Calculando combinaciones")
            if k == 2:
                Dataframe_temp["Item"] = self.__Combinaciones(Soporte_bk["Item"], k)
                if Echo:
                    print("Las combinaciones son :", Dataframe_temp["Item"])
            else:
                Dataframe_temp["Item"] = Soporte_bk["Item"]
            print("Calculando Frec.Soporte")
            Dataframe_temp["Frec. Soporte"] = Dataframe_temp['Item'].apply(lambda x: self.__CalcularFreqSoporteRefractor(x, self.Datos["items"]))
            print("Calculando Soporte")
            Dataframe_temp["Soporte"] = Dataframe_temp["Frec. Soporte"] / len(self.Datos)
            print("Filtrando Soporte mínimo >= " + str(Minimo))

            Dataframe_temp = Dataframe_temp[Dataframe_temp["Frec. Soporte"] >= Minimo]

            if len(Dataframe_temp) == 0:
                print("")
                print("Terminado")
                End = True
                break

            Dataframe_temp = Dataframe_temp.reset_index(drop=True)

            display(Dataframe_temp)

            if len(Dataframe_temp) is not 0:
                self.Soporte = Dataframe_temp.copy()
                self.Soporte = self.Soporte.reset_index(drop=False)
                del self.Soporte["index"]
                self.__CombinacionesGSP(k)
                self.Soporte = self.Soporte.reset_index(drop=True)

                if Echo:
                    display(self.Soporte)

                lista = []

                for index, row in self.Soporte.iterrows():

                    item = self.Soporte.loc[index, "Item"]
                    primeroBorrado = self.Soporte.loc[index, "-1st"]
                    ultimoBorrado = self.Soporte.loc[index, "-Last"]

                    for index2, row2 in self.Soporte.iterrows():

                        item2 = self.Soporte.loc[index2, "Item"]
                        primeroBorrado2 = self.Soporte.loc[index2, "-1st"]
                        ultimoBorrado2 = self.Soporte.loc[index2, "-Last"]

                        if index2 != index and item != item2:
                            if primeroBorrado == ultimoBorrado2:
                                temp = []

                                if len(item) == 1:
                                    for item_ in item:
                                        temp.append(item_)
                                    temp.append(primeroBorrado2[0])
                                else:
                                    temp.append(ultimoBorrado[0])
                                    for item_ in item2:
                                        temp.append(item_)

                                if temp not in lista:
                                    lista.append(temp)

                self.Soporte = pd.DataFrame()

                if len(lista) == 0:
                    print("")
                    print("Terminado")
                    End = True
                    break
                else:
                    self.Soporte["Item"] = lista
                    self.Soporte = self.Soporte.reset_index(drop=True)
                    if Echo:
                        display(self.Soporte)
                    k = k + 1

            elif k == 2:
                print("Terminado")
                End = True
                Soporte_bk = Soporte_bk.iloc[0:0]

            else:
                print("Terminado")
                End = True

            print("")
            print("-------")
            print("")

        self.Reglas = Soporte_bk

    def CalcularReglasDeConfianza(self, FreSoporteMin, Echo=False):
        """
        Función principal para calculas la reglas
        :param FreSoporteMin: Frecuencia soporte mínima de las reglas.
        :param Echo: Indica si se imprime por pantalla el avance de la función.
        """
        self.__CalcularItemSetsFrecuentes(FreSoporteMin, Echo)