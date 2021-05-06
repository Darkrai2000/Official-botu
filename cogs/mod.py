from discord.ext import commands
import discord, json, datetime, typing, asyncio

class mod(commands.Cog, name="Moderator", description="A simple moderator's tool for managing the server."):
	"""A simple moderator's tool for managing the server."""
	
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['arole', 'giverole', 'grole'], brief="Gives a role to the specified member")
	@commands.has_permissions(manage_roles=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.bot_has_permissions(manage_roles=True)
	async def addrole(self, ctx, member: commands.Greedy[discord.Member], role: discord.Role, *, reason:str=None):
		'''
		Gives a role to the specified member(s).

		Syntax:
		`Addrole <User1:Mention/ID> <User2:Mention/ID> ... <Role:Mention/ID> [Reason:Text]`

		Permissions:
		Need Manage Roles permission, for both the user and the bot.

		NOTE: The bot will add role indiscriminately, means it does not care about the role hierarchy, as long as the bot itself has the power to do the give roles, and the target role is below the Bot role. It is adviced that Bot role should be just below the Moderator/Staff role.
		'''
		guild = ctx.guild
		for member in member:
			if guild.me.top_role < member.top_role:
				await ctx.send(f"{ctx.author.mention} can't give the role to {member.name} as it's role is above the bot")

			try:
				await member.add_roles(role, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
				await ctx.send(f"{ctx.author.mention} given {role.name}({role.id}) to {member.name}")
			except Exception as e:
				pass
			await asyncio.sleep(0.25)


	@commands.command(aliases=['hackban'], brief='To ban a member from guild')
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.guild_only()
	async def ban(self, ctx, member : commands.Greedy[discord.Member], days:typing.Optional[int]=0, *, reason:str=None):
		'''
		To ban a member from guild.
		
		Syntax: 
		`Ban <User:Mention/ID> [Delete Days:Whole Number] [Reason:Text]`

		Permissions:
		Need Ban Member permission, for both the user and the bot.

		NOTE: The bot will ban indiscriminately, means it does not care about the role hierarchy, as long as the bot itself has the power to do the ban. It is adviced that Bot role should be just below the Moderator/Staff role.
		'''
		for member in member:
			try:
				await member.ban(reason=f'Action requested by: {ctx.author.name}({ctx.author.id}) || Reason: {reason}', delete_message_days=days)
				await ctx.send(f"**`{member.name}#{member.discriminator}`** is banned! Responsible moderator: **`{ctx.author.name}#{ctx.author.discriminator}`**! Reason: **{reason}**")
			except Exception as e:
				pass # if something went wrong then it will silently ignores it
			await asyncio.sleep(0.25)

	@commands.command(hidden=False, brief="Blocks a user from sending message in that channel.")
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(manage_channels=True, manage_permissions=True, manage_roles=True)
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.guild_only()
	async def block(self, ctx, member : commands.Greedy[discord.Member], *, reason : str=None):
		"""
		Blocks a user from sending message in that channel.
		
		Syntax:
		`Block <User:Mention/ID> [Reason:Text]`
		
		Permissions:
		Need Manage Channels, Manage Permissions, and Manage Roles permissions for the bot, and Kick Member permission for the user.

		NOTE: The bot will block indiscriminately, means it does not care about the role hierarchy, as long as the bot itself has the power to do the block. It is adviced that Bot role should be just below the Moderator/Staff role.
		"""
		guild = ctx.guild
		if (member.id == self.bot.user.id) or (member == ctx.author): return await ctx.send(f"{ctx.author.mention} :\ don't do that, I am only trying to help!")

		for member in member:
			try:
				await ctx.channel.set_permissions(member, send_messages=False, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
				await ctx.send(f'{ctx.author.mention} overwrite permission(s) for **{member.name}** has been created! **View Channel, and Send Messages** is denied!')
			except Exception as e:
				pass # if something went wrong then it will silently ignores it
			await asyncio.sleep(0.25)

	@commands.command(aliases=['nuke'], hidden=False, brief="To clone the channel or to nukes the channel (clones and delete).")
	@commands.has_permissions(manage_channels=True)
	@commands.bot_has_permissions(manage_channels=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	async def clone(self, ctx, channel : discord.TextChannel=None, *, reason:str=None):
		"""
		To clone the channel or to nukes the channel (clones and delete).

		Syntax:
		`Clone [Channel:Mention/ID] [Reason:Text]`
		(If no channel is specified then it will clone that channel in which the command is being executed)

		Permissions:
		Need Manage Channels permission, for both user and the bot.
		"""
		if channel is None: channel = ctx.channel
		
		new_channel = await channel.clone(reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
		await channel.delete(reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
		await new_channel.send(f"{ctx.author.mention}", delete_after=5)
		

	@commands.command(brief='To kick a member form guild')
	@commands.has_permissions(kick_members=True)
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.bot_has_permissions(kick_members=True)
	@commands.guild_only()
	async def kick(self, ctx, member : commands.Greedy[discord.Member], *, reason:str=None):
		'''
		To kick a member from guild.
		
		Syntax:
		`Kick <User:Mention/ID> [Reason:Text]`
		
		Permissions:
		Need Kick Member permission, for both the user and the bot.

		NOTE: The bot will kick indiscriminately, means it does not care about the role hierarchy, as long as the bot itself has the power to do the kick. It is adviced that Bot role should be just below the Moderator/Staff role.
		'''
		for member in member:
			try:
				await member.kick(reason=f'Action requested by: {ctx.author.name}({ctx.author.id}) || Reason: {reason}')
				await ctx.send(f'**`{member.name}#{member.discriminator}`** is kicked! Responsible moderator: **`{ctx.author.name}#{ctx.author.discriminator}`**! Reason: **{reason}**')
			except Exception as e:
				pass  # if something went wrong then it will silently ignores it
			await asyncio.sleep(0.25)

	@commands.command(hidden=False, brief="To lock the channel (Text channel)")
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(manage_channels=True, manage_permissions=True, manage_roles=True)
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.guild_only()
	async def lock(self, ctx, channel : commands.Greedy[discord.TextChannel]=None, *, reason:str=None):
		"""
		To lock the channel (Text channel)
		
		Syntax:
		`Lock [Channel:Mention/ID] [Reason:Text]`
		(If no channel is specified then it will lock that channel in which the command is being executed)

		Permissions:
		Need Manage Channels, Manage Permissions, and Manage Roles permissions for the bot, and Kick Member permission for the user.

		NOTE: This command will deny the server default role (`@everyone`) from sending message in the specified channel. To reverse the change, use `unlock` command. `[p]help unlock` for more info.
		"""
		if channel is None:
			channel = ctx.channel
			overwrite = channel.overwrites_for(ctx.guild.default_role)
			overwrite.send_messages = False
			await channel.set_permissions(ctx.guild.default_role, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}", overwrite=overwrite)
			await ctx.send(f'{ctx.author.mention} channel locked.')
			return

		for channel in channel:
			try:
				overwrite = channel.overwrites_for(ctx.guild.default_role)
				overwrite.send_messages = False
				await channel.set_permissions(ctx.guild.default_role, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}", overwrite=overwrite)
				await ctx.send(f'{ctx.author.mention} channel locked.')
			except Exception as e:
				pass  # if something went wrong then it will silently ignores it
			await asyncio.sleep(0.25)

	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(manage_roles=True)
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.guild_only()
	@commands.command(brief="To restrict a member to sending message in the Server")
	async def mute(self, ctx, member : commands.Greedy[discord.Member], *, reason:str=None):
		'''
		To restrict a member to sending message in the Server
		
		Syntax:
		`Mute <User:Mention/ID> [Reason]`

		Permissions: 
		Need Manage Roles permission for the bot, and Kick Members permission for the user.

		NOTE: The Mute command will only work if the any role exists with exact name `Muted` else Bot will create a role name `Muted`, and create overwrite (Send Messages=False, Read Message History=False) for all the text channels.
		'''

		if ctx.author == member:
			return	await ctx.send(f"{ctx.author.mention} you cannot mute yourself.")

		muted = discord.utils.get(ctx.guild.roles, name="Muted")

		if not muted: 
			muted = await ctx.guild.create_role(name="Muted", reason=f"Setting up mute role. it's first command is execution, by {ctx.author.name}({ctx.author.id})")
			for channel in ctx.guild.channels:
				await channel.set_permissions(muted, send_messages=False, read_message_history=False)

		for member in member:
			try:
				await member.add_roles(muted, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
				await ctx.send(f'{ctx.author.mention} **{member.name}** has been successfully muted till death!')
			except Exception as e:
				pass  # if something went wrong then it will silently ignores it
			await asyncio.sleep(0.25)


	@commands.command(brief='To delete bulk message')
	@commands.has_permissions(manage_messages=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.bot_has_permissions(read_message_history=True, manage_messages=True)
	async def purge(self, ctx, amount : int):
		'''
		To delete bulk message.
		
		Syntax:
		`Purge <Amount:Whole Number>`

		Permissions:
		Need Manage Messages and Read History Messages permissions, for both bot and the user. 
		'''

		deleted = await ctx.channel.purge(limit=amount + 1, bulk=True)
		await ctx.send(f"{ctx.author.mention} {len(deleted)} message deleted :')", delete_after=5)
	


	@commands.command(brief='To delete bulk message, of a specified user')
	@commands.has_permissions(manage_messages=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.bot_has_permissions(manage_messages=True, read_message_history=True)
	async def purgeuser(self, ctx, member:discord.Member, amount : int):
		'''
		To delete bulk message, of a specified user. 
		
		Syntax:
		`Purgeuser <User:Mention/ID> <Amount:Whole Number>`
		
		Permissions:
		Need Manage Message and Read History Messages permissions for both bot and the user.
		'''
		def check_usr(m):
			return m.author == member

		await ctx.channel.purge(limit=amount, bulk=True, check=check_usr)
		await ctx.send(f"{ctx.author.mention} message deleted :')", delete_after=5)
	

	@commands.command(brief='To set slowmode in the specified channel.')
	@commands.has_permissions(manage_channels=True)
	@commands.bot_has_permissions(manage_channels=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	async def slowmode(self, ctx, seconds : int, channel:discord.TextChannel=None, *, reason:str=None):
		'''
		To set slowmode in the specified channel.
		
		Syntax:
		`Slowmode <Seconds:Whole Number> [Channel:Mention/ID] [Reason:Text]`
		(If no channel is specified then it will raise slowmode in that channel in which the command is executed)

		Permissions: 
		Need Manage Channels permission, for both bot and the user.
		'''
		if (seconds <= 21600) and (seconds > 0):
			if channel is None: channel = ctx.channel 
			await channel.edit(slowmode_delay=seconds, reason=f"Action Requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
			await ctx.send(f"{ctx.author.mention} {channel} is not in slowmode, to reverse type [p]slowmode 0")
		if seconds == 0:
			await channel.edit(slowmode_delay=seconds, reason=f"Action Requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
		else: 
			await ctx.send(f"{ctx.author.mention} you can't set slowmode in negative numbers or more than 21600 seconds")



	@commands.command(aliases=['softkill'], brief='To Ban a member from a guild then immediately unban')
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	@commands.guild_only()
	async def softban(self, ctx, member : commands.Greedy[discord.Member], *, reason:str=None):
		'''
		To Ban a member from a guild then immediately unban
		
		Syntax:
		`Softban <User:Mention/ID> [Reason:Text]`

		Permissions:
		Need Ban Members permission, for both bot and the user.

		NOTE: The bot will softban indiscriminately, means it does not care about the role hierarchy, as long as the bot itself has the power to do the ban. It is adviced that Bot role should be just below the Moderator/Staff role.
		'''
		for member in member:
			try:
				await member.ban(reason=f'Action requested by: {ctx.author.name}({ctx.author.id}) || Reason: {reason}')

				banned_users = await ctx.guild.bans()
				member_n, member_d = member.name, member.discriminator
				for ban_entry in banned_users:
					user = ban_entry.user
					if (user.name, user.discriminator) == (member_n, member_d):
						await ctx.guild.unban(user)

				await ctx.send(f'**`{member.name}#{member.discriminator}`** is banned then unbanned! Responsible moderator: **`{ctx.author.name}#{ctx.authoe.discriminator}`**! Reason: **{reason}**')
			except Exception as e:
				pass  # if something went wrong then it will silently ignores it

			await asyncio.sleep(0.25)


	@commands.command(brief='To Unban a member from a guild')
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	async def unban(self, ctx, member : str, *, reason:str=None):
		'''
		To Unban a member from a guild.
		
		Syntax:
		`Unban <User.Name>#<User.Discriminator> [Reason:Text]`
		(Name should be exact, even a single mistake in name wont unban the user, as you know bot is nothing but a computer)

		Permissions:
		Need Ban Member permissions, for both bot and the user.
		'''
		banned_users = await ctx.guild.bans()
	
		member_name, member_discriminator = member.split('#')
		for ban_entry in banned_users:
			user = ban_entry.user
			
			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user, reason=f'Action requested by: {ctx.author.name}({ctx.author.id}) || Reason: {reason}')
				await ctx.send(f"**`{member_name}#{member_discriminator}`** is unbanned! Responsible moderator: **`{ctx.author.name}#{ctx.author.discriminator}`**! Reason: **{reason}**")



	@commands.command(hidden=False, brief='Unblocks a user from the text channel.')
	@commands.has_permissions(manage_permissions=True, manage_roles=True, manage_channels=True)
	@commands.bot_has_permissions(manage_channels=True, manage_permissions=True, manage_roles=True)
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.guild_only()
	async def unblock(self, ctx, member: commands.Greedy[discord.Member], *, reason:str=None):
		"""
		Unblocks a user from the text channel.

		Syntax:
		`Unblock <User:Mention/ID> [Reason:Text]`

		Permissions:
		Need Manage Channels, Manage Permissions, and Manage Roles permissions for the bot, and Kick Member permission for the user.

		NOTE: The bot will unblock indiscriminately, means it does not care about the role hierarchy, as long as the bot itself has the power to do the unblock. It is adviced that Bot role should be just below the Moderator/Staff role.
		"""

		for member in member:
			try:
				if member.permissions_in(ctx.channel).send_messages: await ctx.send(f"{ctx.author.mention} {member.name} is already unblocked. They can send message")
				else: await ctx.channel.set_permissions(member, view_channel=None, send_messages=None, overwrite=None, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
				await ctx.send(f'{ctx.author.mention} overwrite permission(s) for **{member.name}** has been deleted!')
			except Exception as e:
				pass  # if something went wrong then it will silently ignores it
			await asyncio.sleep(0.25)


	@commands.command(hidden=False, brief="To unlock the channel (Text channel)")
	@commands.has_permissions(manage_channels=True)
	@commands.bot_has_permissions(manage_channels=True, manage_roles=True, manage_permissions=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	async def unlock(self, ctx, channel : commands.Greedy[discord.TextChannel]=None, *, reason:str=None):
		"""
		To unlock the channel (Text channel)

		Syntax:
		`Unock [Channel:Mention/ID] [Reason:Text]`
		(If no channel is specified then it will unlock that channel in which the command is being executed)

		Permissions:
		Need Manage Channels, Manage Permissions, and Manage Roles permissions for the bot, and Kick Member permission for the user.

		NOTE: This command will allow the server default role (`@everyone`) from sending message in the specified channel. To reverse the change, use `lock` command. `[p]help lock` for more info."""
		if channel is None:
			channel = ctx.channel
			await channel.set_permissions(ctx.guild.default_role, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}", overwrite=None)
			await ctx.send(f'{ctx.author.mention} channel unlocked.')
			return

		for channel in channel:
			try:
				await channel.set_permissions(ctx.guild.default_role, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}", overwrite=None)
				await ctx.send(f'{ctx.author.mention} channel unlocked.')
			except Exception as e:
				pass
		await asyncio.sleep(0.25)

	@commands.command(brief='To allow a member to sending message in the Text Channels, if muted')
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(manage_roles=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	async def unmute(self, ctx, member: commands.Greedy[discord.Member], *, reason:str=None):
		'''
		To allow a member to sending message in the Text Channels, if muted.
		
		Syntax:
		`Unmute <User:Mention/ID> [Reason:Text]`

		Permissions:
		Need Manage Roles permission for the bot, and Kick Members permission for the user.
		'''
		Muted = "Muted"

		rolem = discord.utils.get(ctx.message.guild.roles, name=Muted)
		for member in member:
			try:
				if rolem in member.roles:
					await ctx.send(f'{ctx.author.mention} **{member.name}** has been unmuted now!')
					await member.remove_roles(rolem, reason=f'Action requested by: {ctx.author.name}({ctx.author.id}) || Reason: {reason}')
				else:
					await ctx.send(f"{ctx.author.mention} **{member.name}** already unmuted :')")
			except Exception as e:
				pass

			await asyncio.sleep(0.25)

	@commands.command(brief="Remove the mentioned to role to mentioned/id member")
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	async def unrole(self, ctx, member: discord.Member, role: discord.Role, *, reason:str=None):
		"""
		Remove the mentioned to role to mentioned/id member

		Syntax:
		`Unrole <User:Mention/ID> <Role:Mention/ID> [Reason:Text]`

		Permissions:
		Need Manage Roles permission, for both the user and the bot.

		NOTE: The bot will role role indiscriminately, means it does not care about the role hierarchy, as long as the bot itself has the power to do the give roles, and the target role is below the Bot role. It is adviced that Bot role should be just below the Moderator/Staff role.
		"""
		guild = ctx.guild
		for member in member:
			if guild.me.top_role < member.top_role:
				await ctx.send(f"{ctx.author.mention} can't give the role to {member.name} as it's role is above the bot")
			try:
				await member.remove_roles(role, reason=f"Action requested by {ctx.author.name}({ctx.author.id}) || Reason: {reason}")
				await ctx.send(f"{ctx.author.mention} removed {role.name}({role.id}) from {member.name}")
			except Exception as e:
				pass
			await asyncio.sleep(0.25)


	@commands.command(pass_context = True,)
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(embed_links=True)
	@commands.cooldown(3, 30, commands.BucketType.guild)
	@commands.guild_only()
	async def warn(self,ctx,member:discord.User, *, reason:str):
		'''To warn a user'''
		with open('reports.json', encoding='utf-8') as f:
			try:
				report = json.load(f)
			except ValueError:
				report = {}
				report['users'] = []

		for current_guild in report['reports']:
			if (current_guild['guild_id'] == ctx.guild.id) and (current_guild['name'] == member.id):
				current_guild['reasons'].append(reason)
				break
		else:
			report['reports'].append({
				'guild_id':ctx.guild.id,
				'name':member.id,
				'reasons': [reason,]
			})
		with open('reports.json', 'w+') as f:
			json.dump(report, f)

		try:
			await member.send(f"{member.name}#{member.discriminator} you are being warned for {reason}")
		except Exception as e:
			await ctx.send(f"{member.name}#{member.discriminator} you are being warned for {reason}")
			pass


	@commands.command(pass_context = True)
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(embed_links=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	async def warnings(self, ctx, member:discord.User):
		"""To see the number of times the user is being warned"""
		with open('reports.json', encoding='utf-8') as f:
			report = json.load(f)
		for current_guild in report['reports']:
			if ( current_guild['guild_id'] == ctx.guild.id ) and ( current_guild['name'] == member.id ):
				await ctx.send(f"{member.name} has been reported {len(current_guild['reasons'])} times : {', '.join(current_guild['reasons'])}")
				break
		else:
			await ctx.send(f"{member.name} has never been reported")


	@commands.command()
	@commands.has_permissions(kick_members=True)
	@commands.bot_has_permissions(embed_links=True)
	@commands.guild_only()
	@commands.cooldown(3, 30, commands.BucketType.guild)
	async def clearwarn(seld, ctx, member:discord.User):
		'''To clear all the warning from the user'''
		with open('reports.json', 'r', encoding='utf-8') as f:
			report = json.load(f)
		for current_guild in report['reports']:
			if member.id == current_guild['name']:
				if ( current_guild['guild_id'] == ctx.guild.id ) and ( current_guild['name'] == member.id ):
					current_guild['reasons'] = []
					await ctx.send(f"{ctx.author.mention} cleared all the warning from {member.name}")
					break
			else:
				await ctx.send(f"{ctx.author.mention} {member.name} never being reported")
		with open('reports.json','w+') as f:
			json.dump(report,f)


def setup(bot):
	bot.add_cog(mod(bot))