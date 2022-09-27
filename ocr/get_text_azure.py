from io import BytesIO
import os
import time
from typing import List

import cv2
import numpy as np
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

from msrest.authentication import CognitiveServicesCredentials

from ocr.azure_read_result import AzureReadResult
from ocr.bounding_box import BoundingBox

subscription_key = os.environ["AZURE_API_KEY"]
endpoint = f"https://pokemon-battle-video.cognitiveservices.azure.com/"

def get_text_azure(im: np.ndarray, image_height: int):
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    encoded = cv2.imencode(".png", im)
    buffer = BytesIO(encoded[1].tobytes())
    read_response = computervision_client.read_in_stream(buffer, language="ja", raw=True)

    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    ocr_result: List[AzureReadResult] = []
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                #print(line.text)
                #print(line.bounding_box)
                bbox = BoundingBox(line.bounding_box[0], line.bounding_box[1], line.bounding_box[4], line.bounding_box[5])
                ocr_result.append(AzureReadResult(line.text, bbox))

    return ocr_result
