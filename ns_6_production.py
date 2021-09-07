from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.properties import NumericProperty, BooleanProperty
from kivy.core.window import Window
from kivymd.toast import toast
import numpy as np
import os


class MainLayout(BoxLayout):
       
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.orientation='vertical'
            #Window.size=(1080,2000)
            #print(Window.size)
            self.a, self.b = Window.size
            
            #Title
            lyt_title = BoxLayout(orientation='vertical',
                             size_hint=(1, 0.1))
                             
            lyt_label = BoxLayout(orientation='vertical',
                             size_hint=(1, 0.2))
            
            
            VB2 = BoxLayout(
                            orientation='vertical',
                            size_hint=(1, None),
                            size=(self.a, 0.53*self.b),
                            pos=(0, .2*self.b)
                            )
                                    
            
                                    
            HB= BoxLayout(orientation='horizontal', 
                          size_hint=(1,.1))
                                
            HB2 = BoxLayout(
                            orientation='horizontal',
                            size_hint=(.7,.05))
            
            HB3 = BoxLayout(
                            orientation='vertical',
                            size_hint=(1, .04))
                                        
                                        
            self.add_widget(lyt_title)
            self.add_widget(lyt_label)
            self.add_widget(VB2)
            self.add_widget(HB2)
            self.add_widget(HB)
            self.add_widget(HB3)
            
            
            self.title = MyLabel(text=
                            'Welcome to NumeroScriptus', 
                            size_hint=(1, 0.1), 
                            font_size= '30sp', 
                            color=[0.85,0.85,0.85,1])
            self.title.col= (0.3, 0.5, .7, 1)        
            
            self.subtitle = MyLabel(text=
                            'Please write the following number on the whiteboard:', 
                            size_hint=(1, 0.05),
                            halign='left',
                            font_size= '18sp', 
                            color=[0.85,0.85,0.85,1])
            self.subtitle.col= (0.5, 0.7, .85, 1)
            
            self.d = DrawInput()
            self.d.bind(numx=self.update_label)
            
            self.label = MyLabel(text=f"{self.d.numx}",                               size_hint= (1, 0.2), font_size= '80sp', color=[0.25,0.25,.30,1])
            self.label.col = (0.5, 0.7, .85, 1)
            
            self.checkbox = Switch(active=False)
            
            self.checkbox.bind(active=self.on_checkbox_active)
            
            self.checklabel = Label(text='Auto save after pen up', 
                                    size_hint=(.7,1), font_size='20sp',
                                    halign='left',
                                    color=[0.5,0.5,0.5,1])
            
            
            b1=Button(text='Save', 
                        size_hint=(0.5, 1), 
                        font_size='25sp', 
                        color=[.9, 1, .9, 1],
                        background_normal='',
                        background_color=[.3, .75, .2, 1])
            b1.bind(on_release=self.d.submit)
            
            b2=Button(text='Clear',
                     size_hint=(0.25, 1), 
                     font_size='20sp', 
                     color=[1, .9, 0.9,1],
                     background_normal='',
                     background_color=[.9, .3 , .2, 1])
            b2.bind(on_release=self.d.background)
            
            b3 = Button(text='Undo',
                     size_hint=(0.25, 1), 
                     font_size='20sp', 
                     color=[1, .9, 0.9,1],
                     background_normal='',
                     background_color=[.9, .6 , .2, 1])
            b3.bind(on_release=self.d.undo_save)
            
            self.footer = MyLabel(
            text='Produced by Moataz - abbasmd.com',size_hint= (1, 0.2),
            font_size= '18sp', color=[0.25,0.25,.30,1])
            self.footer.col = (0.6, 0.6, .6, 1)
            
            lyt_title.add_widget(self.title)
            lyt_label.add_widget(self.subtitle)
            lyt_label.add_widget(self.label)
            VB2.add_widget(self.d)
            HB2.add_widget(self.checkbox)
            HB2.add_widget(self.checklabel)
            HB.add_widget(b1)
            HB.add_widget(b2)
            HB.add_widget(b3)
            HB3.add_widget(self.footer)
            
            
        def update_label(self, instance, value):
            self.label.text = str(value)
            
        def on_checkbox_active(self, instance, value):
            if value:
                self.d.check=True
            else:
                self.d.check=False
            
            
            
class MyLabel(Label):
    col=(0.5,0.5,0.5,1)
    def on_size(self, *args):
        a,b,c,d = self.col
        self.canvas.before.clear()
        with self.canvas.before:
            Color(a,b,c,d)
            Rectangle(pos=self.pos, size=self.size)
        
        
        
class DrawInput(Widget):
    numx = NumericProperty(9)
    check=BooleanProperty(False)
    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.filename=''
            self.fl=[]
            self.gen_num()
            self.background()
            self.touchdown= False
            self.widget_size()
    
    def on_touch_down(self, touch):
           if self.collide_point(touch.x, touch.y):
               with self.canvas:
                   Color(0,0,0,1)
                   touch.ud["line"]= Line(points=(touch.x, touch.y), width=10)
                   self.touchdown=True
           else:
               touch.ud["line"]= Line()
               pass
            
    def on_touch_up(self, touch):
            if self.collide_point(touch.x, touch.y):
                if self.touchdown==True:
                	self.touchdown=False
                	if self.check:
                              	self.submit()
                else:
                	pass
                
    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
              if self.touchdown==True:
              	touch.ud["line"].points += (touch.x, touch.y)
        else:
            pass

    def submit(self, *args):
            self.save_image()
            self.background()
            self.gen_num()

    def save_image(self):
            self.filename= f'images/{self.numx}/no_{self.numx}_s{self.rser}.png'
            #self.filename= f'images/no_{self.numx}_s{self.rser}.png'
            self.fl.append(self.filename)
            print(self.fl)
            self.export_to_png(filename=self.                                                            filename)
            
    def undo_save(self, *args):
               if self.fl:
                   os.remove(self.fl[-1])
                   toast(f'{self.fl[-1]} deleted')
                   self.fl.pop()
               else:
               	toast('No more files')
            
        
    def background(self, *args):
           self.canvas.clear()
           self.widget_size()
           with self.canvas:
                         Color(1,1,1,1)
                         Rectangle(pos=self.pos, size=self.size)
        
        
    def widget_size(self):
                   a,b = Window.size
                   self.size= a, b*.53
                   self.pos= 0, b*.2
                       
    def gen_num(self):
           self.numx= np.random.randint(0,10)
           self.rser = np.random.randint(10000, 																		99999)
       
        
class NumScriptusApp(MDApp):
    def build(self):
        #dir = os.path.join('', 'images')
        for i in range(10):
        	nd= os.path.join('images',f'{i}')
        	if not os.path.exists(nd):
        		os.makedirs(nd)
        		print(nd,' made')
        m = MainLayout()
        return m
        
if __name__ == "__main__":
    NumScriptusApp().run()
    