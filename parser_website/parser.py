from bs4 import BeautifulSoup
import requests
import threading
import datetime
import time
from image_converter import ImageConverter
from gps_converter import GpsConverter
from data_converter import data_converter


class AprsFiParser(threading.Thread):
    def __init__(self, website, queue, logger, path):
        threading.Thread.__init__(self)
        self.last_date = None
        self.path = path
        self.logger = logger
        self.queue = queue
        self.last_packet = ''
        self.call_sign = 'DG2PU-11'
        self.url = 'https://aprs.fi/?c=raw&call={}&limit=1000&view=normal'.format(self.call_sign)

        self.image_converter = ImageConverter(0, self.logger, self.path)
        self.image_converter1 = ImageConverter(1, self.logger, self.path)
        self.gps_covnerter = GpsConverter()
        self.website = website
        self.data_converter = data_converter()

    def get_gps(self):
        return self.data_converter.getLoc()
    def set_gps(self, lat, lon, h):
        self.data_converter.setPos(lat, lon, h)

    def run(self):
        while True:
            if self.website:
                res = requests.get(self.url)
                soup = BeautifulSoup(res.content, 'html.parser')

                tbl = soup.find('div', {'class': 'browselist_data'})
                elements = tbl.find_all('span', recursive=False)
                max_date = self.last_date
                for c in elements:
                    line = c.get_text().split(self.call_sign)
                    d = datetime.datetime.strptime(line[0][:-2], "%Y-%m-%d %H:%M:%S %Z")
                    if max_date is None or max_date < d:
                        max_date = d

                    if self.last_date is None or d > self.last_date:
                        packet = line[1][line[1].index(':')+1:]
                        if packet[0] == '{':
                            self.data_converter.addPacket(packet, max_date)
                            pass
                        elif packet[0] == '/':
                            self.gps_covnerter.addPacket(packet)
                        else:
                            if packet[0] == '0':
                                self.image_converter.addPacket(packet[2:])
                            else:
                                self.image_converter1.addPacket(packet[2:])
                            print(packet)

                self.last_date = max_date
                print(self.last_date)
                time.sleep(60)
            else:
                if not self.queue.empty():
                    self.logger.warn("QUEUE")
                    line = self.queue.get().split(self.call_sign)
                    if len(line) > 1:
                        packet = line[1][line[1].index(':')+1:]
                        if packet[0] == '{':
                            # self.data_converter.addPacket(packet)
                            pass
                        elif packet[0] == '/':
                            self.gps_covnerter.addPacket(packet)
                        else:
                            if packet[0] == '0':
                                self.image_converter.addPacket(packet[2:])
                            else:
                                self.image_converter1.addPacket(packet[2:])

if __name__ == '__main__':
    r = AprsFiParser(True)
    r.daemon = True
    r.start()
    while True:
        pass
