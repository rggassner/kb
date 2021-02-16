#!/usr/bin/python3
from scipy.spatial import distance
import numpy as np
from PIL import Image

im = Image.open('00361.jpg') # Can be many different formats.
pix = im.load()
#print (pix[1,1])  # Get the RGBA Value of the a pixel of an image
#print (sum(pix[1,1])/3)
out = Image.new('RGB', im.size, color = 'red')

def NN(A, start):
    """Nearest neighbor algorithm.
    A is an NxN array indicating distance between N locations
    start is the index of the starting location
    Returns the path and cost of the found solution
    """
    path = [start]
    cost = 0
    N = A.shape[0]
    mask = np.ones(N, dtype=bool)  # boolean values indicating which 
                                   # locations have not been visited
    mask[start] = False
    for i in range(N-1):
        last = path[-1]
        next_ind = np.argmin(A[last][mask]) # find minimum of remaining locations
        next_loc = np.arange(N)[mask][next_ind] # convert to original location
        path.append(next_loc)
        mask[next_loc] = False
        cost += A[last, next_loc]
    return path, cost

for x in range(im.height):
    A = np.zeros([im.width,im.width])
    brightest=0
    bindex=0
    for y in range(im.width):
        if sum(pix[y,x])/3 > brightest:
            bindex=y
            brightest=sum(pix[y,x])/3
        for z in range(im.width):
            A[y,z] = distance.euclidean(pix[y,x],pix[z,x])
    path, _ = NN(A, bindex)
    print('x {} y {} bindex {} color {}'.format(x,y, bindex,pix[bindex,x]))
    #print(path)
    count=0
    for y in path:
        y=int(y)
        #print("x {} count {} y {}".format(x,count,y))
        out.putpixel((count,x),pix[y,x])
        count=count+1
out.save('out.png')
