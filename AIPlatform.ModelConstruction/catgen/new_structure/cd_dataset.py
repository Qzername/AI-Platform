# this dataset loads dataset from
# https://github.com/AnnikaV9/cat-dataset/

from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def load_from_directory():        
    transform = transforms.Compose([
        transforms.Resize((64, 64)),   # resize all images to 64x64
        transforms.ToTensor(),           # convert PIL image to tensor
    ])

    dataset = datasets.ImageFolder(root='dataset', transform=transform)

    return dataset