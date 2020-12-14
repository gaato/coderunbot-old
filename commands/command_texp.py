import asyncio
import os
import subprocess
import io
import random

import discord


async def main(message, arg):

    arg = arg.replace('```tex', '').replace('```', '')
    here = os.path.dirname(__file__)

    with open(f'{here}/tex_template/texp.tex', 'r') as f:
        tex_con = f.read().replace('[REPLACE]', arg.strip())

    with open(f'/tmp/' + fid + '.tex', 'w') as f:
        f.write(tex_con)

    _ = subprocess.run(['uplatex', '-halt-on-error', '-output-directory=/tmp', '/tmp/' + fid + '.tex'])
    dvipdfmx = subprocess.run(['dvipdfmx', '-q', '-o', '/tmp/' + fid + '.pdf', '/tmp/' + fid + '.dvi'])

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
    convert1 = subprocess.run(['convert', '-', '-gravity', 'northwest', '-chop', '0x150', 'png:-'], input=pdftoppm.stdout, stdout=subprocess.PIPE)
    convert2 = subprocess.run(['convert', '-', '-gravity', 'southeast', '-chop', '0x200', 'png:-'], input=convert1.stdout, stdout=subprocess.PIPE)
    convert3 = subprocess.run(['convert', '-', '-background', '#FFFFFF', '-gravity', 'northwest', '-splice', '10x0', 'png:-'], input=convert2.stdout, stdout=subprocess.PIPE)
    convert4 = subprocess.run(['convert', '-', '-background', '#FFFFFF', '-gravity', 'southeast', '-splice', '10x0', 'png:-'], input=convert3.stdout, stdout=subprocess.PIPE)

    embed = discord.Embed(color=0x008000)
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    embed.set_image(url=f'attachment://tex.png')
    return await message.channel.send(file=discord.File(io.BytesIO(convert4.stdout), filename='tex.png'), embed=embed)
