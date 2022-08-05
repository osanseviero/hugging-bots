import os
import json
import requests
import discord

API_TOKEN = os.environ.get("HF_API_TOKEN", None)
BLOOM_ENDPOINT = os.environ.get("BLOOM_ENDPOINT", None)
DISCORD_TOKEN = os.environ.get("DISCORD_BLOOMY_TOKEN", None)

def query(payload):
    response = requests.request(
        "POST",
        BLOOM_ENDPOINT,
        json=payload,
        headers={"Authorization": f"Bearer {API_TOKEN}"},
    )
    return json.loads(response.content.decode("utf-8"))

def generate(text, sample=False):
    payload = {
        "inputs": text,
        "parameters": {
            "max_new_tokens": 32,
            "do_sample": sample,
            "top_p": 0.95,
            "early_stopping": False,
            "length_penalty": 0.0,
            "eos_token_id": None,
        },
    }

    data = query(payload)

    try:
        res = data[0]["generated_text"]
        return res
    except Exception:
        return data.get("error", "The API returned an error without any message")


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.find("!help") != -1:
            await message.reply("Use !greedy or !sampling to generate text based on a prompt with bloom", mention_author=True)


        if message.content.startswith('!greedy') or message.content.startswith('!sampling'):
            sample = True
            if message.content.startswith('!greedy'):
                sample = False
            text = " ".join(message.content.split()[1:])
            result = generate(text, sample)
            await message.reply(result, mention_author=True)

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)
