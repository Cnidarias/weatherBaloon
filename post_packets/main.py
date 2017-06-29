import requests
import time


def main():
    url = 'http://strato.cnidarias.net/data'
    # url = 'http://127.0.0.1:5000/data'
    with open('aprs.log', 'r') as f:
        for l in f:
            requests.post(url, json={"data": l})
            print(l)
            time.sleep(1)


if __name__ == '__main__':
    main()