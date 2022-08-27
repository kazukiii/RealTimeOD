import argparse

from yolov5 import Yolov5

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', default='webcam', help='select webcam or youtube, the default value is webcam')
parser.add_argument('-c', '--channel', type=int, default=0, help='select the camera channel that you want to use')
parser.add_argument('-a', '--arch', default='yolov5', help='select the model that you want to use, the default value is yolov5')


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)

    detector = Yolov5(args.mode, args.channel)
    detector()
