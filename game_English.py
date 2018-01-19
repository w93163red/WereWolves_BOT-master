from wxpy import *
import random
import time
import pyttsx3
import queue


# chinese_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0"
engine = pyttsx3.init()
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
engine.setProperty('volume', volume+0.25)
engine.setProperty('rate', rate-80)
# engine.setProperty('voice', chinese_id)

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
    bot = Bot(cache_path=True)
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
        before = len(self.bot.messages)
        while before - len(self.bot.messages) == 0:
            pass
        return self.bot.messages[-1]

class Player:
    name = ""
    id = 0
    life = True
    role = ""
    uuid = None
    def __init__(self, name, id, role, uuid):
        self.name = name
        self.id = id
        self.role = role
        self.uuid = uuid

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
            msg.sender.reply("Invalid Input! Please Input Again. ")
            continue
        id = int(msg.text.split(' ')[0])
        uuid = msg.sender
        if msg.text.split(' ')[1] == "狼人" or msg.text.split(' ')[1] == "Werewolves" or msg.text.split(' ')[1] == "werewolves":
            role = "Werewolves"
        elif msg.text.split(' ')[1] == "村民" or msg.text.split(' ')[1] == "平民" or msg.text.split(' ')[1] == 'Villager' \
                or msg.text.split(' ')[1] == 'villager':
            role = "Villager"
        elif msg.text.split(' ')[1] == "预言家" or msg.text.split(' ')[1] == 'Seer' or msg.text.split(' ')[1] == 'seer':
            role = "Seer"
        elif msg.text.split(' ')[1] == "女巫" or msg.text.split(' ')[1] == 'Witch' or msg.text.split(' ')[1] == 'witch':
            role = "Witch"
        elif msg.text.split(' ')[1] == "猎人" or msg.text.split(' ')[1] == 'Hunter' or msg.text.split(' ')[1] == 'hunter':
            role = "Hunter"
        elif msg.text.split(' ')[1] == "混混" or msg.text.split(' ')[1] == 'Punk' or msg.text.split(' ')[1] == 'Punk':
            role = "Punk"
        else:
            msg.sender.send('Invalid Input! Please Input Again.')
            i = i-1
            continue
        print(msg.sender.name, id, role, uuid)
        game.player_list.append(Player(msg.sender.name, id, role, uuid))
        uuid.send("Registration Successful!")

def Punk_turn(game):
    #TODO: for wechat model, it should input twice.
    engine.say("Punk open your eyes")
    engine.runAndWait()
    punk = None
    for player in game.player_list:
        if player.role == "Punk":
            punk = player

    # punk = game.bot.friends().search('LinG')
    # punk = game.bot.friends().search(player.uuid)
    # punk = ensure_one(punk)
    punk.uuid.send('Choose a number to be your model: ')
    number = int(game.receive_msg().text)
    game.Punks_model = number
    engine.say("Punk, close your eyes")
    engine.runAndWait()

def Werewolves_turn(game):
    engine.say("Werewolves, open your eyes")
    engine.runAndWait()
    wolveslist = []
    for player in game.player_list:
        if player.role == "Werewolves":
            wolveslist.append(player)
    for player in wolveslist:
        player.uuid.send("Pick one player to kill and send this player's number to me")
    game.kill = int(game.receive_msg().text)
    engine.say("Werewolves, close your eyes")
    engine.runAndWait()
    time.sleep(3)

def Seer_turn(game):
    #TODO: Still not the true seer, use dummy instead, need to be changed.
    number = 0
    engine.say("Seer, Open your eyes")
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
    seer.uuid.send('Pick a player to discover his real identity and tell me his number:')
    number = int(game.receive_msg().text)
    for i in game.player_list:
        if i.id == number:
            if i.role == "Werewolves":
                seer.uuid.send("%s is WEREWOLVES" % i.id)
            else:
                seer.uuid.send("%s is not a werewolves" % i.id)

    time.sleep(3)
    engine.say("预言家请闭眼")
    engine.runAndWait()

def Witch_turn(game):
    engine.say("Witch open your eyes")
    engine.runAndWait()

    witch = None
    for player in game.player_list:
        if player.role == "Witch":
            witch = player
    # witch = game.bot.friends().search('LinG') #TODO: change the name
    # witch = ensure_one(witch)

    if game.healing_potion == 1:
        witch.uuid.send("%d died" % game.kill)
    else:
        witch.uuid.send("someone died")

    witch.uuid.send("save him? (If yes, send the player's number; if no, send 0")
    number = int(game.receive_msg().text)
    game.heal = number
    if game.heal != 0:
        if game.healing_potion == 0:
            witch.uuid.send("You don't have cure potion.")
            game.heal = 0
        else:
            game.healing_potion = 0
    if game.heal == 0:
        witch.uuid.send("Eliminate? (If yes, send the player's number; if no, send 0)")
        number = int(game.receive_msg().text)
        game.poison = number
        if game.poison != 0:
            if game.poison_potion == 0:
                witch.uuid.send("You don't have poison potion.")
                game.poison = 0
            else:
                game.poison_potion = 0
    engine.say("Witch close your eyes")
    engine.runAndWait()
    time.sleep(3)

def Hunter_turn(game):
    engine.say("Hunter, open your eyes")
    engine.runAndWait()
    hunter = None
    for player in game.player_list:
        if player.role == "Hunter":
            hunter = player
    if game.poison != hunter.id:
        hunter.uuid.send("You can eliminate someone.")
    else:
        hunter.uuid.send("You cannot eliminate someone")

    engine.say("Hunter, close your eyes")
    engine.runAndWait()
    time.sleep(3)

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
    game.reset()
    # reservation = ensure_one(game.bot.groups().search('Reservation'))
    # reservation.send("法官已就绪，请发送“号码 身份”至法官注册")
    #register(game)
    engine.say("Night falls, everyone closes their eyes")
    engine.runAndWait()
    #Punk_turn(game)
    #Werewolves_turn(game)
    #Seer_turn(game)
    #Witch_turn(game)
    #Hunter_turn(game)

    engine.say("everyone opens your eyes")
    engine.runAndWait()
    #badge(game)
    msg = game.receive_msg()

    if msg.text == "报死讯":
        if game.kill == game.heal:
            engine.say("It's a peaceful night")
        else:
            if game.poison != 0:
                engine.say("number %s and %s died"%(game.kill, game.poison) )
                for player in game.player_list:
                    if player == game.kill or player == game.poison:
                        player.life = False
            else:
                engine.say("number %s died"% game.kill)
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
