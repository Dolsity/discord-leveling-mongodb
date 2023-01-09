from os import getenv
from nextcord.ext import commands
from utils import create_collection, increase_xp_guild, bot_owner_ids, bot_prefix
import nextcord
from extensions import initial_extensions

class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    async def on_message(self, message : nextcord.Message):
        await create_collection(guild_id=message.guild.id)
        await self.process_commands(message)

        if message.author.bot:
            return

        await increase_xp_guild(guild_id=message.guild.id, user_id=message.author.id)

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = Bot(command_prefix=bot_prefix, owner_ids = set(bot_owner_ids), intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(
        f'Logged in as {bot.user} ({bot.user.id}) ({nextcord.__version__})'
    )

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(getenv('TOKEN'), reconnect=True)