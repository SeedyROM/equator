import math
import os

from flask import Flask, send_file, request
from io import BytesIO
from PIL import Image


app = Flask(__name__)

RENDER_TYPE = {
    'default': 'L',
    'color': 'RGB',
}

MATH_SCOPE = [
    'acos', 'asin', 'atan', 'atan2',
    'ceil', 'cos', 'cosh', 'degrees',
    'e', 'exp', 'fabs', 'floor',
    'fmod', 'frexp', 'hypot',
    'ldexp', 'log', 'log10', 'modf',
    'pi', 'pow', 'radians', 'sin', 'sinh',
    'sqrt', 'tan', 'tanh',
]

MATH_SCOPE = {k: eval(f'math.{k}') for k in MATH_SCOPE}


def return_image(_image):
    image_io = BytesIO()
    _image.save(image_io, 'JPEG')
    image_io.seek(0)
    return send_file(image_io, mimetype='image/jpeg')


@app.route('/')
def default_image_generator():
    _w = int(request.args.get('w', 128))
    _h = int(request.args.get('h', _w))
    scale = int(request.args.get('s', 0))

    image = Image.new(RENDER_TYPE['default'], (_w, _h), 0)

    eq = request.args.get('eq', 'x ^ y')
    w, h = image.size

    pixels = image.load()

    x = y = 0
    scope = {'w': w, 'h': h}
    scope.update(MATH_SCOPE)

    for x in range(w):
        for y in range(h):
            scope.update({'x': x, 'y': y, 't': x * y})
            val = eval(eq, {'__builtins__': None}, scope)
            pixels[x, y] = int(val) & 0xFF

    if scale > 0:
        image = image.resize((w * scale, h * scale), Image.NEAREST)

    return return_image(image)
