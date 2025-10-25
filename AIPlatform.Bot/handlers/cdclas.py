from handlers.handler import Handler
from PIL import Image
from io import BytesIO
import numpy as np

class CDClas(Handler):
    def load_image(self, img_bytes):
        im = Image.open(BytesIO(img_bytes))

        im = im.resize((160,90)).convert("RGB")

        img_array = np.array(im) / 255.0        
        img_array = np.expand_dims(img_array, axis=0)  

        return img_array

    async def get_prediction_from_attachments(self, attachments, model):
        for attachment in attachments: 
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")): 
                img_bytes = await attachment.read()

                prediciton = model.predict(self.load_image(img_bytes))

                prediciton_text = ""

                if(prediciton[0][0] < 0.5):
                    percent = (1 - prediciton[0][0])*100
                    prediciton_text = "Cat, confidence: " + f"{percent:.2f}%"
                else:
                    percent = prediciton[0][0]*100
                    prediciton_text = "Dog, confidence: " + f"{percent:.2f}%"
                    
                return prediciton_text


    async def handle(self, ctx, model):
        msg = ctx.message
        model_keras = model["versions"][model["default"]]["model"]

        if msg.attachments:
            await ctx.send('PREDICTION: ' + await self.get_prediction_from_attachments(msg.attachments, model_keras))
            return

        if msg.reference is not None: 
            replied_message = await msg.channel.fetch_message(msg.reference.message_id)

            if replied_message.attachments: 
                await ctx.send('PREDICTION: ' + await self.get_prediction_from_attachments(replied_message.attachments, model_keras))
