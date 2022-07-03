# -*- coding: utf8 -*-
import ast
import os
import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')
		print(f'[COG] {filename[:-3]} подключен!')

bot.run('token')