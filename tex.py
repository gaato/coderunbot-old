import base64
import io
import urllib

import discord
import aiohttp


async def response(message: discord.Message, arg: str, command: str, spoiler: bool):

    async with message.channel.typing():

        arg = arg.replace('```tex', '').replace('```', '')

        url = f'http://localhost/{command}/' + urllib.parse.quote(arg, safe='')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    result = await r.json()
                else:
                    embed = discord.Embed(
                        title='Connection Error',
                        description=f'{r.status}',
                        color=0xff0000,
                    )
                    return await message.reply(embed=embed)

        if result['status'] == 0:
            embed = discord.Embed(color=0x008000)
            embed.set_author(
                name=message.author.name,
                icon_url=message.author.display_avatar.url,
            )
            if command != 'texpdf':
                embed.set_image(url='attachment://tex.png')
            return await message.reply(
                file=discord.File(
                    io.BytesIO(base64.b64decode(result['result'])),
                    filename='tex.pdf' if command == 'texpdf' else 'tex.png',
                    spoiler=spoiler,
                ),
                embed=embed,
            )
        elif result['status'] == 1:
            embed = discord.Embed(
                title='Rendering Error',
                description=f'```\n{result["error"]}\n```',
                color=0xff0000,
            )
            embed.set_author(
                name=message.author.name,
                icon_url=message.author.display_avatar.url,
            )
            return await message.reply(embed=embed)
        elif result['status'] == 2:
            embed = discord.Embed(
                title='Timed Out',
                color=0xff0000,
            )
            embed.set_author(
                name=message.author.name,
                icon_url=message.author.display_avatar,
            )
            return await message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title='Unhandled Error',
                color=0xff0000,
            )
            embed.set_author(
                name=message.author.name,
                icon_url=message.author.display_avatar.url,
            )
            return await message.reply(embed=embed)