import os
import random
import time
from typing import Dict, List
import discord
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

KICK_CHANCE = 0.025
ROLE_MENTION_INCREASE = 0.3
# we not even printing this out so even the owner doesn't know LOL
# could make this 6 characters, we'll just make it one character for ease
RESET_PASSWORD = uuid4().hex[:1]
BAD_ROLES_PINGS = ["cartoon csgo"]

class SillyBot(discord.Client):
    def __init__(self, *, intents: discord.Intents, **options) -> None:
        super().__init__(intents=intents, **options)
        print("lets go")
        self.quiet = True
        # store all names once, as bot and owner names can start to become majority (since they are skipped over in assignment process)
        self.all_names: Dict[int, List[str]] = {}

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
            await channels[0].send("i am going to commit mischief")

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

        # no one can reset if they don't know password nyeheheh
        if message.content == f"silly reset {RESET_PASSWORD}":
            # set everyone's nicknames to their default name
            for m in members:
                if guild.owner_id == m.id or m.bot:
                    continue
                print("- reseting", m.name, "from", m.nick)
                await m.edit(nick=None)
            self.all_names.pop(guild.id)
            await message.channel.send("mischief reset")
            return
        
        if message.content == "silly kick":
            # kick a random person
            # ok this may be too harsh, not implementing
            guild.kick(m)
            return

        # owner and bots do not trigger mischief effects (safe guys)
        if message.author.id == guild.owner.id or message.author.bot:
            return
        
        # roulette suicidal-kicking
        chance = random.random()
        mentioned_role = False
        # if they mention bad role, they even more dead
        if len(message.role_mentions) > 0 and message.role_mentions[0].name in BAD_ROLES_PINGS:
            chance -= ROLE_MENTION_INCREASE
            mentioned_role = True
        print(message.author.name, "had chance", chance, mentioned_role)
        if chance <= KICK_CHANCE:
            if mentioned_role:
                await message.channel.send("bro pinged cartoon csgo")
            # countdown lmao
            await message.channel.send("lmao")
            for i in range(3, 0, -1):
                await message.channel.send(f"{i}")
                time.sleep(2)
            await message.channel.send("bye.")
            time.sleep(2)
            print("we kickin", message.author.name)
            await guild.kick(message.author)

        
        # give everyone a random name
        if self.all_names.get(guild.id, None) is None:
            self.all_names[guild.id] = [m.display_name for m in members]
        random.shuffle(self.all_names[guild.id])
        print("names:", self.all_names[guild.id])
        
        for idx, m in enumerate(members):
            if guild.owner_id == m.id or m.bot:
                continue
            new_name = self.all_names[guild.id][idx]
            print("- editing", m.name, "to", new_name)
            await m.edit(nick=new_name)
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


