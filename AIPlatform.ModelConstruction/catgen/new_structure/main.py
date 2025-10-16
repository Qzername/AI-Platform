import torch
import random

# local
import hf_dataset
import models

# --- config --- 
manualSeed = 42
print("Random Seed: ", manualSeed)
random.seed(manualSeed)
torch.manual_seed(manualSeed)
torch.use_deterministic_algorithms(True) 

# --- dataset config --- 
def first_run_dataset():
    torch_dataset = hf_dataset.download_dataset()
    torch_dataset = hf_dataset.prepare_dataset(torch_dataset)
    hf_dataset.save_dataset(torch_dataset, "./dataset/")

#first_run_dataset()
torch_dataset = hf_dataset.load_saved_dataset("./dataset/")

batch_size = 64
coddings_size = 256

