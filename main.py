import os
import random
from typing import Dict, List
import discord
from dotenv import load_dotenv

load_dotenv()

class SillyBot(discord.Client):
    def __init__(self, *, intents: discord.Intents, **options) -> None:
        super().__init__(intents=intents, **options)
        print("lets go")
        self.quiet = False
        # store all names once, as bot and owner names can start to become majority (since they are skipped over in assignment process)
        self.all_names: List[str] = []

    async def on_ready(self):
        print(f"{self.user} has connected to the discord fellas")
        # send greeting msg to every connected server
        for guild in self.guilds:
            # get all text channels it has access to in server
            channels = [
                channel
                for channel in guild.channels
                if channel.type == discord.ChannelType.text
                and channel.permissions_for(channel.guild.me).send_messages
            ]
            # sort by visual position
            channels.sort(key=lambda c: c.position)
            # send message to first channel it has access to
            await channels[0].send("ladies and fellas, the silly cat is here")

    async def on_message(self, message: discord.Message):
        # don't respond to itself
        if message.author == self.user:
            return
        
        if message.content == "silly quiet":
            self.quiet = not self.quiet
            print("changing quiet mode to", self.quiet)
            await message.channel.send("ok silly is " + ("quiet" if self.quiet else "not quiet"))
            return

        guild = message.guild
        members = guild.members

        if message.content == "silly reset":
            # set everyone's nicknames to their default name
            for m in members:
                if guild.owner_id == m.id or m.bot:
                    continue
                print("- reseting", m.name, "from", m.nick)
                await m.edit(nick=None)
            self.all_names = []
            await message.channel.send("mischief reset")
            return
        
        if message.content == "silly kick":
            # kick a random person
            # ok this may be too harsh, not implementing
            pass
        
        # give everyone a random name
        if len(self.all_names) == 0:
            self.all_names = [m.display_name for m in members]
        random.shuffle(self.all_names)
        print("names:", self.all_names)
        
        for idx, m in enumerate(members):
            if guild.owner_id == m.id or m.bot:
                continue
            print("- editing", m.name, "to", self.all_names[idx])
            await m.edit(nick=self.all_names[idx])
        if not self.quiet:
            await message.channel.send("mischief done")



if __name__ == "__main__":
    print("we startin")

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.members = True

    client = SillyBot(intents=intents)
    token = os.getenv("DISCORD_TOKEN")
    client.run(token)


