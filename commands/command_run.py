import json
import os
import re
import io

import aiohttp
import discord

url = 'https://wandbox.org/api/compile.json'
here = os.path.dirname(__file__)


async def main(message: discord.Message, arg: str):

    with open(f'{here}/languages.json', 'r') as f:
        language_dict = json.load(f)
    arg = re.sub(r'```[A-z\-\+]*\n', '', arg).replace('```', '')
    language = arg.split()[0]
    code = arg.replace(language, '', 1).lstrip(' \n')
    language = language.lower() \
        .replace('pp', '++').replace('sharp', '#') \
        .replace('clisp', 'lisp').replace('lisp', 'clisp')
    if language not in language_dict.keys():
        embed = discord.Embed(
            title='以下の言語に対応しています',
            description=', '.join(language_dict.keys()),
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    if language == 'nim':
        compiler_option = '--hint[Processing]:off\n' \
            '--hint[Conf]:off\n' \
            '--hint[Link]:off\n' \
            '--hint[SuccessX]:off\n' \
            '--hint[BuildMode]:off'
    else:
        compiler_option = ''
    params = {
        'compiler': language_dict[language],
        'code': code,
        'compiler-option-raw': compiler_option,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as r:
            if r.status == 200:
                result = await r.json()
            else:
                embed = discord.Embed(
                    title='接続エラー',
                    description=f'{r.status}',
                    color=0xff0000
                )
                return await message.reply(embed=embed)

    embed = discord.Embed(title='実行結果')
    embed_color = 0xff0000
    files = []
    for k, v in result.items():
        if k in ('program_message', 'compiler_message'):
            continue
        if k == 'status' and v == '0':
            embed_color = 0x007000
        if language == 'nim' and k == 'compiler_error':
            v = re.sub(r'CC: \S+\n', '', v)
            if v == '':
                continue
        if len(v) > 1000 or len(v.split('\n')) > 100:
            files.append(
                discord.File(
                    io.StringIO(v),
                    k + '.txt'
                )
            )
        else:
            embed.add_field(
                name=k,
                value='```\n' + v + '\n```',
            )
    embed.color = embed_color
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.reply(embed=embed, files=files)
