from .role_reaction_bot import client, DEFAULT_CHANNEL_NAME

@client.command()
async def inrole(ctx, *args):
    role_name = ' '.join(args)
    role_name_lower = role_name.lower()
    for role in ctx.guild.roles:
        if role.name.lower() == role_name_lower:
            members = role.members
            joined_names = '\n'.join(sorted([f'> {member.name}' for member in members]))
            message = f'{len(members)} members have role @{role.name}:\n{joined_names}'
            await ctx.send(message)
            break
    else:
        await ctx.send(f'Role {role_name!r} not found')

@client.command()
async def get_roles_channel(ctx):
    channel_name = client.role_channels.get(ctx.guild.name, DEFAULT_CHANNEL_NAME)
    for channel in ctx.guild.channels:
        if channel.name == channel_name:
            await ctx.send(f'The current roles channel being watched is {channel.mention}')
            break
    else:
        await ctx.send(f'The current roles channel being watched is {channel_name} (not found)')

@client.command()
async def set_roles_channel(ctx, new_name):
    if not ctx.author.permissions_in(ctx.message.channel).administrator:
        await ctx.send(f"I'm sorry {ctx.author.name}, I'm afraid I can't do that. (Because you aren't admin)")
        return
    channel_name = client.role_channels.get(ctx.guild.name, DEFAULT_CHANNEL_NAME)
    for channel in ctx.guild.channels:
        if channel.name == new_name:
            client.update_channel_mapping(ctx.guild, new_name)
            await ctx.send(f'Set roles channel to {channel.mention}')
            break
    else:
        await ctx.send(f'Channel named {new_name} not found')
