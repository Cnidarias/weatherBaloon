import serial.tools.list_ports
from multiprocessing import Queue

from serial_handler import SerialHandler
from camera import CameraHandler

def main():
    ports = list(serial.tools.list_ports.comports())

    tasks = []
    funk_queue = Queue()
    funk_image_queue = Queue()

    camera_handler = CameraHandler(0, funk_image_queue)
    camera_handler.daemon = True
    camera_handler.start()

    for p in ports:
        task = dict()
        task['task'] = SerialHandler(p.device, 115200, p.name, funk_queue)
        task['device'] = p.device
        task['device_name'] = p.name
        task['speed'] = 115200
        task['task'].daemon = True
        task['task'].start()

        tasks.append(task)

    while True:
        if not funk_queue.empty():
            print "DATA: {}".format(funk_queue.get())
        if not funk_image_queue.empty():
            print "IMG: {}".format(funk_image_queue.get())



if __name__ == '__main__':
    main()