import discord

from tex import response


async def main(message: discord.Message, arg: str):
    return await response(message, arg, 'png', False, True)
  