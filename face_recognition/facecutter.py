# -*- coding: utf-8 -*-
"""
Spyder Editor
Requirements : pip install face_recognition Pillow
This script extracts faces recursively from images in the 
current directory and its subfolders. 
It ignores the images below given pixel size

@author: RexieSxK
"""
import os
import face_recognition
from PIL import Image

def extract_faces_from_image(image_path, margin_percentage=0.3): # decrease or increase the margin on how close you want to cut the face
    # Load the image with face_recognition
    image = face_recognition.load_image_file(image_path)

    # Find all face locations in the image
    face_locations = face_recognition.face_locations(image)

    image_height, image_width = image.shape[:2]

    # Loop over each face found in the image
    for index, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location

        # Introduce margin
        face_width = right - left
        face_height = bottom - top

        margin_x = int(face_width * margin_percentage)
        margin_y = int(face_height * margin_percentage)

        top = max(0, top - margin_y)
        right = min(image_width, right + margin_x)
        bottom = min(image_height, bottom + margin_y)
        left = max(0, left - margin_x)

        # Extract the face with margin from the original image
        face_image = Image.fromarray(image[top:bottom, left:right])
        
        # Check for minimum size in pixels
        if face_image.width < 45 or face_image.height < 45:
            continue

        # Create a new path for the detected face
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        directory = os.path.dirname(image_path)
        face_image_path = os.path.join(directory, f"{base_name}_face_{index + 1}.png")
        
        # Save the face to the specified output directory
        face_image.save(face_image_path)

    print(f"Processed {image_path}. Found {len(face_locations)} faces.")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                extract_faces_from_image(os.path.join(root, filename))

if __name__ == "__main__":
    PARENT_DIRECTORY = '.'
    process_directory(PARENT_DIRECTORY)
