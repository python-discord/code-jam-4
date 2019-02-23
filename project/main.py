import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
kivy.require('1.10.1')


class AlphabeticHome(Widget):
    # def __init__(self, **kwargs):
    #     super(AlphabeticHome, self).__init__(**kwargs)
    #
    #     main_layout = GridLayout(rows=2)
    #     main_layout.add_widget(Label(text='text', id='editor'))
    #
    #     # keyboard
    #     grid_layout = GridLayout(cols=3)
    #     for c in list(map(chr, range(97, 123))):
    #         grid_layout.add_widget(
    #                 Button(
    #                     text=c
    #                     )
    #                 )
    #     main_layout.add_widget(grid_layout)
    #     self.add_widget(main_layout)
    pass


class AlphabeticApp(App):

    def build(self):
        return AlphabeticHome()


if __name__ == '__main__':
    AlphabeticApp().run()
