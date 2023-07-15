import os
import cv2
import numpy as np
import time

# Set the desired timeframe (in seconds)
timeframe = 60

# Load images from a folder
image_folder = 'C:/Users/WONDA/Desktop/Mal_image/cell_images/Parasitized'
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]

# Start time
start_time = time.time()

# Initialize the Plasmodium counts
plasmodium_counts = {
    'Plasmodium falciparum': 0,
    'Plasmodium ovale': 0,
    'Plasmodium vivax': 0,
    'Plasmodium malariae': 0,
    'Plasmodium knowlesi': 0
}

# Total parasite count
total_parasite_count = 0

# Process each image
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        print(f"Failed to load image: {image_file}")
        continue
    else:
        print(f"Image loaded successfully: {image_file}")

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# The trophozites stage is represented by minimum diameter
# The Merozoites stage is represented by minimum length
# The Schizont stage is represented by minimum area

    # Define criteria for each Plasmodium species based on literature or research
    criteria = {
        'Plasmodium falciparum': {
            'lower_color': (0, 0, 0),  # black
            'upper_color': (10, 255, 255),  # dark
            'min_diameter': 1.5, # Trophozites
            'min_length': 0.7, #  Merozoites
            'min_area': 5.0  # Schizont
        },
        'Plasmodium ovale': {
            'lower_color': (15, 0, 0),  # light brown
            'upper_color': (30, 255, 255),  # dark brown
            'min_diameter': 2.0, # Trophozoites
            'min_length': 2.0, #  Merozoites
            'min_area': 6.0   # Schizont
        },
        'Plasmodium vivax': {
            'lower_color': (30, 0, 0),  # light orange
            'upper_color': (50, 255, 255),  # dark orange
            'min_diameter': 3.0, # Trophozoites
            'min_length': 1.5, #  Merozoites
            'min_area': 9.0   # Schizont
        },
        'Plasmodium malariae': {
            'lower_color': (70, 0, 0),  # light pink
            'upper_color': (90, 255, 255),  # dark pink
            'min_diameter': 3.0, # Trophozoites
            'min_length': 2.5, #  Merozoites
            'min_area': 6.5   # Schizont
        },
        'Plasmodium knowlesi': {
            'lower_color': (100, 0, 0),  # light purple
            'upper_color': (130, 255, 255),  # dark purple
            'min_diameter': 10.0, # Trophozites
            'min_length': 1.0, #  Merozoites
            'min_area': 40   # Schizont
        }
    }

    # Process each Plasmodium species
    for species, params in criteria.items():
        lower_color = params['lower_color']
        upper_color = params['upper_color']
        min_diameter = params['min_diameter']
        min_length = params['min_length']
        min_area = params['min_area']

        # Create a mask using the color ranges
        mask = cv2.inRange(image, lower_color, upper_color)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            diameter = np.sqrt(area)
            length = len(contour)

            if diameter >= min_diameter and length >= min_length and area >= min_area and cv2.countNonZero(mask) > 0:
                plasmodium_counts[species] += 1
                total_parasite_count += 1

# Calculate the elapsed time
elapsed_time = time.time() - start_time

# Print the results
print("Plasmodium Counts:")
for species, count in plasmodium_counts.items():
    print(f"{species}: {count}")

print(f"Total Parasite Count: {total_parasite_count}")
print(f"Elapsed Time: {elapsed_time} seconds")