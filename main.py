import discord
import asyncio
import os
from discord.ext import commands
from commands.track import ThreadTracker
from dotenv import load_dotenv

load_dotenv()

# defining intents
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True

# initialize bot with intents
bot = commands.Bot(command_prefix="thread!", intents=intents)

# Load the bot token from the .env file
TOKEN = os.getenv("DISCORD_TOKEN")

# main async function to run the bot
async def main():
    async with bot:
        await bot.add_cog(ThreadTracker(bot))
        await bot.start(TOKEN)

# run the main function
asyncio.run(main())