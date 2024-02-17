def _array_mean(number_list):
    number_list_len = len(number_list) - 1
    number_list_array_mean = 0
    for number in range(0, number_list_len):
        number_list_array_mean += number_list[number]
    try:
        number_list_array_mean /= (number_list_len + 1)
    except ZeroDivisionError:
        number_list_array_mean = 0
    return number_list_array_mean

def array_mean_rgba(rgba):
    r = int(_array_mean(rgba[0]))
    g = int(_array_mean(rgba[1]))
    b = int(_array_mean(rgba[2]))
    a = int(_array_mean(rgba[3]))
    return (r, g, b, a)

def map_to_rgba(part):
    r, g, b, a = [], [], [], []
    for x in range(0, len(part) - 1):
        for y in range(0, len(part) - 1):
            r.append(part[x][y][0])
            g.append(part[x][y][1])
            b.append(part[x][y][2])
            if len(part[x][y]) == 4:
                a.append(part[x][y][3])
    return r, g, b, a

def image_blur_processing(image, level):
    _size = image.get_size()
    _old_image_pixels = [[None for _ in range(0, _size[0])] for _ in range(0, _size[1])]
    _new_image_pixels = _old_image_pixels
    boundary_width = level + 1
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            _old_image_pixels[x][y] = image.get_at((x, y))
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            ready_part = []
            try:
                for unit in _old_image_pixels[x - boundary_width : x + boundary_width]:
                    ready_part.append(unit[y - boundary_width : y + boundary_width])
                pixels = array_mean_rgba(map_to_rgba(ready_part))
            except IndexError:
                pixels = (125, 125, 125, 125)
            _new_image_pixels[x][y] = pixels
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            image.set_at((x, y), _new_image_pixels[x][y])
    return image