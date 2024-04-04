import discord
from discord.ext import tasks
from Utils.data import Data
from os import getenv, listdir
from time import time

class Bot(discord.Bot):
    def __init__(self):
        self.data = Data()
        intents = discord.Intents.default()
        super().__init__(intents=intents)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="Questions"))
        self.send_daily_question.start()
        print("Bot is ready")

    @tasks.loop(seconds=60)
    async def send_daily_question(self): 
        next_question_time = self.data.get_next_question_time()
        if not next_question_time:
            self.data.set_next_question_time(time() + 60 * 60 * 24)
            return
        
        next_question_time = int(float(next_question_time.decode("utf-8")))
        
        if next_question_time > time():
            return
        channel_id = self.data.get_channel()
        if not channel_id:
            return
        channel = self.get_channel(int(channel_id))
        if not channel:
            return
        question = self.data.get_random_question_and_remove()
        if not question:
            return
        question = question.decode("utf-8")
        message = await channel.send(f"<@&1193292211698274484> \n <:LGS:1206330526323966012> QUESTION OF THE DAY <:LGS:1206330526323966012> \n {question} \n Drop your answers in the attached thread below")
        
        await message.create_thread(name="Answers")

        self.data.set_next_question_time(time() + 60 * 60 * 24)


bot = Bot()


for filename in listdir("Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

bot.run(getenv("Token"))