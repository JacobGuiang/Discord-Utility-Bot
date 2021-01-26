import discord
from discord.ext import commands
from PyDictionary import PyDictionary
from random import getrandbits

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

COMMAND_LIST = ['coinflip', 'define']
MAX_FLIPS = 1000000
DESCRIPTIONS = {
    'coinflip': f'Flip a coin a number of times.\n\n**Format:** $coinflip <number>\n\n*<number> must be greater than 0 and less than {MAX_FLIPS}.*\n\n**Example:** $coinflip 999',
    'define': 'Define a word.\n\n**Format:** $define <word>\n\n**Example:** $define glacier'
}

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	status = discord.Game('$help')
	await client.change_presence(activity=status)

@client.command()
async def help(ctx, *args):
	response = ''
	if args and len(args) == 1 and args[0] in DESCRIPTIONS.keys():
		response = DESCRIPTIONS[args[0]]
	else:
		response = 'Type "$help <command>" to learn about a command.\n**Example:** $help coinflip\n\nAvailable commands:'
		for c in COMMAND_LIST:
			response += f'\n\t{c}'
	await ctx.send(response)

@client.command()
async def coinflip(ctx, *args):
	response = ''
	if not args or len(args) != 1 or not args[0].isdigit() or int(args[0] > MAX_FLIPS or int(args[0]) < 1):
		response = DESCRIPTIONS['coinflip']
	else:
		if args[0] == '1':
			if getrandbits(1):
				result = 'heads'
			else:
				result = 'tails'
			response = f'Flipping a coin.\nLanded on {result}.'
		else:
			heads_count = 0
			tails_count = 0
			for i in range(int(args[0])):
				if getrandbits(1):
					heads_count += 1
				else:
					tails_count += 1
			total = heads_count + tails_count
			response = f'Flipping a coin {total} times.\nLanded on heads {heads_count} times.\nLanded on tails {tails_count} times.'
	await ctx.send(response)

@client.command()
async def define(ctx, *args):
	response = ''
	if not args or len(args) > 1:
		response = DESCRIPTIONS['define']
	else:
		word = args[0]
		dictionary = PyDictionary(word)
		definitions = dictionary.meaning(word)
		if definitions is None:
			response = f'"{word}" is not a word.'
		else:
			response = f'Defining "{word}"\n\n'
			for word_type, defs in definitions.items():
				if len(defs) > 0:
					response += f'*{word_type}*\n'
					count = 1
					num_defs = len(defs)
					for d in defs:
						response += '\t'
						if num_defs > 1:
							response += f'{count}. '
							count += 1
						response += f'{d}'
						if '(' in d:
							response += ')'
						response += '\n'
					response += '\n'
			synonyms = dictionary.synonym(word)
			if synonyms is not None:
				response += f'*Similar*\n\t'
				for s in range(len(synonyms)-1):
					response += f'{synonyms[s]}, '
				response += f'{synonyms[-1]}'
	await ctx.send(response)

client.run('token')
