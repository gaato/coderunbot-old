import base64
import io
import urllib.parse

import aiohttp
import discord


async def main(message: discord.Message, arg: str):

    arg = arg.replace('```tex', '').replace('```', '')

    url = 'http://localhost:5000/tex/' + urllib.parse.quote(arg, safe='')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                result = await r.json()
            else:
                embed = discord.Embed(
                    title='接続エラー Connection Error',
                    description=f'{r.status}',
                    color=0xff0000,
                )
                return await message.reply(embed=embed)

    if result['status'] == 0:
        embed = discord.Embed(color=0x008000)
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url,
        )
        return await message.reply(
            file=discord.File(
                io.BytesIO(base64.b64decode(result['result'])),
                filename='tex.png',
                spoiler=True,
            ),
            embed=embed,
        )
    elif result['status'] == 1:
        embed = discord.Embed(
            title='レンダリングエラー Rendering Error',
            description=f'```\n{result["error"]}\n```',
            color=0xff0000,
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url,
        )
        return await message.reply(embed=embed)
    elif result['status'] == 2:
        embed = discord.Embed(
            title='タイムアウト',
            color=0xff0000,
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url,
        )
        return await message.reply(embed=embed)
    else:
        embed = discord.Embed(
            title='未知のエラー Unknown Error',
            color=0xff0000,
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url,
        )
        return await message.reply(embed=embed)
