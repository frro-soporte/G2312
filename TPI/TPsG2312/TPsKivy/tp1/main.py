from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

import db

import sqlite3


pagina_detalle_id: int = -1


class PaginaInicio(Screen):
    caja_principal = ObjectProperty(None)
    caja_lista = ObjectProperty(None)
    filas: list[Widget] = []
    cols: Widget = None
    cols_bg_color = [1, 1, 1, 1]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fila_altura = 40
        self.col_boton_ancho = 60
        self.cols = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=self.fila_altura,
        )
        with self.cols.canvas:
            def set_pos(obj, valor):
                obj.pos = valor

            def set_size(obj, valor):
                obj.size = valor

            Color(.234, .456, .678, .8)
            # Setting the size and position of canvas
            rect = Rectangle(
                pos=self.cols.center,
                size=(
                    self.cols.width / 2.,
                    self.cols.height / 2.,
                )
            )
            # Update the canvas as the screen size change
            self.cols.bind(
                pos=lambda _, pos: set_pos(rect, pos),
                size=lambda _, size: set_size(rect, size)
            )
        self.cols.add_widget(Label(
            text="Nombre",
            size_hint_x=None,
        ))
        self.cols.add_widget(Label(
            text="Categoria",
            size_hint_x=None,
        ))
        self.cols.add_widget(Label(
            text="Stock",
            size_hint_x=None,
        ))
        self.cols.add_widget(Widget(
            size_hint_x=None,
            width=self.col_boton_ancho,
        ))

    def ajustar_ancho(self, caja_ancho=0):
        if caja_ancho > self.col_boton_ancho:
            for fila in self.filas:
                for col in fila.children:
                    if type(col) is Label:
                        col.width = (caja_ancho - self.col_boton_ancho) / 3

    def ver_productos(self, termino_busqueda):
        self.caja_principal.bind(width=lambda _, caja_ancho: self.ajustar_ancho(caja_ancho))
        if len(self.filas) > 0:
            self.caja_principal.remove_widget(self.filas.pop(0))
            for w in self.filas:
                self.caja_lista.remove_widget(w)
        self.filas = []
        resultado = db.buscar_producto_por_nombre(termino_busqueda)
        if len(resultado) == 0:
            label = Label(
                text="No hay productos.",
                size_hint_y=None,
                height=40,
            )
            self.caja_principal.add_widget(label)
            self.filas.append(label)
        else:
            self.caja_principal.add_widget(self.cols)
            self.filas.append(self.cols)
        for prod in resultado:
            fila = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=self.fila_altura,
            )
            boton_ver = Button(
                text="Ver",
                size_hint_x=None,
                width=self.col_boton_ancho,
                on_release=self.ver_detalle_prod(prod['id']),
            )
            color = [1, 1, 1]
            if type(prod['stock']) is int:
                if prod['stock'] <= 10:
                    color = [0.8, 0.1, 0.3]
                else:
                    color = [0.2, 0.8, 0.3]
            label_nombre = Label(
                text=f"{prod['nombre']}",
                size_hint_x=None,
                halign="center",
                valign="middle",
                max_lines=2,
            )
            label_nombre.bind(size=lambda s, w: s.setter('text_size')(s, w))
            label_categoria = Label(
                text=f"{str(prod['categoria']) if len(prod['categoria']) > 0 else ''}",
                size_hint_x=None,
                halign="center",
                valign="middle",
                max_lines=2,
            )
            label_categoria.bind(size=lambda s, w: s.setter('text_size')(s, w))
            label_stock = Label(
                text=f"{str(prod['stock']) if type(prod['stock']) is int else ''}",
                size_hint_x=None,
                # halign="center",
                max_lines=2,
                color=color,
            )
            fila.add_widget(label_nombre)
            fila.add_widget(label_categoria)
            fila.add_widget(label_stock)
            fila.add_widget(boton_ver)
            self.caja_lista.add_widget(fila)
            self.filas.append(fila)
        self.ajustar_ancho(self.caja_principal.width)

    def ver_detalle_prod(self, id_prod):
        def ir_a_detalle(*args):
            print("pagina detalle", id_prod)
            global pagina_detalle_id
            pagina_detalle_id = id_prod
            myapp.root.transition = SlideTransition(direction='left', duration=.25)
            myapp.root.current = 'detalle'
        return ir_a_detalle


class PaginaDetalle(Screen):
    nombre = ObjectProperty(None)
    descripcion = ObjectProperty(None)
    categoria = ObjectProperty(None)
    precio = ObjectProperty(None)
    stock = ObjectProperty(None)
    cambio_modificacion = ObjectProperty(None)
    boton_guardar = ObjectProperty(None)

    def ver_detalle(self):
        global pagina_detalle_id
        resultado = db.get_producto_por_id(pagina_detalle_id)
        if resultado is not None:
            self.nombre.text = resultado['nombre']
            self.descripcion.text = str(resultado['descripcion'])
            self.categoria.text = str(resultado['categoria'])
            self.precio.text = str(resultado['precio'])
            self.stock.text = str(resultado['stock'])
        self.nombre.disabled = True
        self.descripcion.disabled = True
        self.categoria.disabled = True
        self.precio.disabled = True
        self.stock.disabled = True
        self.boton_guardar.disabled = True
        self.cambio_modificacion.text = "Modificar"

    def activar_modificacion(self):
        self.nombre.disabled ^= 1
        self.descripcion.disabled ^= 1
        self.categoria.disabled ^= 1
        self.precio.disabled ^= 1
        self.stock.disabled ^= 1
        self.boton_guardar.disabled ^= 1
        self.cambio_modificacion.text = "Modificar" if self.nombre.disabled else "Desactivar modificación"

    def modificar_prod(self):
        if self.nombre.text != "" and self.precio.text != "":
            try:
                global pagina_detalle_id
                db.modificar_producto_por_id(
                    pagina_detalle_id,
                    self.nombre.text,
                    self.descripcion.text,
                    self.categoria.text,
                    self.precio.text,
                    self.stock.text,
                )
                self.activar_modificacion()
            except sqlite3.IntegrityError as e:
                if str(e) == "UNIQUE constraint failed: producto.nombre":
                    error = Label(
                        text=f"Ya existe el producto con nombre: '{self.nombre.text}'",
                        halign="center",
                        valign="middle",
                    )
                    error.bind(size=lambda s, w: s.setter('text_size')(s, w))
                    popup = Popup(
                        size_hint=(None, None),
                        title="Error",
                        content=error,
                        size=(self.width * 0.5, self.height * 0.2)
                    )
                    self.bind(size=lambda s, _: popup.setter('size')(popup, (s.width * 0.5, s.height * 0.2)))
                    popup.open()
        else:
            error = Label(
                text="Falta ingresar nombre y/o precio",
                halign="center",
                valign="middle",
            )
            error.bind(size=lambda s, w: s.setter('text_size')(s, w))
            popup = Popup(
                size_hint=(None, None),
                title="Error",
                content=error,
                size=(self.width * 0.5, self.height * 0.2)
            )
            self.bind(size=lambda s, _: popup.setter('size')(popup, (s.width * 0.5, s.height * 0.2)))
            popup.open()

    def borrar_prod(self):
        global pagina_detalle_id
        db.borrar_producto_por_id(pagina_detalle_id)


class PaginaAlta(Screen):
    nombre = ObjectProperty(None)
    descripcion = ObjectProperty(None)
    categoria = ObjectProperty(None)
    precio = ObjectProperty(None)
    stock = ObjectProperty(None)

    def alta(self):
        if self.nombre.text != "" and self.precio.text != "":
            try:
                db.crear_producto(
                    self.nombre.text,
                    self.descripcion.text,
                    self.categoria.text,
                    self.precio.text,
                    self.stock.text
                )
            except sqlite3.IntegrityError as e:
                if str(e) == "UNIQUE constraint failed: producto.nombre":
                    popup = Popup(size_hint=(None, None))
                    popup.title = "Error"
                    popup.size = (self.width * 0.5, self.height * 0.2)
                    popup.content = Label(text=f"Ya existe el producto con nombre: '{self.nombre.text}'")
                    popup.open()
        else:
            popup = Popup(size_hint=(None, None))
            popup.title = "Error"
            popup.size = (self.width*0.5, self.height*0.2)
            popup.content = Label(text="Falta ingresar nombre y/o precio")
            popup.open()

    def borrar_campos(self):
        self.nombre.text = ""
        self.descripcion.text = ""
        self.categoria.text = ""
        self.precio.text = ""
        self.stock.text = ""


class WindowManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        db.crear_tabla()


if __name__ == "__main__":
    myapp = MyApp()
    myapp.run()
