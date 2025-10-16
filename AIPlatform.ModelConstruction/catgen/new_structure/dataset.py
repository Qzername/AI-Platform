from datasets import load_dataset

def download_dataset(datasetName):
    dataset = load_dataset("microsoft/cats_vs_dogs")
    dataset = dataset.filter(lambda a: a["labels"] == 0)
    return dataset

def prepare_dataset(dataset):
    def to_rgb(example):
        if example["image"].mode != "RGB":
            example["image"] = example["image"].convert("RGB")
        return example
    
    def resize(example):
        example["image"] = example["image"].resize(48,64)
        return example
        
    
    dataset = dataset.map(to_rgb).map(resize)
    pass

def save_dataset(dataset):
    pass

def dataset_to_torch(dataset):
    torch_dataset = dataset.with_format("torch")
    
    def dict_to_tuple(data):
        image = data['image'].float()
        image = (image / 127.5) - 1.0  # map [0,255] → [-1,1]
        label = data['labels'].float()
        return image, label
    


    return torch_dataset