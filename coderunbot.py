import asyncio
import os
import traceback
from collections import OrderedDict
from importlib import import_module
import logging
import random

import discord

from config import DISCORD_TOKEN, PREFIX, SERVER_URL, INVITE_URL


# dictionary to adjust size automatically
class LimitedSizeDict(OrderedDict):


    def __init__(self, *args, **kwds):

        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):

        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):

        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


client = discord.Client()

# save the author of the message the bot sent
message_id_to_author_id = LimitedSizeDict(size_limit=100
# link user's message to the bot's message
user_message_id_to_bot_message = LimitedSizeDict(size_limit=100)

                                          
@client.event
async def on_ready():
    print('It\'s activated')


@client.event
async def on_message(message):
    await reply(message)


@client.event
async def on_message_edit(before, after):

    # if the sent message is a call to the bot
    if before.id in user_message_id_to_bot_message:
        try:
            # delete the bot message
            await globals()['user_message_id_to_bot_message'][before.id].delete()
        except discord.errors.NotFound:
            pass
    # respond to the edited messege
    await reply(after)


@client.event
async def on_reaction_add(reaction, user):

    if user == client.user:
        return

    # if the reacted message is the bot's
    # and the person who reacted is the person who typed the command
    if reaction.message.author == client.user \
        and reaction.message.id in message_id_to_author_id \
        and user.id == message_id_to_author_id[reaction.message.id]:

        if str(reaction.emoji) in ('🚮', '✖️', '🗑️'):
            await reaction.message.delete()


# respond to the sent command
async def reply(message):

    # if the author is a bot other than PythonBot and botphilia
    if message.author.bot:
        return

    if message.content.startswith(PREFIX):

        command = message.content.split()[0][len(PREFIX):]
        arg = message.content[len(PREFIX) + len(command):].lstrip()

        # if the command file exists atthe specified location
        if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/commands/command_{command}.py'):

            tmp_module = import_module(f'commands.command_{command}')
            async with message.channel.typing():
                try:
                    sent_message = await tmp_module.main(message, arg)
                except discord.Forbidden:
                    return
                except Exception as e:
                    logging.exception(e)
                    embed = discord.Embed(
                        title='内部エラー Internal Error',
                        description='公式サーバーで報告してください\nReport it on the official server\n'
                            + SERVER_URL,
                        color=0xff0000
                    )
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    sent_message = await message.channel.send(embed=embed)
                # save the author of the message the bot sent
                message_id_to_author_id[sent_message.id] = message.author.id
                # link user's message to the bot's message
                user_message_id_to_bot_message[message.id] = sent_message
                await sent_message.add_reaction('🚮')
                if random.randrange(100) == 0:
                    embed = discord.Embed(
                        title='招待リンク Invitation Link',
                        description=INVITE_URL
                    )
                    await message.channel.send(embed=embed)
                elif random.randrange(100) == 0:
                    embed = discord.Embed(
                        title='公式サーバー Official Serever',
                        description=SERVER_URL
                    )
                    await message.channel.send(embed=embed)


client.run(DISCORD_TOKEN)
