"""Very simple Discord bot to allow server members to add and remove themselves from roles by
   reacting to messages in a #roles channel.

Permissions needed:

    send_messages
    read_message_history
    add_reactions
    manage_messages
    manage_roles

Also requires server members intent.
"""

import os
import re
import collections
import os.path
import json

import discord
from discord.ext import commands
from .emoji import load_emoji

from role import logger

intents = discord.Intents.default()
intents.members = True

DEFAULT_CHANNEL_NAME = 'roles'
ENGLISH_EMOJI = load_emoji()
CHANNEL_FILE = os.getenv('CHANNEL_FILE', 'role_channels.json')

# def parse_emoji(message):
#     guild = message.guild
#     roles = [guild.get_role(role_id) for role_id in message.raw_role_mentions]
#     id_mapping = {str(role.id): role for role in roles}
#     role_re = re.compile(f"<@&({'|'.join(i for i in id_mapping)})>")

#     emoji_to_role_mapping = collections.OrderedDict()
#     for line in message.content.strip().split('\n'):
#         line = line.strip()
#         m = role_re.search(line)
#         if m:
#             role = id_mapping[m.group(1)]
#             emoji = line.replace(m.group(0), '').strip()
#             if emoji not in ENGLISH_EMOJI:
#                 logger.warning('Invalid emoji for role %s: %s', role.name, emoji,
#                     extra={'guild': guild})
#                 continue
#             emoji_to_role_mapping[emoji] = role

#     logger.info('Parsed %d emoji/role pairs from message by @%s',
#         len(emoji_to_role_mapping), message.author.name, extra={'guild': guild})
#     logger.debug(str(dict(emoji_to_role_mapping)), extra={'guild': guild})

#     return emoji_to_role_mapping

# async def update_message_reactions(message):
#     logger.info('Updating reactions for message by @%s in #%s', message.author.name,
#         message.channel.name, extra={'guild': message.guild})
#     await message.clear_reactions()
#     # Scan through the message to find all emoji used
#     emoji_to_role_mapping = parse_emoji(message)
#     for emoji in emoji_to_role_mapping.keys():
#         await message.add_reaction(emoji)

# Event handlers

class RoleReactionClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$', intents=intents)
        self.channel_file = CHANNEL_FILE
        # self.get_channel_mapping()

    # def get_channel_mapping(self):
    #     if not os.path.isfile(self.channel_file):
    #         self.role_channels = dict()
    #         logger.info('Channel file not found at %s', self.channel_file)
    #     else:
    #         with open(self.channel_file, 'r') as fobj:
    #             self.role_channels = json.load(fobj)
    #             logger.info('Loaded %d role channels from %s', len(self.role_channels), self.channel_file)

    # def update_channel_mapping(self, guild, channel_name):
    #     if channel_name == DEFAULT_CHANNEL_NAME:
    #         logger.info('Resetting role channel for %s to default', guild.name)
    #         if guild.name in self.role_channels:
    #             del self.role_channels[guild.name]
    #     else:
    #         logger.info('Setting role channel for %s to %s', guild.name, channel_name)
    #         self.role_channels[guild.name] = channel_name
    #     with open(self.channel_file, 'w') as fobj:
    #         json.dump(self.role_channels, fobj, indent=2)
    #         logger.info('Saved %d role channels to %s', len(self.role_channels), self.channel_file)

    # def channel_match(self, channel):
    #     return channel.name == self.role_channels.get(channel.guild.name, DEFAULT_CHANNEL_NAME)

    async def on_ready(self):
        logger.info('Logged in as %s', self.user)

    # async def on_message(self, message):
    #     await super().on_message(message)
    #     logger.debug('ON_MESSAGE', extra={'guild': message.guild})
    #     if self.channel_match(message.channel):
    #         await update_message_reactions(message)

    # async def on_raw_message_edit(self, payload):
    #     channel = self.get_channel(payload.channel_id)
    #     logger.debug('ON_RAW_MESSAGE_EDIT', extra={'guild': channel.guild})
    #     if self.channel_match(channel):
    #         message = await channel.fetch_message(payload.message_id)
    #         await update_message_reactions(message)

    # async def on_raw_reaction_add(self, payload):
    #     channel = self.get_channel(payload.channel_id)
    #     logger.debug('ON_RAW_REACTION_ADD', extra={'guild': channel.guild})
    #     if self.channel_match(channel):
    #         member = payload.member
    #         if member == self.user:
    #             return

    #         message = await channel.fetch_message(payload.message_id)
    #         emoji = payload.emoji

    #         emoji_to_role_mapping = parse_emoji(message)
    #         if emoji.name in emoji_to_role_mapping:
    #             role = emoji_to_role_mapping[emoji.name]

    #             if role in member.roles:
    #                 logger.info('Removing role @%s from @%s', role.name, member.name,
    #                     extra={'guild': channel.guild})
    #                 await member.remove_roles(role, reason='Role bot')
    #             else:
    #                 logger.info('Adding role @%s to @%s', role.name, member.name,
    #                     extra={'guild': channel.guild})
    #                 await member.add_roles(role, reason='Role bot')
    #         else:
    #             logger.warning('Unrecognized reaction: %s', emoji)

    #         await message.remove_reaction(emoji, member)

    # async def on_raw_reaction_remove(self, payload):
    #     channel = self.get_channel(payload.channel_id)
    #     logger.debug('ON_RAW_REACTION_REMOVE', extra={'guild': channel.guild})
    #     if self.channel_match(channel):
    #         guild = self.get_guild(payload.guild_id)
    #         member = guild.get_member(payload.user_id)
    #         if member != self.user:
    #             return

    #         message = await channel.fetch_message(payload.message_id)
    #         await update_message_reactions(message)

    async def on_error(self, event, *args, **kwargs):
        logger.error('Some bug happened %s', event, exc_info=True)

client = RoleReactionClient()
