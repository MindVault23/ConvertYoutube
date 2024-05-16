import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO

def descargar_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        ruta_descarga = os.path.join("Descargas", "Videos")
        os.makedirs(ruta_descarga, exist_ok=True)
        ruta_video = stream.download(output_path=ruta_descarga)
        mostrar_mensaje("Descarga completada", "El video se ha descargado exitosamente.")
    except Exception as e:
        mostrar_mensaje("Error", f"No se pudo descargar el video: {e}")

def descargar_audio(url, formato, sample_rate):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        ruta_descarga = os.path.join("Descargas", "Audios")
        os.makedirs(ruta_descarga, exist_ok=True)
        if formato == "MP3":
            ruta_audio = stream.download(output_path=ruta_descarga)
            # Renombrar el archivo para reflejar el formato correcto
            nuevo_nombre = os.path.splitext(ruta_audio)[0] + ".mp3"
            os.rename(ruta_audio, nuevo_nombre)
        elif formato == "WAV":
            ruta_audio = stream.download(output_path=ruta_descarga, filename="audio_temp")
            # Convertir el audio a WAV con la tasa de muestreo seleccionada
            nuevo_nombre = os.path.splitext(ruta_audio)[0] + ".wav"
            os.system(f"ffmpeg -i {ruta_audio} -ar {sample_rate} {nuevo_nombre}")
            os.remove(ruta_audio)  # Eliminar el archivo temporal MP4
        mostrar_mensaje("Descarga completada", "El audio se ha descargado exitosamente.")
    except Exception as e:
        mostrar_mensaje("Error", f"No se pudo descargar el audio: {e}")

def iniciar_descarga():
    formato = seleccion_combobox.get()
    sample_rate = seleccion_sample_rate_combobox.get()
    url = url_entry.get()
    if formato and url:
        if formato == "MP3" or formato == "WAV":
            descargar_audio(url, formato, sample_rate)
        elif formato == "MP4":
            descargar_video(url)
    else:
        mostrar_mensaje("Error", "Por favor, seleccione un formato de descarga y proporcione una URL válida.")

def mostrar_mensaje(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)

def abrir_enlace(url):
    import webbrowser
    webbrowser.open(url)

def cargar_imagen_desde_url(url):
    try:
        # Descargar la imagen desde la URL
        respuesta = requests.get(url)
        imagen = Image.open(BytesIO(respuesta.content))

        # Convertir la imagen a un objeto PhotoImage
        imagen_photo = ImageTk.PhotoImage(imagen)
        return imagen_photo
    except Exception as e:
        print(f"Error al cargar la imagen desde la URL: {e}")
        return None

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("YouTubeConvertPro")

# Establecer el ancho y alto de la ventana
ancho_ventana = 400
alto_ventana = 500
root.geometry(f"{ancho_ventana}x{alto_ventana}")

# Selector de formato de descarga
formato_label = ttk.Label(root, text="Seleccione el formato de descarga:")
formato_label.pack(pady=(20, 5))

formatos = ["MP3", "MP4", "WAV"]
seleccion_combobox = ttk.Combobox(root, values=formatos, width=20)
seleccion_combobox.pack(pady=(0, 10))
seleccion_combobox.current(0)

# Selector de tasa de muestreo para formato WAV
sample_rate_label = ttk.Label(root, text="Seleccione la tasa de muestreo:")
sample_rate_label.pack()

sample_rates = ["44100", "48000"]
seleccion_sample_rate_combobox = ttk.Combobox(root, values=sample_rates, width=10)
seleccion_sample_rate_combobox.pack(pady=(0, 20))
seleccion_sample_rate_combobox.current(0)

# Etiqueta y campo de entrada de la URL
url_label = ttk.Label(root, text="Ingrese la URL del video de YouTube:")
url_label.pack()

url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=(0, 20))

# Botón de descarga
descargar_button = ttk.Button(root, text="Descargar", command=iniciar_descarga)
descargar_button.pack()

# Separador
ttk.Separator(root, orient="horizontal").pack(fill="x", pady=20)

# Redes sociales
social_frame = ttk.Frame(root)
social_frame.pack()

facebook_button = ttk.Button(social_frame, text="WhatsApp", command=lambda: abrir_enlace("https://wa.me/+573173539733"))
facebook_button.grid(row=0, column=0, padx=5, pady=5)

twitter_button = ttk.Button(social_frame, text="YouTube", command=lambda: abrir_enlace("https://www.youtube.com/channel/UCU0RNCbxnXCJ9SlrqUz-8eg"))
twitter_button.grid(row=0, column=1, padx=5, pady=5)

# Enlace a la página web de YouTube
youtube_link = ttk.Label(root, text="¿No tienes un enlace? Encuentra videos en ", foreground="blue", cursor="hand2")
youtube_link.pack(pady=(20, 5))
youtube_link.bind("<Button-1>", lambda e: abrir_enlace("https://www.youtube.com/"))

# URL de la imagen del banner
url_banner = "https://scontent-bog2-2.xx.fbcdn.net/v/t39.30808-6/440805643_122102277404295078_4083621904160993855_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=5f2048&_nc_eui2=AeGxUSb8iLL62MeS1_E6FQXR3CfgWbKDcEDcJ-BZsoNwQHxcpA3kROtsCcVQDdlHNufd-2m5Io_mMJGmwq8gM7U_&_nc_ohc=v6XNeYriuegAb7nPigO&_nc_zt=23&_nc_ht=scontent-bog2-2.xx&oh=00_AfAzeZX9jLyfJjgPZIFxr7MymdJiEItqnmJRkwcYxAJPOg&oe=6635A0F7"

# Cargar la imagen del banner desde la URL
banner_image = cargar_imagen_desde_url(url_banner)
if banner_image:
    banner_label = ttk.Label(root, image=banner_image)
    banner_label.pack(pady=(20, 5))
else:
    print("No se pudo cargar la imagen del banner.")

root.mainloop()
