import discord, datetime, traceback, sys, math
from discord.ext import commands


class CommandErrorHandler(commands.Cog, name="Error Handler"):
		"""This category is of no use for you, ignore it. Mainly to handle the command errors. It will be ignored in the future!"""
		def __init__(self, bot):
				self.bot = bot

		@commands.Cog.listener()
		async def on_command_error(self, ctx, error):
				"""
				To handle the errors!
				"""

				if hasattr(ctx.command, 'on_error'): return

				# get the original exception
				error = getattr(error, 'original', error)

				if isinstance(error, commands.CommandNotFound): return

				if isinstance(error, commands.BotMissingPermissions):
						missing = [
								perm.replace('_', ' ').replace('guild', 'server').title()
								for perm in error.missing_perms
						]
						if len(missing) > 2:
								fmt = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
						else:
								fmt = ' and '.join(missing)
						_message = f'Error: Bot Missing permissions. Please provide the following permission(s) to the bot, in {ctx.guild.name}```\n{fmt}```'
						try:
								await ctx.author.send(_message)
						except Exception:
								await ctx.send(_message)

						return

				if isinstance(error, commands.DisabledCommand):
						return await ctx.send('This command has been disabled.')

				if isinstance(error, commands.CommandOnCooldown):
						return await ctx.send(
								f"{ctx.author.mention} `{ctx.comamnd.name}` you are on command cooldown, please retry in **{math.ceil(error.retry_after)}**s."
						)

				if isinstance(error, commands.MissingPermissions):
						missing = [
								perm.replace('_', ' ').replace('guild', 'server').title()
								for perm in error.missing_perms
						]
						if len(missing) > 2:
								fmt = '{}, and {}'.format("**, **".join(missing[:-1]),
																					missing[-1])
						else:
								fmt = ' and '.join(missing)
						_message = 'Error: Missing Permissions. You need the the following permission(s) to use the command.```\n{}```'.format(
								fmt)
						await ctx.send(_message)
						return

				if isinstance(error, commands.NoPrivateMessage):
						try:
								await ctx.send(
										'Error: No Private Message.```\nThis command cannot be used in direct messages. It can only be used in server(s)```'
								)
						except discord.Forbidden:
								pass
						return

				if isinstance(error, commands.NSFWChannelRequired):
						em = discord.Embed(timestamp=datetime.datetime.utcnow())
						em.set_image(url="https://i.imgur.com/oe4iK5i.gif")
						await ctx.send(
								content=
								"Error: NSFW Channel Required. This command will only run in NSFW marked channel. https://i.imgur.com/oe4iK5i.gif",
								embed=em)
						return

				if isinstance(error, commands.CheckFailure):
						await ctx.reply(
								f"{ctx.author.mention} you do not have permission to use this command."
						)
						return

				if isinstance(error, commands.BadArgument):
						if isinstance(error, commands.MessageNotFound):
								return await ctx.reply(
										f'{ctx.author.mention} that message is not visible in this server by me or message you specified is invalid! Do check the name/ID again'	
								)
						elif isinstance(error, commands.MemberNotFound):
								return await ctx.reply(
										f'{ctx.author.mention} that member is not visible in this server by me or member you specified is invalid! Do check the 1name/ID again'
								)
						elif isinstance(error, commands.UserNotFound):
								return await ctx.reply(
										f'{ctx.author.mention} that user is not visible in this server by me or user you specified is invalid! Do check the name/ID again'
								)
						elif isinstance(error, commands.ChannelNotFound):
								return await ctx.reply(
										f'{ctx.author.mention} that channel is not visible in this server by me or channel you specified is invalid! Do check the name/ID again'
								)
						elif isinstance(error, commands.RoleNotFound):
								return await ctx.reply(
										f'{ctx.author.mention} that role is not visible in this server by me or role you specified is invalid! Do check the name/ID again'
								)
						elif isinstance(error, commands.EmojiNotFound):
								return await ctx.reply(
										f'{ctx.author.mention} that emoji is not visible in this server by me or emoji you specified is invalid! Do check the name/ID again'
								)

				if isinstance(error, commands.MissingRequiredArgument):
						cmd = discord.utils.get(self.bot.commands,
																		name=f"{ctx.command.name}")
						if not cmd.aliases == []: cmd_and_als = "|".join(cmd.aliases)
						else: cmd_and_als = ""
						signature = cmd.signature
						if cmd.aliases == []:
								await ctx.reply(
										f"Error: Missing Required Argument. Please use proper syntax.```\n[p]{cmd} {signature}```"
								)
						else:
								await ctx.reply(
										f"Error: Missing Required Argument. Please use proper syntax.```\n[p]{cmd}|{cmd_and_als} {signature}```"
								)
						return

				print('Ignoring exception in command {}:'.format(ctx.command),
							file=sys.stderr)

				traceback.print_exception(type(error),
																	error,
																	error.__traceback__,
																	file=sys.stderr)

def setup(bot):
		bot.add_cog(CommandErrorHandler(bot))
