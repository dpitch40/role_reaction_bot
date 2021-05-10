from .role_reaction_bot import client

@client.command()
async def inrole(ctx, *role):
    for role in ctx.message.role_mentions:
        members = role.members
        joined_names = '\n'.join(sorted([f'> {member.name}' for member in members]))
        message = f'{len(members)} members have role {role.mention}:\n{joined_names}'
        await ctx.send(message)
