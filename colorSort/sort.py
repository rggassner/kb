from scipy.spatial import distance
from PIL import Image

im = Image.open('00361.jpg') # Can be many different formats.
pix = im.load()
#print im.size  # Get the width and hight of the image for iterating over
print pix[1,1]  # Get the RGBA Value of the a pixel of an image
#pix[x,y] = value  # Set the RGBA Value of the image (tuple)
#im.save('alive_parrot.png')  # Save the modified pixels as .png


# Distance matrix
#A = np.zeros([colours_length,colours_length])
#for x in range(0, colours_length-1):
#    for y in range(0, colours_length-1):
#    A[x,y] = distance.euclidean(colours[x],colours[y])
 
# Nearest neighbour algorithm
#path, _ = NN(A, 0)
 
# Final array
#colours_nn = []
#for i in path:
#    colours_nn.append( colours[i] )
