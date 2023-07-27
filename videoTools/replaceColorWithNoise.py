#!/usr/bin/python3
# Replace all black pixels (or range defined) for a gaussian noise or inpainting
import cv2
import numpy as np
import os
from PIL import Image
import multiprocessing

input_path = "input_directory" 
output_path = "output_directory" 
#gaussian or inpaint
method="inpaint"
save_mask=True
color_threshold = 50


def insert_gaussian_specific_color(image_path, noise_level=50):
    image = cv2.imread(image_path)
    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Define the lower and upper bounds for the target color
    lower_bound = np.array([0,0,0]) - np.array([0, 0, 0])
    upper_bound = np.array([0,0,0]) + np.array([2, 2, 2])
    # Create a mask selecting the pixels within the specified color range
    mask = cv2.inRange(image_rgb, lower_bound, upper_bound)
    # Add noise to the selected color pixels
    noise = np.random.normal(0, noise_level, image.shape).astype(np.uint8)
    # Apply the noise only to the selected color pixels (if any) using the mask
    if mask.any():
        image[mask > 0] = cv2.add(image[mask > 0], noise[mask > 0])
    return image

def inpaint_black_pixels(image_path, filename, color_threshold,inpaint_radius=30):
    # Load the image using PIL
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img)
    # Find black pixels (pixels with RGB values close to (0, 0, 0))
    black_pixels = (img_array.sum(axis=2) <=color_threshold)
    # Create a mask with black pixels
    mask = np.zeros_like(black_pixels, dtype=np.uint8)
    mask[black_pixels] = 255
    # Inpaint the black pixels using OpenCV's inpainting function
    inpainted_image = cv2.inpaint(img_array, mask, inpaintRadius=inpaint_radius, flags=cv2.INPAINT_TELEA)
    if save_mask:
        mask_img = Image.fromarray(mask)
        mask_img.save(output_path+'/mask'+filename)
    return inpainted_image

def process_file(filename):
     file_path = os.path.join(input_path, filename)
     if os.path.exists(output_path+'/'+filename):
         print ("File {} already processed".format(filename))
     else:
         print ("Processing {}".format(filename))
         match method:
             case "gaussian":
                 img=insert_gaussian_specific_color(file_path, noise_level=5)
                 cv2.imwrite(output_path+'/'+filename, img)
             case "inpaint":
                 inpainted_image = inpaint_black_pixels(file_path,filename,color_threshold)
                 inpainted_img = Image.fromarray(inpainted_image)
                 inpainted_img.save(output_path+'/'+filename)

if __name__ == "__main__":
    files_list = os.listdir(input_path)
    files_list = [file for file in files_list if os.path.isfile(os.path.join(input_path, file))]
    with multiprocessing.Pool() as pool:
        pool.map(process_file, files_list)
