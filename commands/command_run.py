import json
import os
import random
import re

import aiohttp
import discord

url = 'https://wandbox.org/api/compile.json'
here = os.path.dirname(__file__)

async def main(message, arg):

    with open(f'{here}/languages.json', 'r') as f:
        language_dict = json.load(f)
    arg = re.sub(r'```[A-z\-\+]*\n', '', arg).replace('```', '')    
    language = arg.split()[0]
    code = arg.replace(language, '', 1).lstrip(' \n')
    language = language.lower().replace('pp', '++').replace('sharp', '#').replace('clisp', 'lisp').replace('lisp', 'clisp')
    if not language in language_dict.keys():
        embed = discord.Embed(
            title='以下の言語に対応しています\nThe following languages are supported',
            description=', '.join(language_dict.keys()),
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.channel.send(embed=embed)
    params = {
        'compiler': language_dict[language],
        'code': code,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as r:
            if r.status == 200:
                result = await r.json()
            else:
                embed = discord.Embed(
                    title='接続エラー Connection Error',
                    description=f'{r.status}',
                    color=0xff0000
                )
                return await message.channel.send(embed=embed)
    
    embed = discord.Embed(title='実行結果 Result')
    embed_color = 0xff0000
    files = []
    for item in result.items():
        if item[0] in ('program_message', 'compiler_message'):
            continue
        if item[0] == 'status' and item[1] == '0':
            embed_color = 0x007000
        if len(item[1]) > 1000 or len(item[1].split('\n')) > 100:
            files.append(
                discord.File(
                    io.StringIO(item[1]),
                    item[0] + '.txt'
                )
            )
        else:
            embed.add_field(
                name=item[0],
                value='```\n' + item[1] + '\n```',
            )
    embed.color = embed_color
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.channel.send(embed=embed, files=files)
