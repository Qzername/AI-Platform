from handlers.handler import Handler
import torch
import torch_devices
import discord
from io import BytesIO
from PIL import Image
import numpy as np

class Catgen(Handler):
    async def handle(self, message, model_info):
        model = model_info["versions"][model_info["default"]]["model"]

        device = torch_devices.get_current()

        noise = torch.randn(16, 256, device=device)
        with torch.no_grad():
            generated_image = model(noise)[0].detach().cpu()
        
        # Clamp and normalize
        generated_image = torch.clamp(generated_image, -1, 1)
        img = (generated_image + 1) / 2
        img = img.permute(1, 2, 0).numpy().clip(0, 1)
        img = (img * 255).astype(np.uint8)  # convert to uint8 for PIL

        # Convert to PIL image and resize to 256x256
        pil_img = Image.fromarray(img)
        pil_img = pil_img.resize((256, 256), Image.BICUBIC)

        # Save image to memory
        buf = BytesIO()
        pil_img.save(buf, format="PNG")
        buf.seek(0)

        # Send it to Discord
        await message.channel.send(file=discord.File(buf, filename="generated.png"))