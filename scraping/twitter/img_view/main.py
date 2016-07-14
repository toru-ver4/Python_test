import os
import time
import fnmatch
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.image import Image
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from threading import Thread
from kivy.clock import mainthread
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('./tview.kv')

const_img_pattern = re.compile(".*\/media\/.*jpg")


class MyWidget(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_picture(self):
        img_dir = './img_cache'
        img_full_path_list = []
        for file_name in os.listdir(img_dir):
            if fnmatch.fnmatch(file_name, '*.jpg'):
                img_full_path_list.append(os.path.join(img_dir, file_name))

        for file_name in img_full_path_list:
            im = Image(source=file_name, size_hint_y=None, height=300)
            self.ids.illust_area.add_widget(im)

    def clear_picture(self):
        self.ids.illust_area.clear_widgets()

    def paste_twitter_illust(self):
        aaa = Thread(target=self.get_and_set_tiwtter_illust, name="aaa")
        aaa.start()

    def get_and_set_tiwtter_illust(self):
        twitter_id = self.ids.id_text_box.text
        url = "https://twitter.com/" + twitter_id + "/media"
        print(url)
        temp_dir = './img_cache'
        r = requests.get(url)
        driver = webdriver.PhantomJS()
        driver.get(url)

        # 以下は必要に応じてコールすること
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        for idx, img_tag in \
                enumerate(soup.findAll("img", {'src': const_img_pattern})):
            img_url = img_tag["src"]
            utc_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_file_name = 'temp_img_' + utc_time + str(idx) + "_.jpg"

            # いったん、Tempとして保存
            r = requests.get(img_url, stream=True)
            if r.status_code == 200:
                file_full_name = os.path.join(temp_dir, temp_file_name)
                with open(file_full_name, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                # 少々ダサいが、ファイルを再オープンして画像を表示
                # ----------------------------------------
                print(file_full_name)
                self.update(file_full_name)
                time.sleep(1)
        driver.close()

    @mainthread
    def update(self, file_full_name):
        im = Image(source=file_full_name, size_hint_y=None, height=300)
        self.ids.illust_area.add_widget(im)


class ImgViewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TwitterViewApp(App):

    def build(self):
        sm = ScreenManager()
        main_screen = MyWidget(name="main")
        img_view_screen = ImgViewScreen(name="img_view")
        sm.add_widget(main_screen)
        sm.add_widget(img_view_screen)
        return sm

    def close_callback(self):
        print("this application to be close...")
        self.stop()


if __name__ == '__main__':
    TwitterViewApp().run()

