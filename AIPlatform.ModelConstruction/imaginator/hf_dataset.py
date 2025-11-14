from datasets import load_dataset, load_from_disk
from PIL import Image
import torch
import numpy as np
import os

# this file manages downloading and preparing of any 
# image hugging face dataset

def download_dataset(url):
    dataset = load_dataset(url)
    return dataset

def prepare_dataset(dataset, image_id):
    def to_rgb(example):
        if example[image_id].mode != "RGB":
            example[image_id] = example[image_id].convert("RGB")
        return example
    
    def resize(example):
        example[image_id] = example[image_id].resize((64,64), Image.Resampling.BILINEAR)
        return example
        
    def normalize(example):
        example[image_id] = torch.tensor(np.array(example[image_id])).permute(2, 0, 1).float()  
        example[image_id] = (example[image_id] / 127.5) - 1.0
        return example

    dataset = dataset.map(to_rgb).map(resize)#.map(normalize)
    return dataset

def load_saved_dataset(path):
    return load_from_disk(path)

def save_dataset(dataset, path):
    dataset.save_to_disk(path)

def dataset_to_torch(dataset):
    return dataset["train"].with_format("torch")

def full_load(url, path, image_label):
    if not os.path.isdir(path):
        dataset = download_dataset(url)
        dataset = prepare_dataset(dataset, image_label)
        save_dataset(dataset, path)

    return load_saved_dataset(path)

