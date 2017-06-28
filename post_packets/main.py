import requests
import time


def main():
    url = 'http://127.0.0.1:5000/data'
    with open('aprs.log', 'r') as f:
        for l in f:
            requests.post(url, json={"data": l})
            time.sleep(2)


if __name__ == '__main__':
    main()