#!/usr/bin/python3
from scipy.spatial import distance
import numpy as np
from PIL import Image

im = Image.open('00361.jpg') # Can be many different formats.
pix = im.load()
#print (pix[1,1])  # Get the RGBA Value of the a pixel of an image
#print (sum(pix[1,1])/3)
out = Image.new('RGB', im.size, color = 'red')
for x in range(im.height):
    line=[]
    count=0
    for y in range(im.width):
        line.append(pix[y,x])
    line.sort()
    for pixel in line:
        out.putpixel((count,x),pixel)
        count=count+1
out.save('out.png')
