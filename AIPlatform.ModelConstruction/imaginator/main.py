import hf_dataset
import os

# --- PREPARE DATASET ---

CATS_DOGS_DATASET_PATH = "./cats_dogs_dataset/"
BIRDS_DATASET_PATH = "./birds_dataset/"
FINAL_DATASET_PATH = "./dataset/"

CATS_DOGS_DATASET_IMAGE_LABEL = "image"
BIRDS_DATASET_IMAGE_LABEL = "jpg"

# 0 - cat
# 1 - dog 
# 2 - bird

cats_dogs_dataset = hf_dataset.full_load("microsoft/cats_vs_dogs", CATS_DOGS_DATASET_PATH, CATS_DOGS_DATASET_IMAGE_LABEL)
birds_dataset = hf_dataset.full_load("birder-project/CUB_200_2011", BIRDS_DATASET_PATH, BIRDS_DATASET_IMAGE_LABEL)

if not os.path.isdir(FINAL_DATASET_PATH) or not os.path.isdir(FINAL_DATASET_PATH+"1/"):
    os.mkdir(FINAL_DATASET_PATH)
    for i in range(3):
        os.mkdir(f"{FINAL_DATASET_PATH}{str(i)}/")

    # save both dogs and cats images
    for i, example in enumerate(cats_dogs_dataset["train"]):
        example[CATS_DOGS_DATASET_IMAGE_LABEL].save("./dataset/" + str(example["labels"]) + "/" + str(i) + ".png")

    # save bird images
    for i, example in enumerate(birds_dataset["train"]):
        example[BIRDS_DATASET_IMAGE_LABEL].save("./dataset/2/" + str(i) + ".jpg")