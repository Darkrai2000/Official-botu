import time
from os import system
import os
import datetime
import jishaku
from keep_alive import keep_alive

system('pip install pynacl')
system('python3 -m pip install -U "discord.py[voice]"')
system('pip install pygicord')
from discord.ext import commands
import traceback, sys
import __main__
import discord, asyncio

client = commands.Bot(command_prefix=commands.when_mentioned_or('n!', 'N!', "nuke"), intents=discord.Intents.all(), case_insensitive=False)
client.remove_command('help')
client.strip_after_prefix = True
client.case_insensitive=False
@client.event
async def on_ready():
		print('Bot is ready to take commands. Status OK')
		print(discord.version_info)
		print(discord.__version__)
		await client.get_channel(819858263767908392).connect() # to connect to main support server!
		while True:
			await client.change_presence(activity=discord.Game(name="with members!"))
			await asyncio.sleep(10)
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"n!killall"), status=discord.Status.dnd)
			await asyncio.sleep(10)
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"n!help"), status=discord.Status.dnd)
			await asyncio.sleep(10)
		

# COGS ADDITIONS

extensions = ['cogs.mod', 'cogs.nuke', 'cogs.help', 'cogs.on_error', 'cogs.kill_all', 'cogs.ult']

if __name__ == '__main__':
		for extension in extensions:
				try:
						client.load_extension(extension)
						print(f'{extension} loaded')
				except Exception as e:
						print(f'Error loading in {extension}', file=sys.stderr)
						print(e)
						traceback.print_exc()
client.load_extension("jishaku")

keep_alive()
print(f"Session opened at {datetime.datetime.utcnow()}")
client.run(os.getenv('TOKEN'))
print(f"Session closed at {datetime.datetime.utcnow()}")


# End of program!