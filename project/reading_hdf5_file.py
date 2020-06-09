import h5py
import cv2

hdf5_file_path = "characters_dataset.hdf5"

if __name__ == "__main__":
    print("[INFO] Reading example, press 'q' to finish the example")
    with h5py.File("characters_dataset.hdf5", "r") as hdf5_file:
        characters_images = hdf5_file["characters_images"]
        characters_labels = hdf5_file["labels"]

        for idx, image in enumerate(characters_images):
            cv2.imshow("Character", image)
            print("[INFO] Label => ", characters_labels[idx])
            
            key = cv2.waitKey(0) & 0xff
            if key == ord('q'):
                break

    print("[INFO] Reading example finished")