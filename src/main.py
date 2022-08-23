import argparse

from yolov5 import Yolov5

parser = argparse.ArgumentParser()
parser.add_argument('--mode', '-m', default='webcam')
parser.add_argument('--channel', '-c', default=0)


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

    detector = Yolov5(args.mode, args.channel)
    detector()
