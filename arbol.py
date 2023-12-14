######## Arbol binario #############
class nodoArbol(object):
    def __init__(self, info):
        self.izq = None
        self.der = None
        self.info = info

    def serialize(self):
        return {"info": self.info}

def insertarNodo(raiz, info):
    if(raiz is None):
        raiz = nodoArbol(info)
    elif(info["nombre"] < raiz.info["nombre"]):
        raiz.izq = insertarNodo(raiz.izq,info)
    else:
        raiz.der = insertarNodo(raiz.der,info)
    return raiz

def arbolVacio(raiz):
    return raiz is None

def remplazar(raiz):
    aux = None
    if(raiz.der is None):
        aux = raiz
        raiz = raiz.izq
    else:
        raiz.der, aux = remplazar(raiz.der)
    return raiz, aux

def eliminarNodo(raiz,info):
    x = None
    if(raiz is not None):
        if(info<raiz.info["nombre"]):
            raiz.izq, x = eliminarNodo(raiz.izq,info)
        elif(info>raiz.info["nombre"]):
            raiz.der, x = eliminarNodo(raiz.der,info)
        else:
            x=raiz.info
            if(raiz.izq is None):
                raiz = raiz.der
            elif(raiz.der is None):
                raiz = raiz.izq
            else:
                raiz.izq, aux = remplazar(raiz.izq)
                raiz.info = aux.info
    return raiz, x

def buscar(raiz, texto, funcion_de_coincidencia):
    if raiz is None:
        return None
    elif funcion_de_coincidencia(texto, raiz):
        print(raiz)
        return raiz
    else:
        if texto.lower() < raiz.info["nombre"].lower():
            return buscar(raiz.izq, texto, funcion_de_coincidencia)
        else:
            return buscar(raiz.der, texto, funcion_de_coincidencia)

def imprimirInOrden(raiz):
    if(raiz is not None):
        imprimirInOrden(raiz.izq)
        print(raiz.info)
        imprimirInOrden(raiz.der)

def imprimirPreOrden(raiz):
    if(raiz is not None):
        print(raiz.info)
        imprimirPreOrden(raiz.izq)
        imprimirPreOrden(raiz.der)

