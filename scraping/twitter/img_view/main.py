from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

Builder.load_file('./tview.kv')

class MyWidget(Widget):
    pass


class TwitterViewApp(App):

    def build(self):
        my_widget = MyWidget()
        return my_widget

    def close_callback(self):
        print("this application to be close...")
        self.stop()

    def clear_picture(self):
        print('cleaning the pallet.')


if __name__ == '__main__':
    TwitterViewApp().run()