import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from operator import itemgetter 
from arbol import nodoArbol, insertarNodo, buscar, imprimirInOrden, imprimirPreOrden, eliminarNodo
import json

with open('Secuencias.json') as f:
            data = json.load(f)

def funcion_de_coincidencia(texto, nodo):
    return texto == nodo.info["nombre"]

class VentanaSecundaria(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Base de datos")
        self.set_default_size(400, 300)
        grid = Gtk.Grid()
        grid.set_row_spacing(6)
        grid.set_column_spacing(6)
        self.add(grid)

        self.entry_buscar = Gtk.Entry()
        self.entry_buscar.set_placeholder_text("Escribe la secuencia a buscar")
        self.entry_buscar.connect("activate", self.on_button_buscar_clicked) 
        grid.attach(self.entry_buscar, 0, 0, 1, 1)

        self.button_buscar = Gtk.Button(label="Buscar")
        self.button_buscar.connect("clicked", self.on_button_buscar_clicked)
        grid.attach_next_to(self.button_buscar, self.entry_buscar, Gtk.PositionType.RIGHT, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        grid.attach(scrolledwindow, 0, 1, 2, 1)

        self.textview_info = Gtk.TextView()
        self.textview_info.set_editable(False)
        self.textview_info.set_cursor_visible(False)
        self.textview_info.set_wrap_mode(Gtk.WrapMode.WORD)
        self.buffer_info = self.textview_info.get_buffer()

        with open('Secuencias.json') as f:
            data = json.load(f)
        
        data = sorted(data, key=itemgetter("nombre"))
        self.raiz = nodoArbol(data[0])
        
        for item in data[1:]:
            insertarNodo(self.raiz, item)
        
        texto_json = json.dumps(data, indent=4)
        self.buffer_info.set_text(texto_json)
        scrolledwindow.add(self.textview_info)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        grid.attach_next_to(vbox, scrolledwindow, Gtk.PositionType.RIGHT, 1, 1)

        label_nombre = Gtk.Label(label="Nombre")
        label_nombre.set_selectable(False)
        vbox.pack_start(label_nombre, True, True, 0)

        self.entry_nombre = Gtk.Entry()
        vbox.pack_start(self.entry_nombre, True, True, 0)

        label_secuencia = Gtk.Label(label="Secuencia")
        label_secuencia.set_selectable(False)
        vbox.pack_start(label_secuencia, True, True, 0)

        self.entry_secuencia = Gtk.Entry()
        vbox.pack_start(self.entry_secuencia, True, True, 0)

        label_info = Gtk.Label(label="Info")
        label_info.set_selectable(False)
        vbox.pack_start(label_info, True, True, 0)

        self.entry_info = Gtk.Entry()
        vbox.pack_start(self.entry_info, True, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.button_reemplazar = Gtk.Button()
        self.button_reemplazar.set_label("Remplazar")
        self.button_reemplazar.connect("clicked", self.on_button_reemplazar_clicked)
        hbox.pack_start(self.button_reemplazar, True, True, 0)

        self.button_eliminar = Gtk.Button()
        self.button_eliminar.set_label("Eliminar")
        self.button_eliminar.connect("clicked", self.on_button_eliminar_clicked)
        hbox.pack_start(self.button_eliminar, True, True, 0)

        self.button_agregar = Gtk.Button()
        self.button_agregar.set_label("Agregar")
        self.button_agregar.connect("clicked", self.on_button_agregar_clicked)
        hbox.pack_start(self.button_agregar, True, True, 0)
    

    def on_button_buscar_clicked(self, widget):
        
        texto = self.entry_buscar.get_text()
        resultado = buscar(self.raiz, texto, funcion_de_coincidencia) 
        print(resultado)

        if resultado is None:
            self.buffer_info.set_text("No se encontró el nombre " + texto)
        else:
            resultado_dict = resultado.serialize()
            texto_resultado = json.dumps(resultado_dict, indent=4)
            self.buffer_info.set_text(texto_resultado)
        imprimirInOrden(self.raiz)

    def on_button_reemplazar_clicked(self, widget):
        nombre = self.entry_nombre.get_text()
        secuencia = self.entry_secuencia.get_text()
        info = self.entry_info.get_text()
        indice = buscar(self.raiz, nombre, funcion_de_coincidencia) 
   
        if indice is not None:
            data[indice]["secuencia"] = secuencia
            data[indice]["informacion"] = info

            with open("Secuencias.json", "w") as f:
                json.dump(data, f, indent=4)
            self.buffer_info.set_text(f"Se reemplazó el dato {nombre} con éxito")
        else:
            self.buffer_info.set_text(f"No se encontró el dato {nombre}")

    def on_button_eliminar_clicked(self, widget):
    
        nombre = self.entry_nombre.get_text()
        self.raiz, x = eliminarNodo(self.raiz, nombre) 
        
        if x is not None:
            data = self.raiz.serialize()
            with open("Secuencias.json", "w") as f:
                json.dump(data, f, indent=4)
            self.buffer_info.set_text(f"Se eliminó el nodo {nombre} con éxito")
        else:
            self.buffer_info.set_text(f"No se encontró el nodo {nombre}")

    def on_button_agregar_clicked(self, widget):

        nombre = self.entry_nombre.get_text()
        secuencia = self.entry_secuencia.get_text()
        info = self.entry_info.get_text()
      
        dato = {"nombre": nombre, "secuencia": secuencia, "informacion": info}
        self.raiz = insertarNodo(self.raiz, dato)
        data = self.raiz.serialize()
      
        with open("Secuencias.json", "w") as f:
            json.dump(data, f, indent=4)
        self.buffer_info.set_text(f"Se agregó el nodo {nombre} con éxito")


#Posibles errores  :)
import generador
generador.datos
        
    