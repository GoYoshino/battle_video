import cv2
import numpy as np
from PIL import Image
from google.cloud import vision
import pyocr

from io import BytesIO

def get_text(screen_im: Image) -> str:
    client = vision.ImageAnnotatorClient()
    b = BytesIO()
    screen_im.save(b, format="JPEG")
    image = vision.Image(content=b.getvalue())

    response = client.text_detection(image=image)
    print(response)
    return response.full_text_annotation.text