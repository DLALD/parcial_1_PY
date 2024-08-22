import tkinter as tk
from PIL import Image, ImageTk

# Función para verificar la respuesta del niño
def verificar_respuesta(respuesta):
    if respuesta == producto_actual:
        mostrar_mensaje_emergente(imagen_aprobacion)
    else:
        mostrar_mensaje_emergente(imagen_error)

# Función para mostrar el GIF animado en una ventana emergente sin marco
def mostrar_mensaje_emergente(imagen_resultado):
    ventana_emergente = tk.Toplevel(ventana)
    
    # Hacer la ventana emergente sin borde y sin título
    ventana_emergente.overrideredirect(True)
    ventana_emergente.geometry("300x300+{}+{}".format(
        ventana.winfo_pointerx() - 150, 
        ventana.winfo_pointery() - 150
    ))

    # Crear una etiqueta para mostrar el GIF animado
    lbl_resultado = tk.Label(ventana_emergente)
    lbl_resultado.pack(pady=20, padx=20, expand=True)

    # Configurar y actualizar el GIF animado
    actualizar_gif(imagen_resultado, lbl_resultado)

    # Cerrar la ventana emergente después de un tiempo
    ventana_emergente.after(2000, ventana_emergente.destroy)  # Cierra después de 2 segundos

# Función para actualizar el GIF animado
def actualizar_gif(imagen_resultado, lbl_resultado):
    if hasattr(imagen_resultado, 'frames'):
        frame = imagen_resultado.frame_index
        lbl_resultado.config(image=imagen_resultado.frames[frame])
        lbl_resultado.image = imagen_resultado.frames[frame]
        imagen_resultado.frame_index = (frame + 1) % imagen_resultado.frame_count
        ventana.after(imagen_resultado.delay, lambda: actualizar_gif(imagen_resultado, lbl_resultado))

# Función para cambiar el producto a reciclar
def cambiar_producto(direccion):
    global producto_actual, imagen_actual
    # Determinar el índice de la imagen actual
    idx = productos.index(imagen_actual)
    
    # Cambiar al producto siguiente o anterior
    if direccion == "siguiente":
        idx = (idx + 1) % len(productos)
    elif direccion == "anterior":
        idx = (idx - 1) % len(productos)
    
    # Actualizar la imagen y el estado del producto actual
    imagen_actual = productos[idx]
    lbl_producto.config(image=imagenes[imagen_actual])
    lbl_producto.image = imagenes[imagen_actual]
    producto_actual = respuestas[imagen_actual]
    lbl_estado.config(text=f"Selecciona el contenedor para el {producto_actual.capitalize()}")

# Función para crear la interfaz
def crear_interfaz():
    global ventana, ruta_imagenes, lbl_producto, lbl_estado, producto_actual, imagen_actual, productos, imagenes, respuestas
    global imagen_aprobacion, imagen_error

    ventana = tk.Tk()
    ventana.title("Reciclaje y Reutilización")
    
    # Configuración del fondo de la ventana
    ventana.config(bg='green')

    # Ruta de las imágenes
    ruta_imagenes = r"C:\Users\Estudiante\Documents\P_A\Parcial_1\imagenes\\"

    # Cargar imágenes
    try:
        img_papel = Image.open(ruta_imagenes + "pp.png")
        img_papel = ImageTk.PhotoImage(img_papel)

        img_plastico = Image.open(ruta_imagenes + "ppl.png")
        img_plastico = ImageTk.PhotoImage(img_plastico)

        img_vidrio = Image.open(ruta_imagenes + "pv.png")
        img_vidrio = ImageTk.PhotoImage(img_vidrio)

        img_pa = Image.open(ruta_imagenes + "pa.png")
        img_pa = ImageTk.PhotoImage(img_pa)

        img_bp = Image.open(ruta_imagenes + "bp.png")
        img_bp = ImageTk.PhotoImage(img_bp)

        img_bv = Image.open(ruta_imagenes + "bv.png")
        img_bv = ImageTk.PhotoImage(img_bv)

        # Cargar imágenes de aprobación y error (GIF)
        img_aprobacion = Image.open(ruta_imagenes + "mg.gif")
        imagen_aprobacion = ImageTk.PhotoImage(img_aprobacion)
        
        img_error = Image.open(ruta_imagenes + "ce.gif")
        imagen_error = ImageTk.PhotoImage(img_error)

        # Configurar GIF animado
        imagen_aprobacion = configurar_gif(img_aprobacion)
        imagen_error = configurar_gif(img_error)
    except Exception as e:
        tk.messagebox.showerror("Error", f"No se pudo cargar una de las imágenes: {e}")
        ventana.quit()
        return

    # Diccionario de imágenes y respuestas
    imagenes = {
        "pa.png": img_pa,
        "bp.png": img_bp,
        "bv.png": img_bv
    }
    
    respuestas = {
        "pa.png": "papel",
        "bp.png": "plastico",
        "bv.png": "vidrio"
    }

    productos = list(imagenes.keys())
    producto_actual = respuestas[productos[0]]
    imagen_actual = productos[0]

    # Etiqueta para mostrar el producto a reciclar
    lbl_producto = tk.Label(ventana, image=imagenes[imagen_actual], bg='green')
    lbl_producto.grid(row=0, column=1, pady=20, padx=20)

    # Etiqueta para mostrar el estado
    lbl_estado = tk.Label(ventana, text=f"Selecciona el contenedor para el {producto_actual.capitalize()}", font=('Arial', 16), bg='green', fg='white')
    lbl_estado.grid(row=1, column=1, pady=10)

    # Botones para cambiar entre imágenes
    btn_anterior = tk.Button(ventana, text="<", command=lambda: cambiar_producto("anterior"), font=('Arial', 18), width=5, height=2, bg='darkgreen', fg='white')
    btn_anterior.grid(row=0, column=0, padx=10)

    btn_siguiente = tk.Button(ventana, text=">", command=lambda: cambiar_producto("siguiente"), font=('Arial', 18), width=5, height=2, bg='darkgreen', fg='white')
    btn_siguiente.grid(row=0, column=2, padx=10)

    # Botones de los contenedores
    btn_papel = tk.Button(ventana, image=img_papel, command=lambda: verificar_respuesta("papel"), bg='green')
    btn_papel.grid(row=2, column=0, padx=10, pady=10)

    btn_plastico = tk.Button(ventana, image=img_plastico, command=lambda: verificar_respuesta("plastico"), bg='green')
    btn_plastico.grid(row=2, column=1, padx=10, pady=10)

    btn_vidrio = tk.Button(ventana, image=img_vidrio, command=lambda: verificar_respuesta("vidrio"), bg='green')
    btn_vidrio.grid(row=2, column=2, padx=10, pady=10)

    ventana.mainloop()

def configurar_gif(imagen):
    frames = []
    try:
        # Cargar todos los frames del GIF animado
        while True:
            frame = imagen.copy()
            frames.append(ImageTk.PhotoImage(frame))
            imagen.seek(imagen.tell() + 1)
    except EOFError:
        pass

    if frames:
        frames[0].frame_count = len(frames)
        frames[0].delay = imagen.info.get('duration', 100)  # Obtener la duración del GIF o usar 100 ms por defecto
        frames[0].frame_index = 0
        frames[0].frames = frames
        frames[0].frame = frames[0]
    return frames[0]

# Ejecutar la interfaz
crear_interfaz()
