class FreeIcon():
	"""自定义图标类"""
	
	check_button = False
	display_button = True
	rect_pos = []
	
	def __init__(self, screen, coordinates, image_1, image_2):
		self.screen = screen
		self.coordinates = coordinates
		self.image = [image_1, image_2]
		self.image_index = 0
		
	def set_index(self, index: int):
		self.image_index = index
		
	def draw(self):
		self.screen.blit(self.image[self.image_index], self.coordinates)
