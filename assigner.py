import os
import discord

DISCORD_TOKEN = "MTAxNDUxMDk0MTk3NjY2MjA5MA.GpSPL_.B2xbTRoxc349-nk64n4pFeWQD4i9J2VWd_W0Vg" # os.environ.get("DISCORD_BLOOMY_TOKEN", None)

roles = {
    "🎨": "diffusers",
    "🤖": "reinforcement-learning",
    "🔊": "ml-4-audio",
    "🧠": "open-source",
    "🤗": "open-science",
    "🖼️": "gradio",
    "🥳": "collaborate",
}

server_id = 879548962464493619
message_id = 1014514727466053733

class MyClient(discord.Client):
    async def on_ready(self):
        self.guild = client.get_guild(server_id)

        self.roles = self.guild.roles
        print('Logged on as', self.user)
        print('Roles', self.roles)

    async def on_raw_reaction_add(self, payload):
        user = payload.member
        emoji = str(payload.emoji)

        if payload.message_id != message_id:
            return

        if emoji not in roles:
            return
        print("Adding role", emoji, roles[emoji], user)

        role = discord.utils.get(self.roles, name=roles[emoji])
        await user.add_roles(role)

        role = discord.utils.get(self.roles, name="role_assigned")
        await user.add_roles(role)

    async def on_raw_reaction_remove(self, payload):
        guild = client.get_guild(payload.guild_id)
        user = discord.utils.get(guild.members, id=payload.user_id)
        emoji = str(payload.emoji)

        if payload.message_id != message_id:
            return

        if emoji not in roles:
            return
        print("Removing role", emoji, roles[emoji], user)

        role = discord.utils.get(self.roles, name=roles[emoji])
        await user.remove_roles(role)

if __name__ == "__main__":
    intents = discord.Intents.all()
    client = MyClient(intents=intents)
    client.run(DISCORD_TOKEN)
