# gestor.py
import os
from arbol import Nodo

class GestorArchivos:
    # E: Un string opcional que determina la ruta del archivo de texto
    # S: Instancia de la clase GestorArchivos
    # F: Inicializa el gestor asignandole la ruta del archivo de trabajo
    # R: Ninguna
    def __init__(self, ruta_archivo="arbol.txt"):
        self.ruta_archivo = ruta_archivo

    # E: El objeto Nodo correspondiente a la raiz del arbol
    # S: Un valor booleano que indica si el proceso fue exitoso o no
    # F: Abre un archivo en modo escritura y arranca el guardado en formato de texto plano
    # R: Permisos de escritura validos en el almacenamiento local
    def guardar_arbol(self, raiz):
        try:
            with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
                self._guardar_recursivo(raiz, f)
            return True
        except Exception:
            return False

    # E: Un objeto Nodo y el descriptor del archivo abierto
    # S: Ninguna
    # F: Recorre de manera recursiva en preorden escribiendo los prefijos correspondientes
    # R: Ninguna
    def _guardar_recursivo(self, nodo, archivo):
        if nodo is None:
            return
        prefijo = "P:" if nodo.es_pregunta else "R:"
        archivo.write(f"{prefijo}{nodo.valor}\n")
        self._guardar_recursivo(nodo.si, archivo)
        self._guardar_recursivo(nodo.no, archivo)

    # E: Ninguna
    # S: El objeto Nodo raiz reconstruido desde el archivo de texto plano
    # F: Lee las lineas secuenciales y genera la estructura binaria de toma de decisiones
    # R: El archivo debe existir, poseer datos y mantener la estructura valida de preorden
    def cargar_arbol(self):
        if not os.path.exists(self.ruta_archivo):
            raise FileNotFoundError("El archivo seleccionado no existe.")
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                lineas = [linea.strip() for linea in f.readlines()]
        except Exception:
            raise IOError("No se pudo leer el archivo. Verifique los permisos.")
        if not lineas or (len(lineas) == 1 and lineas[0] == ""):
            raise ValueError("El archivo está vacío.")
        def construir():
            if not lineas:
                return None
            linea = lineas.pop(0)
            if linea.startswith("P:"):
                nodo = Nodo(linea[2:], es_pregunta=True)
                nodo.si = construir()
                nodo.no = construir()
                return nodo
            elif linea.startswith("R:"):
                return Nodo(linea[2:], es_pregunta=False)
            else:
                raise ValueError("El formato está dañado o es incorrecto.")
        try:
            raiz_reconstruida = construir()
            if raiz_reconstruida is None:
                raise ValueError()
            return raiz_reconstruida
        except Exception:
            raise ValueError("El contenido no permite reconstruir un árbol válido.")

    # E: Ninguna
    # S: Ninguna
    # F: Escribe en disco 5 archivos de texto estructurados segun los temas solicitados
    # R: Cada arbol generado debe contener mas de 10 respuestas en su recorrido binario
    def generar_ejemplos(self):
        ejemplos = {
            "arbol_animales.txt": [
                "P:¿Es terrestre?", 
                "P:¿Es doméstico?", "P:¿Ladra?", "R:perro", "R:gato", 
                "P:¿Tiene cuello largo?", "R:jirafa", "P:¿Tiene rayas?", "R:cebra", "R:elefante",
                "P:¿Vive en el mar?", "P:¿Es un mamífero?", "R:ballena", "R:tiburón", 
                "P:¿Tiene alas?", "P:¿Vuela alto?", "R:águila", "R:gallina", "R:pulpo"
            ],
            "arbol_peliculas.txt": [
                "P:¿Es un personaje?", 
                "P:¿Es de Disney?", "P:¿Es un león?", "R:Simba", "R:Aladdín", 
                "P:¿Es de Marvel?", "R:Iron Man", "P:¿Usa capa?", "R:Batman", "R:Shrek",
                "P:¿Es de animación?", "P:¿Tiene juguetes vivos?", "R:Toy Story", "R:Nemo", 
                "P:¿Es de romance?", "R:Titanic", "P:¿Es en el espacio?", "R:Avatar", "R:Inception"
            ],
            "arbol_comidas.txt": [
                "P:¿Es salado?", 
                "P:¿Lleva queso?", "P:¿Es italiano?", "R:pizza", "R:hamburguesa", 
                "P:¿Lleva arroz?", "R:sushi", "P:¿Usa tortillas?", "R:tacos", "R:papas fritas",
                "P:¿Es un postre?", "P:¿Es frío?", "R:helado", "R:pastel", 
                "P:¿Es una fruta?", "P:¿Es amarilla?", "R:plátano", "R:manzana", "R:chocolate"
            ],
            "arbol_deportes.txt": [
                "P:¿Utiliza una bola?", 
                "P:¿Se juega con los pies?", "P:¿Se juega en cancha grande?", "R:fútbol", "R:fútbol sala", 
                "P:¿Se usa una red?", "R:voleibol", "P:¿Se encesta?", "R:baloncesto", "R:béisbol",
                "P:¿Se juega con raqueta?", "P:¿Tiene una mesa?", "R:ping pong", "R:tenis", 
                "P:¿Es acuático?", "R:natación", "P:¿Es de combate?", "R:boxeo", "R:ajedrez"
            ],
            "arbol_videojuegos.txt": [
                "P:¿Es multijugador?", 
                "P:¿Es un Battle Royale?", "P:¿Es de construcción?", "R:Fortnite", "R:Apex Legends", 
                "P:¿Es de estrategia?", "R:League of Legends", "P:¿Es de disparos?", "R:Counter Strike", "R:Minecraft",
                "P:¿Es de mundo abierto?", "P:El héroe es Link?", "R:Zelda", "R:GTA V", 
                "P:¿Es de carreras?", "R:Mario Kart", "P:¿Es de bloques?", "R:Tetris", "R:Pacman"
            ]
        }
        for nombre_archivo, lineas in ejemplos.items():
            if not os.path.exists(nombre_archivo):
                with open(nombre_archivo, 'w', encoding='utf-8') as f:
                    for linea in lineas:
                        f.write(f"{linea}\n")
