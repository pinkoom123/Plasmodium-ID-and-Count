import os
import cv2
import numpy as np

# Folder containing the images
image_folder = 'C:/Users/WONDA/Desktop/Mal_image/cell_images/Parasitized'

# Output folder for enhanced images
output_folder = 'C:/Users/WONDA/Desktop/Mal_image/cell_images/Eh_Parasitized'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate over the images in the folder
for image_file in os.listdir(image_folder):
    # Read the image
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)

    if image is not None:
        # Apply histogram equalization
        image_eq = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        image_eq[:,:,0] = cv2.equalizeHist(image_eq[:,:,0])
        image_eq = cv2.cvtColor(image_eq, cv2.COLOR_YCrCb2BGR)
        
        # Apply sharpening
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        image_sharpened = cv2.filter2D(image_eq, -1, kernel)
        
        # Save the enhanced image
        output_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_path, image_sharpened)
        
        # Display the enhanced image
        cv2.imshow('Enhanced Image', image_sharpened)
        cv2.waitKey(0)

# Destroy all windows
cv2.destroyAllWindows()