import cv2
import os
import numpy as np
from tqdm import tqdm
import re
import h5py

class H5pyAcess:
    def __init__(self, path_to_save, buffer_size, data_shape):
        self.db_acess = h5py.File(path_to_save, 'w')
        self.characters = self.db_acess.create_dataset("characters_images", data_shape, dtype = np.uint8)
        data_type_str = h5py.special_dtype(vlen = str)
        self.labels = self.db_acess.create_dataset("labels", (data_shape[0], ), dtype = data_type_str)

        # Cria o buffer de dados e o ponteiro para escrever no dataset
        self.buffer_size = buffer_size
        self.buffer = {"characters" : [], "labels" : []}
        self.cursor_to_write = 0

    def add_data(self, characters, labels):
        self.buffer["characters"].extend(characters)
        self.buffer["labels"].extend(labels)
        
        if len(self.buffer["characters"]) >= self.buffer_size:
            self.writes_to_disk()

    def writes_to_disk(self):
        end_cursor = self.cursor_to_write + len(self.buffer["characters"])
        self.characters[self.cursor_to_write : end_cursor] = self.buffer["characters"]
        self.labels[self.cursor_to_write : end_cursor] = self.buffer["labels"]
        
        self.cursor_to_write = end_cursor
        self.buffer = {"characters" : [], "labels" : []}

    def end_connection(self):
        if len(self.buffer["characters"]) > 0:
            self.writes_to_disk()
        self.db_acess.close()
        
def add_border(image, target_size, color, border_type = cv2.BORDER_CONSTANT):
    '''
        Retorna a imagem com borda adicionada
        Parametros:
            - image (np array): Imagem a qual será adicionada a borda
            - target_size (Tupla): Tamanho da imagem após a adição da borda
            - color (Tupla): Tupla no esquema (B, G, R) indicando a cor da borda
            - border_type (Constante cv2): Tipo da borda
        Retorna:
            - image (np array): Imagem com a borda adicionada
    '''
    height, width = image.shape[:2]
    horizontal_border = target_size[0] - width
    vertical_border = target_size[1] - height
    top_size = int(vertical_border / 2) + ( vertical_border % 2 )
    bottom_size = int(vertical_border / 2)
    left_size = int(horizontal_border / 2) + ( horizontal_border % 2 )
    right_size = int(horizontal_border / 2)
    return cv2.copyMakeBorder(image, top = top_size, bottom = bottom_size, left = left_size, right = right_size,
                                 borderType = border_type, value = color)

def segments_image_characters(img, img_name, padding):
    characters = []
    # Gera uma imagem binária para facilitar a segmentação dos caracteres
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_gray, 110, 255, cv2.THRESH_BINARY_INV)

    # Detecta a posição dos caracteres na imagem e as ordena em ordem crescente (Posição no eixo x)
    contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    bounding_boxes = np.array([list(cv2.boundingRect(contour)) for contour in contours])
    bounding_boxes = bounding_boxes[np.argsort(bounding_boxes[:, 0])] 
    
    # Extrai as rois da imagem original com o padding especificado
    for idx, bbox in enumerate(bounding_boxes):
        (xi, yi) = bbox[0] - padding, bbox[1] - padding
        (xf, yf) = xi + bbox[2] + 2*padding, yi + bbox[3] + 2*padding
        roi_character = img[yi : yf, xi : xf]
        
        roi_character = add_border(roi_character, (55, 80), (255, 255, 255))
        characters.append(roi_character)        

    # Gera as labels dos caracteres extraídos
    labels = list(img_name.split("_")[0])

    return characters, labels


def get_imgs_path(path):
    imgs = os.listdir(path)
    imgs_path = [os.path.join(path, img) for img in imgs]
    return imgs_path


def process_imgs_and_save(imgs_path, hdf5_file):
    print("[INFO] Processing images")
    number_of_examples = 0
    for img_path in tqdm(imgs_path):
        img = cv2.imread(img_path)
        img_name = img_path.split("/")[-1]
        characters, labels = segments_image_characters(img, img_name, padding = 4)
        number_of_examples += len(labels)

        hdf5_file.add_data(characters, labels)

    print("[INFO] The number of examples characters is => ", number_of_examples)


PATH = "data/trdg_output/"

if __name__ == "__main__":
    imgs_path = get_imgs_path(PATH)
    hdf5_acess = H5pyAcess("characters_dataset.hdf5", buffer_size = 1000, data_shape = (119705, 80, 55, 3))
    
    process_imgs_and_save(imgs_path, hdf5_acess)
    
    hdf5_acess.end_connection()
    print("[INFO] Characters segmented and exported to hdf5")


