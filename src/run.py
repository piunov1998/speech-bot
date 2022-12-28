import io
import os

import discord
from discord.utils import get
from discord.ext import commands
from discord import app_commands

import speech
#
MY_GUILD = discord.Object(id=358780693595291652)
#
#
# class Bot(discord.Client):
#     def __init__(self):
#         super().__init__(intents=discord.Intents.default())
#         self.tree = app_commands.CommandTree(self)
#
#     async def setup_hook(self):
#         self.tree.copy_global_to(guild=MY_GUILD)
#         await self.tree.sync(guild=MY_GUILD)


class Bot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='bro, ', intents=intents)

    async def setup_hook(self):
        await self.tree.sync(guild=MY_GUILD)


bot = Bot()


@bot.event
async def on_ready():
    print('Started')


@bot.hybrid_command('say', with_app_command=True)
@app_commands.guilds(MY_GUILD)
@commands.has_permissions(administrator=True)
async def say(ctx: commands.Context, text: str):
    try:
        await connect(ctx)
    except AttributeError:
        await ctx.reply('Connect to a voice channel before playing.')
        return

    raw = speech.text_to_speech(text)
    source = speech.save(raw)

    def after_play(_):
        speech.delete(source)

    ctx.voice_client.play(
        discord.FFmpegPCMAudio(str(source.absolute())),
        after=after_play
    )

    await ctx.reply(text)


async def connect(ctx: commands.Context):
    status = get(bot.voice_clients, guild=ctx.guild)
    if not status:
        await ctx.author.voice.channel.connect()


async def disconnect(ctx: commands.Context):
    await ctx.voice_client.disconnect(force=False)


# @bot.tree.command(name='info')
# async def info(interaction: discord.Interaction):
#     resp: discord.InteractionResponse = interaction.response  # noqa
#     await resp.send_message('буду разговаривать')


if __name__ == '__main__':
    bot.run(token=os.getenv('TOKEN'))
