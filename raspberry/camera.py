import time
import io
import base91
from SimpleCV import Camera
import threading
from PIL import Image


class CameraHandler(threading.Thread):
    def __init__(self, cam_id, image_queue):
        threading.Thread.__init__(self)

        self.cam = Camera(cam_id)
        time.sleep(0.1)

        self.last_update = time.time()
        self.wait_time = 60
        self.image_counter = 0

        self.last_image_funk_name = time.time()
        self.image_funk_wait = 60
        self.funk_image_id = 0
        self.image_queue = image_queue

    def run(self):
        while True:
            if time.time() - self.last_update >= self.wait_time:
                self.image_counter += 1
                img = self.cam.getImage()
                img.save("images/IMG{}.png".format(self.image_counter))
                print "Saved Image"
                self.last_update = time.time()

            if time.time() - self.last_image_funk_name >= self.image_funk_wait:
                base91_img = self.generate_image_base91("images/IMG{}.png".format(self.image_counter), 20)
                packets = self.print_file(base91_img, self.funk_image_id)
                for p in packets:
                    print p
                    self.image_queue.put(p)
                self.last_image_funk_name = time.time()

    def generate_image_base91(self, filename, quality):
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

    def generate_header(self, imageID, part):
        r = str(imageID) + "_" + str(part) + "_"
        return r, len(r)

    def print_file(self, bytesToSend, image_id):
        i = 0
        bytescovered = 0
        packets = []

        while bytescovered < len(bytesToSend):
            head = self.generate_header(image_id, i)
            end = bytescovered + (255 - head[1])
            part = head[0] + bytesToSend[bytescovered:end] + "\n"
            bytescovered = end
            i += 1
            packets.append(part)
        return packets
