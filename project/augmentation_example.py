import h5py
import cv2
import numpy as np
from albumentations import (Compose, Rotate, Blur, RandomBrightnessContrast, IAAPerspective, RandomScale)

def read_hdf5_dataset(path_to_hdf5):
    hdf5_dataset = h5py.File(path_to_hdf5, "r")
    characters_images = hdf5_dataset["characters_images"]
    characters_labels = hdf5_dataset["labels"]
    
    return hdf5_dataset, (characters_images, characters_labels)

def apply_image_augmentation(augmentator, image):
    augmented_image = augmentator(image = image)["image"]
    return augmented_image

def horizontal_stack_images(image_1, image_2):
    return np.hstack((image_1, image_2))

if __name__ == "__main__":
    print("[INFO] Augmentation example, press 'q' to finish the example")
    # Instancia o objeto de augmentação
    augmentator = Compose(  [Rotate(15), Blur(5), IAAPerspective(scale = (0.025, 0.05), p = 0.8),
                            RandomBrightnessContrast(brightness_limit = 0.35, contrast_limit = 0.35)], 
                            p = 0.7 )

    dataset, (characters_images, characters_labels) = read_hdf5_dataset("characters_dataset.hdf5")


    for idx, image in enumerate(characters_images):
        augmented_image = apply_image_augmentation(augmentator, image)
        cv2.imshow("Character x Augmented character", horizontal_stack_images(image, augmented_image))
        print("[INFO] Label => ", characters_labels[idx])
        
        key = cv2.waitKey(0) & 0xff
        if key == ord('q'):
            break

    dataset.close()
    print("[INFO] Augmentation example finished")

    