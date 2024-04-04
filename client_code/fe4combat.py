"""Combat"""
import math
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import fe4data


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
            self.duels[i] = fe4data.DuelSim()

    def combatround(self):
        """Combat Round"""
        for number, name in self.duels.items():
            if name.unit.hitpoints > 0 and self.bosshp > 0:
                name.setbosshp(self.bosshp)
                name.hprecover()
                name.hpthreshold()
                if "Vantage" in name.boss.skills and name.boss.hitpoints < (
                    name.boss.maxhp / 2
                ):
                    self.text += f"{name.boss.name} activates Vantage. \n"
                    name.enemyphase()
                else:
                    name.playerphase()
                    name.accost()
                self.bosshp = name.boss.hitpoints
                self.text += name.dueltext
                name.reset_text()
        for number, name in self.duels.items():
            if self.bosshp > 0 and name.unit.hitpoints > 0:
                if name.boss.maxhp > self.bosshp and name.terrain is True:
                    self.bosshp = min(
                        self.bosshp + (math.floor(0.2 * name.boss.maxhp) - 1),
                        name.boss.maxhp,
                    )
                    self.text += f"{name.boss.name} heals to {self.bosshp} HP at the start of the round.\n"
                if "Renewal" in name.boss.skills and name.boss.maxhp > self.bosshp:
                    self.bosshp = min(self.bosshp + 10, name.boss.maxhp)
                    self.text += f"{name.boss.name} heals to {self.bosshp} HP at the start of the round. \n"
                break
        for number, name in self.duels.items():
            if name.unit.hitpoints > 0 and self.bosshp > 0:
                name.setbosshp(self.bosshp)
                name.hpthreshold()
                if "Vantage" in name.unit.skills and name.unit.hitpoints < (
                    name.unit.maxhp / 2
                ):
                    self.text += f"{name.unit.name} activates Vantage. \n"
                    name.playerphase()
                else:
                    name.enemyphase()
                    name.accost()
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
            self.successrate *= (
                (name.unithit**name.hitno)
                * (name.unitavoid**name.iniavo)
                * (name.unitcrit**name.inicrit)
                * (name.unitdodge**name.iniddg)
                * (name.unit.accostrate)
                * (name.unit.adeptrate**name.iniadept)
                * (name.unit.adeptcancel**name.inicanceladept)
                * (name.unit.solrate**name.inisol)
                * (name.unit.lunarate**name.iniluna)
                * (name.unit.astrarate**name.iniastra)
                * (name.unit.pavisecancel**name.cancelpaviseno)
                * (name.unit.paviserate**name.inipavise)
            )
        self.etc = self.turns / (self.successrate)
        self.text += f"This outcome has a {self.successrate: 0.2f} chance of occurring. The Estimated Turn Count is {self.etc: 0.2f}."
        return self.text

    def reset(self):
        """Reset"""
        for number, name in self.duels.items():
            name.hitno = 0
            name.cancelpaviseno = 0
        self.text = ""
        self.successrate = 1
