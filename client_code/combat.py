import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import data
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#
@anvil.server.portable_class
class CombatSim:
  """Combat Sim"""
  def __init__(self):
    self.text = ""
    self.turns = 0
    self.bosshp = 0
    self.turn = 0
    self.rate1 = 0
    self.rate2 = 0
    self.rate3 = 0
    self.successrate = 0
    self.etc = 0

  def set_turns(self, turnno):
    """Set Turns"""
    self.turns = turnno
  
  def setduels(self):
    """Set Duels"""
    self.duel1 = data.DuelSim()
    self.duel2 = data.DuelSim()
    self.duel3 = data.DuelSim()
    def combatround(self):
        """Combat Round"""
        if self.duel1.unit.hitpoints > 0:
            self.duel1.setbosshp(self.bosshp)
            self.duel1.playerphase()
            self.bosshp = self.duel1.boss.hitpoints
            self.text += self.duel1.dueltext
            self.duel1.reset_text()
        if self.duel2.unit.hitpoints > 0:
            self.duel2.setbosshp(self.bosshp)
            self.duel2.playerphase()
            self.bosshp = self.duel2.boss.hitpoints
            self.text += self.duel2.dueltext
            self.duel2.reset_text()
        if self.duel3.unit.hitpoints > 0:
            self.duel3.setbosshp(self.bosshp)
            self.duel3.playerphase()
            self.bosshp = self.duel3.boss.hitpoints
            self.text += self.duel3.dueltext
            self.duel3.reset_text()
        if self.bosshp > 0 and (self.duel1.unit.hitpoints > 0 or self.duel2.unit.hitpoints > 0 or self.duel3.unit.hitpoints > 0):
            if self.duel3.boss.maxhp > self.bosshp and self.duel3.terrain is True:
                self.bosshp = min(self.bosshp + 10, self.duel3.boss.maxhp)
                self.text += "%s heals to %d HP at the start of the round.\n" % (self.duel3.boss.name, self.bosshp)
            if self.duel1.unit.hitpoints > 0 and self.duel1.boss.counter is True:
                self.duel1.setbosshp(self.bosshp)
                self.duel1.enemyphase()
                self.bosshp = self.duel1.boss.hitpoints
                self.text += self.duel1.dueltext
                self.duel1.reset_text()
            elif self.duel2.unit.hitpoints > 0 and self.duel2.boss.counter is True:
                self.duel2.setbosshp(self.bosshp)
                self.duel2.enemyphase()
                self.bosshp = self.duel2.boss.hitpoints
                self.text += self.duel2.dueltext
                self.duel2.reset_text()
            elif self.duel3.unit.hitpoints > 0 and self.duel3.boss.counter is True:
                self.duel3.setbosshp(self.bosshp)
                self.duel3.enemyphase()
                self.bosshp = self.duel3.boss.hitpoints
                self.text += self.duel3.dueltext
                self.duel3.reset_text()
    def battle(self):
        """Battle"""
        self.turn = 0
        for self.turn in range(self.turns):
            if self.turn == 0:
                self.bosshp = self.duel1.boss.hitpoints
            self.combatround()
            self.turn += 1
        self.rate1 = (self.duel1.unithit ** self.duel1.hitno) * (self.duel1.unitavoid ** self.duel1.avoidno) * (self.duel1.unitcrit ** self.duel1.critno) * (self.duel1.unitdodge ** self.duel1.ddgno)
        self.rate2 = (self.duel2.unithit ** self.duel2.hitno) * (self.duel2.unitavoid ** self.duel2.avoidno) * (self.duel2.unitcrit ** self.duel2.critno) * (self.duel2.unitdodge ** self.duel2.ddgno)
        self.rate3 = (self.duel3.unithit ** self.duel3.hitno) * (self.duel3.unitavoid ** self.duel3.avoidno) * (self.duel3.unitcrit ** self.duel3.critno) * (self.duel3.unitdodge ** self.duel3.ddgno)
        self.successrate = self.rate1 * self.rate2 * self.rate3
        self.etc = self.turns / (self.successrate)
        self.text += (
        "This outcome has a %.2f chance of occurring. The Estimated Turn Count is %.2f."
        % (self.successrate, self.etc)
        )
        return self.text
    def reset(self):
        """Reset"""
        self.text = ""
        self.duel1.hitno = 0
        self.duel2.hitno = 0
        self.duel3.hitno = 0
  
