from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.properties import NumericProperty, BooleanProperty
from kivy.core.window import Window
import numpy as np


class BoxLayoutExample(BoxLayout):
       
        def __init__(self, **kwargs):
        	super().__init__(**kwargs)
        	self.orientation='vertical'
        	VB1 = BoxLayout(orientation='vertical',
                             size_hint=(1, 0.15))
        	
        	VB2 = BoxLayout(
        							orientation='vertical',
        							size_hint=(1, 0.7))
        							
        	VB3 = BoxLayout(
        								orientation='horizontal',
        								size_hint=(0.4,.05))
        							
        	HB= BoxLayout(
        						orientation='horizontal', 										size_hint=(1,.1))
        	
        						
        	self.add_widget(VB1)
        	self.add_widget(VB2)
        	self.add_widget(VB3)
        	self.add_widget(HB)
        	
        	self.d = DrawInput()
        	self.d.bind(numx=self.update_label)
        	
        	self.label = MyLabel(text=f"{self.d.numx}", 
        							size_hint= (1, 0.2), 													font_size= '80dp',
        							color=[0.85,0.85,.85,1])
        							
        	self.checkbox = CheckBox(
        						size_hint=(.2,1),
        						color=[0.5,0.5,0.5,1])
        	self.checkbox.bind(active=self.on_checkbox_active)
        	self.l2 = Label(text='Auto Submit',
        						size_hint=(.8,1),
        						font_size='18dp',
        						color=[0.5,0.5,0.5,1])
        	
        	
        	VB1.add_widget(self.label)
        	VB2.add_widget(self.d)
        	VB3.add_widget(self.checkbox)
        	VB3.add_widget(self.l2)
        	
        	b1=Button(text='Submit', 
        			size_hint=(0.7, 1), 
        			font_size='30dp', 
        			color=[.9, 1, .9, 1],
        			background_normal='',
        			background_color=[.3, .8, .2, 1])
        	HB.add_widget(b1)
        	b1.bind(on_release=self.d.submit)
        	
        	b2=Button(text='Clear',
        			 size_hint=(0.3, 1), 
        			 font_size='20dp', 
        			 color=[1, .9, 0.9,1],
        			 background_normal='',
        			 background_color=[1, 0 , 0, 1])
        	HB.add_widget(b2)
        	b2.bind(on_release=self.d.wipe)
        	
        def update_label(self, instance, value):
        	self.label.text = str(value)
        	
        def on_checkbox_active(self, instance, value):
        	if value:
        		self.d.check=True
        		
        	else:
        		self.d.check=False
        	
        	
class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.3, .7, 1, .8)
            Rectangle(pos=self.pos, size=self.size)

        
class DrawInput(Widget):
    numx = NumericProperty(9)
    check=BooleanProperty(False)
    lst=[]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gen_num()
        self.background()
    	
    def on_touch_down(self, touch):
    	with self.canvas:
    		Color(0,0,0,1)
    		touch.ud["line"]= Line(points=(touch.x, touch.y), width=10)
    		
    def on_touch_move(self, touch):
        touch.ud["line"].points += (touch.x, touch.y)
        self.lst += touch.ud["line"].points
    	
    def on_touch_up(self, touch):
        #auto_on = self.check
        if len(self.lst) >0:
            print(self.lst)
            if self.check:
                self.submit(self.check)
                self.lst=[]
        
        
    def submit(self, instance):
        print(self.lst)
        if len(self.lst) >0:
            print(self.lst)
            self.lst=[]
            self.save_image()
            self.background()
            self.gen_num()

    def clear(self, instance):
        self.background()
        self.gen_num()
    
    def save_image(self):
        	self.export_to_png(
        	f'images/{self.numx}/no_{self.numx}_s{self.rser}.png')
        
    def background(self):
        a,b = Window.size
        b=b*.85
        self.canvas.clear()
        with self.canvas:
        	   	Color(1, 1, 1, 1)
        	   	Rectangle(pos=(0,0), size=(a,b))
        	   	
    def gen_num(self):
        self.numx= np.random.randint(0,10)
        self.rser = np.random.randint(10000, 999999)
    	
    def wipe(self, instance):
    	self.background()
       
		
class NumScriptusApp(App):
    def build(self): 
        return BoxLayoutExample()
		
if __name__ == "__main__":
    NumScriptusApp().run()
	
