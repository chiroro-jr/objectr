# libraries
from io import BytesIO
from tempfile import NamedTemporaryFile
import cv2 as cv
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from PIL import Image
from starlette.responses import StreamingResponse

from object_detector import ObjectDetector

# create app
app = FastAPI()

# add CORS middleware
origins = [
    "http://127.0.0.1:5173/",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create the detection model
model = ObjectDetector()


# a function to filter frames that match the search query
def find_object(frames, query):
    for frame in frames:
        if query in frame[1]:
            # return from the function with the frame containing the object
            return frame

    # Object not found
    return None


@app.post("/detect")
def detect_objects(file: UploadFile = File(...), query: str | None = Form()):
    # create a temporary file to read the video from the request and pass it to OpenCV
    temp_file = NamedTemporaryFile(delete=False)
    try:
        contents = file.file.read()
        with temp_file as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Video could not be process. Please try another one.")
    finally:
        file.file.close()

    video = cv.VideoCapture(temp_file.name)

    # handle error of the capturing failed
    if not video.isOpened():
        raise HTTPException(status_code=500, detail="Video could not be process. Please try another one.")

    frames = []

    # loop over video frames
    while video.isOpened():
        # read the next frame from the video
        #  if success ok = True, frame = ndarray of pixel values in the frame
        # if fail ok = False, frame = empty ndarray
        success, frame = video.read()

        # check if frame was read correctly
        # stop processing if there are more frames
        if not success:
            break  # or break. We'll see what's best later

        # detect objects in the frame and draw bounding boxes around them
        # this will return a ndarray (of what shape).
        frame = model.detect_objects(frame)
        frames.append(frame)

    # release video from memory to prevent memory leaks
    video.release()

    # Delete the temp file to prevent clutter
    os.remove(temp_file.name)

    # find any frame with the object
    frame = find_object(frames, query)

    if frame is None:
        raise HTTPException(status_code=404, detail="Object not found")

    # Convert the frame into an image
    image = cv.cvtColor(frame[0], cv.COLOR_RGB2BGR)

    # create a PIL Image object from the ndarray
    image = Image.fromarray(image)

    # Save the image to a buffer
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    # send back the image as a stream of bytes
    return StreamingResponse(buffer, media_type="image/jpeg")
