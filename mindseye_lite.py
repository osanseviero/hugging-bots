import os
import discord
import gradio as gr
import io, base64
from PIL import Image
import random
import shortuuid

DISCORD_TOKEN = os.environ.get("DISCORD_MINDS_EYE_TOKEN", None)

diffusion = gr.Interface.load("spaces/multimodalart/diffusion")

def text2image_diffusion(text, steps_diff=40, images_diff=2, weight=5, clip=False):
    results = diffusion(text, steps_diff, images_diff, weight, clip)
    image_paths = []
    print(results)
    for image in results:
        image_str = image
        image_str = image_str.replace("data:image/png;base64,","")
        decoded_bytes = base64.decodebytes(bytes(image_str, "utf-8"))
        img = Image.open(io.BytesIO(decoded_bytes))
        url = shortuuid.uuid()
        temp_dir = './tmp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        image_path = f'{temp_dir}/{url}.png'
        img.save(f'{temp_dir}/{url}.png')
        image_paths.append(image_path)
    return(image_paths)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.find("!help") != -1:
            await message.reply("Use !latent_diffuse <TEXT PROMPT>. Have fun!", mention_author=True)


        if message.content.startswith('!latent_diffuse'):
            print("Generating")
            text = " ".join(message.content.split()[1:])
            result = text2image_diffusion(text)
            await message.reply(f'Here are your diffused images', file=discord.File(result))


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)