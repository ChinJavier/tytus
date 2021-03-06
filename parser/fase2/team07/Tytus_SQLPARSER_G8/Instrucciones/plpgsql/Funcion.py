from Instrucciones.TablaSimbolos.Instruccion import Instruccion

class Funcion(Instruccion):
    def __init__(self, id, parametros, tipo, declaraciones, instrucciones, strGram, linea, columna, strSent):
        Instruccion.__init__(self,None,linea,columna, strGram, strSent)
        self.id = id
        self.parametros = parametros
        self.tipo = tipo
        self.declaraciones = declaraciones
        self.instrucciones = instrucciones

    def ejecutar(self, tabla, arbol):
        tabla.setFuncion(self, arbol)

    def traducir(self,tabla,arbol,cadenaTraducida):
        tabla.setFuncion(self, arbol)
        codigo = ""

        #Se declara la funcion con el nombre
        codigo += "\t@with_goto\n"
        codigo += "\tdef " + self.id + "("

        #Se añaden los parametros si es que estos existen
        if self.parametros is not None:
            contadorParametros = 0
            for par in self.parametros[:-1]:
                if par == "$":
                    codigo += "S" + str(contadorParametros) + ","
                else:
                    codigo += par + ","
                contadorParametros = contadorParametros + 1
            
            if self.parametros[-1] == "$":
                codigo += "S" + str(contadorParametros)
            else:
                codigo += self.parametros[-1]


        codigo += "):\n"

        #Se agregan las declaraciones
        if self.declaraciones is not None:
            for dec in self.declaraciones:
                codigo += dec.traducir(tabla,arbol,cadenaTraducida).replace("\t", "\t\t") + "\n"

        #Se agrega todo el contenido de las instrucciones traducido a 3D
        for ins in self.instrucciones:
            temp = ins.traducir(tabla,arbol,cadenaTraducida).replace("\t", "\t\t") + "\n"
            codigo += temp.replace("\t\t\t\t", "\t\t\t")

        return codigo