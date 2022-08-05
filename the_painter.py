import os
import discord
import gradio as gr

DISCORD_TOKEN = os.environ.get("DISCORD_PAINTER_TOKEN", None)

jojogan = gr.Blocks.load(name="spaces/akhaliq/JoJoGAN")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.find("!help") != -1:
            await message.reply("Use !jojo !disney !spidey or !sketch. Have fun!", mention_author=True)

        style = None
        if message.content.startswith('!jojo'):
            style = 'JoJo'
        if message.content.startswith('!disney'):
            style = 'Disney'
        if message.content.startswith('!spidey'):
            style = 'Spider-Verse'
        if message.content.startswith('!sketch'):
            style = 'sketch'

        if style:
            print("Painting")
            if message.attachments:
                attachment = message.attachments[0]
                im = jojogan(attachment.url, style)
                await message.reply(f'Here is the {style} version of it', file=discord.File(im))
            else:
                await message.channel.send("No attachments to be found...Can't animify dat! Try sending me an image 😉")

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)