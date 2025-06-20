# main.py
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.core.text import LabelBase

Builder.load_file("desenho.kv")

cor = (0,0,0,1)

class TelaBrancaCisHetero(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.corTrans = (0,0,0,1)
        self.grossura = 1

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:  
                Color(*self.corTrans)
                touch.ud["line"] = Line(points=(touch.x, touch.y), width=self.grossura)
            return True
        
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if "line" in touch.ud:
            touch.ud["line"].points += [touch.x, touch.y]

    def desenhar(self):
        self.corTrans = (1,1,1,1)
        self.grossura = 6

    def mudarCor(self,newcolor):
        self.corTrans = newcolor

    def mudarGrossura(self,novaGrossura):
        self.grossura = novaGrossura


class FlopPaintApp(App):
    def build(self):
        self.layout = RootWidget()
        return self.layout
    

class RootWidget(Screen):
    pass

if __name__ == "__main__":
    FlopPaintApp().run()
    