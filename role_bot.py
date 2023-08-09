import os
import argparse

from role.role_reaction_bot import client
import role.commands

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', action='store_true')
    args = parser.parse_args()

    if args.dev:
        token = os.environ['DISCORD_DEV_TOKEN']
    else:
        token = os.environ['DISCORD_TOKEN']
    client.run(token)

if __name__ == '__main__':
    main()
