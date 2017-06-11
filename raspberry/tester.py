from __future__ import print_function
from camera import CameraHandler
import time
import io
import base91
import threading
from PIL import Image




def main(file_names):
    i = 0
    for img in file_names:
        base91_img = generate_image_base91('test_images/{}'.format(img), 20)
        packets = print_file(base91_img, i)
        with open('images.txt', 'a') as f:
            for p in packets:
                f.write(p)

        i += 1

def generate_image_base91(filename, quality):
    try:
        img = Image.open(filename, mode='r')
    except IOError as e:
        pass
    img.thumbnail((320, 240), Image.ANTIALIAS)
    img = img.convert('L')
    outputCompressed = io.BytesIO()
    img.save(outputCompressed, format='jpeg', optimize=True, quality=quality)
    dataCompressed = outputCompressed.getvalue()
    resCompressed = base91.encode(dataCompressed)
    resCompressed += "__END"
    return resCompressed

def generate_header(imageID, part):
    r = str(imageID) + "_" + str(part) + "_"
    return r, len(r)

def print_file(bytesToSend, image_id):
    i = 0
    bytescovered = 0
    packets = []

    while bytescovered < len(bytesToSend):
        head = generate_header(image_id, i)
        end = bytescovered + (255 - head[1])
        part = head[0] + bytesToSend[bytescovered:end] + "\n"
        bytescovered = end
        i += 1
        packets.append(part)
    return packets

if __name__ == '__main__':
    main(['0.jpg', '1.jpg', '2.jpg'])
