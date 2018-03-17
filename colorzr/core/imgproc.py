#!/usr/bin/env python3
import os
import argparse
import numpy as np
from tempfile import NamedTemporaryFile
import subprocess
from pathlib import Path
from imageio import imwrite, imread

from contextlib import contextmanager

Image = np.ndarray

@contextmanager
def ftemp() -> Path:
    os.makedirs('/tmp/colorzr/', exist_ok=True)
    f = NamedTemporaryFile(dir='/tmp/colorzr/', suffix='.png')

    try:
        yield Path(f.name).resolve()
    finally:
        f.close()

def colorize_py_file() -> Path:
    return (Path(__file__).resolve().parent.parent.parent / 'extern' / 'colorization' / 'colorization' / 'colorize.py').resolve()

def colorize(src_img: Image) -> Image:
    """ Colorize the given black and white image. """
    ret = None # type: Image

    with ftemp() as img_in:
        with ftemp() as img_out:
            imwrite(str(img_in), src_img)

            p = subprocess.run(['python3', str(colorize_py_file()),
                '-img_in', str(img_in),
                '-img_out', str(img_out)],
                cwd=str(colorize_py_file().parent.parent),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            if p.returncode != 0:
                print(p.stdout)
                print(p.stderr)
                p.check_returncode()

            ret = imread(str(img_out))

    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Image colorizer.')
    parser.add_argument('-i', '--input_image', type=str, help='Input image.', required=True)
    parser.add_argument('-o', '--output_image', type=str, help='Output image.', required=True)

    args = parser.parse_args()

    src_img = imread(args.input_image)
    imwrite(args.output_image, colorize(src_img))
