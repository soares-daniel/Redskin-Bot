import os

from bot.bot import PRDBot
from settings import DISCORD_BOT_TOKEN

if not os.path.exists("./logs"):
    os.makedirs("./logs")
    with open("./logs/discord.log", "w") as file:
        pass


bot = PRDBot()

for filename in os.listdir("./bot/cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"bot.cogs.{filename[:-3]}")

bot.run(DISCORD_BOT_TOKEN)
