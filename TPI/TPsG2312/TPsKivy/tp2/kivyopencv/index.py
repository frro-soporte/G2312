from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.filechooser import FileChooserListView

from HandDetectionScreen import CameraScreen
from LoginScreen import LoginScreen2

class IndexScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Menú"
        layout = BoxLayout(orientation='vertical')
        
        label = Label(text="Menú")
        layout.add_widget(label)

        buttonsLayout = BoxLayout(orientation='horizontal', spacing=10, padding = [20, 20, 20, 20])

        files_button = Button(text="Archivos", size=(150, 50))
        files_button.bind(on_press=self.go_to_files)
        buttonsLayout.add_widget(files_button)

        camera_button = Button(text="Cámara", size=(150, 50))
        camera_button.bind(on_press=self.go_to_camera)
        buttonsLayout.add_widget(camera_button)

        layout.add_widget(buttonsLayout)

        self.add_widget(layout)
        
    
    def go_to_camera(self, instance):
        if "camera" not in self.manager.screen_names:
            self.manager.add_widget(CameraScreen(name="camera"))
        self.manager.current = "camera"

    def go_to_files(self, instance):
        self.manager.current = "files"

    def on_pre_enter(self):
        App.get_running_app().title = self.title


class FileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Archivos"
        layout = BoxLayout(orientation='vertical')

        self.file_chooser = FileChooserListView(path='C:\\Users\\carad\\Documents\\TP-soporte-kivy-G2312\\tp2\\kivyopencv\\archivos\\', filters=['*.jpg', '*.png', '*.mp4'])
        layout.add_widget(self.file_chooser)

        self.media_widget = BoxLayout(orientation='vertical')
        layout.add_widget(self.media_widget)

        files_button = Button(text="Atrás", size_hint=(None, None), size = (100, 50))
        files_button.bind(on_press=self.go_to_index)
        layout.add_widget(files_button)

        self.add_widget(layout)

        self.file_chooser.bind(selection=self.load_media)


    def load_media(self, instance, value):
        self.media_widget.clear_widgets()

        selected = value
        if selected:
            selected_file = selected[0]

            if selected_file.lower().endswith(('.jpg', '.png')):
                image_widget = Image(source=selected_file)
                self.media_widget.add_widget(image_widget)
            elif selected_file.lower().endswith('.mp4'):
                video_player = VideoPlayer(source=selected_file, state='play')
                self.media_widget.add_widget(video_player)

    def go_to_index(self, instance):
        self.manager.current = "index"

    def on_pre_enter(self):
        App.get_running_app().title = self.title


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen2(name="login"))
        sm.add_widget(IndexScreen(name="index"))
        sm.add_widget(FileScreen(name="files"))
        return sm


if __name__ == '__main__':
    MyApp().run()
