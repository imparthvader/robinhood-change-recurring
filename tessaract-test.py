import time
from PIL import ImageGrab  # screenshot
from PIL import Image

import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = (r"tesseract-ocr\tesseract.exe"
                                         )  # needed for Windows as OS

screen = ImageGrab.grab()  # screenshot
cap = screen.convert('L')  # make grayscale

data = pytesseract.image_to_boxes(cap, output_type=Output.DICT)

# print(data)
cap.save("tess-screencap/x.png")