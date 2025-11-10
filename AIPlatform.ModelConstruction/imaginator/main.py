import hf_dataset
import os

# you have to install bird dataset manually
# it is available on kaggle (klu2000030172/birds-image-dataset)
# https://www.kaggle.com/datasets/klu2000030172/birds-image-dataset

dataset = hf_dataset.full_load("microsoft/cats_vs_dogs")
# 0 - cat
# 1 - dog 
# 2 - bird

if not os.path.isdir('./dataset_hf/') or not os.path.isdir("./dataset_hf/1/"):
    os.mkdir("./dataset/")
    for i in range(3):
        os.mkdir("./dataset/"+str(i)+"/")

    for i, example in enumerate(dataset["train"]):
        example["image"].save("./dataset/" + str(example["labels"]) + "/" + str(i) + ".png")

if not os.path.isdir("./dataset_hf/3/"):
    print("You have to install birds image dataset manually")
    exit()

