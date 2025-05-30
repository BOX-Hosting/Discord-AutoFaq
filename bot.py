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

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Server online")
    print(f"✅  Бот {bot.user} запущен!")
    await bot.change_presence(
        status=status_mapping.get(config.STATUS, discord.Status.online),
        activity=discord.Game(name=config.STATUS_TEXT)
    )
    await bot.load_extension("cogs.faq")

bot.run(config.DISCORD_TOKEN)
