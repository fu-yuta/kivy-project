# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle

class WhiteStone(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update)
        self.bind(size=self.update)
        self.update()
    def update(self, *args):
        self.canvas.clear()
        self.canvas.add(Color(0.451,0.3059,0.1882,1))
        self.canvas.add(Rectangle(pos=self.pos, size=self.size))
        self.canvas.add(Color(1,1,1,1))
        self.canvas.add(Ellipse(pos=self.pos, size=self.size))

class BlackStone(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update)
        self.bind(size=self.update)
        self.update()
    def update(self, *args):
        self.canvas.clear()
        self.canvas.add(Color(0.451,0.3059,0.1882,1))
        self.canvas.add(Rectangle(pos=self.pos, size=self.size))
        self.canvas.add(Color(0,0,0,1))
        self.canvas.add(Ellipse(pos=self.pos, size=self.size))

class OthelloApp(App):
    title = 'オセロ'
    def build(self):
        num = 8
        grid = GridLayout(cols=num, spacing=[3,3])
        for i in range(1,num*num+1):
            if i == 28 or i == 37:
                grid.add_widget(WhiteStone())
            elif i == 29 or i == 36:
                grid.add_widget(BlackStone())
            else:
                grid.add_widget(Button(background_color=(0.451,0.3059,0.1882,1), background_normal=""))
        return grid


OthelloApp().run()