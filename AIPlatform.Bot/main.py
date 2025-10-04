import configparser
import tensorflow as tf
from PIL import Image
import numpy as np
from io import BytesIO

config = configparser.ConfigParser()
config.read('config.ini')

token = config['BASE']['token']

import json

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
            prediciton = model_collection[model_name]["versions"][0]["model"].predict(load_image(img_bytes))

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
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="$aip help | " + config['BASE']['version']))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    splited = message.content.split(' ')
    model_name = ""
    
    if len(splited) > 2:
       model_name = splited[2]
    
    model_version = ""

    if len(splited) > 3:
        model_version = splited[3]

    if message.content.startswith("$aip help"):
        await message.channel.send("""
$aip predict [model name] - depending on model, result can be diffrent
$aip list - lists all models implemented into bot
$aip structure [model name] [version name] - gives advanced description about model structure
                                   """)
        return

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
            final_message += "# " + k + "\nDescription: " + v["description"] + "\n"
            
            final_message += "\nversions:\n"
            for version in v["versions"]:
                final_message += "- " + version["name"] + "\n"

        await message.channel.send(final_message)

    if message.content.startswith("$aip structure"):
        versions = model_collection[model_name]["versions"]
                                        
        if model_version == "":
            await message.channel.send("Provide version of the model")
        else:
            versionIndex = 0

            for version in versions:
                if version["name"] == model_version:
                    break
                else:
                    versionIndex+=1

            await message.channel.send(versions[versionIndex]["structure"])

client.run(token)
