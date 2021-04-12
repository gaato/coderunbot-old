import os
import json

import discord

with open(os.path.dirname(__file__) + '/../config.json', 'r') as f:
    config_dict = json.load(f)

INVITE_URL = config_dict['invite_url']

async def main(message, arg):

    embed = discord.Embed(
        title='招待 invite me',
        description=INVITE_URL
    )
    return await message.reply(embed=embed)
