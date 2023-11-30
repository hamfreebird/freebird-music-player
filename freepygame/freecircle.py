import pygame
import pygame.gfxdraw
import pygame.draw

def _degree_to_radians(_degree):
	return _degree * float(6.283185307179586 / 360)

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
