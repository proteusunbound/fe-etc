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
    self.successrate = 1
    self.etc = 0
    self.duels = {}

  def set_turns(self, turnno):
    """Set Turns"""
    self.turns = turnno
  
  def setduels(self, duelno):
    """Set Duels"""
    for i in range(0, duelno):
      self.duels[i] = data.DuelSim()

  def combatround(self):
    """Combat Round"""
    for number, name in self.duels.items():
      if name.unit.hitpoints > 0:
        name.setbosshp(self.bosshp)
        name.playerphase()
        self.bosshp = name.boss.hitpoints
        self.text += name.dueltext
        name.reset_text()
    for number, name in self.duels.items():
      if self.bosshp > 0 and name.unit.hitpoints > 0:
        if name.boss.maxhp > self.bosshp and name.terrain is True:
          self.bosshp = min(self.bosshp + 10, name.boss.maxhp)
          self.text += "%s heals to %d HP at the start of the round.\n" % (name.boss.name, self.bosshp)
          break
    for number, name in self.duels.items():
      if name.unit.hitpoints > 0 and name.boss.counter is True:
        name.setbosshp(self.bosshp)
        name.enemyphase()
        self.bosshp = name.boss.hitpoints
        self.text += name.dueltext
        name.reset_text()
        break
                
  def battle(self):
    """Battle"""
    for self.turn in range(self.turns):
      if self.turn == 0:
        self.bosshp = self.duels[0].boss.hitpoints
      self.combatround()
      self.turn += 1
    for number, name in self.duels.items():
      self.successrate *= ((name.unithit ** name.hitno) * (name.unitavoid ** name.avoidno) * (name.unitcrit ** name.critno) * (name.unitdodge ** name.ddgno))
    self.etc = self.turns / (self.successrate)
    self.text += (
      "This outcome has a %.2f chance of occurring. The Estimated Turn Count is %.2f."
      % (self.successrate, self.etc)
    )
    return self.text

  def reset(self):
    """Reset"""
    for number, name in self.duels.items():
      name.hitno = 0
    self.text = ""