import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from PyDictionary import PyDictionary
from random import getrandbits
import requests
import json
from pprint import pprint

client = discord.Client()
slash = SlashCommand(client, sync_commands=True)

DISCORD_KEY = 'NzQ5MTA2MTQyOTQ0Mjk3MDIw.X0nJdg.MLpArywr1Om8hYO9B-6FN8cAy-k'
WEATHER_KEY = '50dee7e0d1221c08d5c0bf5aa2ae848d'

DESCRIPTIONS = {
    'coinflip': 'Flip a coin a number of times.\n\n**Format:** /coinflip <number>\n\n*<number> must be greater than 0 and less than or equal to 1000000.*\n\n**Example:** /coinflip 999',
    'define': 'Define a word.\n\n**Format:** /define <word>\n\n**Example:** /define glacier',
    'weather': 'Display current weather for a city.\n\n**Format:** /weather <city>\n\n**Example:** /weather austin'
}

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  status = discord.Game('/help')
  await client.change_presence(activity=status)

@slash.slash(name='help',
             description='Get information on available commands.',
             options=[
               create_option(
                 name='command',
                 description='Which command would you like to learn about?',
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name='coinflip',
                    value='coinflip'
                  ),
                  create_choice(
                    name='define',
                    value='define'
                  ),
                  create_choice(
                    name='weather',
                    value='weather'
                  )
                ]
               )
             ])
async def help(ctx, command):
  await ctx.send(DESCRIPTIONS[command])

@slash.slash(name='coinflip',
             description='Flip a coin a number of times.',
             options=[
               create_option(
                name='number',
                description='Enter the number of times you want to flip a coin.',
                option_type=4,
                required=True
               )
             ])
async def coinflip(ctx, number):
  response = ''
  if number < 0 or number > 1000000:
    response = 'Number must be greater than 0 or less than or equal to 1000000'
  else:
    if number == 1:
      if getrandbits(1):
        result = 'heads'
      else:
        result = 'tails'
      response = f'Flipping a coin.\nLanded on {result}.'
    else:
      heads_count = 0
      tails_count = 0
      for i in range(number):
        if getrandbits(1):
          heads_count += 1
        else:
          tails_count += 1
      response = f'Flipping a coin {number} times.\nLanded on heads {heads_count} times.\nLanded on tails {tails_count} times.'
  await ctx.send(response)

@slash.slash(name='define',
             description='Define a word.',
             options=[
               create_option(
                name='word',
                description='Enter the word you want the definition of.',
                option_type=3,
                required=True
               )
             ])
async def define(ctx, word):
  response = ''
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

@slash.slash(name='weather',
             description='Display current weather for a city.',
             options=[
               create_option(
                name='city',
                description='Enter the city you want the weather of.',
                option_type=3,
                required=True
               )
             ])
async def weather(ctx, city):
  response = ''
  city = city.replace(' ', '%20')
  url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=imperial'
  data = json.loads(requests.get(url).content)
  if data['cod'] == 200:
    response = f'__Weather in {data["name"]}__\n\n'
    temp_data = data["main"]
    response += f'{data["weather"][0]["description"].title()}\n'
    response += f'**Feels like:** {temp_data["feels_like"]} °F\n'
    response += f'**Temperature:** {temp_data["temp"]} °F\n'
    response += f'**High:** {temp_data["temp_max"]} °F\n'
    response += f'**Low:** {temp_data["temp_min"]} °F\n'
  else:
    response = f'{data["message"]}\n'
  await ctx.send(response)

client.run(DISCORD_KEY)
