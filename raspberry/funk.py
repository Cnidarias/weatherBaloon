import logging
import threading
import serial
import time


def has_time_passed(time_pass, oldtime):
    return time.time() - oldtime >= time_pass


class Funk(threading.Thread):
    def __init__(self, serial_port, serial_speed, device_name, funk_queue):

        self.serial_port = serial_port
        self.serial_speed = serial_speed

        self.funk_queue = funk_queue

        self.can_send_message = True

        logging.basicConfig(
            filename='{}.log'.format("FUNK"),
            level=logging.DEBUG,
            format='%(relativeCreated)6d %(threadName)s %(message)s'
        )

        threading.Thread.__init__(self)

    def run(self):
        # connect to serial device
        self.retry_connection()

        while True:
            # we should prolly send a package when we have one,
            # once we have a confirmation on that message we can send the next one,
            # meaning we should only get the reply once it was processed and sent
            try:
                if not self.funk_queue.empty() and self.can_send_message:
                    self.ser.write(self.funk_queue.get())
                    self.can_send_message = False
                if not self.can_send_message:
                    resp = self.ser.readline()
                    self.can_send_message = True

            except (serial.SerialException, serial.SerialTimeoutException, ValueError) as e:
                logging.info("Could not read/write line from/to: {}: {}".format("FUNK", e))
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
