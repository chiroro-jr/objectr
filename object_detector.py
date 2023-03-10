import os
import cv2 as cv
import numpy as np


class ObjectDetector:
    def __init__(self):
        PROJECT_PATH = os.path.abspath(os.getcwd())
        MODELS_PATH = os.path.join(PROJECT_PATH, "models")

        self.MODEL = cv.dnn.readNet(
            os.path.join(MODELS_PATH, "yolov4-tiny.weights"),
            os.path.join(MODELS_PATH, "yolov4-tiny.cfg")
        )

        self.CLASSES = []
        with open(os.path.join(MODELS_PATH, "coco.names"), "r") as f:
            self.CLASSES = [line.strip() for line in f.readlines()]

        self.OUTPUT_LAYERS = [
            self.MODEL.getLayerNames()[i - 1] for i in self.MODEL.getUnconnectedOutLayers()
        ]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.COLORS /= (np.sum(self.COLORS ** 2, axis=1) ** 0.5 / 255)[np.newaxis].T

    def detect_objects(self, frame, query="person"):
        height, width, channels = frame.shape
        blob = cv.dnn.blobFromImage(
            frame, 1 / 255, (416, 416), swapRB=True, crop=False
        )

        self.MODEL.setInput(blob)
        outs = self.MODEL.forward(self.OUTPUT_LAYERS)

        class_ids = []
        confidences = []
        boxes = []
        objects = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # * Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # * Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    objects.append({"class_id": class_id, "confidence": float(confidence)})

        # Draw boxes around objects in each frame
        # labels of objects in the frame
        labels = []
        indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]

                label = str(self.CLASSES[class_ids[i]])
                labels.append(label)

                color = self.COLORS[i]
                cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv.putText(frame, label, (x, y - 5), font, 2, color, 2)
        return frame, labels
