import kivy
from kivy.app import App
from kivy.uix.label import Label
kivy.require('1.10.1')  # replace with your current kivy version !


class MyApp(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    MyApp().run()
