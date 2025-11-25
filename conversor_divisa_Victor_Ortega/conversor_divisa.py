import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox

# --- 1. Carga y Parsing ---
try:
    response = requests.get("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    root = ET.fromstring(response.content)
    ns = {'d': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

    # REQUISITO CUMPLIDO: Extraer la fecha del XML 
    nodo_tiempo = root.find('.//d:Cube[@time]', ns)
    fecha_actualizacion = nodo_tiempo.attrib['time']

    # Extraer tasas (Añadimos Euro manual)
    tasas = {'EUR': 1.0}
    for cubo in nodo_tiempo:
        tasas[cubo.attrib['currency']] = float(cubo.attrib['rate'])

except Exception:
    # Si falla la carga (ej. sin internet), ponemos valores por defecto para que abra
    fecha_actualizacion = "Error de carga"
    tasas = {'EUR': 1.0, 'USD': 1.0}

# --- 2. Funciones ---
def calcular():
    try:
        cant = float(entry_cant.get())
        # Conversión cruzada [cite: 68]
        tasa_origen = tasas[combo_de.get()]
        tasa_destino = tasas[combo_a.get()]
        res = (cant / tasa_origen) * tasa_destino
        lbl_res.config(text=f"{res:.2f} {combo_a.get()}")
    except ValueError:
        # Validación de error si meten letras [cite: 73]
        messagebox.showerror("Error", "Introduce solo números válidos.")

# --- 3. Interfaz Gráfica (GUI) ---
ventana = tk.Tk()
ventana.title("Conversor Divisas BCE")
ventana.geometry("300x250")

# REQUISITO CUMPLIDO: Mostrar fecha visiblemente 
lbl_fecha = tk.Label(ventana, text=f"Datos actualizados al: {fecha_actualizacion}", fg="blue")
lbl_fecha.pack(pady=10) # pady da espacio para que se vea bien

# Entradas
entry_cant = tk.Entry(ventana); entry_cant.pack(pady=5)

# Selectores
frame_monedas = tk.Frame(ventana); frame_monedas.pack()
combo_de = ttk.Combobox(frame_monedas, values=list(tasas.keys()), width=10); combo_de.set("EUR"); combo_de.pack(side="left")
tk.Label(frame_monedas, text=" a ").pack(side="left")
combo_a = ttk.Combobox(frame_monedas, values=list(tasas.keys()), width=10); combo_a.set("USD"); combo_a.pack(side="left")

# Botón y Resultado
tk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)
lbl_res = tk.Label(ventana, text="---", font=("Arial", 14, "bold")); lbl_res.pack()

ventana.mainloop()