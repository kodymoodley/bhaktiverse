# bot.py
import os

import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Bhakti Verse Server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'hare krsna' in message.content.lower() or 'hare krishna' in message.content.lower():
        response = f'Hare Krsna {message.author}!'
        await message.channel.send(response)
    
    if message.content.lower()[:2] in ['sb', 'cc', 'bg'] and \
        len(message.content.split('.')) == 3:
            if len(message.content.split()) == 2:
                verse_type = message.content.lower().split()[1].strip()
                book = message.content.lower()[:2]
                parts = message.content.lower().split('.')
                first = parts[0].replace(book, '')
                second = parts[1]
                third = parts[2].split()[0].strip()
                suffix = ''
                if book == 'sb':
                    suffix = book+"/"+first+"/"+second+"/"+third
                if book == 'bg':
                    suffix = book+"/"+first+"/"+second
                page = requests.get("https://vedabase.io/en/library/"+suffix)
                soup_page = BeautifulSoup(page.content, 'html.parser')
                response = None
                if verse_type == 'v':
                    response = soup_page.select("div.wrapper-verse-text")[0]
                    sans = ''
                    for div in response.findChildren("div"):
                        sans += div.get_text(separator=' ', strip=True)
                    await message.channel.send(sans)
                elif verse_type == 't':
                    english = soup_page.select("div.r.r-lang-en.r-translation p")[0].get_text()
                    await message.channel.send(english)
            elif len(message.content.split()) == 1:
                book = message.content.lower().strip()[:2]
                parts = message.content.lower().strip().split('.')
                first = parts[0].replace(book, '')
                second = parts[1]
                third = parts[2].split()[0].strip()
                suffix = ''
                if book == 'sb':
                    print('heres3')
                    suffix = book+"/"+first+"/"+second+"/"+third
                if book == 'bg':
                    print('here')
                    suffix = book+"/"+first+"/"+second

                print('suffix: ', suffix)
                print("https://vedabase.io/en/library/"+suffix)
                page = requests.get("https://vedabase.io/en/library/"+suffix)
                soup_page = BeautifulSoup(page.content, 'html.parser')
                response = soup_page.select("div.wrapper-verse-text")[0]
                sans = ''
                for div in response.findChildren("div"):
                    sans += div.get_text(separator=' ', strip=True)
                await message.channel.send(sans)


client.run(TOKEN)