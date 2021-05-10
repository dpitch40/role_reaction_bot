"""Very simple Discord bot to allow server members to add and remove themselves from roles by
   reacting to messages in a #roles channel.

Permissions needed:

    manage_messages
    send_messages
    manage_roles

Also requires server members intent.
"""

import re
import collections

import discord
from discord.ext import commands

from role import logger

intents = discord.Intents.default()
intents.members = True

CHANNEL_NAME = 'roles'

def channel_match(channel):
    return channel.name == CHANNEL_NAME

def parse_emoji(message):
    guild = message.guild
    roles = [guild.get_role(role_id) for role_id in message.raw_role_mentions]
    id_mapping = {str(role.id): role for role in roles}
    role_re = re.compile(f"<@&({'|'.join(i for i in id_mapping)})>")

    emoji_to_role_mapping = collections.OrderedDict()
    for line in message.content.strip().split('\n'):
        line = line.strip()
        m = role_re.search(line)
        if m:
            role = id_mapping[m.group(1)]
            line = line.replace(m.group(0), '').strip()
            emoji_to_role_mapping[line] = role

    logger.info('Parsed %d emoji from message by @%s', len(emoji_to_role_mapping), message.author.name)
    logger.debug(str(dict(emoji_to_role_mapping)))

    return emoji_to_role_mapping

async def update_message_reactions(message):
    logger.info('Updating reactions for message by @%s in #%s', message.author.name,
        message.channel.name)
    await message.clear_reactions()
    # Scan through the message to find all emoji used
    emoji_to_role_mapping = parse_emoji(message)
    for emoji in emoji_to_role_mapping.keys():
        await message.add_reaction(emoji)

# Event handlers

class RoleReactionClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$', intents=intents)

    async def on_ready(self):
        logger.info('Logged in as %s', self.user)

    async def on_message(self, message):
        await super().on_message(message)
        logger.debug('ON_MESSAGE')
        if channel_match(message.channel):
            await update_message_reactions(message)

    async def on_raw_message_edit(self, payload):
        logger.debug('ON_RAW_MESSAGE_EDIT')
        channel = self.get_channel(payload.channel_id)
        if channel_match(channel):
            message = await channel.fetch_message(payload.message_id)
            await update_message_reactions(message)

    async def on_raw_reaction_add(self, payload):
        logger.debug('ON_RAW_REACTION_ADD')
        channel = self.get_channel(payload.channel_id)
        if channel_match(channel):
            member = payload.member
            if member == self.user:
                return

            message = await channel.fetch_message(payload.message_id)
            emoji = payload.emoji

            emoji_to_role_mapping = parse_emoji(message)
            if emoji.name in emoji_to_role_mapping:
                role = emoji_to_role_mapping[emoji.name]

                if role in member.roles:
                    logger.info('Removing role @%s from @%s', role.name, member.name)
                    await member.remove_roles(role, reason='Role bot')
                else:
                    logger.info('Adding role @%s to @%s', role.name, member.name)
                    await member.add_roles(role, reason='Role bot')
            else:
                logger.warning('Unrecognized reaction: %s', emoji)

            await message.remove_reaction(emoji, member)

    async def on_raw_reaction_remove(self, payload):
        logger.debug('ON_RAW_REACTION_REMOVE')
        channel = self.get_channel(payload.channel_id)
        if channel_match(channel):
            guild = self.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member != self.user:
                return

            message = await channel.fetch_message(payload.message_id)
            await update_message_reactions(message)

client = RoleReactionClient()