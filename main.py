import time
from crawler import Crawler


def main():
    while True:
        try:
            crawler = Crawler()
            crawler.start()
            time.sleep(120)
        except KeyboardInterrupt:
            print('Operation cancelled by the user')
        except Exception as e:
            print(f' general exception: {str(e)}')


if __name__ == '__main__':
    main()
