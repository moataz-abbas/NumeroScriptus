#pylint:disable=W0311
#pylint:disable=W0613
#pylint:disable=E0611
#pylint:disable=E1101
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.label import Label
#from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.properties import NumericProperty, BooleanProperty
from kivy.core.window import Window
import numpy as np
import os


class MainLayout(BoxLayout):
       
        def __init__(self, **kwargs):
        	super().__init__(**kwargs)
        	self.orientation='vertical'
        	
        	self.a, self.b = Window.size
        	
        	
        	VB0 = BoxLayout(orientation='vertical',
                             size_hint=(1, 0.1))
                             
        	VB1 = BoxLayout(orientation='vertical',
                             size_hint=(1, 0.2))
        	
        	
        	VB2 = BoxLayout(
        							orientation='vertical',
        							size_hint=(1, None),
        							size=(self.a, 0.6*self.b),
        							pos=(0, .1*self.b)
        							)
        							
        	
        							
        	HB= BoxLayout(
        						orientation='horizontal', 										size_hint=(1,.15))
        						
        	HB2 = BoxLayout(
        								orientation='horizontal',
        								size_hint=(.7,.05))
        	
        	HB3 = BoxLayout(
        								orientation='horizontal',
        								size_hint=(1, .15))
        								
        								
        	self.add_widget(VB0)					
        	self.add_widget(VB1)
        	self.add_widget(VB2)
        	self.add_widget(HB2)
        	self.add_widget(HB)
        	self.add_widget(HB3)
        	
        	
        	self.title = MyLabel(text=
        					'Welcome to Numero Scriptus', 
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
        	
        	self.label = MyLabel(text=f"{self.d.numx}",								size_hint= (1, 0.2), 													font_size= '80sp',
        						color=[0.25,0.25,.30,1])
        	self.label.col = (0.5, 0.7, .85, 1)
        	
        	
        	self.checkbox = Switch(
        								active=False,
        								#size_hint=(None, None),
        								#size=(300,50)
        								)
        	self.checkbox.bind(active=self.												on_checkbox_active)
        	
        	self.checklabel = Label(text='Auto save after pen up', size_hint=(.7,1), font_size='20sp',
        						halign='left',
        						color=[0.5,0.5,0.5,1])
        	
        	

        	
        	b1=Button(text='Save', 
        			size_hint=(0.4, 1), 
        			font_size='25sp', 
        			color=[.9, 1, .9, 1],
        			background_normal='',
        			background_color=[.3, .75, .2, 1])
        	
        	b1.bind(on_release=self.d.submit)
        	
        	b2=Button(text='Clear',
        			 size_hint=(0.3, 1), 
        			 font_size='20sp', 
        			 color=[1, .9, 0.9,1],
        			 background_normal='',
        			 background_color=[.9, .3 , .2, 1])
        	b2.bind(on_release=self.d.background)
        	
        	b3 = Button(text='Undo',
        			 size_hint=(0.3, 1), 
        			 font_size='20sp', 
        			 color=[1, .9, 0.9,1],
        			 background_normal='',
        			 background_color=[.9, .6 , .2, 1])
        	
        	b3.bind(on_release=self.d.undo_save)
        	
        	self.footer = MyLabel(
        	text='Produced by Moataz@abbasmd.com',	size_hint= (1, 0.2), 													font_size= '18sp',
        					color=[0.25,0.25,.30,1])
        	self.label.col = (0.5, 0.7, .85, 1)
        	
        	VB0.add_widget(self.title)
        	VB1.add_widget(self.subtitle)
        	VB1.add_widget(self.label)
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
	
	def on_touch_down(self, touch):
	   	if self.collide_point(touch.x, touch.y):
	   		with self.canvas:
	   			Color(0,0,0,1)
	   			touch.ud["line"]= Line(points=(touch.x, touch.y), width=10)
	   	else:
	   		touch.ud["line"]= Line()
    		
	def on_touch_up(self, touch):
        	if self.collide_point(touch.x, touch.y):
        		if self.check:
        		     	 	self.submit()
        	else:
        		pass
        		
	def on_touch_move(self, touch):
		if self.collide_point(touch.x, touch.y):
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
        	self.export_to_png(filename=self.															filename)
        	
	def undo_save(self, *args):
	       	if self.fl:
	       		os.remove(self.fl[-1])
	       		self.fl.pop()
        	
        
	def background(self, *args):
	       self.canvas.clear()
	       self.widget_size()
	       with self.canvas:
        	   		Color(0,0,0, 1)
        	  	 	Rectangle(pos=self.pos, size=self.size)
        
        
	def widget_size(self):
        	   	a,b = Window.size
        	   	self.size= a, b*.6
        	   	self.pos= 0, b*.15
        	   		
	def gen_num(self):
	       self.numx= np.random.randint(0,10)
	       self.rser = np.random.randint(10000, 99999)
       
		
class NumScriptusApp(MDApp):
    def build(self): 
    	m = MainLayout()
    	return m
		
if __name__ == "__main__":
    NumScriptusApp().run()
	