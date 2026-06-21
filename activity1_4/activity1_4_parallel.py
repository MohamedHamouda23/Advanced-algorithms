'''
To install face_recognition, simply use 'pip install face_recognition' in a terminal
However, often you may meet an error about the 'dlib' library with cmake.
The easy solution is to visit https://github.com/z-mahmud22/Dlib_Windows_Python3.x and download the 
compiled wheels locally with the python version, and install it from local

if you want to show the found image with the known face, you need opencv and also uncomment the related code.

'''

import cv2
import time
import face_recognition
import os
from multiprocessing import Pool, Manager


def create_chunks(filenames, num_chunks=5):
    """Divide list of filenames into equal chunks for parallel processing"""
    total_files = len(filenames)
    chunk_size = total_files // num_chunks
    remainder = total_files % num_chunks
    chunks = []
    start = 0

    for i in range(num_chunks):
        # Calculate end index for this chunk
        end = start + chunk_size
        
        # Add one extra file to first 'remainder' chunks
        if i < remainder:
            end += 1
        
        # Extract this chunk using list slicing
        current_chunk = filenames[start:end]
        chunks.append(current_chunk)
        
        # Move start to next position
        start = end

    return chunks


def process_chunk_queue(filenames_chunk, output_queue):
    """Process a chunk of images and push matches to a shared queue"""
    for filename in filenames_chunk:
        result = process_image(filename)
        if result:
            output_queue.put(result)


def show_found_image(unknown_image):
    """Display image with rectangles drawn around detected faces"""
    # Find all face locations in the image
    face_locations = face_recognition.face_locations(unknown_image)

    # Draw rectangles around faces
    for top, right, bottom, left in face_locations:
        cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the image
    cv2.imshow("Found Image", cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Load the known face image and get the features of the face
known_image = face_recognition.load_image_file("known_man.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Get list of all files in the image folder
folder_path = "imageset/"
filenames = [file.name for file in os.scandir(folder_path) if file.is_file()]


def process_image(filename):
    """Check if an image contains the known face"""
    
    # Load the unknown face image
    unknown_image = face_recognition.load_image_file(folder_path+filename)
    
    # Find faces and encodings in the unknown image
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    
    # Compare each face found in the image
    for unknown_encoding in unknown_encodings:
        # Compare the unknown face encoding with the known encoding
        matches = face_recognition.compare_faces([known_encoding], unknown_encoding)
        
        if matches[0]:  
            return filename  # Return filename if match found
    
    return None  # No match found


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    start_parallel = time.time()
    
    manager = Manager()
    output_queue = manager.Queue()
    
    # Use number of CPU cores as number of chunks
    num_chunks = os.cpu_count()
    filename_chunks = create_chunks(filenames, num_chunks)
    
    with Pool(processes=num_chunks) as pool:
        for chunk in filename_chunks:
            pool.apply_async(process_chunk_queue, args=(chunk, output_queue))
        pool.close()
        pool.join()
    
    # Collect matches from queue
    matches = []
    while not output_queue.empty():
        matches.append(output_queue.get())
    
    end_parallel = time.time()
    print("Parallel processing time:", end_parallel - start_parallel)
    
    # Now show the matched images (outside timing)
    for match in matches:
        print("Match found! in " + match)
        matched_image = face_recognition.load_image_file(folder_path + match)
        show_found_image(matched_image)