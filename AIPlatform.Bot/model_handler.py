import json
import tensorflow as tf
import torch
from enum import Enum

import handlers.catgen as catgenHandler
import handlers.cdclas as cdclasHandler

#TODO: fix this
from models import Generator

class FileType(Enum):
    KERAS = 0
    PTH = 1

model_collection = {}

def load_model(fileType, path):
    if fileType == FileType.KERAS.value:
        return tf.keras.models.load_model(path + ".keras")
    elif fileType == FileType.PTH.value:
        return torch.load(path + ".pth",map_location="cpu", weights_only=False)

def load_handler(model_id):
    if model_id == "catgen":
        return catgenHandler.Catgen()
    else:
        return cdclasHandler.CDClas()

def get_path_for_model(modelName, modelVersion):
    return "models/" + modelName + "." + modelVersion

def prepare_collection():
    print("loading models...")

    with open("models_info.json") as f:
        models_info = json.load(f)

        for model_info in models_info:
            versions = {}

            for version in model_info["versions"]:
                model_path = get_path_for_model(model_info["id"],version["id"])

                model = load_model(version["fileType"],model_path)
                
                versions[version["id"]] = {
                    "fileType": version["fileType"],
                    "model": model,
                    "structure": version["structure"]
                }

            model_collection[model_info["id"]] = {
                "id":model_info["id"],
                "description": model_info["description"],
                "default": model_info["default"],
                "versions": versions,
                "handler": load_handler(model_info["id"])
            }
            print("loaded model:", model_info["id"])

    print("models loaded")