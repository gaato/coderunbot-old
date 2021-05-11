'''
    CodeRunBot - Discord Bot
    Copyright (C) 2021 Gakuto Furuya

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import os
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
message_id_to_author_id = LimitedSizeDict(size_limit=100)
# link user's message to the bot's message
user_message_id_to_bot_message = LimitedSizeDict(size_limit=100)

here = os.path.dirname(os.path.abspath(__file__))


@client.event
async def on_ready():
    print('It\'s activated')


@client.event
async def on_message(message: discord.Message):
    await reply(message)


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):

    # if user message has an embed
    if before.content == after.content:
        return

    global user_message_id_to_bot_message
    # if the sent message is a call to the bot
    if before.id in user_message_id_to_bot_message:
        try:
            # delete the bot message
            await user_message_id_to_bot_message[before.id].delete()
        except discord.errors.NotFound:
            pass
    # respond to the edited messege
    await reply(after)


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):

    if payload.user_id == client.user.id:
        return

    # if the reacted message is the bot's
    # and the person who reacted is the person who typed the command
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.author == client.user \
            and message.id in message_id_to_author_id \
            and payload.user_id == message_id_to_author_id[message.id]:
        if str(payload.emoji) == '🚮':
            await message.delete()


# respond to the sent command
async def reply(message: discord.Message):

    # if the author is a bot other than PythonBot and botphilia
    if message.author.bot:
        return

    if message.content.startswith(PREFIX):

        command = message.content.split()[0][len(PREFIX):]
        arg = message.content[len(PREFIX) + len(command):].lstrip()

        # if the command file exists atthe specified location
        if os.path.exists(f'{here}/commands/command_{command}.py'):

            command_module = import_module(f'commands.command_{command}')
            async with message.channel.typing():
                try:
                    sent_message = await command_module.main(message, arg)
                except discord.Forbidden:
                    return
                except Exception as e:
                    logging.exception(e)
                    embed = discord.Embed(
                        title='内部エラー Internal Error',
                        description='公式サーバーで報告してください\n'
                                    'Report it on the official server\n'
                                    + SERVER_URL,
                        color=0xff0000
                    )
                    embed.set_author(
                        name=message.author.name,
                        icon_url=message.author.avatar_url
                    )
                    sent_message = await message.reply(embed=embed)
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
                    await message.reply(embed=embed)
                elif random.randrange(100) == 0:
                    embed = discord.Embed(
                        title='公式サーバー Official Serever',
                        description=SERVER_URL
                    )
                    await message.reply(embed=embed)


client.run(DISCORD_TOKEN)
