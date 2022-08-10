from time import time

import cv2
import numpy as np
import pafy
import torch


class Yolov5:
    def __init__(self, mode) -> None:
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
        self.mode = mode

    def get_video_stream(self):
        if self.mode != "webcam":
            URL = "https://www.youtube.com/watch?v=HL8Er3cP2b4"  # URL to parse
            play = pafy.new(URL).streams[-1]  #'-1' means read the lowest quality of video.
            assert play is not None  # we want to make sure their is a input to read.
            stream = cv2.VideoCapture(play.url)  # create a opencv video stream.
        else:
            stream = cv2.VideoCapture(0)

        return stream

    """
    The function below identifies the device which is availabe to make the prediction and uses it to load and infer the frame. Once it has results it will extract the labels and cordinates(Along with scores) for each object detected in the frame.
    """

    def score_frame(self, frame):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(device)
        frame = [np.array(frame)]
        results = self.model(frame)
        labels = results.xyxyn[0][:, -1].numpy()
        cord = results.xyxyn[0][:, :-1].numpy()
        return labels, cord

    """
    The function below takes the results and the frame as input and plots boxes over all the objects which have a score higer than our threshold.
    """

    def plot_boxes(self, results, frame):
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            # If score is less than 0.2 we avoid making a prediction.
            if row[4] < 0.2:
                continue
            x1 = int(row[0] * x_shape)
            y1 = int(row[1] * y_shape)
            x2 = int(row[2] * x_shape)
            y2 = int(row[3] * y_shape)
            bgr = (0, 255, 0)  # color of the box
            classes = self.model.names  # Get the name of label index
            label_font = cv2.FONT_HERSHEY_SIMPLEX  # Font for the label.
            cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)  # Plot the boxes
            cv2.putText(frame, classes[int(labels[i])], (x1, y1), label_font, 0.9, bgr, 2)  # Put a label over box.
        return frame

    """
    The Function below oracestrates the entire operation and performs the real-time parsing for video stream.
    """

    def __call__(self):
        player = self.get_video_stream()  # Get your video stream.
        assert player.isOpened()  # Make sure that their is a stream.
        # Below code creates a new video writer object to write our
        # output stream.
        x_shape = int(player.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(player.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")  # Using MJPEG codex
        out_file = "result.mov"
        out = cv2.VideoWriter(out_file, four_cc, 20, (x_shape, y_shape))
        ret, frame = player.read()  # Read the first frame.
        while ret:  # Run until stream is out of frames
            start_time = time()  # We would like to measure the FPS.
            results = self.score_frame(frame)  # Score the Frame
            frame = self.plot_boxes(results, frame)  # Plot the boxes.
            end_time = time()
            fps = 1 / np.round(end_time - start_time, 3)  # Measure the FPS.
            print(f"Frames Per Second : {fps}")
            if self.mode != "webcam":
                out.write(frame)  # Write the frame onto the output.
            else:
                cv2.imshow("camera", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            ret, frame = player.read()  # Read next frame.

        player.release()
        cv2.destroyAllWindows()
