import hf_dataset
import os
import random
from torchvision import datasets, transforms
import torch.nn as nn
import torch.optim as optimizers
import torch
import devices
import shutil

# --- PREPARE DATASET ---
CATS_DOGS_DATASET_PATH = "./cats_dogs_dataset/"
BIRDS_DATASET_PATH = "./birds_dataset/"
FINAL_DATASET_PATH = "./dataset/"

CATS_DOGS_DATASET_IMAGE_LABEL = "image"
BIRDS_DATASET_IMAGE_LABEL = "jpg"

# 0 - cat
# 1 - dog 
# 2 - bird

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

    shutil.rmtree(CATS_DOGS_DATASET_PATH)
    shutil.rmtree(BIRDS_DATASET_PATH)

    # --- CONFIG --- 
if __name__ == '__main__':

    manualSeed = 44
    print("Random Seed: ", manualSeed)
    random.seed(manualSeed)
    torch.manual_seed(manualSeed)
    
    device = devices.get_current()
        
    # --- MODEL & TRAINING --- 

    import model 
    from torch.utils.data import DataLoader
    import time

    EPOCHES = 100
    BATCH_SIZE = 256

    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
    ])

    dataset = datasets.ImageFolder(root="dataset", transform=transform)

    num_workers = min(8, os.cpu_count())

    dataloader = DataLoader(dataset,
                            BATCH_SIZE, 
                            shuffle=True,
                            num_workers=num_workers, 
                            pin_memory=True,        
                            persistent_workers=True)

    imaginator = model.Imaginator()
    imaginator.to(device)

    optimizer = optimizers.Adam(imaginator.parameters(), lr=1e-4)
    loss = nn.CrossEntropyLoss()

    for epoch in range(EPOCHES): 

        total_num = 0
        running_loss = 0.0
        start_time = time.time()

        for i, (inputs, labels) in enumerate(dataloader, 0):
            inputs = inputs.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            optimizer.zero_grad()

            outputs = imaginator(inputs)
            loss_v = loss(outputs, labels)
            loss_v.backward()
            optimizer.step()

            running_loss += loss_v.item()
            total_num += 1

        print("--------------")
        print("EPOCH: ", epoch+1)
        print(f'LOSS: {running_loss / total_num:.3f}')

        end_time = time.time()
        elapsed_time = end_time - start_time

        print("ELAPSED TIME: ", elapsed_time)

    print('Finished Training')
    torch.save(imaginator, "./imaginator.pth")