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
        self.tile_id = tile_id

    def on_press(self):
        print(self.tile_id)
        put_x = self.tile_id[0]
        put_y = self.tile_id[1]
        check =[]
        turn = self.parent.parent.turn
        
        # 左上確認
        check += self.can_reverse_check(self.tile_id[0], self.tile_id[1], -1, -1, turn)
        # 上確認
        check += self.can_reverse_check(self.tile_id[0], self.tile_id[1], -1, 0, turn)
        # 右上確認
        check += self.can_reverse_check(self.tile_id[0], self.tile_id[1], -1, 1, turn)
        # 右確認
        check += self.can_reverse_check(self.tile_id[0], self.tile_id[1], 0, 1, turn)
        # 右下確認
        check += self.can_reverse_check(self.tile_id[0], self.tile_id[1], 1, 1, turn)
        # 下確認
        check += self.can_reverse_check(self.tile_id[0], self.tile_id[1], 1, 0, turn)
        # 左下確認
        check += self.can_reverse_check(self.tile_id[0], self.tile_id[1], 1, -1, turn)
        # 左確認
        check += self.can_reverse_check(self.tile_id[0], self.tile_id[1], 0, -1, turn)
        if check:
            self.parent.parent.tile[put_x][put_y] = turn
            for x, y in check:
                self.parent.parent.tile[x][y] = turn
            self.parent.parent.put_stone()
    
    def can_reverse_check(self, check_x, check_y, dx, dy, turn):
        tmp = []
        while True:
            check_x += dx
            check_y += dy
            if check_x < 0 or check_x > 7:
                tmp = []
                break
            if check_y < 0 or check_y > 7:
                tmp = []
                break

            if self.parent.parent.tile[check_x][check_y] == turn:
                break
            elif self.parent.parent.tile[check_x][check_y] == ' ':
                tmp = []
                break
            else:
                tmp.append((check_x, check_y))
        return tmp

class OthelloApp(App):
    title = 'オセロ'
    def build(self):
        return OthelloGrid()


OthelloApp().run()