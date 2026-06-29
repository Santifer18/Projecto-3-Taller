# main.py
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from arbol import ArbolDecision, Nodo
from gestor import GestorArchivos

class InterfazJuego:
    # E: El objeto de ventana principal root de Tkinter
    # S: Instancia de la clase InterfazJuego
    # F: Inicializa los componentes graficos, la logica y genera los archivos de muestra
    # R: Ninguna
    def __init__(self, root):
        self.root = root
        self.root.title("Puedo leer tu mente")
        self.root.geometry("500x500")
        self.juego = ArbolDecision()
        self.gestor = GestorArchivos()
        self.gestor.generar_ejemplos()
        try:
            self.imagen_personaje = tk.PhotoImage(file="personaje.png")
        except Exception:
            self.imagen_personaje = None
        self.frame_actual = None
        self.mostrar_pantalla_inicial()

    # E: Ninguna
    # S: Ninguna
    # F: Destruye el contenedor grafico activo para dar espacio a la siguiente pantalla
    # R: Ninguna
    def limpiar_pantalla(self):
        if self.frame_actual:
            self.frame_actual.destroy()

    # E: Ninguna
    # S: Ninguna
    # F: Renderiza el menu principal con el titulo, la imagen y los botones de control uniformes
    # R: Ninguna
    def mostrar_pantalla_inicial(self):
        self.limpiar_pantalla()
        self.juego.reiniciar_partida()
        self.frame_actual = tk.Frame(self.root)
        self.frame_actual.pack(fill="both", expand=True, padx=20, pady=20)
        titulo = tk.Label(self.frame_actual, text="Puedo leer tu mente", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)
        if self.imagen_personaje:
            lbl_img = tk.Label(self.frame_actual, image=self.imagen_personaje)
            lbl_img.pack(pady=10)
        else:
            lbl_img_placeholder = tk.Label(self.frame_actual, text="[personaje.png]", font=("Arial", 10, "italic"))
            lbl_img_placeholder.pack(pady=10)
        instrucciones = tk.Label(self.frame_actual, text="Piensa en algo, con mis poderes leere tu mente y adivinare tu pensamiento.", justify="center")
        instrucciones.pack(pady=15)
        btn_jugar = tk.Button(self.frame_actual, text="Iniciar Partida", width=25, command=self.iniciar_partida)
        btn_jugar.pack(pady=5)
        btn_cargar = tk.Button(self.frame_actual, text="Cargar Árbol desde Archivo", width=25, command=self.solicitar_cargar_archivo)
        btn_cargar.pack(pady=5)
        btn_salir = tk.Button(self.frame_actual, text="Salir", width=25, command=self.root.quit)
        btn_salir.pack(pady=5)

    # E: Ninguna
    # S: Ninguna
    # F: Despliega el buscador de archivos de sistema e intenta mutar la raiz logica del juego
    # R: El archivo seleccionado debe pasar los filtros de consistencia del Gestor
    def solicitar_cargar_archivo(self):
        ruta = filedialog.askopenfilename(title="Seleccionar árbol de decisión", filetypes=[("Archivos de texto", "*.txt")])
        if ruta:
            lector = GestorArchivos(ruta)
            try:
                nueva_raiz = lector.cargar_arbol()
                self.juego.raiz = nueva_raiz
                self.gestor = lector  
                messagebox.showinfo("Éxito", "El árbol se ha cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error de Carga", f"{str(e)}\nSe mantendrá el árbol por defecto.")

    # E: Ninguna
    # S: Ninguna
    # F: Limpia la interfaz e invoca el ciclo de renderizado de preguntas
    # R: Ninguna
    def iniciar_partida(self):
        self.limpiar_pantalla()
        self.juego.reiniciar_partida()
        self.mostrar_pregunta_o_hoja()

    # E: Ninguna
    # S: Ninguna
    # F: Evalua el tipo de nodo actual para pintar botones de recorrido o botones de prediccion
    # R: Ninguna
    def mostrar_pregunta_o_hoja(self):
        self.limpiar_pantalla()
        self.frame_actual = tk.Frame(self.root)
        self.frame_actual.pack(fill="both", expand=True, pady=40)
        nodo = self.juego.nodo_actual
        if nodo.es_pregunta:
            lbl_pregunta = tk.Label(self.frame_actual, text=nodo.valor, font=("Arial", 14), wraplength=400)
            lbl_pregunta.pack(pady=30)
            frame_btn = tk.Frame(self.frame_actual)
            frame_btn.pack(pady=10)
            btn_si = tk.Button(frame_btn, text="Sí", width=10, command=lambda: self.procesar_respuesta(True))
            btn_si.pack(side="left", padx=20)
            btn_no = tk.Button(frame_btn, text="No", width=10, command=lambda: self.procesar_respuesta(False))
            btn_no.pack(side="left", padx=20)
        else:
            lbl_prediccion = tk.Label(self.frame_actual, text=f"¿Estabas pensando en: {nodo.valor}?", font=("Arial", 14, "bold"), wraplength=400)
            lbl_prediccion.pack(pady=30)
            frame_btn = tk.Frame(self.frame_actual)
            frame_btn.pack(pady=10)
            btn_correcto = tk.Button(frame_btn, text="¡Sí, adivinaste!", width=15, command=self.sistema_gana)
            btn_correcto.pack(side="left", padx=20)
            btn_incorrecto = tk.Button(frame_btn, text="No, fallaste", width=15, command=self.sistema_falla)
            btn_incorrecto.pack(side="left", padx=20)

    # E: Un valor booleano
    # S: Ninguna
    # F: Ejecuta el metodo avanzar del arbol logico y actualiza la ventana grafica
    # R: Ninguna
    def procesar_respuesta(self, es_si):
        self.juego.responder(es_si)
        self.mostrar_pregunta_o_hoja()

    # E: Ninguna
    # S: Ninguna
    # F: Informa la victoria mediante un cuadro de dialogo y retorna al menu de inicio
    # R: Ninguna
    def sistema_gana(self):
        messagebox.showinfo("¡Gané!", "¡Excelente! He adivinado correctamente.")
        self.mostrar_pantalla_inicial()

    # E: Ninguna
    # S: Ninguna
    # F: Captura los nuevos strings de datos mediante dialogos emergentes y aplica re-estructuracion mecanica
    # R: Las entradas del usuario no pueden enviarse en blanco
    def sistema_falla(self):
        respuesta_incorrecta = self.juego.nodo_actual.valor
        nueva_resp = simpledialog.askstring("Aprendizaje", "¿En qué estabas pensando?")
        if not nueva_resp or nueva_resp.strip() == "":
            messagebox.showwarning("Validación", "La respuesta no puede estar vacía.")
            return self.mostrar_pantalla_inicial()
        nueva_preg = simpledialog.askstring("Aprendizaje", f"Escribe una pregunta que diferencie a '{nueva_resp.strip()}' de '{respuesta_incorrecta}':")
        if not nueva_preg or nueva_preg.strip() == "":
            messagebox.showwarning("Validación", "La pregunta no puede estar vacía.")
            return self.mostrar_pantalla_inicial()
        nueva_preg = nueva_preg.strip()
        if not (nueva_preg.startswith("¿") or nueva_preg.endswith("?")):
            nueva_preg = f"¿{nueva_preg}?"
        confirmacion = messagebox.askyesno("Confirmación", f"Para '{nueva_resp.strip()}', ¿la respuesta a la pregunta '{nueva_preg}' sería SÍ?")
        self.juego.aprender(respuesta_incorrecta, nueva_resp.strip(), nueva_preg, confirmacion)
        exito_guardado = self.gestor.guardar_arbol(self.juego.raiz)
        if exito_guardado:
            messagebox.showinfo("Aprendizaje Completo", f"¡He aprendido algo nuevo y guardé mi conocimiento en {self.gestor.ruta_archivo}!")
        else:
            messagebox.showwarning("Error de guardado", "Aprendí la respuesta, pero hubo problemas escribiendo en el disco.")
        self.mostrar_pantalla_inicial()


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazJuego(root)
    root.mainloop()
