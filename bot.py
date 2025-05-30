import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True

status_mapping = {
    "online": discord.Status.online,
    "idle": discord.Status.idle,
    "dnd": discord.Status.dnd,
    "invisible": discord.Status.invisible
}

activity_status = {
    "game": discord.Game(name=config.STATUS_TEXT),
    "stream": discord.Streaming(name=config.STATUS_TEXT, url=config.STATUS_URLSTREM),
    "watching": discord.Activity(type=discord.ActivityType.watching, name=config.STATUS_TEXT),
    "listening": discord.Activity(type=discord.ActivityType.listening, name=config.STATUS_TEXT)
}

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Server online")
    print(f"✅  Бот {bot.user} запущен!")
    await bot.change_presence(
        status=status_mapping.get(config.STATUS, discord.Status.online),
        activity=activity_status.get(config.ACTIVY, discord.Activity(type=discord.ActivityType.watching, name=config.STATUS_TEXT))
    )
    await bot.load_extension("cogs.faq")

bot.run(config.DISCORD_TOKEN)
