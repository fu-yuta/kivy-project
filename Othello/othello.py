# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Ellipse, Rectangle

class OthelloGrid(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num = 8
        self.tile = [[' ' for x in range(self.num)] for x in range(self.num)]
        self.turn = 'W'

        self.window_size = Window.width if Window.width <= Window.height else Window.height
        self.grid = GridLayout(cols=self.num, spacing=[3,3], size_hint_y=7)

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

        self.creat_view('White Turn')
    
    def put_stone(self):
        self.grid = GridLayout(cols=self.num, spacing=[3,3], size_hint_y=7)
        pass_flag = True
        finish_flag = True
        check = []
        next_turn = 'W' if self.turn == 'B' else 'B'

        for x in range(self.num):
            for y in range(self.num):
                if self.tile[x][y] == 'W':
                    self.grid.add_widget(WhiteStone())
                elif self.tile[x][y] == 'B':
                    self.grid.add_widget(BlackStone())
                else:
                    self.grid.add_widget(PutButton(background_color=(0.451,0.3059,0.1882,1), background_normal='', tile_id=[x, y]))
        
        for x in range(self.num):
            for y in range(self.num):
                if self.tile[x][y] == ' ':
                    finish_flag = False
                    check += self.can_reverse_check(x, y, next_turn)
                if check:
                    pass_flag = False
                    break

        if finish_flag:
            content = Button(text=self.judge_winner())
            popup = Popup(title='Game set!', content=content, auto_dismiss=False, size_hint=(None, None), size=(Window.width/3, Window.height/3))
            content.bind(on_press=popup.dismiss)
            popup.open()
            self.restart_game()
        else:    
            if pass_flag:
                skip_turn_text = 'White Turn' if self.turn == 'B' else 'Black Turn'
                content = Button(text='OK')
                popup = Popup(title=skip_turn_text+' Skip!', content=content, auto_dismiss=False, size_hint=(None, None), size=(Window.width/3, Window.height/3))
                content.bind(on_press=popup.dismiss)
                popup.open()
            else:
                self.turn = next_turn

            turn_text = 'Black Turn' if self.turn == 'B' else 'White Turn'
            self.creat_view(turn_text)
    
    def can_reverse_check(self, check_x, check_y, turn):
        check =[]
        # 左上確認
        check += self.reverse_list(check_x, check_y, -1, -1, turn)
        # 上確認
        check += self.reverse_list(check_x, check_y, -1, 0, turn)
        # 右上確認
        check += self.reverse_list(check_x, check_y, -1, 1, turn)
        # 右確認
        check += self.reverse_list(check_x, check_y, 0, 1, turn)
        # 右下確認
        check += self.reverse_list(check_x, check_y, 1, 1, turn)
        # 下確認
        check += self.reverse_list(check_x, check_y, 1, 0, turn)
        # 左下確認
        check += self.reverse_list(check_x, check_y, 1, -1, turn)
        # 左確認
        check += self.reverse_list(check_x, check_y, 0, -1, turn)
        return check

    def reverse_list(self, check_x, check_y, dx, dy, turn):
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

            if self.tile[check_x][check_y] == turn:
                break
            elif self.tile[check_x][check_y] == ' ':
                tmp = []
                break
            else:
                tmp.append((check_x, check_y))
        return tmp

    def judge_winner(self):
        white = 0
        black = 0
        for x in range(self.num):
            for y in range(self.num):
                if self.tile[x][y] == 'W':
                    white += 1
                elif self.tile[x][y] == 'B':
                    black += 1
        print(white)
        print(black)
        return 'White Win!' if white >= black else 'Black Win!'

    def restart_game(self):
        print("restart game")
        self.tile = [[' ' for x in range(self.num)] for x in range(self.num)]
        self.turn = 'W'
        self.grid = GridLayout(cols=self.num, spacing=[3,3], size_hint_y=7)

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

        self.creat_view('White Turn')

    def creat_view(self, turn_text):
        self.clear_widgets()
        self.turn_label = Label(text=turn_text, width=self.window_size, size_hint_y=1, font_size='30sp')
        self.restart_button = RestartButton(text='Restart')
        self.layout = BoxLayout(orientation='vertical', spacing=10, size=(self.window_size, self.window_size))
        self.layout.add_widget(self.turn_label)
        self.layout.add_widget(self.grid)
        self.layout.add_widget(self.restart_button)
        self.add_widget(self.layout)

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
        turn = self.parent.parent.parent.turn
        
        check += self.parent.parent.parent.can_reverse_check(self.tile_id[0], self.tile_id[1], turn)
        if check:
            self.parent.parent.parent.tile[put_x][put_y] = turn
            for x, y in check:
                self.parent.parent.parent.tile[x][y] = turn
            self.parent.parent.parent.put_stone()

class RestartButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_press(self):
        content = Button(text='OK')
        popup = Popup(title='Restart Game!', content=content, auto_dismiss=False, size_hint=(None, None), size=(Window.width/3, Window.height/3))
        content.bind(on_press=popup.dismiss)
        popup.open()
        self.parent.parent.restart_game()

class OthelloApp(App):
    title = 'オセロ'
    def build(self):
        return OthelloGrid()


OthelloApp().run()