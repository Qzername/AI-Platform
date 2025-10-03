import configparser
import tensorflow as tf
from PIL import Image
import numpy as np
from io import BytesIO

config = configparser.ConfigParser()
config.read('config.ini')

token = config['BASE']['token']

import json

test = { "s" : """
**Definitions:**
- `DefaultConv2D` is Convoluted layer 2D with `kernel_size=3, padding="same", activation="relu", kernel_initializer="he_normal"`

**Structure:**
1. `DefaultConv2D` with `filters=64, kernel_size=7, input_shape=[160,90,3]`
2. Max Pooling 2D
3. `DefaultConv2D` with `filters=128`
4. Max Pooling 2D
5. Flatten
6. `Dense` with `units=64, activation="relu", kernel_initializer="he_normal"`
7. `Dense` with `units=1, activation="sigmoid"`

Output is 0.0-1.0 float value with 0 meaning cat is more likely to be on the picture, and 1 meaning dog is more likely to be on the picture

**Dataset and training**
Trained 10 epoches on microsoft/cats_vs_dogs dataset

Model is compiled with parameters: `loss="binary_crossentropy", optimizer="nadam", metrics=["accuracy"]`

**Statistics**
Total params: 14,584,836 (55.64 MB)
 Trainable params: 7,292,417 (27.82 MB)
 Non-trainable params: 0 (0.00 B)
 Optimizer params: 7,292,419 (27.82 MB)
"""}

json.

model_collection = {}

with open('models_info.json') as f:
    d = json.load(f)
    for model_info in d:
        versions = []

        for version in model_info["versions"]:
            versions.append({
                "name": version["name"],
                "model": tf.keras.models.load_model(version["path"]),
                "structure": version["structure"] 
            })

        model_collection[model_info["name"]] = {
            "description": model_info["description"],
            "versions": versions
        }

def load_image(img_bytes):
    im = Image.open(BytesIO(img_bytes))

    im = im.resize((160,90)).convert("RGB")

    img_array = np.array(im) / 255.0        
    img_array = np.expand_dims(img_array, axis=0)  

    return img_array

async def get_prediction_from_attachments(attachments, model_name):
    for attachment in attachments: 
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")): 
            img_bytes = await attachment.read()
            prediciton = model_collection[model_name]["versions"][0].predict(load_image(img_bytes))

            prediciton_text = ""

            if(prediciton[0][0] < 0.5):
                percent = (1 - prediciton[0][0])*100
                prediciton_text = "Cat, confidence: " + f"{percent:.2f}%"
            else:
                percent = prediciton[0][0]*100
                prediciton_text = "Dog, confidence: " + f"{percent:.2f}%"
                
            return prediciton_text


import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    model_name = message.content.split(' ')[-1]

    if message.content.startswith('$aip predict'):
        if message.attachments:
            await message.channel.send('PREDICTION: ' + await get_prediction_from_attachments(message.attachments, model_name))
            return

        if message.reference is not None: 
            replied_message = await message.channel.fetch_message(message.reference.message_id)

            if replied_message.attachments: 
                await message.channel.send('PREDICTION: ' + await get_prediction_from_attachments(replied_message.attachments, model_name))

    if message.content.startswith('$aip list'):
        final_message = ""
        
        for k,v in model_collection.items():
            final_message += "**" + k + "** - " + v["description"] 

        await message.channel.send(final_message)

    if message.content.startswith("$aip structure"):
        await message.channel.send(model_collection[model_name]["versions"][0]["structure"])

client.run(token)
