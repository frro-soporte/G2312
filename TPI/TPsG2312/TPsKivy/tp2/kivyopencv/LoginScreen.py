import cv2

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import datetime

from Validar_identidad.validar_identidad import validar_identidad 

class LoginScreen2(Screen):
    log_in = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Inicio"
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Ingresar", size_hint_y=None, height=30)
        layout.add_widget(self.label)

        self.capture = cv2.VideoCapture(0)
        self.image = Image()
        layout.add_widget(self.image)

        buttonsLayout = BoxLayout(orientation='horizontal', spacing=10, size_hint= (None, None), height=50, padding = 10, pos_hint = {'center_x': 0.40})
         
        login_button = Button(text="Ingresar", size_hint=(None, None), size=(150, 50))
        login_button.bind(on_press=self.capture_validate_image)
        buttonsLayout.add_widget(login_button)
# 
        login_button = Button(text="Crear Usuario", size_hint=(None, None), size=(150, 50))
        login_button.bind(on_press=self.create_user)
        buttonsLayout.add_widget(login_button)

        layout.add_widget(buttonsLayout)

        Clock.schedule_interval(self.update, 1.0 / 30.0)

        self.add_widget(layout)


    def update(self, dt):

        ret, frame = self.capture.read()

        if ret:
            frame = cv2.flip(frame, 1)
            buf = cv2.flip(frame, 0).tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture1

        if self.log_in:
            self.on_stop()
            self.go_to_index()

    

    def capture_validate_image(self, instance):

        self.label.text = "Buscando"

        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite("captured_image.jpg", frame)

        try:
            self.log_in = validar_identidad()
            if not self.log_in:
                self.label.text = f"Usuario no encontrado."

        except Exception as e:
            print(e)

    
    def create_user(self, instance):

        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite(f"usuarios/{date_time_str}.jpg", frame)
            self.label.text = f"Usuario creado."


    def go_to_index(self):
        self.manager.current = "index"


    def on_pre_enter(self):
        App.get_running_app().title = self.title


    def on_stop(self):
        self.capture.release()
        Clock.unschedule(self.update)

