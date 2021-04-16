import os
import json

import discord

with open(os.path.dirname(__file__) + '/../config.json', 'r') as f:
    config_dict = json.load(f)

HELP_URL = config_dict['help_url']


async def main(message: discord.Message, arg: str):

    embed = discord.Embed(
        title='使い方 Help',
        description=HELP_URL
    )
    return await message.reply(embed=embed)
