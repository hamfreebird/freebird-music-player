def _array_mean(number_list):
    """
    Calculate the mean of a list of numbers.

    Parameters:
    number_list (list): A list of numbers.

    Returns:
    float: The mean of the numbers in the list. If the list is empty, returns 0.

    Raises:
    ZeroDivisionError: If the list is empty.
    """
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
    """
    Calculate the mean of RGBA values and convert them to integers.

    Parameters:
    rgba (list): A list of four lists, each containing the red, green, blue, and alpha values respectively.

    Returns:
    tuple: A tuple containing four integers, representing the mean red, green, blue, and alpha values respectively.

    Raises:
    ZeroDivisionError: If any of the input lists is empty.
    """
    r = int(_array_mean(rgba[0]))  # Calculate the mean red value and convert it to integer
    g = int(_array_mean(rgba[1]))  # Calculate the mean green value and convert it to integer
    b = int(_array_mean(rgba[2]))  # Calculate the mean blue value and convert it to integer
    a = int(_array_mean(rgba[3]))  # Calculate the mean alpha value and convert it to integer
    return (r, g, b, a)  # Return the mean RGBA values as a tuple

def map_to_rgba(part):
    """
    Extracts red, green, blue, and alpha values from a 2D list of pixel data.

    Parameters:
    part (list): A 2D list where each element is a list containing RGB or RGBA values.

    Returns:
    tuple: A tuple containing four lists, each representing the red, green, blue, and alpha values respectively.

    Raises:
    IndexError: If the input list is not a 2D list or if the inner lists do not contain at least 3 elements.
    """
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
    """
    Applies a blur effect to an image using a specified level of blur.

    Parameters:
    image (pygame.Surface): The input image to be blurred.
    level (int): The level of blur to be applied. Higher values result in more blur.

    Returns:
    pygame.Surface: The blurred image.

    Raises:
    IndexError: If the input image is not a 2D list or if the inner lists do not contain at least 3 elements.
    """
    _size = image.get_size()  # Get the size of the image
    _old_image_pixels = [[None for _ in range(0, _size[0])] for _ in range(0, _size[1])]  # Initialize a 2D list to store the old image pixels
    _new_image_pixels = _old_image_pixels  # Initialize a 2D list to store the new image pixels
    boundary_width = level + 1  # Calculate the boundary width for the blur effect

    # Store the old image pixels in the _old_image_pixels list
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            _old_image_pixels[x][y] = image.get_at((x, y))

    # Apply the blur effect to the image
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            ready_part = []  # Initialize a list to store the ready part of the image for blurring
            try:
                # Extract the ready part of the image for blurring
                for unit in _old_image_pixels[x - boundary_width : x + boundary_width]:
                    ready_part.append(unit[y - boundary_width : y + boundary_width])

                # Calculate the mean RGBA values of the ready part and convert them to integers
                pixels = array_mean_rgba(map_to_rgba(ready_part))
            except IndexError:
                # If an IndexError occurs, set the pixels to a default value
                pixels = (125, 125, 125, 125)

            # Store the new image pixels in the _new_image_pixels list
            _new_image_pixels[x][y] = pixels

    # Update the image with the new image pixels
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            image.set_at((x, y), _new_image_pixels[x][y])

    return image  # Return the blurred image