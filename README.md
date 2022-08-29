# Real-Time Object Detection
## Preparation
the version of Python is below
```bash
$ python -V
3.9.10
```
### Install poetry if not
```bash
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
reference: https://python-poetry.org/docs/
## Usage
```bash
$ poetry install # install the necessary libraries
$ poetry shell # enter the virtual environment
$ python src/main.py # run this program
```
### options
- **mode**: the resource which is webcam or youtube
- **channel**: the channel of camera that you want to use
- **arch**: the architecture that you want to use

For more details, type the command below
```bash
$ python src/main.py -h
usage: main.py [-h] [-m MODE] [-c CHANNEL] [-a ARCH]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  select webcam or youtube, the default value is webcam
  -c CHANNEL, --channel CHANNEL
                        select the camera channel that you want to use
  -a ARCH, --arch ARCH  select the model that you want to use, the default value is yolov5
```
## Demonstration
![output](https://user-images.githubusercontent.com/23211788/186126317-ef038c11-f2d5-4153-b3d9-bb55fe14d0c8.gif)
