import os

import discord

here = os.path.dirname(__file__)


async def main(message: discord.Message, arg: str):

    if os.path.exists(f'{here}/saved_codes/{message.author.id}.json'):
        os.remove(f'{here}/saved_codes/{message.author.id}.json')
        embed = discord.Embed(
            title='Deleted',
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.display_avatar.url
        )
        return await message.reply(embed=embed)
    else:
        embed = discord.Embed(
            title='Code not saved',
            color=0xff0000,
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.display_avatar.url
        )
        return await message.reply(embed=embed)
