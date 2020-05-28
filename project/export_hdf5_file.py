import cv2
import os
import numpy as np
from tqdm import tqdm

def segments_image_characters(img, img_name, padding):
    characters = []
    # Gera uma imagem binária para facilitar a segmentação dos caracteres
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_gray, 110, 255, cv2.THRESH_BINARY_INV)

    # Detecta a posição dos caracteres na imagem e as ordena em ordem crescente (No eixo x)
    contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    bounding_boxes = np.array([list(cv2.boundingRect(contour)) for contour in contours])
    bounding_boxes = bounding_boxes[np.argsort(bounding_boxes[:, 0])] 
    
    # Extrai as rois da imagem original com o padding especificado
    for idx, bbox in enumerate(bounding_boxes):
        (xi, yi) = bbox[0] - padding, bbox[1] - padding
        (xf, yf) = xi + bbox[2] + 2*padding, yi + bbox[3] + 2*padding
        roi_character = img[yi : yf, xi : xf]
        characters.append(roi_character)

    # Gera as labels dos caracteres extraídos
    labels = list(img_name.split("_")[0])

    return characters, labels


def get_imgs_path(path):
    imgs = os.listdir(path)
    imgs_path = [path + img for img in imgs]
    return imgs_path


def process_imgs(imgs_path, hdf5_file):
    print("[INFO] Processing images")
    for img_path in tqdm(imgs_path):
        img = cv2.imread(img_path)
        img_name = img_path.split("/")[-1]
        characters, labels = segments_image_characters(img, img_name, padding = 4)


if __name__ == "__main__":
    PATH = "data/trdg_output/"
    imgs_path = get_imgs_path(PATH)
    
    process_imgs(imgs_path, None)

