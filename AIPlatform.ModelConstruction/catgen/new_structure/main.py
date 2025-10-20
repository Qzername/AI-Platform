import torch
import random

# local
import hf_dataset
import cd_dataset
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

# --- dataset config --- 

# torch_datastet = hf_dataset.full_load("microsoft/cats_vs_dogs")
torch_dataset = cd_dataset.load_from_directory()

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

# sound_notification.play("./finished.mp3")