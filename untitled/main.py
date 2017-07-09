import requests
from bs4 import BeautifulSoup
import re
import time

def main():
    patternStr = 'gps:(\d+\.\d+)\,(\d+\.\d+)\,(\d+\.\d+)\,(\d+\.\d+)\;'
    pattern = re.compile(patternStr, re.MULTILINE | re.DOTALL)
    call_sign = 'DG2PU-11'
    url = 'https://aprs.fi/?c=raw&call={}&limit=1000&view=normal'.format(call_sign)

    while True:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        tbl = soup.find('div', {'class': 'browselist_data'})
        elements = tbl.find_all('span', recursive=False)
        for c in elements:
            line = c.get_text().split(call_sign)
            packet = line[1][line[1].index(':')+1:]

            res = pattern.search(packet)

            if res is not None:
                res = res.groups()
                if float(res[0]) != 0:
                    requests.post('http://strato.cnidarias.net/set_data', data={'lat': float(res[1]), 'lon': float(res[2]), 'h': float(res[0])})
                    print(res)

        time.sleep(60)




if __name__ == '__main__':
    main()