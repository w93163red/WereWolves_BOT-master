from wxpy import *
import pyttsx3
import io
import time

'''
语音包
chinese_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0"
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)
engine.setProperty('voice', chinese_id)
engine.say('天黑请闭眼')
engine.say('狼人请睁眼')
engine.say('狼人请闭眼')
engine.say('女巫请睁眼')
engine.say('女巫请闭眼')
engine.say('预言家请睁眼')
engine.say('预言家请闭眼')
engine.say('猎人请睁眼，你的开枪状态是')
engine.runAndWait()
#engine.say("Close your eyes")
#engine.say("Werewolves' Turn, give me the number")
#engine.say("Witch's Turn")
#engine.say("Hunter's Turn")
#engine.say("Seer's turn")
'''


Room_ID = '@@baebce92053b339c9af8ee3fbfb8cfda23d4b23f15ecb94b976d9010fe292796'

bot = Bot(cache_path="True")
myself = bot.self
while(1):
    if len(bot.messages) > 0:
        print(bot.messages[0].text)
        bot.messages = bot.messages[1:]