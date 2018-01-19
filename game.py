import random
import time
import pyttsx3
import queue
import threading
import win32com.client
import os

qinfo = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
q1info = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
computer_name = os.getenv('COMPUTERNAME')
qinfo.FormatName="direct=os:"+computer_name+"\\PRIVATE$\\123"
q1info.FormatName = "direct=os:"+computer_name+"\\PRIVATE$\\321"
rec_q = qinfo.Open(1, 0)
send_q = q1info.Open(2, 0)

chinese_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0"
engine = pyttsx3.init()
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
engine.setProperty('volume', volume+0.25)
engine.setProperty('rate', rate-80)
engine.setProperty('voice', chinese_id)

class Game:
    players_no = 12
    seer = 1
    witch = 1
    hunter = 1
    idiot = 0
    punk = 1
    villager = 4
    werewolves = 4
    live_mask = 1 << players_no
    player_list = []
    healing_potion = 1
    poison_potion = 1
    kill = 0
    heal = 0
    poison = 0
    Punks_model = 0
    msg = None

    def reset(self):
        self.seer = 1
        self.witch = 1
        self.hunter = 1
        self.idiot = 0
        self.punk = 1
        self.villager = 4
        self.werewolves = 4
        self.live_mask = 1 << self.players_no
        self.healing_potion = 1
        self.poison_potion = 1
        self.kill = 0
        self.heal = 0
        self.poison = 0
        self.Punks_model = 0

    def print_gameinfo(self):
        print("-------------------------------")
        for player in self.player_list:
            print("%s\t%s\t%s" % (player.id, player.role, player.life))
        print("-------------------------------")

    def receive_msg(self):
        msg = rec_q.receive()
        return msg.Body

    def send(self, m):
        msg=win32com.client.Dispatch("MSMQ.MSMQMessage")
        msg.Label = ""
        msg.Body = m
        msg.Send(send_q)


class Player:
    name = ""
    id = 0
    life = True
    role = ""
    uuid = None
    def __init__(self, name, id, role):
        self.name = name
        self.id = id
        self.role = role


#TODO: Still need to change this function to adapt the wechat
def register(game):
    # for i in range(1, 5):
    #     player = Player(str(i), i, "Villager")
    #     game.player_list.append(player)
    # for i in range(5, 9):
    #     player = Player(str(i), i, "Werewolves")
    #     game.player_list.append(player)
    # game.player_list.append(Player("9", 9, "Seer"))
    # game.player_list.append(Player("10", 10, "Witch"))
    # game.player_list.append(Player("11", 11, "Hunter"))
    # game.player_list.append(Player("12", 12, "Punk"))
    # game.print_gameinfo()
    #for i in range(0, game.players_no):
    for i in range(0, game.players_no):
        msg = game.receive_msg()  #号码 身份 "1 狼人"
        if (len(msg.text.split(' ')) != 2):
            i = i-1
            game.send("格式错误，注册无效 请重新输入")
            continue
        id = int(msg.text.split(' ')[0])
        if msg.text.split(' ')[1] == "狼人":
            role = "Werewolves"
        elif msg.text.split(' ')[1] == "村民" or msg.text.split(' ')[1] == "平民":
            role = "Villager"
        elif msg.text.split(' ')[1] == "预言家":
            role = "Seer"
        elif msg.text.split(' ')[1] == "女巫":
            role = "Witch"
        elif msg.text.split(' ')[1] == "猎人":
            role = "Hunter"
        elif msg.text.split(' ')[1] == "混混":
            role = "Punk"
        else:
            msg.sender.send('身份有误 请重新输入')
            i = i-1
            continue
        print(msg.sender.name, id, role)
        game.player_list.append(Player(msg.sender.name, id, role))
        game.send("注册成功")

def Punk_turn(game):
    #TODO: for wechat model, it should input twice.
    engine.say("混混请睁眼，将爹的号码发送给法官")
    engine.runAndWait()
    punk = None
    for player in game.player_list:
        if player.role == "Punk":
            punk = player

    # punk = game.bot.friends().search('LinG')
    # punk = game.bot.friends().search(player.uuid)
    # punk = ensure_one(punk)
    game.send('选择一个号码作为你的榜样')
    number = int(game.receive_msg())
    game.Punks_model = number
    engine.say("混混请闭眼")
    engine.runAndWait()
    time.sleep(5)

def Werewolves_turn(game):
    engine.say("狼人请睁眼")
    engine.runAndWait()
    wolveslist = []
    for player in game.player_list:
        if player.role == "Werewolves":
            wolveslist.append(player)
    for player in wolveslist:
        game.send("请告诉我你要刀的号码")
    game.kill = int(game.receive_msg())
    engine.say("狼人请闭眼")
    engine.runAndWait()
    time.sleep(5)

def Seer_turn(game):
    #TODO: Still not the true seer, use dummy instead, need to be changed.
    number = 0
    engine.say("预言家请睁眼")
    engine.runAndWait()
    seer = None
    for player in game.player_list:
        if player.role == "Seer":
            seer = player

    # seer = game.bot.friends().search('bj')
    # seer = ensure_one(seer)
    # while True:
    #     seer.send('请选择你要验的人')
    #     number1 = game.receive_msg().text
    #     seer.send('确定是这个号码吗？（输入相同号码即为确定）')
    #     number2 = game.receive_msg().text
    #     if number1 == number2:
    #         number = number1
    #         break
    game.send('请选择你要验的人')
    number = int(game.receive_msg())
    for i in game.player_list:
        if i.id == number:
            if i.role == "Werewolves":
                game.send("%s 的身份是狼人" % i.id)
            else:
                game.send("%s 的身份是好人" % i.id)
    engine.say("预言家请闭眼")
    engine.runAndWait()
    time.sleep(5)

def Witch_turn(game):
    engine.say("女巫请睁眼")
    engine.runAndWait()

    witch = None
    for player in game.player_list:
        if player.role == "Witch":
            witch = player
    # witch = game.bot.friends().search('LinG') #TODO: change the name
    # witch = ensure_one(witch)

    if game.healing_potion == 1:
        game.send("%d 今晚死了" % game.kill)
    else:
        game.send("他今晚死了")

    game.send('是否使用解药（输入0表示不用药）')
    number = int(game.receive_msg())
    game.heal = number
    if game.heal != 0:
        if game.healing_potion == 0:
            game.send("你没解药了")
            game.heal = 0
        else:
            game.healing_potion = 0
    if game.heal == 0:
        game.send("是否使用毒药(输入0表示不用药）")
        number = int(game.receive_msg())
        game.poison = number
        if game.poison != 0:
            if game.poison_potion == 0:
                game.send("你没有毒药了")
                game.poison = 0
            else:
                game.poison_potion = 0
    engine.say("女巫请闭眼")
    engine.runAndWait()
    time.sleep(5)

def Hunter_turn(game):
    engine.say("猎人请睁眼")
    engine.runAndWait()
    hunter = None
    for player in game.player_list:
        if player.role == "Hunter":
            hunter = player
    if game.poison != hunter.id:
        game.send("你可以开枪")
    else:
        game.send("你不可以开枪")

    engine.say("猎人请闭眼")
    engine.runAndWait()
    time.sleep(5)

def badge(game):
    before = len(game.bot.messages)
    engine.say("请要上警的玩家在3秒内发 1 给法官")
    engine.runAndWait()
    time.sleep(3)
    badge_list = set()
    for i in range(before, len(game.bot.messages)):
        for player in game.player_list:
            if game.bot.messages[i].sender == player.uuid:
                badge_list.add(player.id)
                break
    words = " ".join(str(x) for x in badge_list)
    engine.say("上警的玩家有："+ words)
    engine.runAndWait()


def game_controller():
    game = Game()
    #game.reset()
    # reservation = ensure_one(game.bot.groups().search('Reservation'))
    # reservation.send("法官已就绪，请发送“号码 身份”至法官注册")
    register(game)
    engine.say("天黑请闭眼")
    engine.runAndWait()
    Punk_turn(game)
    Werewolves_turn(game)
    Seer_turn(game)
    Witch_turn(game)
    Hunter_turn(game)

    engine.say("天亮了")
    engine.runAndWait()
    #badge(game)
    msg = game.receive_msg()

    if msg.text == "报死讯":
        if game.kill == game.heal:
            engine.say("昨天晚上平安夜")
        else:
            if game.poison != 0:
                engine.say("昨天晚上%s %s死了"%(game.kill, game.poison) )
                for player in game.player_list:
                    if player == game.kill or player == game.poison:
                        player.life = False
            else:
                engine.say("昨天晚上%s 死了"% game.kill)
        game.print_gameinfo()
    engine.runAndWait()
    # msg = game.receive_msg()
    # print(msg.text)
    # # register(game)
    # day = 1
    # while True:
    #     if day == 1:
    #         Punk_turn(game)
    #     Werewolves_turn(game)
    #     Seer_turn(game)
    #     Witch_turn(game)
    #     Hunter_turn(game)



if __name__ == "__main__":
    game_controller()
