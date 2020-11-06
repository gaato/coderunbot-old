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

    cp = subprocess.run(["tex2jpg"], input=tex_con.encode('UTF-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if cp.returncode != 0:
        embed = discord.Embed(
            title='エラー Error',
            description=f'```\n{cp.stderr.decode("UTF-8")}\n```',
            color=0xff0000
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(color=0x008000)
        embed.set_image(url=f'attachment://tex.jpg')
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(file=discord.File(io.BytesIO(cp.stdout), filename="tex.jpg"), embed=embed)