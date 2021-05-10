import os

from role.role_reaction_bot import client
import role.commands

client.run(os.environ['DISCORD_TOKEN'])
