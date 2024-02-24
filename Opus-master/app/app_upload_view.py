from kivy.clock import Clock
from kivy.config import Config
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
import os
from gdrive_phone_facade import *
import init_db
from kivy.metrics import dp

KV = '''
<IconListItem>

    IconLeftWidget:
        icon: root.icon


MDScreen:

        
    MDTextField:
        id: person_name
        hint_text: "New"
        helper_text_mode: "on_error"
        helper_text: "Input is required"
        size_hint_x: None
        pos_hint: {"center_x":.5, "center_y": .9}
        on_text_validate: app.on_enter_name()
        mode: "rectangle"
        width: "200dp"
    
        
    MDTextField:
        id: raw_data
        hint_text: "Enter sentence"
        helper_text_mode: "on_error"
        helper_text: "Input is required"
        size_hint_x: .7
        size_hint_y: .5
        pos_hint: {"center_x":.5, "center_y": .5}
        on_text_validate: app.on_enter_raw()
        multiline: True
        mode: "rectangle"

    MDTextField:
        id: name
        pos_hint: {'center_x': .5, 'center_y': .8}
        size_hint_x: None
        width: "200dp"
        hint_text: "Name"
        on_focus: if self.focus: app.menu.open()
        mode: "rectangle"


    # MDTextField:
    #     id: tags
    #     hint_text: "Enter tags"
    #     size_hint_x: .9
    #     pos_hint: {"center_x":.5, "center_y": .4}
    #     on_text_validate: app.on_enter_tag()
    # 
    # MDTextField:
    #     id: attribute
    #     hint_text: "Enter attributes"
    #     size_hint_x: .9
    #     pos_hint: {"center_x":.5, "center_y": .3}
    #     on_text_validate: app.on_enter_attribute()
    #     
    # MDSwitch:
    #     id: switch_tag
    #     pos_hint: {'center_x': 0.10, 'center_y': .8}
    #     on_active: app.switch_activate("tag")
    # MDLabel:
    #     id: tag_text
    #     text: "- Tags"
    #     pos_hint: {'center_x': .675, 'center_y': .8}
    #     
    # MDSwitch:
    #     id: switch_attribute
    #     pos_hint: {'center_x': 0.10, 'center_y': .75}
    #     on_active: app.switch_activate("attribute")
    # MDLabel:
    #     id: attribute_text
    #     text: "- Attributes"
    #     pos_hint: {'center_x': .675, 'center_y': .75}
    # 

    MDFillRoundFlatButton:
        id: upload
        text: "Upload data"
        # md_bg_color: "red"
        pos_hint: {'center_x': .25  , 'center_y': .05}
        size_hint_x: 0.4
        on_press: app.on_upload()


    MDFillRoundFlatButton:
        id : commit
        text: "Commit data"
        # md_bg_color: "red"
        pos_hint: {'center_x': .75  , 'center_y': .05}
        size_hint_x: 0.4
        on_press: app.on_enter_raw()
'''

class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class AppUploadScreen(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
        self.screen = Builder.load_string(KV)
        self.create_dropdown()
        phone_all()

    def create_dropdown(self):
        self.db = init_db.Database()
        people_names = self.db.get_all_names()
        print(people_names)
        people_names = [item for sublist in people_names for item in sublist]

        people_names.sort()
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": people_names[i],
                "height": dp(56),
                "on_release": lambda x=people_names[i]: self.set_item(x),
            } for i in range(len(people_names))
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.name,
            items=menu_items,
            position="bottom",
            width_mult=2,
        )
        # self.menu.bind()

    def set_item(self, text__item):
        self.screen.ids.name.text = text__item
        self.menu.dismiss()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        sm = ScreenManager()
        return self.screen

    def set_error_message(self, instance_textfield):
        if instance_textfield.text == "":
            self.screen.ids.username.error = True

    def on_stop(self):
        self.db.close_connections()
        # gdrive.main_pc()

    def upload_file_to_drive(self, file_path):
        file_name = os.path.basename(file_path)
        f = self.drive.CreateFile({'title': file_name})
        f.SetContentFile(file_path)
        f.Upload()

    def switch_activate(self, data_type):

        if self.screen.ids.switch_attribute.active and data_type == "attribute":
            self.screen.ids.switch_tag.active = False

        elif self.screen.ids.switch_tag.active and data_type == "tag":
            self.screen.ids.switch_attribute.active = False

        else:
            return ValueError()

    # Add name to db
    def on_enter_name(self):
        self.db.add_person_without_data(name=self.screen.ids.person_name.text)
        self.create_dropdown()

    def on_enter_raw(self):
        data = self.screen.ids.raw_data.text
        print(self.screen.ids.name.text)
        if len(self.screen.ids.name.text) > 0:
            person_id = self.db.get_person_id(self.screen.ids.name.text)[0]
            self.db.add_sentence(data, person_id)
            self.screen.ids.commit.text = "Commit Successful!"
            Clock.schedule_once(lambda dt: setattr(self.screen.ids.commit, 'text', "Commit data"), 5)

        else:
            self.screen.ids.commit.text = "Error!"
            Clock.schedule_once(lambda dt: setattr(self.screen.ids.commit, 'text', "Commit data"), 5)



    def on_enter_attribute(self):
        # att = self.screen.ids.attribute.text
        # if len(att) > 0:
        #     self.db.add_attribute(att)
        pass
    def on_enter_tag(self):
        # tag = self.screen.ids.tags.text
        # if len(tag) > 0:
        #     self.db.add_tag(tag)
        pass

    #manually parse the data
    def on_submit(self):
        pass

    #uploading the database to GDrive

    def on_upload(self):
        self.screen.ids.upload.text = "Uploading...!"

        # Commit sentence data to db
        sentence = self.screen.ids.raw_data.text
        person_id = self.db.get_person_id(name=self.screen.ids.name.text)
        if len(person_id) > 0:
            person_id = person_id[0]
            self.db.add_sentence(sentence, person_id)

            self.db.close_connections()

            upload()
            self.screen.ids.upload.text = "Upload successful!"
            # Upload db to cloud
            Clock.schedule_once(lambda dt: setattr(self.screen.ids.upload, 'text', "Upload data"), 5)
        else:
            self.screen.ids.upload.text = "Upload failed"

        self.db = init_db.Database()


AppUploadScreen().run()





