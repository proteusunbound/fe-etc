"""Combat"""
import math
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import fe5data

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
            self.duels[i] = fe5data.DuelSim()

    def combatround(self):
        """Combat Round"""
        for number, name in self.duels.items():
            if name.unit.hitpoints > 0 and self.bosshp > 0:
                name.setbosshp(self.bosshp)