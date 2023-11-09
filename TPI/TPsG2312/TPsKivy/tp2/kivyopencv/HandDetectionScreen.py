from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

import mediapipe as mp
import time
from threading import Thread
import datetime

from google.protobuf.json_format import MessageToDict

from kivy.uix.screenmanager import Screen


class CameraScreen(Screen):
    left_counter = 0
    right_counter = 0
    is_recording = False
    photo_taken = False


    video_writer = None 
    frame_width = int(cv2.VideoCapture(0).get(3))
    frame_height = int(cv2.VideoCapture(0).get(4))


    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Cámara"


        layout = BoxLayout(orientation='vertical')
        self.capture = cv2.VideoCapture(0)
        self.image = Image()

        layout.add_widget(self.image)

        self.label = Label(text="", size_hint_y=None, height=50)
        layout.add_widget(self.label)

        files_button = Button(text="Atrás", size_hint=(None, None), size = (100, 50))
        files_button.bind(on_press=self.go_to_index)
        layout.add_widget(files_button)


        timer_thread = Thread(target=self.timer_function)
        timer_thread.daemon = True
        timer_thread.start()


        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS

        self.add_widget(layout)
    


    def timer_function(self):
        while True:
            time.sleep(1)
            self.right_counter += 1
            self.left_counter += 1
            if self.left_counter == 6:
                self.left_counter = 0
                self.photo_taken = False


    def update(self, dt):

        ret, frame = self.capture.read()

        if ret:


            frame = cv2.flip(frame, 1)
            img = self.capture
            img2 = cv2.flip(frame, 0).tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(img2, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture1


            success, img = img.read()
            img = cv2.flip(img, 1)


            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)


            if results.multi_hand_landmarks:

                now = datetime.datetime.now()
                date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

                if len(results.multi_handedness) == 2:
                    self.label.text = f"Las dos manos levantadas"
                    self.right_counter = 0
                    self.left_counter = 0
                    if self.is_recording:
                        self.video_writer.release()
                        self.is_recording = False

                else:
                    for i in results.multi_handedness:
                        

                        etiqueta = MessageToDict(i)['classification'][0]['label']

                        if etiqueta == 'Left':

                            if self.left_counter == 5 and not self.photo_taken:
                                self.label.text = f"Foto tomada"
                                cv2.imwrite(f"archivos/imagen{date_time_str}.jpg", img)
                                self.photo_taken = True
                            else:
                                self.label.text = f"{5 - self.left_counter} segundos para sacar foto"
                            
                        if etiqueta == 'Right':

                            if self.right_counter >= 5:
                                self.label.text = f"grabando por {self.right_counter - 5} segundos."
                                if not self.is_recording:
                                    self.video_writer = cv2.VideoWriter(f"archivos/video{date_time_str}.mp4", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (self.frame_width, self.frame_height))
                                    self.is_recording = True
                            else:
                                self.label.text = f"{5 - self.right_counter} segundos para grabar"
            
            else:
                self.label.text = f""
                self.right_counter = 0
                self.left_counter = 0

            if self.is_recording:
                self.video_writer.write(img)


    def on_pre_enter(self):
        App.get_running_app().title = self.title

    def go_to_index(self, instance):
        self.manager.current = "index"

    def on_stop(self):
        self.capture.release()
        Clock.unschedule(self.update)

