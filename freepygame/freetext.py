import pygame
import pygame.gfxdraw
import pygame.draw

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
		try:
			self._font = pygame.font.Font(font, size)
		except TypeError:
			self._font = font
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
		del self._font, self.img_text
		try:
			self._font = pygame.font.Font(self.font, self.size)
		except TypeError:
			self._font = self.font
		self.img_text = self._font.render(self.msg, True, color)

	def set_fout(self, font):
		"""改变文本字体"""
		del self._font, self.img_text
		try:
			self._font = pygame.font.Font(font, self.size)
		except TypeError:
			self._font = font
		self.img_text = self._font.render(self.msg, True, self.color)

	def set_size(self, size):
		"""改变文本大小"""
		del self._font, self.img_text
		try:
			self._font = pygame.font.Font(self.font, size)
		except TypeError:
			self._font = self.font
		self.img_text = self._font.render(self.msg, True, self.color)

	def set_msg(self, msg):
		"""改变文本内容"""
		del self._font, self.img_text
		try:
			self._font = pygame.font.Font(self.font, self.size)
		except TypeError:
			self._font = self.font
		self.img_text = self._font.render(msg, True, self.color)

	def set_coordinates(self, coordinates):
		"""改变文本位置"""
		self.x, self.y = coordinates[0], coordinates[1]

	def draw(self):
		"""绘制文本"""
		self.screen.blit(self.img_text, (self.x, self.y))
		
class SuperText(FreeText):
	"""超级文本类，继承自FreeText"""

	def __init__(self, screen, coordinates, msg, font = 'SimHei', size = 24, color = (0, 0, 0), dsm = 1):
		"""初始化文本:
		screen -> 设置的窗口, coordinates[x,y] -> 文本左上角坐标, msg -> 文本, font -> 字体,
		size -> 文本大小, color(R,G,B) -> 文本颜色"""
		super().__init__(screen, coordinates, msg, font, size, color)
		self.msg_len_next = -1
		self.dsm = dsm
		
	def draw(self):
		"""绘制文本"""
		self.screen.blit(self.img_text, (self.x * self.dsm, self.y * self.dsm))

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
		
class MidSuperText(SuperText):
	def __init__(self, screen, coordinates, rect, msg, font = 'SimHei', size = 24, color = (0, 0, 0), dsm = 1):
		super().__init__(screen, coordinates, msg, font, size, color, dsm)
		self.rect = pygame.Rect(0, 0, rect[0] * self.dsm, rect[1] * self.dsm)
		self.rect.centerx = (self.x + rect[0] / 2)
		self.rect.centery = (self.y + rect[1] / 2)
		self.img_text = self._font.render(self.msg, True, self.color, (0, 0, 0)).convert()
		self.img_text_rect = self.img_text.get_rect()
		self.img_text_rect.center = self.rect.center
		
	def draw(self):
		"""绘制文本"""
		self.screen.blit(self.img_text, self.img_text_rect)
		
class FreeMsg():
	def __init__(self, screen, coordinates, rect, msg, font, size, color, highlight, dsm):
		self.screen = screen
		self.coordinates = coordinates
		self.rect = rect
		self.msg = msg
		self.font = font
		self.size = size
		self.color = color
		self.highlight = highlight
		self.dsm = dsm
		self._font = pygame.font.Font(font, 20)
		self.img_text = self._font.render(self.msg, True, color)
		self.write = False
		self.text = ""
		self.rect_pos = [self.coordinates, (self.coordinates[0] + self.rect[0], self.coordinates[1]),
		                 (), (self.coordinates[0] + self.rect[0], self.coordinates[1] + self.rect[1])]
		
	def get_coordinates(self):
		return self.rect_pos
		
	def write_start(self):
		self.write = True
		
	def write(self, text):
		self.msg = self.msg + text
		self.img_text = self._font.render(self.msg, True, self.color)
		
	def write_end(self):
		self.write = False
		
	def write_type(self):
		return self.write
		
	def check(self, text):
		if self.write is True:
			return False
		else:
			if self.msg == text:
				return True
			else:
				return False
			
	def delete(self):
		if self.write is not True:
			self.text = ""
			self.img_text = self._font.render("", True, self.color)
			return True
		else:
			return False
		
	def draw(self):
		self.screen.blit(self.img_text, (self.coordinates[0], self.coordinates[1]))
		if self.write is True:
			pygame.draw.rect(self.screen, self.highlight, (self.coordinates[0], self.coordinates[1],
			                                               self.rect[0], self.rect[1]))
	
