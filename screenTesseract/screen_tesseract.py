import numpy as np
from numpy import *
from PIL import Image
from PIL import *
from PIL import ImageGrab
import pytesseract,cv2,os,time,math

def get_region():
    im = ImageGrab.grab()
    width, height = im.size
    im = ImageGrab.grab((math.floor(width/3),math.floor(height/4),width-math.floor(width/3),height-math.floor(2*height/3)))
    width, height = im.size
    im.resize((width*2, height*2)).save("screen.png", 'PNG')

def get_string(img_path):
    img = cv2.imread(img_path)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("screen_removed_noise.png", img)
    # threshold
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    ret,img = cv2.threshold(img,180, 255,cv2.THRESH_BINARY)
    cv2.imwrite("screen_thres.png", img)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    result = pytesseract.image_to_string(Image.open("screen_thres.png"))
    return result

def main():
    get_region()
    print ("OCR Output: ")
    print (get_string("screen.png"))

main()
