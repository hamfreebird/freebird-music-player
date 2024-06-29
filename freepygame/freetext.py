import pygame
import pygame.gfxdraw
import pygame.draw

class FreeText():
    """
    Customized text class.
    """

    check_text = False
    display_text = True

    def __init__(self, screen, coordinates, msg, font = 'SimHei', size = 24, color=(0, 0, 0)):
        """
        Initialize the text.

        Parameters:
        screen (pygame.Surface): The window where the text will be displayed.
        coordinates (list): The top-left corner coordinates of the text.
        msg (str): The text content.
        font (str): The font of the text. Default is 'SimHei'.
        size (int): The size of the text. Default is 24.
        color (tuple): The color of the text. Default is (0, 0, 0).
        """
        self.screen, self.msg, self.font, self.size, self.color = screen, msg, font, size, color
        self.x, self.y = coordinates[0], coordinates[1]
        try:
            self._font = pygame.font.Font(font, size)
        except TypeError:
            self._font = font
        self.img_text = self._font.render(self.msg, True, color)

    def __str__(self):
        """
        Return a string representation of the class.

        Returns:
        str: The string representation of the class.
        """
        return """Customized text class"""
    __repr__ = __str__

    def get_attribute(self):
        """
        Get the attributes of the text object.

        Returns:
        dict: A dictionary containing the attributes of the text object.
        """
        attribute = {"screen": self.screen, "coordinates": [self.x, self.y], "msg": self.msg,
                     "font": self.font, "size": self.size, "color": self.color}
        return attribute

    def get_coordinates(self):
        """
        Get the coordinates of the text.

        Returns:
        list: The coordinates of the text.
        """
        return [self.x, self.y]

    def set_color(self, color):
        """
        Change the color of the text.

        Parameters:
        color (tuple): The new color of the text.
        """
        del self._font, self.img_text
        try:
            self._font = pygame.font.Font(self.font, self.size)
        except TypeError:
            self._font = self.font
        self.img_text = self._font.render(self.msg, True, color)

    def set_fout(self, font):
        """
        Change the font of the text.

        Parameters:
        font (str): The new font of the text.
        """
        del self._font, self.img_text
        try:
            self._font = pygame.font.Font(font, self.size)
        except TypeError:
            self._font = font
        self.img_text = self._font.render(self.msg, True, self.color)

    def set_size(self, size):
        """
        Change the size of the text.

        Parameters:
        size (int): The new size of the text.
        """
        del self._font, self.img_text
        try:
            self._font = pygame.font.Font(self.font, size)
        except TypeError:
            self._font = self.font
        self.img_text = self._font.render(self.msg, True, self.color)

    def set_msg(self, msg):
        """
        Change the content of the text.

        Parameters:
        msg (str): The new content of the text.
        """
        del self._font, self.img_text
        try:
            self._font = pygame.font.Font(self.font, self.size)
        except TypeError:
            self._font = self.font
        self.img_text = self._font.render(msg, True, self.color)

    def set_coordinates(self, coordinates):
        """
        Change the position of the text.

        Parameters:
        coordinates (list): The new coordinates of the text.
        """
        self.x, self.y = coordinates[0], coordinates[1]

    def draw(self):
        """
        Draw the text on the screen.
        """
        self.screen.blit(self.img_text, (self.x, self.y))
		
class SuperText(FreeText):
    """
    超级文本类，继承自FreeText
    """

    def __init__(self, screen, coordinates, msg, font='SimHei', size=24, color=(0, 0, 0), dsm=1):
        """
        初始化文本:
        screen -> 设置的窗口, coordinates[x,y] -> 文本左上角坐标, msg -> 文本, font -> 字体,
        size -> 文本大小, color(R,G,B) -> 文本颜色

        Parameters:
        screen (pygame.Surface): The window where the text will be displayed.
        coordinates (list): The top-left corner coordinates of the text.
        msg (str): The text content.
        font (str): The font of the text. Default is 'SimHei'.
        size (int): The size of the text. Default is 24.
        color (tuple): The color of the text. Default is (0, 0, 0).
        dsm (int): The scaling factor for the text. Default is 1.
        """
        super().__init__(screen, coordinates, msg, font, size, color)
        self.msg_len_next = -1
        self.dsm = dsm

    def draw(self):
        """
        绘制文本
        """
        self.screen.blit(self.img_text, (self.x * self.dsm, self.y * self.dsm))

    def __del__(self):
        """
        析构方法，返回文本左上角坐标

        Returns:
        dict: A dictionary containing the attributes of the text object.
        """
        return super().get_attribute()

    def __add__(self, data):
        """
        快捷改变文本内容，使用一个新的字符串(或SuperText类对象)扩展本对象的msg属性

        Parameters:
        data (str or SuperText): The new text content to be added.

        Returns:
        str: The updated text content.
        """
        if type(data) == SuperText:
            super().set_msg(self.msg + data.get_attribute().get("msg"))
        elif type(data) == str:
            super().set_msg(self.msg + data)
        else:
            super().set_msg(self.msg + str(data))
        return super().get_attribute().get("msg")

    def __lshift__(self, data: tuple):
        """
        << 快捷改变参数:
        1个元数时改变字体大小，2个元素时改变位置，3个元素时改变颜色

        Parameters:
        data (tuple): The new parameters for the text.
        """
        if len(data) == 1:
            super().set_size(data[0])
        elif len(data) == 2:
            super().set_coordinates(data)
        elif len(data) == 3:
            super().set_color(data)
        else:
            raise AssertionError("Redundant parameter -> 冗余参数")

    def __len__(self):
        """
        获取文本的字符数

        Returns:
        int: The number of characters in the text.
        """
        return len(super().get_attribute())

    def __iter__(self):
        """
        使文本类可迭代

        Returns:
        str: The text content.
        """
        self.msg_len_next = -1
        return super().get_attribute().get("msg")

    def __next__(self):
        """
        获取文本的下一个字符

        Returns:
        str: The next character in the text.

        Raises:
        StopIteration: If there are no more characters in the text.
        """
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
	
