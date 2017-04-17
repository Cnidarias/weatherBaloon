import logging
import threading
import serial
import time


def has_time_passed(time_pass, oldtime):
    return time.time() - oldtime >= time_pass


class SerialHandler(threading.Thread):
    def __init__(self, serial_port, serial_speed, device_name, funk_queue):

        self.serial_port = serial_port
        self.serial_speed = serial_speed

        self.wait_funk_timer = 10
        self.last_funkupdate = time.time()
        self.funk_queue = funk_queue
        self.latest_data = ""

        logging.basicConfig(filename='{}.log'.format(device_name), level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
        threading.Thread.__init__(self)

    def run(self):
        # connect to serial device
        self.retry_connection()

        # read all data and log them, add them to message queue and be happy
        while True:
            result = self.read_data()
            if has_time_passed(self.wait_funk_timer, self.last_funkupdate) and result:
                self.funk_queue.put(self.latest_data)
                self.last_funkupdate = time.time()
            if not result:
                self.ser.close()
                self.retry_connection()

    def retry_connection(self):
        while not self.connect_to_serialport():
            time.sleep(5)

    def connect_to_serialport(self):
        try:
            self.ser = serial.Serial(self.serial_port, self.serial_speed, timeout=15)
            logging.info('Connected to device {} at speed {}'.format(self.serial_port, self.serial_speed))
        except (ValueError, serial.SerialException) as e:
            logging.info('Could not connect to device: {}: {}'.format(self.serial_port, e))
            self.latest_data = "FAILURE"
            return False

        return True

    def read_data(self):
        try:
            self.latest_data = self.ser.readline()
            logging.info('DATA:{}'.format(self.latest_data))
        except (ValueError, serial.SerialException, serial.SerialTimeoutException) as e:
            logging.info('Could no read line from: {}: {}'.format(self.serial_port, e))
            self.latest_data = "FAILURE"
            return False

        return True
