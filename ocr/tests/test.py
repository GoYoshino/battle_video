from ocr.get_text import get_text
from PIL import Image
import cv2
import numpy as np

if __name__ == "__main__":
    im = cv2.imread("../../prototype/frames/11430_00_message.png")
    im2 = cv2.imread("../../prototype/frames/4830_00_message.png")
    #separator = np.zeros((24, im.shape[1], 3), dtype="uint8")
    #//cv2.putText(separator, "@", (0, 0), cv2.FONT_HERSHEY_PLAIN, 24, (255, 255, 255))

    concatted = cv2.vconcat([im, im2])
    cv2.imwrite("../../prototype/test.png", concatted)
    get_text(Image.fromarray(concatted))