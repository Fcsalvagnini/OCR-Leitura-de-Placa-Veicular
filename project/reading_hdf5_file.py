import h5py
import cv2

hdf5_file_path = "characters_dataset.hdf5"

def read_hdf5_dataset(path_to_hdf5):
    hdf5_dataset = h5py.File(path_to_hdf5, "r")
    characters_images = hdf5_dataset["characters_images"]
    characters_labels = hdf5_dataset["labels"]
    
    return hdf5_dataset, (characters_images, characters_labels)

if __name__ == "__main__":
    print("[INFO] Reading example, press 'q' to finish the example")

    dataset, (characters_images, characters_labels) = read_hdf5_dataset("characters_dataset.hdf5")

    for idx, image in enumerate(characters_images):
        cv2.imshow("Character", image)
        print("[INFO] Label => ", characters_labels[idx])
        
        key = cv2.waitKey(0) & 0xff
        if key == ord('q'):
            break

    dataset.close()
    print("[INFO] Reading example finished")