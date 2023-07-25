#!/usr/bin/python3
import cv2
import numpy as np
import os

directory_path = "inputframes"  
output_path = "outputframes"
target_color = [0, 0, 0]  # Replace with the RGB value of your target color to be replaced with noise

def insert_noise_to_specific_color(image_path, target_color, noise_level=50):
    image = cv2.imread(image_path)
    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Define the lower and upper bounds for the target color
    lower_bound = np.array(target_color) - np.array([0, 0, 0])
    upper_bound = np.array(target_color) + np.array([2, 2, 2])
    # Create a mask selecting the pixels within the specified color range
    mask = cv2.inRange(image_rgb, lower_bound, upper_bound)
    # Add noise to the selected color pixels
    noise = np.random.normal(0, noise_level, image.shape).astype(np.uint8)
    # Apply the noise only to the selected color pixels (if any) using the mask
    if mask.any():
        image[mask > 0] = cv2.add(image[mask > 0], noise[mask > 0])
    else:
        return image
    return image

if __name__ == "__main__":
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            print(file_path)
            img=insert_noise_to_specific_color(file_path, target_color, noise_level=5)
            cv2.imwrite(output_path+'/'+filename, img)
