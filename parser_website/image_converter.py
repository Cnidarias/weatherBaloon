import io
import base91
import os
from PIL import Image, ImageFile
import logging


class ImageConverter:
    def __init__(self, camera, logger, path):
        self.items = dict()
        self.logger = logger
        self.camera = camera
        self.path = path

    def addPacket(self, packet):
        self.logger.error("TEST")
        packet = packet.rstrip('\n')
        packet = packet.split('_', 2)
        image_name = packet[0]
        image_index = int(packet[1])
        image_content = packet[2]
        print('Name: {} Index: {} Content: {}'.format(image_name, image_index, image_content))
        if image_name in self.items:
            if image_content[-5:] == '__END':
                image_content = image_content[:-5]
                print("GOT END")
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
                print("GOT END")
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

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img = Image.open(ioBuffer)
        img.save(os.path.join(self.path, '{}_{}.jpg'.format(self.camera, imname)))
        self.logger.error('SAVED FILE')
        self.logger.error('SAVED FILE')
        return True
