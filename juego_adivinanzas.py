# main.py
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from arbol import ArbolDecision, Nodo
from gestor import GestorArchivos

class InterfazJuego:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina en qué estoy pensando")
        self.root.geometry("500x400")
        
        # Instancias básicas de lógica y persistencia
        self.juego = ArbolDecision()
        self.gestor = GestorArchivos()
        
        # Generar los 5 archivos de prueba automáticamente al arrancar
        self.gestor.generar_5_ejemplos_obligatorios()
        
        # Contenedor principal de pantallas
        self.frame_actual = None
        self.mostrar_pantalla_inicial()

    def limpiar_pantalla(self):
        if self.frame_actual:
            self.frame_actual.destroy()

    def mostrar_pantalla_inicial(self):
        """RF-01: Pantalla Inicial"""
        self.limpiar_pantalla()
        self.juego.reiniciar_partida()
        
        self.frame_actual = tk.Frame(self.root)
        self.frame_actual.pack(fill="both", expand=True, padx=20, pady=20)
        
        titulo = tk.Label(self.frame_actual, text="¡Adivina en qué estoy pensando!", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)
        
        instrucciones = tk.Label(self.frame_actual, text="Piensa en algo. Intentaré adivinarlo haciendo preguntas de Sí o No.\nSi fallo, ¡aprenderé de ti!", justify="center")
        instrucciones.pack(pady=10)
        
        btn_jugar = tk.Button(self.frame_actual, text="Iniciar Partida", width=20, bg="#4CAF50", fg="white", command=self.iniciar_partida)
        btn_jugar.pack(pady=10)
        
        btn_cargar = tk.Button(self.frame_actual, text="Cargar Árbol desde Archivo", width=20, command=self.solicitar_cargar_archivo)
        btn_cargar.pack(pady=10)
        
        btn_salir = tk.Button(self.frame_actual, text="Salir", width=20, bg="#f44336", fg="white", command=self.root.quit)
        btn_salir.pack(pady=10)

    def solicitar_cargar_archivo(self):
        """RF-02: Selección y carga controlada de archivos."""
        ruta = filedialog.askopenfilename(title="Seleccionar árbol de decisión", filetypes=[("Archivos de texto", "*.txt")])
        if ruta:
            lector = GestorArchivos(ruta)
            try:
                nueva_raiz = lector.cargar_arbol()
                self.juego.raiz = nueva_raiz
                self.gestor = lector  # Actualizamos el gestor activo para autoguardado en este archivo
                messagebox.showinfo("Éxito", "El árbol se ha cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error de Carga", f"{str(e)}\nSe mantendrá el árbol por defecto.")

    def iniciar_partida(self):
        """Cambia el entorno a modo juego."""
        self.limpiar_pantalla()
        self.juego.reiniciar_partida()
        self.mostrar_pregunta_o_hoja()

    def mostrar_pregunta_o_hoja(self):
        """RF-13: Visualización dinámica según el tipo de nodo."""
        self.limpiar_pantalla()
        
        self.frame_actual = tk.Frame(self.root)
        self.frame_actual.pack(fill="both", expand=True, pady=40)
        
        nodo = self.juego.nodo_actual
        
        if nodo.es_pregunta:
            # Pantalla de Pregunta Intermedia (RF-04 / RF-05)
            lbl_pregunta = tk.Label(self.frame_actual, text=nodo.valor, font=("Arial", 14), wraplength=400)
            lbl_pregunta.pack(pady=30)
            
            frame_btn = tk.Frame(self.frame_actual)
            frame_btn.pack(pady=10)
            
            btn_si = tk.Button(frame_btn, text="Sí", width=10, bg="#2196F3", fg="white", command=lambda: self.procesar_respuesta(True))
            btn_si.pack(side="left", padx=20)
            
            btn_no = tk.Button(frame_btn, text="No", width=10, bg="#E91E63", fg="white", command=lambda: self.procesar_respuesta(False))
            btn_no.pack(side="left", padx=20)
        else:
            # Pantalla de Predicción Final (RF-06)
            lbl_prediccion = tk.Label(self.frame_actual, text=f"¿Estabas pensando en: {nodo.valor}?", font=("Arial", 14, "bold"), wraplength=400)
            lbl_prediccion.pack(pady=30)
            
            frame_btn = tk.Frame(self.frame_actual)
            frame_btn.pack(pady=10)
            
            btn_correcto = tk.Button(frame_btn, text="¡Sí, adivinaste!", width=15, bg="#4CAF50", fg="white", command=self.sistema_gana)
            btn_correcto.pack(side="left", padx=20)
            
            btn_incorrecto = tk.Button(frame_btn, text="No, fallaste", width=15, bg="#f44336", fg="white", command=self.sistema_falla)
            btn_incorrecto.pack(side="left", padx=20)

    def procesar_respuesta(self, es_si):
        self.juego.responder(es_si)
        self.mostrar_pregunta_o_hoja()

    def sistema_gana(self):
        """RF-07: Mensaje de victoria."""
        messagebox.showinfo("¡Gané!", "¡Excelente! He adivinado correctamente.")
        self.mostrar_pantalla_inicial()

    def sistema_falla(self):
        """RF-08 y RF-14: Despliega los formularios para el nuevo aprendizaje."""
        respuesta_incorrecta = self.juego.nodo_actual.valor
        
        # Pedir respuesta correcta
        nueva_resp = simpledialog.askstring("Aprendizaje", "¿En qué estabas pensando?")
        if not nueva_resp or nueva_resp.strip() == "":
            messagebox.showwarning("Validación", "La respuesta no puede estar vacía.")
            return self.mostrar_pantalla_inicial()
            
        # Pedir pregunta diferenciadora
        nueva_preg = simpledialog.askstring("Aprendizaje", f"Escribe una pregunta que diferencie a '{nueva_resp.strip()}' de '{respuesta_incorrecta}':")
        if not nueva_preg or nueva_preg.strip() == "":
            messagebox.showwarning("Validación", "La pregunta no puede estar vacía.")
            return self.mostrar_pantalla_inicial()
            
        # Asegurar formato de pregunta
        nueva_preg = nueva_preg.strip()
        if not (nueva_preg.startswith("¿") or nueva_preg.endswith("?")):
            nueva_preg = f"¿{nueva_preg}?"

        # Validar si la respuesta a esa pregunta es Sí o No
        confirmacion = messagebox.askyesno("Confirmación", f"Para '{nueva_resp.strip()}', ¿la respuesta a la pregunta '{nueva_preg}' sería SÍ?")
        
        # Modificar el árbol lógicamente
        self.juego.aprender(respuesta_incorrecta, nueva_resp.strip(), nueva_preg, confirmacion)
        
        # RF-10: Guardado automático obligatorio
        exito_guardado = self.gestor.guardar_arbol(self.juego.raiz)
        if exito_guardado:
            messagebox.showinfo("Aprendizaje Completo", f"¡He aprendido algo nuevo y guardé mi conocimiento en {self.gestor.ruta_archivo}!")
        else:
            messagebox.showwarning("Error de guardado", "Aprendí la respuesta, pero hubo problemas escribiendo en el disco.")
            
        self.mostrar_pantalla_inicial()


# ==========================================
# BLOQUE DE EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazJuego(root)
    root.mainloop()