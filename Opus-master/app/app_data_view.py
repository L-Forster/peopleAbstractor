from kivy.clock import Clock
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
import os
from gdrive_phone_facade import *
import init_db
from kivy.metrics import dp


# VIEWING ALL THE DATA FROM SOMEONE. THEIR PERSONAL PROFILE:
 # Stuff stored in person
 # Their sentences.


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.garden.graph import BarPlot, MeshLinePlot, Graph
from kivymd.uix.scrollview import MDScrollView
KV = '''
MDScreen:

    BoxLayout:
        padding: 50
        MDTextField:
            id: username
            hint_text: "Select Username"
            on_focus: if self.focus: app.show_menu(self)
            pos_hint: {"right_x": 0.9, "center_y": .95}
            size_hint_x: 0.4
    
    
        MDFlatButton:
            text: "Submit"
            on_release: app.on_show_person()
            pos_hint: {"center_x": .1, "center_y": .95}
    
        FloatLayout:
    
            CustomBarChart:  # Use the CustomBarChart widget
                id: bar_chart
                size_hint: (1.5,0.4)
    
        
        ScrollView:
            do_scroll_x: False
            size_hint_y: 0.3
            height: 300
            width: 500
            pos_hint: {"right_x": -.9, "center_y": .6}
            
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                spacing: dp(50)

                height: self.minimum_height  # Adjust height dynamically based on content
                MDLabel:
                    id: Birthplace
                    text: ""
                    halign: 'left'
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines 
                MDLabel:
                    id: Date of birth
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -.35}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines     
                MDLabel:
                    id: Job
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -.55}
                    height: self.texture_size[1]  # Adjust height based on content
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines      
                MDLabel:
                    id: Nationality
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -1.15}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines 
                MDLabel:
                    id: Sex
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -1.15}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines     
                MDLabel:
                    id: Age
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -1.15}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines     
                MDLabel:
                    id: Profiles
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -1.15}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines  
                                                                                            
        ScrollView:
            do_scroll_x: False
            size_hint_y: 0.3
            height: 300
            width: 500
            pos_hint: {"left_x": -.9, "center_y": .6}           
                      
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                spacing: dp(50)
                height: self.minimum_height  # Adjust height dynamically based on content
                MDLabel:
                    id: Social event    
                    text: ""
                    halign: 'left'
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines
                MDLabel:
                    id: Hobby
                    text: ""
                    halign: 'left'
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines
                MDLabel:
                    id: Political opinion
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": .45}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Personality trait
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": .25}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Wealth
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": .05}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Education
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -.15}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Home
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -.95}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
       
                MDLabel:
                    id: Language
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -1.35}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Family
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -1.55}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: History
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -1.75}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Influencing others
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -1.95}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Philosophy
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -2.15}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Societies
                    text: ""
                    halign: 'left'
                    # pos_hint: {"left_x": .9, "center_y": -2.35}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Technical skill
                    text: ""
                    halign: 'left'
                    # pos_hint: {"left_x": .9, "center_y": -2.55}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Trauma
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -2.75}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Award
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -2.95}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Strength
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -3.15}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Vulnerability
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -3.35}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Fear
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -3.55}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines        
                MDLabel:
                    id: Love
                    text: ""
                    halign: 'left'
                    pos_hint: {"left_x": .9, "center_y": -3.75}
                    height: self.texture_size[1]  # Adjust height based on content
                    text_size: self.width, None  # Enable multiple lines            

'''


class CustomBarChart(FloatLayout):
    def __init__(self, labels=[], values=[], **kwargs):
        super(CustomBarChart, self).__init__(**kwargs)
        self.labels = labels
        self.values = values
        self.create_chart()

    def create_chart(self):
        graph = Graph(xlabel='Attribute', ylabel='Score', x_ticks_minor=5, x_ticks_major=25, y_ticks_major=10,
                      y_grid_label=True,
                      x_grid_label=True, padding=5, x_grid=True, y_grid=True, ymax=11)

        num_bars = len(self.labels)
        if num_bars > 0:
            bar_spacing = 5
            bar_width = 5
            x_pos = bar_spacing
            z = -4
            for label, value in zip(self.labels, self.values):
                if value > 8:
                    plot = MeshLinePlot(color=(255, 0, 0, 1))

                else:
                    plot = MeshLinePlot(color=(0, 128, 128, 1))
                plot.points = [(x_pos, 0), (x_pos, value), (x_pos + bar_width, value), (x_pos + bar_width, 0)]
                x_pos += bar_width + bar_spacing
                graph.add_plot(plot)
                label_text = Label(text=label, pos=(100 * z * 1.5 , ((z+4) % 2)*20 + 190),
                                   size=(bar_width, 30), halign='left')
                self.add_widget(label_text)
                # graph.x_grid_label =
                z += 1
            self.add_widget(graph)


class DataViewer(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        self.chart_container = BoxLayout(orientation="vertical")
        self.db = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.screen.ids.username.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        return self.screen

    def show_menu(self, instance_textfield):
        self.db = init_db.Database()
        names = self.db.get_all_names()
        # Creating a dropdown menu
        menu_items = [{"text": name, "viewclass": "OneLineListItem", "on_release": lambda x=name: self.set_item(x)} for name in names]
        self.menu = MDDropdownMenu(
            caller=instance_textfield,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def set_item(self, text_item):
        # Set the selected username to the text field
        self.root.ids.username.text = text_item
        self.menu.dismiss()

    def set_error_message(self, err):
        print("Err", err)

    def on_show_attributes(self, person_id):
        scores = self.db.get_person_attributes(person_id)

        for i in range(len(scores)):
            if scores[i]['value'] is None:
                scores[i]['value'] = 0.0
        print(scores)
        self.root.ids.bar_chart.clear_widgets()
        l = [item['attribute'] for item in scores]
        v = [item['value'] for item in scores]
        custom_bar_chart = CustomBarChart(labels=l, values=v)
        self.root.ids.bar_chart.add_widget(custom_bar_chart)

    def on_show_summary(self, person_id):
        db = init_db.Database()
        summary = db.get_person_column(person_id=1, column="summary")
        print(summary)
        db.close_connections()

    def on_show_categories(self, person_id):
        db = init_db.Database()
        categories = db.get_person_categories(person_id)
        print(categories)

        for category in categories:
            print(category['category'])
            output = category['category'] + ": " + str(category['data'])

            print(output)

            temp_id = category['category']
            label = self.root.ids[temp_id]
            label.text = output

    def on_show_person(self):
        self.db = init_db.Database()
        print(self.root.ids.username.text)
        name = self.root.ids.username.text
        if len(name) == 0:
            return -1
        person_id = self.db.get_person_id(name)[0]
        ###
        self.on_show_summary(person_id)
        self.on_show_categories(person_id)
        self.on_show_attributes(person_id)

        self.db.close_connections()


DataViewer().run()


# def display_recent_sentences(self):
#     sentence_ids = self.db.get_recent_sentences_id()
#     sentences = []
#     for sentence_id in sentence_ids:
#         sentences.append(self.db.get_sentence(sentence_id))
#     print(sentences)


