from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder



Builder.load_file('editor.kv')

class MyLayout(Widget):
    def selected(self, filename):
        try:
            self.ids.my_image.source = filename[0]
            print(filename[0])
        except:
            pass

class FileChooserApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    FileChooserApp().run()