# arbol.py

class Nodo:
    # E: Un valor string y un booleano que indica si es pregunta o no
    # S: Instancia de la clase Nodo
    # F: Inicializa un nodo para la estructura del arbol binario
    # R: Ninguna
    def __init__(self, valor, es_pregunta=True):
        self.valor = valor
        self.es_pregunta = es_pregunta
        self.si = None   
        self.no = None   


class ArbolDecision:
    # E: Ninguna
    # S: Instancia de la clase ArbolDecision
    # F: Construye el arbol de decision asignando la raiz por defecto y el puntero de juego
    # R: Ninguna
    def __init__(self):
        self.raiz = self.crear_arbol_defecto()
        self.nodo_actual = self.raiz

    # E: Ninguna
    # S: Un objeto de tipo Nodo que sirve como raiz
    # F: Genera la estructura base del juego preguntando si es una persona
    # R: El arbol inicial debe ser binario y poseer al menos la estructura base
    def crear_arbol_defecto(self):
        raiz = Nodo("¿Es una persona?", es_pregunta=True)
        raiz.si = Nodo("¿Es un deportista?", es_pregunta=True)
        raiz.si.si = Nodo("Messi", es_pregunta=False)
        raiz.si.no = Nodo("Einstein", es_pregunta=False)
        raiz.no = Nodo("¿Es un objeto?", es_pregunta=True)
        raiz.no.si = Nodo("Celular", es_pregunta=False)
        raiz.no.no = Nodo("Pino", es_pregunta=False)
        return raiz

    # E: Ninguna
    # S: Ninguna
    # F: Restablece el puntero del nodo actual regresandolo a la raiz del arbol
    # R: Ninguna
    def reiniciar_partida(self):
        self.nodo_actual = self.raiz

    # E: Un valor booleano que representa la respuesta del usuario (Si/No)
    # S: El objeto Nodo al que se avanzo en la estructura
    # F: Desplaza el puntero actual del juego hacia el hijo izquierdo o derecho
    # R: El nodo actual debe tener hijos asignados validos
    def responder(self, respuesta_si):
        if respuesta_si:
            self.nodo_actual = self.nodo_actual.si
        else:
            self.nodo_actual = self.nodo_actual.no
        return self.nodo_actual

    # E: Dos strings de respuestas, un string de pregunta y un booleano de direccion
    # S: Ninguna
    # F: Transforma una hoja en una pregunta e interconecta la respuesta vieja y la nueva
    # R: Los campos de texto suministrados no deben estar vacios
    def aprender(self, respuesta_incorrecta, nueva_respuesta, nueva_pregunta, respuesta_es_si):
        nodo_nueva_resp = Nodo(nueva_respuesta, es_pregunta=False)
        nodo_vieja_resp = Nodo(respuesta_incorrecta, es_pregunta=False)
        self.nodo_actual.valor = nueva_pregunta
        self.nodo_actual.es_pregunta = True
        if respuesta_es_si:
            self.nodo_actual.si = nodo_nueva_resp
            self.nodo_actual.no = nodo_vieja_resp
        else:
            self.nodo_actual.si = nodo_vieja_resp
            self.nodo_actual.no = nodo_nueva_resp
