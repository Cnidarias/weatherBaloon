class data_converter:
    def __init__(self):
        date = None
        data = None
        self.gpsLat = None
        self.gpsLon = None
        self.height = None

    def addPacket(self, packet, date):
        self.date = date
        self.data = packet

        parts = self.data.split(';')
        if parts[0].startswith('{gps:'):
            gps = parts[0].split(':')[1]

            gps_parts = gps.split(',')
            print(gps_parts)
            if len(gps_parts) != 4: return
            self.height = gps_parts[0]
            self.gpsLat = gps_parts[1]
            self.gpsLon = gps_parts[2]
            print(self.height, self.gpsLat, self.gpsLon)

    def getLoc(self):
        return self.gpsLat, self.gpsLon, self.height
