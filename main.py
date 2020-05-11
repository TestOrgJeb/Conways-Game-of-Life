import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy_deps import sdl2, glew
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.config import Config
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line
from kivy.core.window import Window
from Untitled import Environment

#TODO add the ability to change probability of initial cell condition
#TODO add ability to set seed
#TODO add the ability to save current state to pick up where you left off
#TODO determine if slowdown is due to a memory leak, graphics rendering, or computations
    #TODO if memory leak --> fix
    #TODO if graphics --> optimize
    #TODO if computations --> add threading

class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.E = None
        self.step = None
        self.dropdown = SpeedDropDown()
        self.speed_select = Button(text='Normal', pos_hint={'x':.15, 'y':.6}, size_hint=(.2, .06))
        self.add_widget(self.speed_select)
        self.speed_select.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x:setattr(self.speed_select, 'text', x))
        self.dropdown.bind(on_select=lambda instance, x:self.change_speed(self.speed_select.text))
        self.w = 0 
        self.h = 0
        self.anchor_x = 0
        self.anchor_y = 0
        self.ready=False
        self.ready_check  = Clock.schedule_interval(self.confirm_settings, .1)
        self.tick_time = 1
        self.pool_wall = 0
        self.cell_width = 0
        self.cell_height = 0
        self.all_cells = {}
        self.active_cells = {}
        self.stop_butt.disabled = True

    def continuous_run(self, dt):
        self.step_once()

    def step_once(self):
        if self.ready:
            self.E.tick()
            changes = self.E.delta_cells
            self.update_drawing(changes)
        gen_text = 'generations' if self.E.generation >1 else 'generation'
        print(f'{self.E.generation} {gen_text} run')
    
    def start_game(self):
        if self.ready:
            print('Game Started')        
            print(self.to_window(self.pool.pos[0], self.pool.pos[1]))
            self.anchor_x = self.to_window(self.pool.pos[0], self.pool.pos[1])[0]
            self.anchor_y = self.to_window(self.pool.pos[0], self.pool.pos[1])[1]
            self.pool_wall = self.to_window(self.pool.size[0], self.pool.size[1])[0]
            self.draw_base_grid()
            self.start_butt.disabled = True
            self.step_butt.disabled = True
            self.stop_butt.disabled = False
            self.step = Clock.schedule_interval(self.continuous_run, self.tick_time)
            
        else:
            print('Please set all settings')
    
    def stop_game(self):
        self.step.cancel()
        self.stop_butt.disabled = True
        self.start_butt.disabled = False
        self.step_butt.disabled = False
        print('Game Stopped')
    
    def reset_game(self):
        self.__init__()
        print('Game Reset')
    
    def change_speed(self, new_speed):
        self.tick_time = 2 if new_speed == 'Slow' else .5  if new_speed == 'Normal' else .1
        print(self.tick_time)
    
    def set_w(self):
        try:
            self.w = int(self.grid_width.text)
        except:
            print('Failed to set width') #notify that it needs to be an int
    
    def set_h(self):
        try:
            self.h = int(self.grid_height.text)
        except:
            print('Failed to set height') #notifiy that it needs to be an int
    
    def confirm_settings(self, dt):
        if self.w != 0 and self.h != 0:
            self.ready = True
            self.E = Environment(self.w, self.h)
            self.ready_check.cancel()
            print('Ready!')
    
    def draw_base_grid(self):
        self.cell_width = self.pool_wall/self.w
        self.cell_height = self.cell_width
        print(self.cell_width, self.cell_height)
        for i in range(self.w):
            for j in range(self.h):
                _x = self.anchor_x + (self.cell_width* i)
                _y = self.anchor_y + (self.cell_height*j) 
                _w = self.cell_width
                _h = self.cell_height
                r, g, b, a = self.get_cell_color((i, j))
                self._draw(i, j, _x, _y, _w, _h, r, g, b, a)

    def _draw(self,i, j, x, y, w, h, r, g, b, a):
        with self.pool.canvas:
            Color(r, g, b, a)
            rect = Rectangle(pos=[x, y], size=[w, h])
        self.all_cells[(i, j)] = [x, y, w, h, r, g, b, a]
    
    def get_cell_color(self, loc):
        if self.E.grid[loc]:
            return 0, 0, 0, 1
        return 1, 1, 1, 1
    
    def update_drawing(self, cells):
        for cell in cells:
            self.all_cells[cell][4] = abs(self.all_cells[cell][4]-1)
            self.all_cells[cell][5] = abs(self.all_cells[cell][5]-1)
            self.all_cells[cell][6] = abs(self.all_cells[cell][6]-1)
            self._draw( cell[0], cell[1],
                        self.all_cells[cell][0],
                        self.all_cells[cell][1],
                        self.all_cells[cell][2],
                        self.all_cells[cell][3],
                        self.all_cells[cell][4],
                        self.all_cells[cell][5],
                        self.all_cells[cell][6],
                        self.all_cells[cell][7])
        
class SpeedDropDown(DropDown):
    pass

class mainApp(App):
    def build(self):
        return MainScreen()

if __name__ =='__main__':
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    mainApp().run()