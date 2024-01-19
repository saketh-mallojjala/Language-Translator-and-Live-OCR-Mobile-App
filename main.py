import googletrans
import kivy.resources
from googletrans import Translator
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from gtts import gTTS
import os
import arabic_reshaper
import bidi.algorithm
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, FadeTransition, WipeTransition
import speech_recognition as sr
import pyttsx3
import time
from kivy.lang import Builder
import cv2
from PIL import Image
from pytesseract import pytesseract
import numpy as np
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
import plyer
import time
import requests
import json
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

firebase_url = "https://kivybackend-default-rtdb.firebaseio.com/.json"

# Window.size = (320, 600)

translator = Translator()
dic1 = googletrans.LANGUAGES
dic2 = googletrans.LANGCODES
dic3 = {

    "telugu": "tel",
    "english": "eng",
    "hindi": "hin",
    "malayalam": "mal",
    "tamil": "tam",
    "nepali": "nep",
    "kannada": "kan",

}

l1 = ["zulu", "yoruba", "xhosa", "welsh", "vietnamese", "uzbek", "ukrainian", "turkish", "tajik", "swedish",
      "sundanese", "spanish", "somali", "slovenian", "slovak", "shona", "serbian", "scots gaelic", "russian",
      "romanian",
      "portuguese", "polish", "norwegian", "mongolian", "maori", "maltese", "malay", "macedonian", "luxembourgish",
      "lithuanian", "latvian", "kyrgyz", "kazakh", "javanese", "italian",
      "irish", "indonesian", "igbo", "icelandic", "hungarian", "hmong", "hawaiian", "hausa", "haitian creole", "greek",
      "german", "galician", "frisian", "french", "finnish", "filipino", "estonian", "esperanto", "english", "dutch",
      "danish", "czech", "croatian", "corsican", "cebuano", "catalan", "bulgarian", "basque", "azerbaijani", "albanian",
      "afrikaans"

      ]

l2 = [

    "uyghur", "urdu", "sindhi", "persian", "pashto", "arabic"

]

l3 = [
    "nepali", "marathi", "hindi"

]

l4 = [
    "yiddish", "hebrew"
]

f1 = {

    "NotoSansEthiopic": "amharic",
    "NotoSansArmenian": "armenian",
    "NotoSansBengali": "bengali",
    "NotoSansMalayalam": "malayalam",
    "NotoSansTelugu": "telugu",
    "NotoSansTamil": "tamil",

    "NotoSansGeorgian": "georgian",
    "NotoSansGujarati": "gujarati",

    "NotoSansKannada": "kannada",

    "NotoSansMyanmar": "myanmar",
    "NotoSansOriya": "odia",
    "NotoSansGurmukhi": "punjabi",
    "NotoSansThai": "thai",

}

f2 = {
    "NotoSansDisplay": l1,
    "NotoSansArabic": l2,
    "NotoSansDevanagari": l3,
    "NotoSansHebrew": l4,
}
f3 = {
    "NotoSansSC": "chinese (simplified)",
    "NotoSansTC": "chinese (traditional)",
    "NotoSansKR": "korean",
    "NotoSansJP": "japanese",

}


# camera.set(3, 1920)
# camera.set(4, 1080)
# camera.set(3, 1280)
# camera.set(4, 720)

class P:
    pass


class CustomTextInput(TextInput):
    pass


class WindowManager(ScreenManager, GridLayout, BoxLayout, Camera):
    l1 = ""
    l2 = ""
    l3 = ""
    l4 = ""
    l5 = ""
    i = 0
    pic = ""
    detect = ""
    firebase_font = ""
    firebase_inputtext = ""
    firebase_inputlang = ""
    firebase_destlang = ""
    firebase_desttext = ""
    input_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key in dic1:
            self.ids.spinner_id.values.append(dic1[key])
        for key in dic1:
            self.ids.spinner_id1.values.append(dic1[key])
        for k in dic3:
            self.ids.datatrain.values.append(k)

    def clicked1(self, value, root):
        print(f"dest language is {value}")
        try:
            self.l2 = dic2[value]
            self.ids.tolang.text = self.l2
            for key in f1:
                if f1[key] == value:
                    print(key)
                    self.ids.totext.font_name = f"fonts\{key}-Regular.ttf"
            for key in f2:
                if value in f2[key]:
                    print(key)
                    self.ids.totext.font_name = f"fonts\{key}-Regular.ttf"
            for key in f3:
                if f3[key] == value:
                    print(key)
                    print("is this chinese")
                    self.ids.totext.font_name = f"fonts\{key}-Regular.otf"

            self.firebase_font = self.ids.totext.font_name



        except:
            print("not selected")

    def clicked(self, value, root):
        try:
            print(value)
            self.l1 = dic2[value]
            self.ids.fromlang.text = self.l1

        except:
            print("Not selected")

    def text(self, root):
        try:
            ques = self.ids.fromtext.text
            self.firebase_inputtext = ques
            print(ques)
            print(self.l1)
            print(self.l2)
            translation = translator.translate(text=ques, src=self.l1, dest=self.l2)
            print(translation.text)
            self.ids.totext.text = translation.text
            self.firebase_desttext = translation.text
            self.firebase_inputlang = self.l1
            self.firebase_destlang = self.l2

        #   myobj = gTTS(text=translation.text, lang=self.l2, slow=True)
        #   myobj.save("welcome.mp3")
        #   os.system("start welcome.mp3")
        except:
            print("error occured!!")

    def voiceinput(self, root):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print(MyText)
                self.ids.inputques1.text = MyText

                self.l3 = MyText
        except sr.UnknownValueError as e:

            print("ünknown value error")
        except sr.RequestError as e:

            print("Request error")

    def srcinput(self, root):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print(MyText)
                self.l4 = dic2[MyText]
                self.ids.inputsrc.text = MyText
        except sr.UnknownValueError as e:

            print("ünknown value error")
        except sr.RequestError as e:

            print("Request error")

    def destinput(self, root):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                self.l5 = dic2[MyText]
                print(MyText)
                self.ids.inputdes.text = MyText
                for key in f1:
                    if f1[key] == MyText:
                        print(key)
                        self.ids.inputrans.font_name = f"fonts\{key}-Regular.ttf"
                for key in f2:
                    if MyText in f2[key]:
                        print(key)
                        self.ids.inputrans.font_name = f"fonts\{key}-Regular.ttf"
                for key in f3:
                    if f3[key] == MyText:
                        print(key)
                        self.ids.inputrans.font_name = f"fonts\{key}-Regular.otf"



        except sr.UnknownValueError as e:

            print("ünknown value error")
        except sr.RequestError as e:

            print("Request error")

    def speechtranslate(self, root):
        translation = translator.translate(text=self.l3, src=self.l4, dest=self.l5)
        print(translation.text)
        self.ids.inputrans.text = translation.text

        # myobj = gTTS(text=translation.text, lang=self.l2, slow=True)
        # myobj.save("welcome.mp3")
        # os.system("start welcome.mp3")

    def capture(self, root):
        cv2.namedWindow("camera1", 1)
        camera = cv2.VideoCapture()
        camera.open(0)
        while True:
            frame = camera.read()[1]
            cv2.imshow('camera1', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite(f"sak{self.i}.jpg", frame)
                break
            self.i += 1

        cv2.destroyWindow("camera1")
        camera.release()

        self.i = 0

    def extract(self, root):
        path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.tesseract_cmd = path_to_tesseract
        try:
            text1 = pytesseract.image_to_string(Image.open(f'sak{self.i}.jpg'), lang=self.detect)
            print("taken")
            print(text1)
            self.ids.extracttext.text = text1
            os.remove(f'sak{self.i}.jpg')


        except:

            print("error")
            self.imgtext(root)

    # def select(self, root):
    #     from plyer import filechooser
    #     try:
    #         filechooser.open_file(on_selection=self.selected)
    #     except:
    #         print("error occured")
    #
    # def selected(self, root, selection):
    #     print(selection)
    #     self.pic = selection

    def imgtext(self, root):
        path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.tesseract_cmd = path_to_tesseract
        try:
            text2 = pytesseract.image_to_string(Image.open(f"{self.pic}"), lang=self.detect)
            print("taken")
            print(text2)
            self.ids.extracttext.text = text2
        except:
            print("choose image error")

    def data(self, value, root):
        self.detect = dic3[value]
        self.ids.train.text = self.detect

        for key in f1:
            if f1[key] == value:
                print(key)
                self.ids.extracttext.font_name = f"fonts\{key}-Regular.ttf"
        for key in f2:
            if value in f2[key]:
                print(key)
                self.ids.extracttext.font_name = f"fonts\{key}-Regular.ttf"
        for key in f3:
            if f3[key] == value:
                print(key)
                self.ids.extracttext.font_name = f"fonts\{key}-Regular.otf"

    def fileselected(self, value, root):

        try:
            print(value)
            print(value[0])
            self.pic = value[0]
            root.transition = FadeTransition()
            root.current = "screen4"
        except:
            print("file not choosen")

    def select_file(self, root):
        try:

            from plyer import filechooser
            filechooser.open_file(on_selection=self.selected)

        except:
            print("Photo not selected")

    def selected(self, selection):
        print(selection[0])
        self.pic = selection[0]

    def get_history(self, root):
        root.transition = FadeTransition()
        root.current = "screen6"
        res = requests.get(url=firebase_url)
        print(res.json())
        fire = res.json()
        layout = self.ids.box2
        for key in fire:
            fp = fire[key]
            x = fp["source"]
            y = fp["destination"]
            z = fp["InputText"]
            a = fp["TranslatedText"]
            fn = fp['font-name']
            val = f"Source : {x}\nDestination : {y}\nInputText : {z}\nTranslatedText : {a}"
            textadd = TextInput(text=val, font_name=fn, size_hint_y=None, height=150)
            layout.add_widget(textadd)

    def savefirebase(self, root):
        fdata = {
            "source": self.firebase_inputlang,
            "destination": self.firebase_destlang,
            "InputText": self.firebase_inputtext,
            "TranslatedText": self.firebase_desttext,
            "font-name": self.firebase_font
        }
        res = requests.post(url=firebase_url, json=fdata)
        print(res)

    def screenrefresh(self, root):
        self.ids.fromlang.text = ""
        self.ids.tolang.text = ""
        self.ids.fromtext.text = ""
        self.ids.totext.text = ""

    def get_voice(self, txt, root):
        myobj = gTTS(text=txt, lang=self.l2, slow=True)
        myobj.save("welcome.mp3")
        os.system("start welcome.mp3")

    def screenrefresh1(self, root):
        self.ids.inputques1.text = ""
        self.ids.inputsrc.text = ""
        self.ids.inputdes.text = ""
        self.ids.inputrans.text = ""

    def screenrefresh2(self, root):
        self.ids.train.text = ""
        self.ids.extracttext.text = ""


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'BlueGray'
        # self.theme_cls.accent_palette = 'Teal'
        # self.theme_cls.accent_hue = '400'

        sm = WindowManager()
        return sm


ob = MyApp()
ob.run()
