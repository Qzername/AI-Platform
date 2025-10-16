import dataset

torch_dataset = dataset.download_dataset()
torch_dataset = dataset.prepare_dataset(torch_dataset)
dataset.save_dataset(torch_dataset)