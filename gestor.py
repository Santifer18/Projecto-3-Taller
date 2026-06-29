# gestor.py
import os
from arbol import Nodo

class GestorArchivos:
    def __init__(self, ruta_archivo="arbol.txt"):
        self.ruta_archivo = ruta_archivo

    def guardar_arbol(self, raiz):
        """Guarda el árbol en un archivo .txt usando recorrido Preorden."""
        try:
            with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
                self._guardar_recursivo(raiz, f)
            return True
        except Exception:
            return False

    def _guardar_recursivo(self, nodo, archivo):
        if nodo is None:
            return
        prefijo = "P:" if nodo.es_pregunta else "R:"
        archivo.write(f"{prefijo}{nodo.valor}\n")
        self._guardar_recursivo(nodo.si, archivo)
        self._guardar_recursivo(nodo.no, archivo)

    def cargar_arbol(self):
        """Carga y reconstruye el árbol desde el archivo validando errores (RF-02)."""
        if not os.path.exists(self.ruta_archivo):
            raise FileNotFoundError("El archivo seleccionado no existe.") [cite: 80]
        
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                lineas = [linea.strip() for linea in f.readlines()]
        except Exception:
            raise IOError("No se pudo leer el archivo. Verifique los permisos.") [cite: 80]
        
        if not lineas or (len(lineas) == 1 and lineas[0] == ""):
            raise ValueError("El archivo está vacío.") [cite: 81]
            
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
                raise ValueError("El formato está dañado o es incorrecto.") [cite: 81]

        try:
            raiz_reconstruida = construir()
            if raiz_reconstruida is None:
                raise ValueError()
            return raiz_reconstruida
        except Exception:
            raise ValueError("El contenido no permite reconstruir un árbol válido.") [cite: 81]

    def generar_5_ejemplos_obligatorios(self):
        """Genera los 5 archivos .txt requeridos con al menos 10 respuestas cada uno (RF-15)."""
        ejemplos = {
            "arbol_animales.txt": [
                "P:¿Vive en el agua?", "P:¿Es un mamífero?", "R:ballena", "R:tiburón",
                "P:¿Tiene alas?", "P:¿Vuela alto?", "R:águila", "R:gallina",
                "P:¿Es doméstico?", "P:¿Ladra?", "R:perro", "R:gato",
                "P:¿Tiene rayas?", "R:cebra", "P:¿Tiene cuello largo?", "R:jirafa", "R:elefante"
            ],
            "arbol_peliculas.txt": [
                "P:¿Es de animación?", "P:¿Es de Disney?", "R:El Rey León", "R:Shrek",
                "P:¿Es de superhéroes?", "P:¿Es de Marvel?", "R:Iron Man", "R:Batman",
                "P:¿Tiene varitas mágicas?", "R:Harry Potter", "P:¿Es en el espacio?",
                "P:¿Usa sables de luz?", "R:Star Wars", "R:Interstellar", "R:Titanic"
            ],
            "arbol_comidas.txt": [
                "P:¿Es un plato salado?", "P:¿Lleva queso?", "P:¿Es de origen italiano?", "R:pizza", "R:hamburguesa",
                "P:¿Es comida típica mexicana?", "R:tacos", "R:sushi",
                "P:¿Es un postre?", "P:¿Es frío?", "R:helado", "R:pastel",
                "P:¿Es una fruta?", "P:¿Es roja?", "R:manzana", "R:plátano", "R:café"
            ],
            "arbol_deportes.txt": [
                "P:¿Se juega en equipo?", "P:¿Se usa un balón redondo?", "P:¿Se juega principalmente con los pies?", "R:fútbol", "R:baloncesto",
                "P:¿Se usa una red?", "R:voleibol", "R:béisbol",
                "P:¿Se usa una raqueta?", "P:¿Se juega en una mesa?", "R:ping pong", "R:tenis",
                "P:¿Es un deporte acuático?", "R:natación", "P:¿Es de combate?", "R:boxeo", "R:ajedrez"
            ],
            "arbol_videojuegos.txt": [
                "P:¿Es un juego multijugador?", "P:¿Es del género Battle Royale?", "R:Fortnite", "P:¿Es de estrategia?", "R:League of Legends", "R:Minecraft",
                "P:¿Es de mundo abierto?", "P:¿El protagonista es Link?", "R:Zelda: Breath of the Wild", "R:GTA V",
                "P:¿Es de plataformas?", "P:¿El protagonista es un fontanero?", "R:Super Mario Odyssey", "R:Sonic", "R:Tetris"
            ]
        }
        
        for nombre_archivo, lineas in ejemplos.items():
            if not os.path.exists(nombre_archivo):
                with open(nombre_archivo, 'w', encoding='utf-8') as f:
                    for linea in lineas:
                        f.write(f"{linea}\n")