import kivy
from kivy.app import App
from kivy.uix.widget import Widget
kivy.require('1.10.1')


class AlphabeticHome(Widget):
    pass


class AlphabeticApp(App):

    def build(self):
        return AlphabeticHome()


if __name__ == '__main__':
    AlphabeticApp().run()
