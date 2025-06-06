import face_recognition
import os
import pickle
import shutil

ENCODINGS_FILE = "faces.pkl"

def save_image_to_train_dir(user_email: str, imagePath: str):
    """
    Cria a pasta /face/train/{user-email}/ se não existir e copia a imagem para lá.
    """

    source_dir = "imagens"
    train_dir = "face/train"
    print("========================================================")
    print(imagePath)
    # Caminho de origem da imagem
    source_image_path = os.path.join(source_dir, imagePath)
    # Caminho de destino
    user_train_dir = os.path.join(train_dir, user_email)
    os.makedirs(user_train_dir, exist_ok=True)
    dest_image_path = os.path.join(user_train_dir, imagePath)
    # Copia a imagem apenas se ainda não existir no diretório de treino
    if not os.path.isfile(dest_image_path):
        shutil.copy2(source_image_path, dest_image_path)
    return dest_image_path



def load(imagePath, name, encodings):
    image = face_recognition.load_image_file(imagePath)
    encoding = face_recognition.face_encodings(image)
    if encoding: 
        encodings[name] = encoding[0]
        
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump(encodings, f)

def train(directory):
    print("=================TRAIN IN MAIN.PY=======================================")
    
    encodings = {}
    for person_name in os.listdir(directory):
        person_directory = os.path.join(directory, person_name)
        print(person_directory)
        if os.path.isdir(person_directory):
            for image_name in os.listdir(person_directory):
                imagePath = os.path.join(person_directory, image_name)
                if os.path.isfile(imagePath):
                    load(imagePath, person_name, encodings)

def load_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def recognize(imagePath):
    unknown_image = face_recognition.load_image_file(imagePath)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    print("=================RECOGNIZE IN MAIN.PY=======================================")
    print(imagePath)
    print(unknown_image)
    if not unknown_encoding:
        return None  
    print("Unknown encoding found:", unknown_encoding)
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
        imagePath = os.path.join(val_directory, image_name)
        if os.path.isfile(imagePath):
            name = recognize(imagePath)
            if name:
                print(f"Recognized {name} in {image_name}")
            else:
                print(f"Did not recognize anyone in {image_name}")
