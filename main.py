import discord
import os

client = discord.Client()

@client.event
async def on_ready():
  print(f"We have logged in as {client}")

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("Hello"):
    await message.channel.send("World!")

my_secret = os.environ['TOKEN']
client.run(my_secret)
