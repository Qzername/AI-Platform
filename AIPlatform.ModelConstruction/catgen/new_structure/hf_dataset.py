from datasets import load_dataset
from datasets import load_from_disk
from PIL import Image
import torch
import numpy as np

def download_dataset():
    dataset = load_dataset("microsoft/cats_vs_dogs")
    dataset = dataset.filter(lambda a: a["labels"] == 0)
    return dataset

def prepare_dataset(dataset):
    def to_rgb(example):
        if example["image"].mode != "RGB":
            example["image"] = example["image"].convert("RGB")
        return example
    
    def resize(example):
        example["image"] = example["image"].resize((48,64), Image.Resampling.BILINEAR)
        return example
        
    def normalize(example):
        example["image"] = torch.tensor(np.array(example["image"])).permute(2, 0, 1).float()  # CHW
        example["image"] = (example["image"] / 127.5) - 1.0
        return example

    dataset = dataset.map(to_rgb).map(resize).map(normalize)
    return dataset

def load_saved_dataset(path):
    return load_from_disk(path)

def save_dataset(dataset, path):
    dataset.save_to_disk(path)

def dataset_to_torch(dataset):
    return dataset.with_format("torch")