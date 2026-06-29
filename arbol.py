# arbol.py

class Nodo:
    def __init__(self, valor, es_pregunta=True):
        self.valor = valor
        self.es_pregunta = es_pregunta
        self.si = None   # Rama izquierda para el "Sí"
        self.no = None   # Rama derecha para el "No"


class ArbolDecision:
    def __init__(self):
        self.raiz = self.crear_arbol_defecto()
        self.nodo_actual = self.raiz

    def crear_arbol_defecto(self):
        """Crea el árbol básico por defecto requerido (RF-03)."""
        raiz = Nodo("¿Es un animal?", es_pregunta=True)
        raiz.si = Nodo("perro", es_pregunta=False)
        raiz.no = Nodo("computadora", es_pregunta=False)
        return raiz

    def reiniciar_partida(self):
        """Regresa el puntero del juego a la raíz (RF-12)."""
        self.nodo_actual = self.raiz

    def responder(self, respuesta_si):
        """Avanza en el árbol según la respuesta Sí/No (RF-04)."""
        if respuesta_si:
            self.nodo_actual = self.nodo_actual.si
        else:
            self.nodo_actual = self.nodo_actual.no
        return self.nodo_actual

    def aprender(self, respuesta_incorrecta, nueva_respuesta, nueva_pregunta, respuesta_es_si):
        """
        Modifica el árbol reemplazando la respuesta incorrecta por una pregunta
        y reubicando ambas respuestas en sus respectivas ramas (RF-09).
        """
        nodo_nueva_resp = Nodo(nueva_respuesta, es_pregunta=False)
        nodo_vieja_resp = Nodo(respuesta_incorrecta, es_pregunta=False)
        
        # El nodo actual muta a nodo de pregunta
        self.nodo_actual.valor = nueva_pregunta
        self.nodo_actual.es_pregunta = True
        
        # Se posicionan las respuestas según la condición dada
        if respuesta_es_si:
            self.nodo_actual.si = nodo_nueva_resp
            self.nodo_actual.no = nodo_vieja_resp
        else:
            self.nodo_actual.si = nodo_vieja_resp
            self.nodo_actual.no = nodo_nueva_resp