import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Pango
from ventana_secundaria import VentanaSecundaria
from Bio import Align
import json

import generador

generador.datos
with open('Secuencias.json') as f:
    data = json.load(f)


class MainWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Ventana principal")
        self.set_border_width(10)
        self.set_default_size(600, 300)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(hbox)

        vbox_text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hbox.pack_start(vbox_text, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text("Escribe algo aquí")
        vbox_text.pack_start(self.entry, True, True, 0)

        self.label_bottom = Gtk.Label(label="Esta etiqueta no permite escritura")
        self.label_bottom.set_selectable(False)
        vbox_text.pack_start(self.label_bottom, True, True, 0)

        vbox_menu = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hbox.pack_start(vbox_menu, False, False, 0)

        self.button_manual = Gtk.Button(label="Manual")
        self.button_manual.connect("clicked", self.on_button_manual_clicked)
        vbox_menu.pack_start(self.button_manual, True, True, 0)

        self.button_database = Gtk.Button(label="Base de datos")
        self.button_database.connect("clicked", self.on_button_database_clicked)
        vbox_menu.pack_start(self.button_database, True, True, 0)

        self.button_execute = Gtk.Button(label="Ejecutar")
        self.button_execute.connect("clicked", self.on_button_execute_clicked)
        vbox_menu.pack_start(self.button_execute, True, True, 0)

    # Funcion boton manual
    def on_button_manual_clicked(self, widget):
        manual_window = Gtk.Window(title="Manual")
        manual_window.set_default_size(770, 400)  
        manual_label = Gtk.Label()
        manual_label.modify_font(Pango.FontDescription('Arial 12'))  
        manual_scroll = Gtk.ScrolledWindow()
        manual_scroll.add(manual_label)
        manual_window.add(manual_scroll)

        with open("manual.json") as f: 
            data = json.load(f) 
            manual_text = data["Manual"] 
            manual_text_str = "Manual\n\n"
            for key, value in manual_text.items():
                if isinstance(value, list):
                    manual_text_str += key + ":\n" + "\n".join(value) + "\n\n"
                else:
                    manual_text_str += key + ": " + value + "\n\n"

            manual_label.set_text(manual_text_str)
        
        manual_window.show_all()

    # Funcion botón base de datos
    def on_button_database_clicked(self, widget):
        ventana_secundaria = VentanaSecundaria()
        ventana_secundaria.show_all()

    # Funcion boton ejecutar
    def on_button_execute_clicked(self, widget):
        text = self.entry.get_text()
        text = text.upper()
        self.label_bottom.set_text(text)

        aligner = Align.PairwiseAligner()
        aligner.match_score = 2
        aligner.mismatch_score = -1
        aligner.open_gap_score = -2
        aligner.extend_gap_score = -1

        resultados = []

        for item in data:
            nombre = item["nombre"]
            secuencia = item["secuencia"]
            alignment = aligner.align(text, secuencia)
            puntaje = alignment[0].score
            numero = text.count(secuencia)
            #print(numero)
        
            if numero == 0: 
                mutacion = "No"
            else: 
                mutacion = "Si"
        
            resultados.append((nombre, puntaje, mutacion))

        resultados.sort(key=lambda x: x[1], reverse=True)
        resultados_mutados = [resultado for resultado in resultados if resultado[2] == "Si"]

        if resultados_mutados:
            texto_label = ""
            for resultado in resultados_mutados:
                nombre = resultado[0]
                puntaje = resultado[1]
                mutacion = resultado[2]

                texto_label += f"{nombre}: Puntaje maximo en el alinamiento = {puntaje}, Mutacion = {mutacion}\n"
                secuencia = [item["secuencia"] for item in data if item["nombre"] == nombre][0]
                alignment = aligner.align(text, secuencia)
                texto_label += f"{alignment[0]}\n"
        else:
        
            texto_label = "No se encontró esa secuencia en la base de datos"

        self.label_bottom.set_text(texto_label)


#   Ejecucion
window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()