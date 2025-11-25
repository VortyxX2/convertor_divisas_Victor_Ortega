import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox

try:
    response = requests.get("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    root = ET.fromstring(response.content)
    ns = {'d': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

    nodo_tiempo = root.find('.//d:Cube[@time]', ns)
    fecha_actualizacion = nodo_tiempo.attrib['time']

    tasas = {'EUR': 1.0}
    for cubo in nodo_tiempo:
        tasas[cubo.attrib['currency']] = float(cubo.attrib['rate'])

except Exception:
    fecha_actualizacion = "Error de carga"
    tasas = {'EUR': 1.0, 'USD': 1.0}

def calcular():
    try:
        cant = float(entry_cant.get())
        tasa_origen = tasas[combo_de.get()]
        tasa_destino = tasas[combo_a.get()]
        res = (cant / tasa_origen) * tasa_destino
        lbl_res.config(text=f"{res:.2f} {combo_a.get()}")
    except ValueError:
        messagebox.showerror("Error", "Introduce solo números válidos.")

ventana = tk.Tk()
ventana.title("Conversor Divisas BCE")
ventana.geometry("300x250")

lbl_fecha = tk.Label(ventana, text=f"Datos actualizados al: {fecha_actualizacion}", fg="blue")
lbl_fecha.pack(pady=10) 

entry_cant = tk.Entry(ventana); entry_cant.pack(pady=5)

frame_monedas = tk.Frame(ventana); frame_monedas.pack()
combo_de = ttk.Combobox(frame_monedas, values=list(tasas.keys()), width=10); combo_de.set("EUR"); combo_de.pack(side="left")
tk.Label(frame_monedas, text=" a ").pack(side="left")
combo_a = ttk.Combobox(frame_monedas, values=list(tasas.keys()), width=10); combo_a.set("USD"); combo_a.pack(side="left")

tk.Button(ventana, text="Calcular", command=calcular).pack(pady=10)
lbl_res = tk.Label(ventana, text="---", font=("Arial", 14, "bold")); lbl_res.pack()

ventana.mainloop()