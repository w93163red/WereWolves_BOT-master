from wxpy import *

bot = Bot(cache_path=True)

before = len(bot.messages)
while len(bot.messages) - before == 0:
    pass
print(bot.messages[-1])

