import asyncio
import random
import os
import subprocess
import io

import discord


async def main(message, arg):

    arg = arg.replace('```tex', '').replace('```', '')
    fid = str(random.SystemRandom().randint(10000, 99999))
    here = os.path.dirname(__file__)

    with open(f'{here}/tex_template/tex.tex', 'r') as f:
        tex_con = f.read().replace('[REPLACE]', arg.strip())
    
    if '\\input' in tex_con or '\\include' in tex_con or '\\csname' in tex_con:
        embed = discord.Embed(
            title='使用できない文字列が含まれています\\Contains a string that cannot be used',
            color=0xff0000
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(embed=embed)

    with open(f'/tmp/' + fid + '.tex', 'w') as f:
        f.write(tex_con)

    try:
        _ = subprocess.run(['uplatex', '-halt-on-error', '-output-directory=/tmp', '/tmp/' + fid + '.tex'], timeout=5)
        dvipdfmx = subprocess.run(['dvipdfmx', '-q', '-o', '/tmp/' + fid + '.pdf', '/tmp/' + fid + '.dvi'], timeout=5)
    except subprocess.TimeoutExpired:
        embed = discord.Embed(
            title='タイムアウト Timeout',
            color=0xff0000
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(embed=embed)

    if dvipdfmx.returncode != 0:
        with open('/tmp/' + fid + '.log', 'r') as f:
            err = f.read().split('!')[1].split('Here')[0]
        embed = discord.Embed(
            title='エラー Error',
            description=f'```\n{err}\n```',
            color=0xff0000
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(embed=embed)
    
    _ = subprocess.run(['pdfcrop', '/tmp/' + fid + '.pdf', '--margins', '4 4 4 4'])
    pdftoppm = subprocess.run(['pdftoppm', '-png', '-r', '800', '/tmp/' + fid + '-crop.pdf'], stdout=subprocess.PIPE)

    embed = discord.Embed(color=0x008000)
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    embed.set_image(url=f'attachment://tex.png')
    return await message.channel.send(file=discord.File(io.BytesIO(pdftoppm.stdout), filename='tex.png'), embed=embed)
