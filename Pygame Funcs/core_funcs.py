import pygame
import math


def read_f(path: str) -> str:
    f = open(path, 'r')
    dat = f.read()
    f.close()

    return dat


def write_f(path: str, dat: str) -> None:
    f = open(path, 'w')
    f.write(dat)
    f.close()


def swap_color(img: pygame.Surface, old_c: tuple[int, int, int], new_c: tuple[int, int, int]) -> pygame.Surface:
    global e_colorkey
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))

    return surf


def clip(surf: pygame.Surface, x: int, y: int, x_size: int, y_size: int) -> pygame.Surface:
    """
    It takes a surface, and returns a surface that is a copy of the original surface, but only the part
    that is within the rectangle defined by the parameters x,y,x_size,y_size
    
    Args:
      surf: The surface you want to clip.
      x: The x coordinate of the top left corner of the clipping rectangle.
      y: The y coordinate of the top left corner of the clipping rectangle.
      x_size: The width of the image
      y_size: The height of the image
    
    Returns:
      A copy of the image.
    """
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())

    return image.copy()


def rect_corners(points):
    point_1 = points[0]
    point_2 = points[1]
    out_1 = [min(point_1[0], point_2[0]), min(point_1[1], point_2[1])]
    out_2 = [max(point_1[0], point_2[0]), max(point_1[1], point_2[1])]
    
    return [out_1, out_2]


def corner_rect(points):
    points = rect_corners(points)
    r = pygame.Rect(points[0][0], points[0][1], points[1][0] - points[0][0], points[1][1] - points[0][1])

    return r


def points_between_2d(points):
    points = rect_corners(points)
    width = points[1][0] - points[0][0] + 1
    height = points[1][1] - points[0][1] + 1
    point_list = []
    for y in range(height):
        for x in range(width):
            point_list.append([points[0][0] + x, points[0][1] + y])

    return point_list


def angle_to(points):
    return math.atan2(points[1][1] - points[0][1], points[1][0] - points[0][0])
