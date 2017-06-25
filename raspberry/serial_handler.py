import threading
import serial
import time
import logger
from datetime import datetime


def metersToFeet(meters):
    return float(meters) / 0.3048


def gpsdecimalToDMS(gps, dir_char):
    gps = float(gps)
    # 50.3569
    # 7.5890
    d = int(gps)
    m = int((gps * 60.0) % 60)
    s = int((abs(gps) * 3600 % 60) * 1.0/60.0 * 100.0)
    if dir_char == 'N':
        return "{0:02}{1:02}.{2:02}{3}".format(d, m, s, dir_char)
    else:
        return "{0:02}{1:03}.{2:02}{3}".format(d, m, s, dir_char)


def getAPRSGPSString(gpsparts):
    parts = gpsparts.split(",")
    if len(parts) == 4:
        # 0 = altitude
        # 1 = lat
        # 2 = long
        # 3 = num of sats
        lat = gpsdecimalToDMS(parts[1], 'N')
        lon = gpsdecimalToDMS(parts[2], 'E')
        time = datetime.utcnow().strftime("%H%M%S")
        return "/{0}h{1}/{2}O/A={3:.2f}\n".format(time, lat, lon, metersToFeet(parts[0]))


def has_time_passed(time_pass, oldtime):
    return time.time() - oldtime >= time_pass


class SerialHandler(threading.Thread):
    def __init__(self, serial_port, serial_speed, device_name, funk_queue, image_queue):

        self.ser = None
        self.serial_port = serial_port
        self.serial_speed = serial_speed

        self.wait_funk_timer = 60
        self.last_funkupdate = time.time()
        self.funk_queue = funk_queue
        self.funk_image_queue = image_queue
        self.latest_data = ""

        self.type = "SENSOR"

        self.can_send_message = False

        self.logger = logger.make_logger(device_name)

        threading.Thread.__init__(self)

    def run(self):
        # connect to serial device
        self.retry_connection()

        # read all data and log them, add them to message queue and be happy
        while True:
            if self.type == "SENSOR":
                self.sensor_board()
            else:
                self.funk_board()

    def sensor_board(self):
        result = self.read_data()
        if has_time_passed(self.wait_funk_timer, self.last_funkupdate) and result:
            if self.latest_data.startswith("gps"):
                coords = self.latest_data[3:self.latest_data.index(";")]
                if int(coords[1]) != 0:
                    self.funk_queue.put(getAPRSGPSString(coords))
            self.funk_queue.put("{{{0}\n".format(self.latest_data))
            self.last_funkupdate = time.time()
        if not result:
            self.ser.close()
            self.retry_connection()

    def funk_board(self):
        try:
            if not self.funk_queue.empty() and self.can_send_message:
                msg = self.funk_queue.get()
                print msg
                self.ser.write(msg)
                self.can_send_message = False
            elif not self.funk_image_queue.empty() and self.can_send_message:
                msg = self.funk_image_queue.get()
                print msg
                self.ser.write(msg)
                self.can_send_message = False
            if not self.can_send_message:
                resp = self.ser.readline()
                while resp == '':
                    resp = self.ser.readline()
                if resp.startswith("FUNK"):
                    print "FUNK READY"
                    self.can_send_message = True

        except (serial.SerialException, serial.SerialTimeoutException, ValueError) as e:
            self.logger.info("Could not read/write line from/to: {}: {}".format("FUNK", e))
            self.ser.close()
            self.retry_connection()

    def retry_connection(self):
        while not self.connect_to_serialport():
            time.sleep(5)

        line = self.ser.readline()
        while line == '':
            line =self.ser.readline()
        if line.startswith("FUNK"):
            self.type = "FUNK"
            self.can_send_message = True
            self.logger.info("FUNK")
        else:
            self.type = "SENSOR"
            self.logger.info("SENSOR")

    def connect_to_serialport(self):
        try:
            self.ser = serial.Serial(self.serial_port, self.serial_speed, timeout=15)
            self.logger.info('Connected to device {} at speed {}'.format(self.serial_port, self.serial_speed))
        except (ValueError, serial.SerialException) as e:
            self.logger.info('Could not connect to device: {}: {}'.format(self.serial_port, e))
            self.latest_data = "FAILURE"
            return False

        return True

    def read_data(self):
        try:
            self.latest_data = self.ser.readline()
            self.logger.info('DATA:{}'.format(self.latest_data))
        except (ValueError, serial.SerialException, serial.SerialTimeoutException) as e:
            self.logger.info('Could no read line from: {}: {}'.format(self.serial_port, e))
            self.latest_data = "FAILURE"
            return False
        return True
