import PIL.Image
import PIL.ImageOps


def to_bw(src_img: PIL.Image.Image) -> PIL.Image.Image:
    """ Turn the given image to black and white. """
    return src_img.convert(mode='L')


def to_color(src_img: PIL.Image.Image) -> PIL.Image.Image:
    """ Colorize the given black and white image. """
    return PIL.ImageOps.colorize(PIL.ImageOps.grayscale(src_img), "#000099", "#99CCFF")
