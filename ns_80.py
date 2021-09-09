from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.properties import NumericProperty, BooleanProperty
from kivy.core.window import Window
#from kivymd.toast import toast
import numpy as np
import os


class MainLayout(BoxLayout):
    def __init__(self, **kwargs): 
        super(MainLayout, self).__init__(**kwargs)
        self.orientation='vertical'
        self.a, self.b = Window.size
        
        ##MAIN LABEL
        self.title = MyLabel(text=
                            'Welcome to NumeroScriptus', 
                            size_hint=(1, 0.1), 
                            font_size= '30sp', 
                            color=[0.85,0.85,0.85,1]
                            )
        self.title.col = (0.3, 0.5, .7, 1)
        self.title_lyot = BoxLayout(orientation='vertical',
                             size_hint=(1, 0.1))
        self.title_lyot.add_widget(self.title)
        
        ##SUBTITLE - INSTRUCTIONS
        self.subtitle = MyLabel(text=
                            'Please write the following number on the whiteboard:', 
                            size_hint=(1, 0.05),
                            halign='left',
                            font_size= '18sp', 
                            color=[0.85,0.85,0.85,1]
                            )
        self.subtitle.col = (0.5, 0.7, .85, 1)
        self.sub_lyot =                                                                     BoxLayout(orientation='vertical',
                                       size_hint=(1, 0.2))
        self.sub_lyot.add_widget(self.subtitle)
                 
                            
        ## INITIALIZING DRAWING OBJECT
        self.d=DrawMe()
        self.d.bind(numx=self.update_label)
        
        ## NUMBER BAR
        self.num_bar = MyLabel(
                                    text=str(self.d.numx),
                                    size_hint= (1, .2),
                                    font_size= '70sp',
                                    color=[0.25,0.25,.30,1])
        self.num_bar.col = (0.5, 0.7, .85, 1)
        
        self.sub_lyot.add_widget(self.num_bar)
        
        ## MAIN DRAWING PANEL LAYOUT
        self.panel_lyot = BoxLayout(
                            orientation='vertical',
                            size_hint=(1, None), 
                            size=(self.a, 0.53*self.b),
                            pos=(0, .2*self.b)
                            )
        self.panel_lyot.add_widget(self.d)
        
        ## SWITCH LAYOUT
        self.switch_lyot = BoxLayout(
                            orientation='horizontal',
                            size_hint=(.7,.05),
                            padding=(0,0,0,30))
                            
        with self.switch_lyot.canvas:
            Color(.9,.9,.9,1)
            Rectangle(pos=(0, self.b*.133), size=(self.a, .066*self.b))
        self.myswitch = Switch(active=False)
            
        self.myswitch.bind(active=self.on_checkbox_active)
            
        self.switch_label = Label(text='Auto save after pen up', size_hint=(.7,1), font_size='20sp', halign='left', color=[0.5,0.5,0.5,1])
        
        self.switch_lyot.add_widget(self.myswitch)
        self.switch_lyot.add_widget(self.switch_label)
        
        ## BUTTONS LAYOUT
        self.buttons_lyot =                                                                 BoxLayout(orientation='horizontal', 
                                       size_hint=(1,.1))
        self.b1=Button(text='Save', 
                        size_hint=(0.5, 1), 
                        font_size='25sp', 
                        color=[.9, 1, .9, 1],
                        background_normal='',
                        background_color=[.3, .75, .2, 1])
        self.b1.bind(on_release=self.d.submit)
            
        self.b2=Button(text='Clear',
                     size_hint=(0.25, 1), 
                     font_size='20sp', 
                     color=[1, .9, 0.9,1],
                     background_normal='',
                     background_color=[.9, .3 , .2, 1])
        self.b2.bind(on_release=self.d.background)
            
        self.b3 = Button(text='Undo',
                     size_hint=(0.25, 1), 
                     font_size='20sp', 
                     color=[1, .9, 0.9,1],
                     background_normal='',
                     background_color=[.9, .6 , .2, 1])
        self.b3.bind(on_release=self.d.undo_save)
        
        
        ## FOOTER
        self.foot_lyot = BoxLayout(
                                    orientation='vertical',
                                    size_hint=(1, .04))
                                    
        self.msg = MyLabel(
            text='Produced by Moataz - abbasmd.com', size_hint= (1, 0.2), font_size= '16sp', color=[0.25,0.25,.30,1])
        self.msg.col = (0.6, 0.6, .6, 1)
        
        self.foot_lyot.add_widget(self.msg)
        
        self.buttons_lyot.add_widget(self.b1)
        self.buttons_lyot.add_widget(self.b2)
        self.buttons_lyot.add_widget(self.b3)
        
        ### LAYOUT SETUP
      
        self.add_widget(self.title_lyot)
        self.add_widget(self.sub_lyot)
        self.add_widget(self.panel_lyot)
        self.add_widget(self.switch_lyot)
        self.add_widget(self.buttons_lyot)
        self.add_widget(self.foot_lyot)
        
    def update_label(self, instance, value):
        self.num_bar.text = str(value)
            
    def on_checkbox_active(self, instance, value):
        if value:
            self.d.check=True
        else:
            self.d.check=False


class DrawMe(Widget):
    numx = NumericProperty(9)
    check=BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(DrawMe, self).__init__(**kwargs)
        self.filename=''
        self.fl=[]
        self.gen_num()
        self.background()
        self.touchdown= False
        self.widget_size()
        self.numlst=[]
    
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
            if self.touchdown:
                self.touchdown=False
                if self.check:
                    self.submit()
        else:
            pass
                
    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.touchdown:
                touch.ud["line"].points += (touch.x, touch.y)
            else:
                pass
 
    def submit(self, *args):
        self.save_image()
        self.background()
        self.gen_num()

    def save_image(self):
        self.filename = os.path.join('images', str(self.numx), 'num_{}_s{}.png'.format(self.numx, self.rser))
        self.numlst.append(self.numx)
        self.fl.append(self.filename)
     #print(self.numlst)
        self.export_to_png(filename=self.filename)
            
    def undo_save(self, *args):
        if self.fl:
            os.remove(self.fl[-1])
            #toast('Previous number "{}" card is deleted.'.format(self.numlst[-1]))
            self.fl.pop()
            self.numlst.pop()
            #toast('Remaining {} card(s) saved'.format(len(self.numlst)))
        else:
            #toast('No cards to delete!')
            pass
        
    def background(self, *args):
        self.canvas.clear()
        self.widget_size()
        with self.canvas:
            Color(1,1,1,1)
            Rectangle(pos=self.pos, size=self.size)
        
    def widget_size(self):
        a,b = Window.size
        self.size= a, b*.53
        self.pos= 0, b*.20
                       
    def gen_num(self):
        self.numx= np.random.randint(0,10)
        self.rser = np.random.randint(10000, 99999)
               
 
class MyLabel(Label):
    col=(0.5,0.5,0.5,1)
    def on_size(self, *args):
        a,b,c,d = self.col
        self.canvas.before.clear()
        with self.canvas.before:
            Color(a,b,c,d)
            Rectangle(pos=self.pos, size=self.size)
        
        
class NumScriptApp(App):
    def build(self):
        #dir = os.path.join('', 'images')
        for i in range(10):
        	nd= os.path.join('images', str(i))
        	if not os.path.exists(nd):
        		os.makedirs(nd)
        		print(nd,' made')
        m = MainLayout()
        return m
        
if __name__ in ('__main__', '__android__'):
    NumScriptApp().run()
    