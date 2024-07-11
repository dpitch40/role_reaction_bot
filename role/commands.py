import itertools

import discord

from .role_reaction_bot import client, DEFAULT_CHANNEL_NAME

def parse_color_string(s):
    s = s.strip('#').lower()
    if len(s) != 6:
        raise ValueError("Invalid color string format")
    r_hex = s[:2]
    g_hex = s[2:4]
    b_hex = s[4:]
    try:
        r = int(r_hex, 16)
    except ValueError:
        raise ValueError("Invalid color string format")
    try:
        g = int(g_hex, 16)
    except ValueError:
        raise ValueError("Invalid color string format")
    try:
        b = int(b_hex, 16)
    except ValueError:
        raise ValueError("Invalid color string format")
    return r, g, b


def is_assignable(role):
    # Returns None if the role is assignable, a reason otherwise
    if role.is_bot_managed():
        return "You can't fool me, you aren't a bot"
    if role.is_premium_subscriber():
        return "Nice try, cheapskate"
    if role.is_integration() or not role.is_assignable():
        return "Can't apply this role"
    return None

@client.slash_command(description="Check who has a pingable role")
async def inrole(ctx,
    role: discord.Option(
        discord.SlashCommandOptionType.role,
        description="The role to check",
        required=True),
):
    members = role.members
    joined_names = '\n'.join(sorted([f'> {member.name}' for member in members]))
    message = f'{len(members)} members have role @{role.name}:\n{joined_names}'
    await ctx.respond(message)

# @client.command()
# async def get_roles_channel(ctx):
#     channel_name = client.role_channels.get(ctx.guild.name, DEFAULT_CHANNEL_NAME)
#     for channel in ctx.guild.channels:
#         if channel.name == channel_name:
#             await ctx.send(f'The current roles channel being watched is {channel.mention}')
#             break
#     else:
#         await ctx.send(f'The current roles channel being watched is {channel_name} (not found)')

# @client.command()
# async def set_roles_channel(ctx, new_name):
#     if not ctx.author.permissions_in(ctx.message.channel).administrator:
#         await ctx.send(f"I'm sorry {ctx.author.display_name}, I'm afraid I can't do that. (Because you aren't admin)")
#         return
#     channel_name = client.role_channels.get(ctx.guild.name, DEFAULT_CHANNEL_NAME)
#     for channel in ctx.guild.channels:
#         if channel.name == new_name:
#             client.update_channel_mapping(ctx.guild, new_name)
#             await ctx.send(f'Set roles channel to {channel.mention}')
#             break
#     else:
#         await ctx.send(f'Channel named {new_name} not found')

@client.application_command(description="Create a new pingable role")
async def create_role(ctx,
    name: discord.Option(
        discord.SlashCommandOptionType.string,
        description="The name of the role to add",
        required=True),
    # character: discord.Option(
    #     discord.SlashCommandOptionType.string,
    #     description="Character(s) the role pertains to",
    #     required=True),
    color: discord.Option(
        discord.SlashCommandOptionType.string,
        description="Role color, in #xxxxxx format",
        required=True),
    # description: discord.Option(
    #     discord.SlashCommandOptionType.string,
    #     description="Additional description of the role",
    #     required=False),
):
    for role in ctx.guild.roles:
        if role.name == name:
            await ctx.respond(f"Role @{role.name} already exists")
            break
    else:
        # Create role
        try:
            r, g, b = parse_color_string(color)
        except ValueError as exc:
            return await ctx.respond(str(exc))

        color = discord.Colour.from_rgb(r, g, b)
        role = await ctx.guild.create_role(name=name, colour=color, hoist=True, mentionable=True)
        await ctx.respond(f"Created role {role.mention}!")

@client.slash_command(description="Give yourself a pingable role")
async def apply_role(ctx,
    role: discord.Option(
        discord.SlashCommandOptionType.role,
        description="The role to add",
        required=True),
):
    if assignable := is_assignable is not None:
        return await ctx.respond(assignable)
    await ctx.author.add_roles(role)
    await ctx.respond(f"Added you to {role.name}")

@client.slash_command(description="Remove a pingable role from yourself")
async def remove_role(ctx,
    role: discord.Option(
        discord.SlashCommandOptionType.role,
        description="The role to remove",
        required=True),
):
    if assignable := is_assignable is not None:
        return await ctx.respond(assignable)
    await ctx.author.remove_roles(role)
    await ctx.respond(f"Removed you from {role.name}")
