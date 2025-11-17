import hf_dataset
import os
import random
import torch

# --- CONFIG --- 

manualSeed = 44
print("Random Seed: ", manualSeed)
random.seed(manualSeed)
torch.manual_seed(manualSeed)

# --- PREPARE DATASET ---

CATS_DOGS_DATASET_PATH = "./cats_dogs_dataset/"
BIRDS_DATASET_PATH = "./birds_dataset/"
FINAL_DATASET_PATH = "./dataset/"

CATS_DOGS_DATASET_IMAGE_LABEL = "image"
BIRDS_DATASET_IMAGE_LABEL = "jpg"

# 0 - cat
# 1 - dog 
# 2 - bird

dataset = []

if not os.path.isdir(FINAL_DATASET_PATH) or not os.path.isdir(FINAL_DATASET_PATH+"1/"):
    cats_dogs_dataset = hf_dataset.full_load("microsoft/cats_vs_dogs", CATS_DOGS_DATASET_PATH, CATS_DOGS_DATASET_IMAGE_LABEL)
    birds_dataset = hf_dataset.full_load("birder-project/CUB_200_2011", BIRDS_DATASET_PATH, BIRDS_DATASET_IMAGE_LABEL)

    os.mkdir(FINAL_DATASET_PATH)
    for i in range(3):
        os.mkdir(f"{FINAL_DATASET_PATH}{str(i)}/")

    # save both dogs and cats images
    for i, example in enumerate(cats_dogs_dataset["train"]):
        example[CATS_DOGS_DATASET_IMAGE_LABEL].save("./dataset/" + str(example["labels"]) + "/" + str(i) + ".png")

    # save bird images
    for i, example in enumerate(birds_dataset["train"]):
        example[BIRDS_DATASET_IMAGE_LABEL].save("./dataset/2/" + str(i) + ".jpg")


# --- MODEL & TRAINING --- 
import model 
from torch.utils.data import DataLoader

EPOCHES = 10
BATCH_SIZE = 32

dataloader = DataLoader(dataset, BATCH_SIZE, shuffle=True)

imaginator = model.Imaginator()

for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(dataloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
            running_loss = 0.0

print('Finished Training')