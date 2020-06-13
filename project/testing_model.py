from tensorflow.keras.models import load_model
import json
import cv2
import numpy as np
import string

# WARNING: Image for service opencv_python was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.

NUMBERS = [str(i) for i in range(10)]
LETTERS = list(string.ascii_uppercase)

def get_letter(idx):
    return LETTERS[idx]

def get_number(idx):
    return NUMBERS[idx]

def draw_characters(image, characters, positions):
    for character, position in zip(characters, positions):
        cv2.rectangle(image, position[0], position[1], color = (0, 69, 255), thickness = 2)
        x_text, y_text = position[0]
        y_text -= 10
        cv2.putText(image, character, (x_text, y_text), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1.5, color = (0, 69, 255), thickness = 3)

if __name__ == "__main__":
    number_classifier = load_model("models/numbers_model.h5")
    letter_classifier = load_model("models/letters_model.h5")

    with open("characters_position.json") as json_file:
        data = json.load(json_file)
    
    images = data.keys()
    
    for image in images:
        image_data = cv2.imread(data[image]['path'])
        
        letters = []
        letters_position = []
        for letter_position in data[image]["letters"]:
            xi, yi, xf, yf = data[image]["letters"][letter_position]
            letters_position.append([(xi, yi), (xf, yf)])
            character_segmented = image_data[yi : yf, xi : xf]
            character_segmented = cv2.resize(character_segmented, (55, 80), cv2.INTER_AREA)
            letters.append(character_segmented)
        letters = np.stack(letters, axis = 0)
        letters_recognized = letter_classifier.predict(letters)
        letters_recognized = letters_recognized.argmax(axis = 1)
        letters_recognized = list(map(get_letter, letters_recognized))
        draw_characters(image_data, letters_recognized, letters_position)
     
        numbers = []
        numbers_position = []
        for letter_position in data[image]["numbers"]:
            xi, yi, xf, yf = data[image]["numbers"][letter_position]
            numbers_position.append([(xi, yi), (xf, yf)])
            character_segmented = image_data[yi : yf, xi : xf]
            character_segmented = cv2.resize(character_segmented, (55, 80), cv2.INTER_AREA)
            numbers.append(character_segmented)
        numbers = np.stack(numbers, axis = 0)
        numbers_recognized = number_classifier.predict(numbers)
        numbers_recognized = numbers_recognized.argmax(axis = 1)
        numbers_recognized = list(map(get_number, numbers_recognized))
        draw_characters(image_data, numbers_recognized, numbers_position)


        cv2.imshow("Output", image_data)
        key = cv2.waitKey(0) & 0xFF