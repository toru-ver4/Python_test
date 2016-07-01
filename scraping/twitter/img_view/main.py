import os
import fnmatch
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.image import Image

Builder.load_file('./tview.kv')


class MyWidget(Widget):
    def add_picture(self):
        img_dir = './img_cache'
        img_full_path_list = []
        for file_name in os.listdir(img_dir):
            if fnmatch.fnmatch(file_name, '*.jpg'):
                img_full_path_list.append(os.path.join(img_dir, file_name))

        for file_name in img_full_path_list:
            im = Image(source=file_name, size_hint=(1, None))
            self.ids.illust_area.add_widget(im)

    def clear_picture(self):
        self.ids.illust_area.clear_widgets()


class TwitterViewApp(App):

    def build(self):
        my_widget = MyWidget()
        return my_widget

    def close_callback(self):
        print("this application to be close...")
        self.stop()


if __name__ == '__main__':
    TwitterViewApp().run()
