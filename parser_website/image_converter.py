import io
import base91
from PIL import Image


class ImageConverter:
    def __init__(self):
        self.items = dict()

    def addPacket(self, packet):
        packet = packet.split('_', 2)
        image_name = packet[0]
        image_index = int(packet[1])
        image_content = packet[2]
        print(image_index)
        print(image_content)
        if image_name in self.items:
            if image_content[-5:] == '__END':
                image_content = image_content[:-5]
                print("OK")
                self.items[image_name]['has_end'] = True

            self.items[image_name]['elements'][image_index] = image_content
            self.items[image_name]['parts'] += 1

            if self.items[image_name]['has_end'] and not self.items[image_name]['image_saved']:
                self.items[image_name]['image_saved'] = self.gen_image(image_name)
        else:
            n = dict()
            n['has_end'] = False
            n['elements'] = dict()
            n['elements'][image_index] = image_content
            n['image_saved'] = False
            n['parts'] = 1

            self.items[image_name] = n

            if image_content[-5:] == '__END':
                image_content = image_content[:-5]
                print("OK")
                self.items[image_name]['has_end'] = True
                n['elements'][image_index] = image_content


    def gen_image(self, imname):
        parts = self.items[imname]['parts']
        elements = self.items[imname]['elements']
        print("gen_image")
        i = 0
        while i < parts:
            if i not in elements.keys():
                return False
            i += 1

        imageBuffer = ""
        i = 0
        while i < parts:
            imageBuffer += elements[i]
            i += 1

        decodedImage = base91.decode(imageBuffer)
        ioBuffer = io.BytesIO()
        ioBuffer.write(decodedImage)
        ioBuffer.seek(0)

        img = Image.open(ioBuffer)
        img.save('static/images/{}.jpg'.format(imname))
        return True
