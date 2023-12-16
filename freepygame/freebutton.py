import pygame
import pygame.gfxdraw
import pygame.draw

from freepygame.freecircle import FreeCircle

def position_button(button, pos: tuple[int, int]) -> bool:
	"""判断给定的坐标是否和按钮对象的坐标重合。
	注意，本函数对圆型按钮（CircleButton）类的坐标使用的是外切矩形的坐标！"""
	if (button.get_coordinates()[1][0] >= pos[0] >= button.get_coordinates()[0][0] and
		button.get_coordinates()[3][1] >= pos[1] >= button.get_coordinates()[0][1]):
		return True
	return False

class FreeButton():
	"""自定义按钮类"""

	check_button = False
	display_button = True

	def __init__(self, screen, coordinates, button_size, msg, font = 'SimHei', size = 24, border_width = 1, draw_border = True, draw_line = False, msg_tran = False,
				 line_width = 1, button_color = (0, 0, 0), text_color = (255, 255, 255), border_color = (0, 0, 0), line_color = (255, 255, 255), dsm = 1):
		"""初始化按钮:
		screen -> 设置的窗口, coordinates[x,y] -> 按钮左上角坐标, button_size[x,y] -> 按钮大小, msg -> 文本, font -> 字体, size -> 文本大小, msg_tran -> 透明
		border_width -> 边框宽度, draw_border -> 显示边框, draw_line -> 显示线, line_width -> 线宽度, button_color(R,G,B) -> 按钮背景色,
		text_color(R,G,B) -> 文本颜色(前景色), border_color(R,G,B) -> 边框颜色, line_color(R,G,B) -> 线颜色, dsm -> 放大倍数"""
		self.msg = msg
		self.dsm = dsm
		self.screen = screen
		self.width = button_size[0] * self.dsm
		self.height = button_size[1] * self.dsm
		self.coordinates = coordinates
		self.coordinates[0] *= self.dsm
		self.coordinates[1] *= self.dsm
		self.button_color = button_color
		self.text_color = text_color
		self.draw_line = draw_line
		self.draw_border = draw_border
		self.border = [border_width, border_color]
		self.line = [line_width, line_color]
		self.msg_tran = msg_tran
		self.font = pygame.font.Font(font, size)
		self.rect = pygame.Rect(0, 0, self.width * self.dsm, self.height * self.dsm)
		self.rect.centerx = (self.coordinates[0] + self.width / 2)
		self.rect.centery = (self.coordinates[1] + self.height / 2)
		self.msg_img = self.font.render(self.msg, True, self.text_color, self.button_color).convert()
		if self.msg_tran is True: self.msg_img.set_colorkey(self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.rect.center

	def __str__(self):
		return """自定义按钮类"""
	__repr__ = __str__

	def get_attribute(self) -> dict:
		"""获取按钮对象的信息"""
		return {"screen": self.screen, "coordinates": [self.coordinates[0], self.coordinates[1]], "button_size": [self.width, self.height],
				"msg": self.msg, "font": self.font, "draw_border": self.draw_border, "draw_line": self.draw_line,
				"border_width": self.border[0], "line_width": self.line[0], "text_color": self.text_color,
				"button_color": self.button_color, "border_color": self.border[1], "line_color": self.line[1]}

	def get_coordinates(self) -> list:
		"""获取坐标信息"""
		return [[self.coordinates[0], self.coordinates[1]], [self.coordinates[0] + self.width, self.coordinates[1]],
				[self.coordinates[0] + self.width, self.coordinates[1] + self.height], [self.coordinates[0], self.coordinates[1] + self.height]]

	def open_line(self, draw_line: bool):
		"""是否显示线"""
		self.draw_line = draw_line

	def open_border(self, draw_border: bool):
		"""是否显示边框"""
		self.draw_border = draw_border

	def set_msg(self, msg):
		"""改变文本"""
		self.msg = msg
		self.msg_img = self.font.render(self.msg, True, self.text_color, self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.rect.center

	def set_line_color(self, color):
		"""改变线的颜色"""
		self.line[1] = color

	def set_msg_color(self, color):
		self.text_color = color
		self.msg_img = self.font.render(self.msg, True, self.text_color, self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.rect.center

	def set_border_color(self, color):
		"""改变边框颜色"""
		self.border[1] = color

	def set_button_color(self, color):
		"""改变按钮颜色"""
		self.button_color = color
		self.msg_img = self.font.render(self.msg, True, self.text_color, self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.rect.center

	def set_text_color(self, color):
		"""改变文本颜色"""
		self.msg_img = self.font.render(self.msg, True, color, self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.rect.center

	def set_line_width(self, width):
		"""改变线的宽度"""
		self.line[0] = width

	def set_border_width(self, width):
		"""改变边框宽度"""
		self.border[0] = width
		
	def set_msg_tran(self, msg_tran):
		if msg_tran is True: self.msg_img.colorkeys(self.button_color)
		self.msg_tran = msg_tran

	def draw(self):
		"""绘制按钮"""
		if self.msg_tran is False: self.screen.fill(self.button_color, self.rect)
		if self.draw_line is True:
			pygame.draw.line(self.screen, self.line[1], (self.coordinates[0], self.coordinates[1]),
							 (self.coordinates[0] + self.width, self.coordinates[1] + self.height), self.line[0])
			pygame.draw.line(self.screen, self.line[1], (self.coordinates[0] + self.width, self.coordinates[1]),
							 (self.coordinates[0], self.coordinates[1] + self.height), self.line[0])
		if self.msg_tran is True: self.msg_img.set_colorkey(self.button_color)
		self.screen.blit(self.msg_img, self.msg_img_rect)
		if self.draw_border is True:
			pygame.draw.rect(self.screen, self.border[1], (self.coordinates[0], self.coordinates[1],
							self.width, self.height), self.border[0])

class CircleButton(FreeCircle):
	"""圆形按钮类, 继承自FreeCircle"""

	check_button = False
	display_button = True

	def __init__(self, screen, coordinates, radius, msg, font = 'SimHei', size = 24, width = 0, rect = (0, 0), angle = (0, 360), aa = True, draw_border = False,
				 border_width = 1, color = (0, 0, 0), border_color = (0, 0, 0), msg_color = (255, 255, 255), button_color = (0, 0, 0), msg_tran = False, dsm = 1):
		super().__init__(screen, coordinates, radius, width, rect, angle, aa,
				 draw_border, border_width, color, border_color)
		self.msg = msg
		self.dsm = dsm
		self._font = pygame.font.Font(font, size)
		self.button_color = button_color
		self.size = size
		self.msg_color = msg_color
		self.msgrect = pygame.Rect(0, 0, rect[0] * self.dsm, rect[1] * self.dsm)
		self.msgrect.centerx = self.coordinates[0] * self.dsm
		self.msgrect.centery = self.coordinates[1] * self.dsm
		self.msg_tran = msg_tran
		self.msg_img = self._font.render(self.msg, True, self.msg_color, self.button_color).convert()
		if self.msg_tran is True: self.msg_img.set_colorkey(self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.msgrect.center

	def draw(self):
		"""绘制按钮"""
		super().draw()
		if self.msg_tran is True: self.msg_img.set_colorkey(self.button_color)
		self.screen.blit(self.msg_img, self.msg_img_rect)

	def set_button_color(self, color):
		self.button_color = color
		self.color = color
		self.msg_img = self._font.render(self.msg, True, self.msg_color, self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.msgrect.center

	def set_msg_color(self, color):
		self.msg_color = color
		self.msg_img = self._font.render(self.msg, True, self.msg_color, self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.msgrect.center

	def set_msg(self, msg):
		self.msg = msg
		self.msg_img = self._font.render(self.msg, True, self.msg_color, self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.msgrect.center

	def set_msg_tran(self, msg_tran):
		if msg_tran is True: self.msg_img.colorkeys(self.button_color)
		self.msg_tran = msg_tran
		
# pygame.gfxdraw.aacircle
# pygame.draw.ellipse 2
