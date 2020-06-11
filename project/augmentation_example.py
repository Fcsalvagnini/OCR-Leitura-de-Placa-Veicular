import h5py
import cv2
from albumentations import Rotate

hdf5_file_path = "characters_dataset.hdf5"

def apply_image_augmentation(augmentator, image):
    augmented_image = augmentator(image = image)["image"]
    return augmented_image

if __name__ == "__main__":
    # Instancia o objeto de augmentação
    augmentator = Rotate(15, p = 0.5)

    print("[INFO] Augmentation example, press 'q' to finish the example")
    with h5py.File("characters_dataset.hdf5", "r") as hdf5_file:
        characters_images = hdf5_file["characters_images"]
        characters_labels = hdf5_file["labels"]



        for idx, image in enumerate(characters_images):
            augmented_image = apply_image_augmentation(augmentator, image)
            print(augmented_image)
            cv2.imshow("Character", image)
            cv2.imshow("Augmented character", augmented_image)
            print("[INFO] Label => ", characters_labels[idx])
            
            key = cv2.waitKey(0) & 0xff
            if key == ord('q'):
                break


    print("[INFO] Augmentation example finished")

    