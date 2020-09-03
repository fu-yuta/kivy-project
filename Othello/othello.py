# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle

class OthelloGrid(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num = 8
        self.tile = [[' ' for x in range(self.num)] for x in range(self.num)]
        self.turn = 'W'

        self.window_size = Window.width if Window.width <= Window.height else Window.height
        self.grid = GridLayout(cols=self.num, spacing=[3,3], size=(self.window_size, self.window_size))

        for x in range(self.num):
            for y in range(self.num):
                if x == 3 and y == 3 or x == 4 and y == 4:
                    self.grid.add_widget(WhiteStone())
                    self.tile[x][y] = 'W'
                elif x == 4 and y == 3 or x == 3 and y == 4:
                    self.grid.add_widget(BlackStone())
                    self.tile[x][y] = 'B'
                else:
                    self.grid.add_widget(PutButton(background_color=(0.451,0.3059,0.1882,1), background_normal='', tile_id=[x, y]))
        self.add_widget(self.grid)
    
    def put_stone(self, *args):
        self.clear_widgets()
        self.grid = GridLayout(cols=self.num, spacing=[3,3], size=(self.window_size, self.window_size))
        
        for x in range(self.num):
            for y in range(self.num):
                if self.tile[x][y] == 'W':
                    self.grid.add_widget(WhiteStone())
                elif self.tile[x][y] == 'B':
                    self.grid.add_widget(BlackStone())
                else:
                    self.grid.add_widget(PutButton(background_color=(0.451,0.3059,0.1882,1), background_normal='', tile_id=[x, y]))
        self.add_widget(self.grid)

        self.turn = 'W' if self.turn == 'B' else 'B'


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

class PutButton(Button):
    def __init__(self, tile_id,  **kwargs):
        super().__init__(**kwargs)
        self.tile_id =tile_id

    def on_press(self):
        print(self.tile_id)
        x = self.tile_id[0]
        y = self.tile_id[1]
        self.parent.parent.tile[x][y] = self.parent.parent.turn
        self.parent.parent.put_stone()

class OthelloApp(App):
    title = 'オセロ'
    def build(self):
        return OthelloGrid()


OthelloApp().run()