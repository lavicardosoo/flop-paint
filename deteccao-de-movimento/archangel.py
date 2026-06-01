import cv2
from kivy.app import App
from kivy.uix.image import Image 
from kivy.clock import Clock
from kivy.graphics.texture import Texture 
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.core.text import LabelBase
import mediapipe as mp

Window.size = (900,360)

Builder.load_file("assets/desenho.kv")

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


class TelaTrans(Screen):
	def __init__(self, **kwargs):
		
		super().__init__(**kwargs)
		
		print(self.ids.camera_view)

    #add o caminho do seu vídeo aqui !
    #caso queira usar sua webcam, basta adicionar o parâmetro 0 ao invés do caminho do vídeo.
		self.video = cv2.VideoCapture("video.mp4")

		Clock.schedule_interval(self.update, 1.0/60.0)

		self.maozinha = mp.solutions.hands
		self.maozinhaDrawing = mp.solutions.drawing_utils
		self.maozinhaConfig = self.maozinha.Hands()

		with self.canvas:
			Color(0,0,1,1)
			self.line = Line(points=[],width=2)

	def update(self,dt):
		ret,frame = self.video.read()
		
		frame = cv2.resize(frame, (640, 360))
		frame = cv2.rotate(frame, cv2.ROTATE_180)
		frame = cv2.flip(frame,1)

		cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		colorido = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

		maozinha = self.maozinhaConfig.process(colorido)

		self.resultado = self.maozinhaConfig.process(colorido)
		
		if maozinha.multi_hand_landmarks:
			
			maos = self.resultado.multi_hand_landmarks[0]

			im = maos.landmark[8]

			h,w,c = frame.shape

			kivy_x = int(im.x * w) + 250
			kivy_y = int(im.y * h) - 100

			self.line.points += [kivy_x, kivy_y]

			for ponto in maozinha.multi_hand_landmarks:
				
				self.maozinhaDrawing.draw_landmarks(
					frame,
					ponto,
					self.maozinha.HAND_CONNECTIONS
				)

		buf = frame.tobytes()

		texture = Texture.create(
			size=(frame.shape[1], frame.shape[0]),
			colorfmt='bgr'
		)

		texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
		self.ids.camera_view.texture = texture

class FlopApp(App):

    def build(self):
        self.layout = TelaTrans()
        return self.layout
   
FlopApp().run()
