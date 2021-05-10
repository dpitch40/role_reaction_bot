# Role Reaction Bot

This is a very simple, lightweight Discord bot that allows members of a server to add or remove themselves from roles by reacting to 

## How it Works

The bot lists for activity on a channel called #roles. (The expected name is currently not changeable) This channel is assumed to be restricted for most server members so they can't post messages or add reactions.

Specifically, the bot looks for messages in this channel consisting of a series of lines, each containing an emoji and a role mention. When such a message is added or edited, it will automatically add a reaction to the message for each detected emoji. Example:

![Role message example](screenshots/role_message_example.png)

Users can then add a reaction to any of the generated emoji to be added to/removed from the corresponding role.

## Commands

Currently only one command, `inrole`, is implemented.

### `$inrole`

Enter the command `$inrole`, then mention one or more roles. The bot will list the members that belong to each role.

![$inrole example](screenshots/inrole_example.png)
