import pygame
from typing import Dict, Tuple, List
import pygame


# It loads a spritesheet and allows you to get images from it
class Spritesheet:
    def __init__(self, filename: str) -> None:
        """
        It loads the image and converts it to a format that pygame can use.
        
        :param filename: The filename of the sprite sheet
        """
        self.sheet: Surface = pygame.image.load(filename).convert_alpha()
        self.sheet.set_colorkey((0, 0, 0, 0), pygame.RLEACCEL)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle: pygame.Rect, colorkey: int=None) -> pygame.Surface:
        """
        It takes a rectangle (x, y, width, height) and returns an image of that rectangle
        
        :param rectangle: The rectangle that defines the area of the sprite sheet to be cropped
        :param colorkey: If not None, this color will be transparent. If -1, the top left pixel will be
        transparent
        :return: The image at the given rectangle.
        """
        rect: Rect = pygame.Rect(rectangle)
        image: Surface = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey: Tuple[int, int, int, int] = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects: List[pygame.Rect], colorkey: int=None) -> List[pygame.Surface]:
        """
        It takes a list of rectangles and returns a list of images
        
        :param rects: A list of Rects
        :param colorkey: If not None, this color will be transparent
        :return: A list of images.
        """
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect: pygame.Rect, image_count: int, colorkey: int=None) -> List[pygame.Surface]:
        """
        It takes a sprite sheet and returns a list of images
        
        :param rect: The rectangle of the sprite sheet to load
        :param image_count: The number of images in the strip
        :param colorkey: If you want to set a color to be transparent, pass the color as a tuple, for
        example, (255, 0, 0) for red
        :return: A list of images.
        """
        tups: List[Tuple[int, int, int, int]] = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


    def load_anims(self, sizex: int, sizey: int, anim_names: List[str], frames: List[int]) -> Dict[str, List[pygame.Surface]]:
        """
        It takes a spritesheet, a size, a list of animation names, and a list of frames per animation,
        and returns a dictionary of animation names mapped to lists of frames
        
        :param size: The size of each frame in the spritesheet
        :param anim_names: A list of strings that will be the names of the animations
        :param frames: The number of frames in the animation
        :return: A dictionary of lists of images.
        """
        # 1 quadetto sono 8 pixel, una volte prende 4 quadretti in lunghezza
        # e facciamo anche 4 in altezza
        anims: dict = {}
        square: rect = pygame.Rect(0, 0, sizex, sizey)
        for anim_name, anim_frame in zip(anim_names, frames):
            anims[anim_name]: list = []
            square.y: int = frames.index(anim_frame) * sizey
            for i in range(anim_frame):
                square.x: int = i * sizex
                anims[anim_name].append(self.image_at(square, -1))

        return anims
            
            
    def convert_decimal_pixel_to_rgb(self, pixel: int) -> Tuple[int, int, int]:
        """
        Convert LONG to RGB
        
        :param pixel: The pixel value to convert
        :return: A tuple of 3 values.
        """
        '''Convert LONG to RGB'''
        B: int = pixel / 65536
        G: int = (pixel - B * 65536) / 256
        R: int = pixel - B * 65536 - G * 256
        return (R, G, B)    # B is actually a float


    def draw(self, surface: pygame.Surface, frame: pygame.Surface, pos: Tuple[int, int]) -> None:
        """
        It takes a surface, a frame, and a position, and draws the frame onto the surface at the
        position.
        
        :param surface: The surface to draw the image on
        :param frame: The frame to be drawn
        :param pos: The position of the sprite on the screen
        """
        surface.blit(frame, pos)
