import demo
from Grupp1 import main as Grupp1main
from Grupp2 import main as Grupp2main


class message:
    def __init__(self, team:demo.teamEnum, giver:demo.Entity, taker:demo.Entity, action):
        self.receiver = team
        self.giver = giver
        self.taker = taker
        self.action = action


class messageHandler:
    messages = []

    def sendMsg(self, msg):
        messages.Append(msg)

    def distributeMsg(self):
        for _ in len(messages):
            current_msg = messages.pop()
            if current_msg.receiver == demo.teamEnum.GRUPP_1:
                Grupp1main.HandleMessage(current_msg)
            
            else:
                Grupp2main.HandleMessage(current_msg)