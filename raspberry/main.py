import time
import serial.tools.list_ports
from multiprocessing import Queue

from serial_handler import SerialHandler
from camera import CameraHandler
from funk import Funk


def main():
    send_image = False
    # funk_serial_port = '/dev/ttyABC'
    ports = list(serial.tools.list_ports.comports())

    tasks = []
    funk_queue = Queue()
    funk_image_queue = Queue()

    camera_handler = CameraHandler(0, funk_image_queue)
    camera_handler.daemon = True
    camera_handler.start()

    for p in ports:
        task = dict()
        task['task'] = SerialHandler(p.device, 9600, p.name, funk_queue, funk_image_queue)
        task['device'] = p.device
        task['device_name'] = p.name
        task['timeout'] = time.time()
        task['speed'] = 9600
        task['task'].daemon = True
        task['task'].start()

        print "Started {}".format(p.device)
        tasks.append(task)

    while True:
        # check if threads are still doing okay
        # if not check if the serial device still exists if so,
        # remake the thread and _hope_ it lives longer this time
        for t in tasks:
            if not t['task'].isAlive() and time.time() - t['timeout'] >= 5:
                device = t['device']

                # check if port is available again
                ports = list(serial.tools.list_ports.comports())
                for p in ports:
                    if device == p.device:
                        t['task'] = SerialHandler(device, 9600, t['name'], funk_queue)
                        t['task'].daemon = True
                        t['task'].start()
                        break
                # if we were not able to revive the thread,
                # set the timeout so we only check again in a couple of sec
                if not t['task'].isAlive():
                    t['timeout'] = time.time()
                    pass

if __name__ == '__main__':
    main()
