"""freebird的pygame自定义模块"""

import pygame
import pygame.gfxdraw
import pygame.draw

__all__ = ["FreeButton", "FreeText", "SuperText", "NaSuperText", "FreeAllCircle",
		   "FreeCircle", "SuperCircle", "CircleButton", "position_button", "FreeAARectangle", "Point"]

def _degree_to_radians(_degree):
	return _degree * float(6.283185307179586 / 360)

def position_button(button, pos: tuple[int, int]) -> bool:
	"""判断给定的坐标是否和按钮对象的坐标重合。
	注意，本函数对圆型按钮（CircleButton）类的坐标使用的是外切矩形的坐标！"""
	if (button.get_coordinates()[1][0] >= pos[0] >= button.get_coordinates()[0][0] and
		button.get_coordinates()[3][1] >= pos[1] >= button.get_coordinates()[0][1]):
		return True
	return False

class Point():
	
	def __init__(self, screen, coordinates, r, color = (0, 0, 0)):
		self.screen = screen
		self.coordinates = coordinates
		self.r = r
		self.color = color
		
	def move(self, coordinates):
		self.coordinates = coordinates
		
	def draw(self):
		pygame.draw.circle(self.screen, self.color, self.coordinates, self.r)

class FreeAARectangle():

	def __init__(self, screen, coordinates, size, color = (0, 0, 0)):
		self.screen = screen
		self.coordinates = coordinates
		self.size = size
		self.color = color

	def get_attribute(self):
		return {"screen": self.screen, "coordinates": self.coordinates, "size": self.size, "color": self.color}

	def det_coordinates(self):
		return [[self.coordinates[0], self.coordinates[1]], [self.coordinates[0] + self.size[0], self.coordinates[1]],
				[self.coordinates[0] + self.size[0], self.coordinates[1] + self.size[1]], [self.coordinates[0], self.coordinates[1] + self.size[1]]]

	def get_center_coordinates(self):
		return [self.coordinates[0] + int(self.size[0] / 2), self.coordinates[1] + int(self.size[1] / 2)]

	def set_coordinates(self, coordinates):
		self.coordinates = coordinates

	def set_size(self, size):
		self.size = size

	def set_color(self, color):
		self.color = color

	def draw(self):
		pygame.gfxdraw.rectangle(self.screen, (self.coordinates[0], self.coordinates[1], self.size[0], self.size[1]), self.color)

class FreeAllCircle():
	"""自定义圆类: 静态方法"""

	@staticmethod
	def draw_circle(screen, coordinates, radius, width = 1, color = (0, 0, 0)):
		"""画一个普通圆:
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius -> 半径, width -> 边宽度, color(R,G,B) -> 颜色"""
		pygame.draw.circle(screen, color, coordinates, radius, width)

	@staticmethod
	def draw_aacircle(screen, coordinates, radius, color = (0, 0, 0)):
		"""画一个抗锯齿空心圆:
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius -> 半径, color(R,G,B) -> 颜色"""
		pygame.gfxdraw.aacircle(screen, coordinates[0], coordinates[1], radius, color)

	@staticmethod
	def draw_saacircle(screen, coordinates, radius, color = (0, 0, 0)):
		"""画一个实心圆:
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius -> 半径, color(R,G,B) -> 颜色"""
		pygame.gfxdraw.filled_circle(screen, coordinates[0], coordinates[1], radius, color)

	@staticmethod
	def draw_advanced_circle(screen, coordinates, radius, width = 1, rect = (0, 0), angle = (0, 360), color = (0, 0, 0)):
		"""画一个高级空心圆(或弧):
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius -> 半径, width -> 边宽度, rect[rx, ry] = 长半轴和短半轴,
		angle[start, stop] -> 起始范围(度), color(R,G,B) -> 颜色"""
		if rect == (0, 0): _rect = (coordinates[0] - radius, coordinates[1] - radius, radius * 2, radius * 2)
		else: _rect = (coordinates[0] - rect[0], coordinates[1] - rect[1], rect[0] * 2, rect[1] * 2)
		_angle = [_degree_to_radians(angle[0]), _degree_to_radians(angle[1])]
		pygame.draw.arc(screen, color, _rect, _angle[0], _angle[1], width)

	@staticmethod
	def draw_advanced_aacircle(screen, coordinates, radius, angle = (0, 359), color = (0, 0, 0)):
		"""画一个高级抗锯齿空心圆(或弧):
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius -> 半径, angle[start, stop] -> 起始范围(度), color(R,G,B) -> 颜色"""
		pygame.gfxdraw.arc(screen, coordinates[0], coordinates[1], radius, angle[0], angle[1], color)

	@staticmethod
	def draw_advanced_aaellipse(screen, coordinates, radius, color = (0, 0, 0)):
		"""画一个高级抗锯齿空心椭圆:
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius[rx, ry] -> 长半轴和短半轴, color(R,G,B) -> 颜色"""
		pygame.gfxdraw.aaellipse(screen, coordinates[0], coordinates[1], radius[0], radius[1], color)

	@staticmethod
	def draw_bezier(surface, points, steps, color = (0, 0, 0)):
		pygame.gfxdraw.bezier(surface, points, steps, color)

class FreeText():
	"""自定义文本类"""

	check_text = False
	display_text = True

	def __init__(self, screen, coordinates, msg, font = 'SimHei', size = 24, color=(0, 0, 0)):
		"""初始化文本:
		screen -> 设置的窗口, coordinates[x,y] -> 文本左上角坐标, msg -> 文本, font -> 字体,
		size -> 文本大小, color(R,G,B) -> 文本颜色"""
		self.screen, self.msg, self.font, self.size, self.color = screen, msg, font, size, color
		self.x, self.y = coordinates[0], coordinates[1]
		self._font = pygame.font.SysFont(font, size)
		self.img_text = self._font.render(self.msg, True, color)

	def __str__(self):
		return """自定义文本类"""
	__repr__ = __str__

	def get_attribute(self):
		"""获取文本对象的信息"""
		attribute = {"screen": self.screen, "coordinates": [self.x, self.y], "msg": self.msg,
					 "font": self.font, "size": self.size, "color": self.color}
		return attribute

	def get_coordinates(self):
		"""获取坐标信息"""
		return [self.x, self.y]

	def set_color(self, color):
		"""改变文本颜色"""
		self.img_text = self._font.render(self.msg, True, color)

	def set_fout(self, font):
		"""改变文本字体"""
		self._font = pygame.font.SysFont(font, self.size)
		self.img_text = self._font.render(self.msg, True, self.color)

	def set_size(self, size):
		"""改变文本大小"""
		self._font = pygame.font.SysFont(self.font, size)
		self.img_text = self._font.render(self.msg, True, self.color)

	def set_msg(self, msg):
		"""改变文本内容"""
		self._font = pygame.font.SysFont(self.font, self.size)
		self.img_text = self._font.render(msg, True, self.color)

	def set_coordinates(self, coordinates):
		"""改变文本位置"""
		self.x, self.y = coordinates[0], coordinates[1]

	def draw(self):
		"""绘制文本"""
		self.screen.blit(self.img_text, (self.x, self.y))

class FreeButton():
	"""自定义按钮类"""

	check_button = False
	display_button = True

	def __init__(self, screen, coordinates, button_size, msg, font = 'SimHei', size = 24, border_width = 1, draw_border = True, draw_line = False, msg_tran = False,
				 line_width = 1, button_color = (0, 0, 0), text_color = (255, 255, 255), border_color = (0, 0, 0), line_color = (255, 255, 255)):
		"""初始化按钮:
		screen -> 设置的窗口, coordinates[x,y] -> 按钮左上角坐标, button_size[x,y] -> 按钮大小, msg -> 文本, font -> 字体, size -> 文本大小, msg_tran -> 透明
		border_width -> 边框宽度, draw_border -> 显示边框, draw_line -> 显示线, line_width -> 线宽度, button_color(R,G,B) -> 按钮背景色,
		text_color(R,G,B) -> 文本颜色(前景色), border_color(R,G,B) -> 边框颜色, line_color(R,G,B) -> 线颜色"""
		self.msg = msg
		self.screen = screen
		self.width = button_size[0]
		self.height = button_size[1]
		self.coordinates = coordinates
		self.button_color = button_color
		self.text_color = text_color
		self.draw_line = draw_line
		self.draw_border = draw_border
		self.border = [border_width, border_color]
		self.line = [line_width, line_color]
		self.msg_tran = msg_tran
		self.font = pygame.font.SysFont(font, size)
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.centerx = self.coordinates[0] + self.width / 2
		self.rect.centery = self.coordinates[1] + self.height / 2
		self.msg_img = self.font.render(self.msg, True, self.text_color, self.button_color)
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

class FreeCircle():
	"""自定义圆，弧，曲线类"""

	check_circle = False
	display_circle = True

	def __init__(self, screen, coordinates, radius, width = 1, rect = (0, 0), angle = (0, 360), aa = True,
				 draw_border = False, border_width = 1, color = (0, 0, 0), border_color = (0, 0, 0)):
		"""画一个圆(或弧):
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius -> 半径, width -> 边宽度, rect[rx, ry] = 长半轴和短半轴,
		angle[start, stop] -> 起始范围(度), aa -> 是否开启抗锯齿, draw_border -> 是否绘制边框, border_width -> 边框宽度，
		color(R,G,B) -> 颜色， border_color(R,B,G) -> 边框颜色"""
		self.screen = screen
		self.coordinates = coordinates
		self.radius = radius
		self.width = width
		self.rect = rect
		self.angle = angle
		self.aa = aa
		self.draw_border = draw_border
		self.border_width = border_width
		self.color = color
		self.border_color = border_color
		self._border_angle = [0, 360]

	def __str__(self):
		return """自定义圆，弧，曲线类"""
	__repr__ = __str__

	def get_attribute(self):
		"""获取对象属性"""
		return {"screen": self.screen, "coordinates": self.coordinates, "radius": self.radius, "width": self.width,
				"rect": self.rect, "angle": self.angle, "aa": self.aa, "draw_border": self.draw_border,
				"border_width": self.border_width, "color": self.color, "border_color": self.border_color}

	def get_center_coordinates(self):
		"""获取圆的中心坐标"""
		return self.coordinates

	def get_coordinates(self):
		"""获取圆的矩形范围坐标"""
		if self.rect == (0, 0):
			return [[self.coordinates[0] - self.radius, self.coordinates[1] - self.radius],
					[self.coordinates[0] + self.radius, self.coordinates[1] - self.radius],
					[self.coordinates[0] + self.radius, self.coordinates[1] + self.radius],
					[self.coordinates[0] - self.radius, self.coordinates[1] + self.radius]]

	def set_coordinates(self, coordinates):
		"""改变中心坐标"""
		self.coordinates = coordinates

	def set_radius(self, radius):
		"""改变半径"""
		self.radius = radius

	def set_width(self, width):
		"""改变宽度"""
		self.width = width

	def set_rect(self, rect):
		"""改变长短半轴"""
		self.rect = rect

	def set_angle(self, angle):
		"""改变弧的起始位置"""
		self.angle = angle

	def set_aa(self, aa):
		"""是否开启抗锯齿"""
		self.aa = aa

	def open_border(self, draw_border: bool):
		"""是否开启边框"""
		self.draw_border = draw_border

	def set_border_width(self, border_width):
		"""改变边框宽度"""
		self.border_width = border_width

	def set_color(self, color):
		"""改变圆的颜色"""
		self.color = color

	def set_border_color(self, border_color):
		"""改变边框颜色"""
		self.border_color = border_color

	def _open_border_angle(self, _border_angle: tuple[int, int]):
		"""开启弧边缘边框: _border_angle -> 边框的起点与终点"""
		self._border_angle = _border_angle

	def draw(self):
		"""绘制图形"""
		try:
			if self.aa is True and self.angle != (0, 360) and self.width != 0 and self.rect == (0, 0):
				self.angle -= 1
				pygame.gfxdraw.arc(self.screen, self.coordinates[0], self.coordinates[1], self.radius,
								   self.angle[0], self.angle[1], self.color)
			elif self.aa is True and self.angle == (0, 360) and self.width != 0 and self.rect == (0, 0):
				pygame.gfxdraw.aacircle(self.screen, self.coordinates[0], self.coordinates[1], self.radius, self.color)
			elif self.aa is True and self.angle != (0, 360) and self.width != 0 and self.rect != (0, 0):
				pygame.gfxdraw.aaellipse(self.screen, self.coordinates[0], self.coordinates[1],
										 self.radius[0], self.radius[1], self.color)
			elif self.aa is True and self.angle == (0, 360) and self.width == 0 and self.rect == (0, 0):
				pygame.gfxdraw.filled_circle(self.screen, self.coordinates[0], self.coordinates[1], self.radius, self.color)
			elif self.aa is False and self.angle == (0, 360) and self.rect == (0, 0):
				pygame.draw.circle(self.screen, self.color, self.coordinates, self.radius, self.width)
			elif self.aa is False and self.angle == (0, 360):
				if self.rect == (0, 0):
					_rect = (self.coordinates[0] - self.radius, self.coordinates[1] - self.radius, self.radius * 2, self.radius * 2)
				else:
					_rect = (self.coordinates[0] - self.rect[0], self.coordinates[1] - self.rect[1], self.rect[0] * 2, self.rect[1] * 2)
				pygame.draw.ellipse(self.screen, self.color, _rect, self.width)
			elif self.aa is False and self.width != 0:
				if self.rect == (0, 0):
					_rect = (self.coordinates[0] - self.radius, self.coordinates[1] - self.radius, self.radius * 2, self.radius * 2)
				else:
					_rect = (self.coordinates[0] - self.rect[0], self.coordinates[1] - self.rect[1], self.rect[0] * 2, self.rect[1] * 2)
				_angle = [_degree_to_radians(self.angle[0]), _degree_to_radians(self.angle[1])]
				pygame.draw.arc(self.screen, self.color, _rect, _angle[0], _angle[1], self.width)
			else:
				raise AssertionError("Unable to draw graphics with the parameters given -> 无法用给定的参数绘制图形")
			if self.draw_border is True and self.border_width != 0 and self._border_angle != [0, 360]:
				if self.rect == (0, 0):
					_rect = (self.coordinates[0] - self.radius, self.coordinates[1] - self.radius, self.radius * 2, self.radius * 2)
				else:
					_rect = (self.coordinates[0] - self.rect[0], self.coordinates[1] - self.rect[1], self.rect[0] * 2, self.rect[1] * 2)
				_angle = [_degree_to_radians(self._border_angle[0]), _degree_to_radians(self._border_angle[1])]
				pygame.draw.arc(self.screen, self.border_color, _rect, _angle[0], _angle[1], self.border_width)
			elif self.draw_border is True and self.border_width != 0:
				if self.rect == (0, 0):
					_rect = (self.coordinates[0] - self.radius, self.coordinates[1] - self.radius, self.radius * 2, self.radius * 2)
				else:
					_rect = (self.coordinates[0] - self.rect[0], self.coordinates[1] - self.rect[1], self.rect[0] * 2, self.rect[1] * 2)
				pygame.draw.ellipse(self.screen, self.border_color, _rect, self.border_width)
		except:
			raise AssertionError("Unable to draw graphics with the parameters given -> 无法用给定的参数绘制图形")

	def draw_bezier(self, surface, points, steps, color = (0, 0, 0)):
		"""绘制贝塞尔曲线"""
		if color != self.color:
			pygame.gfxdraw.bezier(surface, points, steps, color)
		else:
			pygame.gfxdraw.bezier(surface, points, steps, self.color)

class SuperCircle(FreeCircle, FreeAllCircle):
	"""超级圆类， 继承自FreeAllCircle, FreeCircle"""

	__mro__ = ("FreeCircle", "FreeAllCircle")

	def __init__(self, screen, coordinates, radius, width = 1, rect = (0, 0), angle = (0, 360), aa = True,
				 draw_border = False, border_width = 1, color = (0, 0, 0), border_color = (0, 0, 0)):
		"""画一个圆(或弧):
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius -> 半径, width -> 边宽度, rect[rx, ry] = 长半轴和短半轴,
		angle[start, stop] -> 起始范围(度), aa -> 是否开启抗锯齿, draw_border -> 是否绘制边框, border_width -> 边框宽度，
		color(R,G,B) -> 颜色， border_color(R,B,G) -> 边框颜色"""
		super().__init__(screen, coordinates, radius, width, rect, angle, aa, draw_border, border_width, color, border_color)

	def __lshift__(self, data: tuple):
		"""<< 快捷改变参数:
		1个元数时改变半径，2个元素时改变长短半轴，3个元素时改变颜色"""
		if len(data) == 1:
			super().set_radius(data[0])
		elif len(data) == 2:
			super().set_rect(data)
		elif len(data) == 3:
			super().set_color(data)
		else:
			raise AssertionError("Redundant parameter -> 冗余参数")

	def open_border_angle(self, angle: tuple[int, int]):
		"""开启弧边缘边框: angle -> 边框的起点与终点"""
		super()._open_border_angle(angle)

	@staticmethod
	def draw_scircle(screen, coordinates, radius, width = 1, color = (0, 0, 0)):
		"""画一个普通圆:
		screen -> 设置的窗口, coordinates[x,y] -> 坐标, radius -> 半径, width -> 边宽度, color(R,G,B) -> 颜色"""
		FreeAllCircle.draw_circle(screen, coordinates, radius, width, color)

class SuperText(FreeText):
	"""超级文本类，继承自FreeText"""

	def __init__(self, screen, coordinates, msg, font = 'SimHei', size = 24, color = (0, 0, 0)):
		"""初始化文本:
		screen -> 设置的窗口, coordinates[x,y] -> 文本左上角坐标, msg -> 文本, font -> 字体,
		size -> 文本大小, color(R,G,B) -> 文本颜色"""
		super().__init__(screen, coordinates, msg, font, size, color)
		self.msg_len_next = -1

	def __del__(self):
		"""析构方法，返回文本左上角坐标"""
		return super().get_attribute()

	def __add__(self, data):
		"""快捷改变文本内容，使用一个新的字符串(或SuperText类对象)扩展本对象的msg属性"""
		if type(data) == SuperText:
			super().set_msg(self.msg + data.get_attribute().get("msg"))
		elif type(data) == str:
			super().set_msg(self.msg + data)
		else:
			super().set_msg(self.msg + str(data))
		return super().get_attribute().get("msg")

	def __lshift__(self, data: tuple):
		"""<< 快捷改变参数:
		1个元数时改变字体大小，2个元素时改变位置，3个元素时改变颜色"""
		if len(data) == 1:
			super().set_size(data[0])
		elif len(data) == 2:
			super().set_coordinates(data)
		elif len(data) == 3:
			super().set_color(data)
		else:
			raise AssertionError("Redundant parameter -> 冗余参数")

	def __len__(self):
		return len(super().get_attribute())

	def __iter__(self):
		self.msg_len_next = -1
		return super().get_attribute().get("msg")

	def __next__(self):
		self.msg_len_next += 1
		if self.msg_len_next >= len(super().get_attribute().get("msg")):
			raise StopIteration
		return super().get_attribute().get("msg")[self.msg_len_next]

class NaSuperText(SuperText):
	def __init__(self, screen, coordinates, rect, msg, font = 'SimHei', size = 24, color = (0, 0, 0)):
		"""初始化文本:
		screen -> 设置的窗口, coordinates[x,y] -> 文本左上角坐标, msg -> 文本, rect -> 限定范围, font -> 字体,
		size -> 文本大小, color(R,G,B) -> 文本颜色"""
		super().__init__(screen, coordinates, msg, font, size, color)
		self.rect = pygame.Rect(0, 0, rect[0], rect[1])
		self.rect.centerx = self.x + rect[0] / 2
		self.rect.centery = self.y + rect[1] / 2
		self.msg_img = self._font.render(self.msg, True, self.color, None)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.rect.center

	def draw(self):
		"""绘制文本"""
		self.screen.blit(self.msg_img, self.msg_img_rect)

class CircleButton(FreeCircle):
	"""圆形按钮类, 继承自FreeCircle"""

	check_button = False
	display_button = True

	def __init__(self, screen, coordinates, radius, msg, font = 'SimHei', size = 24, width = 0, rect = (0, 0), angle = (0, 360), aa = True, draw_border = False,
				 border_width = 1, color = (0, 0, 0), border_color = (0, 0, 0), msg_color = (255, 255, 255), button_color = (0, 0, 0), msg_tran = False):
		super().__init__(screen, coordinates, radius, width, rect, angle, aa,
				 draw_border, border_width, color, border_color)
		self.msg = msg
		self._font = pygame.font.SysFont(font, size)
		self.button_color = button_color
		self.size = size
		self.msg_color = msg_color
		self.msgrect = pygame.Rect(0, 0, rect[0], rect[1])
		self.msgrect.centerx = self.coordinates[0]
		self.msgrect.centery = self.coordinates[1]
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


if __name__ == '__main__':
	print("freebird的pygame自定义模块\n", __all__)
