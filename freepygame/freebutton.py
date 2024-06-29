import pygame
import pygame.gfxdraw
import pygame.draw

from freepygame.freecircle import FreeCircle

def position_button(rect: tuple[int, int, int, int] | list[int, int, int, int], pos: tuple[int, int]) -> bool:
    """
    Checks if a given position is within the boundaries of a rectangle.

    Parameters:
    rect (tuple[int, int, int, int] | list[int, int, int, int]): The rectangle's boundaries. It should be a tuple or list of four integers representing the left, right, top, and bottom coordinates of the rectangle.
    pos (tuple[int, int]): The position to check. It should be a tuple of two integers representing the x and y coordinates.

    Returns:
    bool: True if the position is within the rectangle's boundaries, False otherwise.

    Example:
    >>> position_button((10, 50, 10, 50), (20, 30))
    True
    >>> position_button([10, 50, 10, 50], (60, 30))
    False
    """
    if rect[0] <= pos[0] <= rect[1] and rect[2] <= pos[1] <= rect[3]:
        return True
    return False

def position_button_class(button, pos: tuple[int, int]):
    """
    Check if a given position overlaps with the coordinates of a button object.
    Note: This function uses the bounding rectangle coordinates for CircleButton class.

    Parameters:
    button (object): The button object to check.
    pos (tuple[int, int]): The position to check. It should be a tuple of two integers representing the x and y coordinates.

    Returns:
    bool: True if the position overlaps with the button's coordinates, False otherwise.

    Example:
    >>> button = CircleButton(screen, (100, 100), 50, "Click me")
    >>> position_button_class(button, (120, 120))
    True
    >>> position_button_class(button, (200, 200))
    False
    """
    if (button.get_coordinates()[1][0] >= pos[0] >= button.get_coordinates()[0][0] and
        button.get_coordinates()[3][1] >= pos[1] >= button.get_coordinates()[0][1]):
        return True
    return False

class FreeButton():
    """
    A custom button class that allows for various customization options.
    """

    check_button = False
    display_button = True

    def __init__(self, screen, coordinates, button_size, msg, font='SimHei', size=24, border_width=1, draw_border=True, draw_line=False, msg_tran=False,
                 line_width=1, button_color=(0, 0, 0), text_color=(255, 255, 255), border_color=(0, 0, 0), line_color=(255, 255, 255), dsm=1):
        """
        Initialize the button with the given parameters.

        Parameters:
        - screen: The pygame display surface where the button will be drawn.
        - coordinates: A list of two integers representing the top-left coordinates of the button.
        - button_size: A list of two integers representing the width and height of the button.
        - msg: A string representing the text to be displayed on the button.
        - font: A string representing the font to be used for the text.
        - size: An integer representing the size of the font.
        - border_width: An integer representing the width of the border.
        - draw_border: A boolean indicating whether to draw the border.
        - draw_line: A boolean indicating whether to draw lines.
        - msg_tran: A boolean indicating whether the text is transparent.
        - line_width: An integer representing the width of the lines.
        - button_color: A tuple of three integers representing the RGB color of the button.
        - text_color: A tuple of three integers representing the RGB color of the text.
        - border_color: A tuple of three integers representing the RGB color of the border.
        - line_color: A tuple of three integers representing the RGB color of the lines.
        - dsm: An integer representing the scale factor for the button.
        """
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
        return "Custom Button Class"

    def get_attribute(self) -> dict:
        """
        Return a dictionary containing the attributes of the button.

        Returns:
        - A dictionary with the attributes of the button.
        """
        return {"screen": self.screen, "coordinates": [self.coordinates[0], self.coordinates[1]], "button_size": [self.width, self.height],
                "msg": self.msg, "font": self.font, "draw_border": self.draw_border, "draw_line": self.draw_line,
                "border_width": self.border[0], "line_width": self.line[0], "text_color": self.text_color,
                "button_color": self.button_color, "border_color": self.border[1], "line_color": self.line[1]}

    def get_coordinates(self) -> list:
        """
        Return a list of the coordinates of the button.

        Returns:
        - A list of two integers representing the top-left coordinates of the button.
        """
        return [[self.coordinates[0], self.coordinates[1]], [self.coordinates[0] + self.width, self.coordinates[1]],
                [self.coordinates[0] + self.width, self.coordinates[1] + self.height], [self.coordinates[0], self.coordinates[1] + self.height]]

    def open_line(self, draw_line: bool):
        """
        Set whether to draw lines on the button.

        Parameters:
        - draw_line: A boolean indicating whether to draw lines.
        """
        self.draw_line = draw_line

    def open_border(self, draw_border: bool):
        """
        Set whether to draw a border on the button.

        Parameters:
        - draw_border: A boolean indicating whether to draw the border.
        """
        self.draw_border = draw_border

    def set_msg(self, msg):
        """
        Set the text to be displayed on the button.

        Parameters:
        - msg: A string representing the text to be displayed.
        """
        self.msg = msg
        self.msg_img = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def set_line_color(self, color):
        """
        Set the color of the lines on the button.

        Parameters:
        - color: A tuple of three integers representing the RGB color of the lines.
        """
        self.line[1] = color

    def set_msg_color(self, color):
        """
        Set the color of the text on the button.

        Parameters:
        - color: A tuple of three integers representing the RGB color of the text.
        """
        self.text_color = color
        self.msg_img = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def set_border_color(self, color):
        """
        Set the color of the border on the button.

        Parameters:
        - color: A tuple of three integers representing the RGB color of the border.
        """
        self.border[1] = color

    def set_button_color(self, color):
        """
        Set the color of the button.

        Parameters:
        - color: A tuple of three integers representing the RGB color of the button.
        """
        self.button_color = color
        self.msg_img = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def set_text_color(self, color):
        """
        Set the color of the text on the button.

        Parameters:
        - color: A tuple of three integers representing the RGB color of the text.
        """
        self.msg_img = self.font.render(self.msg, True, color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def set_line_width(self, width):
        """
        Set the width of the lines on the button.

        Parameters:
        - width: An integer representing the width of the lines.
        """
        self.line[0] = width

    def set_border_width(self, width):
        """
        Set the width of the border on the button.

        Parameters:
        - width: An integer representing the width of the border.
        """
        self.border[0] = width

    def set_msg_tran(self, msg_tran):
        """
        Set whether the text on the button is transparent.

        Parameters:
        - msg_tran: A boolean indicating whether the text is transparent.
        """
        if msg_tran is True:
            self.msg_img.set_colorkey(self.button_color)
        self.msg_tran = msg_tran

    def draw(self):
        """
        Draw the button on the screen.
        """
        if self.msg_tran is False: self.screen.fill(self.button_color, self.rect)
        if self.draw_line is True:
            pygame.draw.line(self.screen, self.line[1], (self.coordinates[0], self.coordinates[1]),
                             (self.coordinates[0] + self.width, self.coordinates[1] + self.height), self.line[0])
            pygame.draw.line(self.screen, self.line[1], (self.coordinates[0] + self.width, self.coordinates[1]),
                             (self.coordinates[0], self.coordinates[1] + self.height), self.line[0])
        if self.msg_tran is True:
            self.msg_img.set_colorkey(self.button_color)
        self.screen.blit(self.msg_img, self.msg_img_rect)
        if self.draw_border is True:
            pygame.draw.rect(self.screen, self.border[1], (self.coordinates[0], self.coordinates[1],
                            self.width, self.height), self.border[0])

class CircleButton(FreeCircle):
    """
    CircleButton class, inherits from FreeCircle.
    This class represents a circular button with text and color properties.
    """

    check_button = False
    display_button = True

    def __init__(self, screen, coordinates, radius, msg, font='SimHei', size=24, width=0, rect=(0, 0), angle=(0, 360), aa=True, draw_border=False,
                 border_width=1, color=(0, 0, 0), border_color=(0, 0, 0), msg_color=(255, 255, 255), button_color=(0, 0, 0), msg_tran=False, dsm=1):
        """
        Initialize CircleButton instance.
        """
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
        """
        Draw the CircleButton on the screen.
        """
        super().draw()
        if self.msg_tran is True: self.msg_img.set_colorkey(self.button_color)
        self.screen.blit(self.msg_img, self.msg_img_rect)

    def set_button_color(self, color):
        """
        Set the color of the CircleButton.
        """
        self.button_color = color
        self.color = color
        self.msg_img = self._font.render(self.msg, True, self.msg_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.msgrect.center

    def set_msg_color(self, color):
        """
        Set the color of the text on the CircleButton.
        """
        self.msg_color = color
        self.msg_img = self._font.render(self.msg, True, self.msg_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.msgrect.center

    def set_msg(self, msg):
        """
        Set the text displayed on the CircleButton.
        """
        self.msg = msg
        self.msg_img = self._font.render(self.msg, True, self.msg_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.msgrect.center

    def set_msg_tran(self, msg_tran):
        """
        Set whether the text on the CircleButton is transparent.
        """
        if msg_tran is True: self.msg_img.set_colorkey(self.button_color)
        self.msg_tran = msg_tran
		
# pygame.gfxdraw.aacircle
# pygame.draw.ellipse 2
