import face_recognition
import os
import pickle

ENCODINGS_FILE = "faces.pkl"

def load(image_path, name, encodings):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)
    if encoding: 
        encodings[name] = encoding[0]
        
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump(encodings, f)

def train(directory):
    encodings = {}
    for person_name in os.listdir(directory):
        person_directory = os.path.join(directory, person_name)
        if os.path.isdir(person_directory):
            for image_name in os.listdir(person_directory):
                image_path = os.path.join(person_directory, image_name)
                if os.path.isfile(image_path):
                    load(image_path, person_name, encodings)

def load_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def recognize(image_path):
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    
    if not unknown_encoding:
        return None  
    
    unknown_encoding = unknown_encoding[0]
    encodings = load_encodings()

    for name, encoding in encodings.items():
        results = face_recognition.compare_faces([encoding], unknown_encoding)
        
        if results[0]:
            return name
    return None

if __name__ == "__main__":
    train("train")
    val_directory = "val"
    for image_name in os.listdir(val_directory):
        image_path = os.path.join(val_directory, image_name)
        if os.path.isfile(image_path):
            name = recognize(image_path)
            if name:
                print(f"Recognized {name} in {image_name}")
            else:
                print(f"Did not recognize anyone in {image_name}")
