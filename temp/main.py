import face_recognition
import cv2
import os

# Function to load and encode all faces from a given folder
def load_and_encode_faces(folder_path):
    known_face_encodings = []
    known_face_names = []

    # Loop through each image file in the folder
    for file_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, file_name)

        # Load the image and convert it from BGR (OpenCV format) to RGB
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Find all the faces in the image and encode them
        face_encodings = face_recognition.face_encodings(rgb_image)

        # Assume each image contains only one face for simplicity
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(file_name)  # Use the file name as the person's name

    return known_face_encodings, known_face_names

# Function to recognize the face from a user input image
def recognize_face_from_input(input_image_path, known_face_encodings, known_face_names):
    # Load the input image and convert it from BGR to RGB
    input_image = cv2.imread(input_image_path)
    rgb_input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    # Find the face encodings in the input image
    input_face_encodings = face_recognition.face_encodings(rgb_input_image)

    if input_face_encodings:
        input_face_encoding = input_face_encodings[0]

        # Compare the input face encoding to the known encodings
        results = face_recognition.compare_faces(known_face_encodings, input_face_encoding)

        # Check if there is a match
        if True in results:
            match_index = results.index(True)
            return f"Match found: {known_face_names[match_index]}"
        else:
            return "No match found."
    else:
        return "No face found in the input image."

# Main execution
if __name__ == "__main__":
    # Path to the folder containing known faces
    folder_path = "images"

    # Load and encode known faces
    known_face_encodings, known_face_names = load_and_encode_faces(folder_path)

    # Path to the user input image
    input_image_path = "photo.jpg"

    # Recognize the face
    result = recognize_face_from_input(input_image_path, known_face_encodings, known_face_names)
    print(result)
