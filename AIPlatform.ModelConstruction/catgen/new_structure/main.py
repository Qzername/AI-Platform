import torch
import random
import os

# local
import hf_dataset
import devices
import models
import train
import sound_notification

# --- config --- 
manualSeed = 44
print("Random Seed: ", manualSeed)
random.seed(manualSeed)
torch.manual_seed(manualSeed)
#torch.use_deterministic_algorithms(True) 

# --- get device ---
device = devices.get_current()
1
# --- dataset config --- 
def first_run_dataset():
    dataset = hf_dataset.download_dataset()
    dataset = hf_dataset.prepare_dataset(dataset)
    hf_dataset.save_dataset(dataset, "./dataset/")

if not os.path.isdir('./dataset/'):
    first_run_dataset()

dataset = hf_dataset.load_saved_dataset("./dataset/")
torch_dataset = hf_dataset.dataset_to_torch(dataset)

# --- train model(s) ---
batch_size = 64
coddings_size = 256
n_epoches = 50

generator = models.Generator()
discriminator = models.Discriminator()

train.dcgan(generator, 
            discriminator, 
            torch_dataset,
            batch_size,
            coddings_size,
            n_epoches,
            device)

# --- summary ---
torch.save(generator, "./generator.pth")
torch.save(discriminator, "./discriminator.pth")

sound_notification.play("./finished.mp3")