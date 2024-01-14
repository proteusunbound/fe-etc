"""Data"""
import math
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

@anvil.server.portable_class
class ActiveUnit:
    """Active Unit"""

    def __init__(self, keyword):
        self.char = app_tables.fe4_unit_stats.get(Name=keyword)
        self.name = self.char["Name"]
        self.maxhp = self.char["HP"]
        self.strength = self.char["Str"]
        self.magic = self.char["Mag"]
        self.skill = self.char["Skl"]
        self.speed = self.char["Spd"]
        self.defense = self.char["Def"]
        self.luck = self.char["Lck"]
        self.resistance = self.char["Res"]
        self.followup = self.char["Follow-Up"]
        self.hitpoints = 0
        self.doubles = False
        self.damage = 0
        self.hit = 0
        self.attack = 0

@anvil.server.portable_class
class ActiveWeapon:
    """Active Weapon"""

    def __init__(self, keyword):
        weapon = app_tables.fe4_weapon_stats.get(Name=keyword)
        self.name = weapon["Name"]
        self.might = weapon["Mgt"]
        self.weight = weapon["Wgt"]
        self.hit = weapon["Hit"]

@anvil.server.portable_class
class ActiveBoss:
    """Active Boss"""

    def __init__(self, keyword):
        boss = app_tables.fe4_boss_stats.get(Name=keyword)
        self.name = boss["Name"]
        self.maxhp = boss["HP"]
        self.strength = boss["Str"]
        self.magic = boss["Mag"]
        self.skill = boss["Skl"]
        self.speed = boss["Spd"]
        self.luck = boss["Lck"]
        self.defense = boss["Def"]
        self.resistance = boss["Res"]
        self.followup = boss["Follow-Up"]
        self.hitpoints = 0
        self.doubles = False
        self.damage = 0
        self.hit = 0
        self.attack = 0
        self.avoid = 0
        self.hitchance = 0

def attack_speed(keyword, weapon):
    """Attack Speed"""
    keyword.AS = keyword.speed - weapon.weight

def hitrate(keyword, weapon):
    """Hit Rate"""
    keyword.hit = keyword.skill * 2 + weapon.hit

def get_attack(keyword, weapon):
    """Attack"""
    keyword.attack = keyword.strength + weapon.might

def physdamage(attacker, defender):
    """Physical Damage"""
    attacker.damage = max(0, attacker.attack - defender.defense)

@anvil.server.portable_class
class DuelSim:
    """Duel Simulator"""

    def __init__(self):
        self.dueltext = ""
        self.hitno = 0
        self.avoidno = 0
        self.iniavo = 0
        self.unithit = 0
        self.unitavoid = 0

    def setunit(self, unit):
        """Set Unit"""
        self.unit = ActiveUnit(unit)

    def setboss(self, boss):
        """Set Boss"""
        self.boss = ActiveBoss(boss)

    def setunitweapon(self, weapon):
        """Set Unit Weapon"""
        self.unitweapon = ActiveWeapon(weapon)

    def setbossweapon(self, weapon):
        """Set Boss Weapon"""
        self.bossweapon = ActiveWeapon(weapon)

    def setunithp(self, hitpoints):
        """Set Unit HP"""
        self.unit.hitpoints = hitpoints

    def setavoidno(self, avoidno):
        """Set Avoid Number"""
        self.avoidno = avoidno
        self.iniavo = avoidno

    def setbosshp(self, hitpoints):
        """Set Boss HP"""
        self.boss.hitpoints = hitpoints

    def unitdisplay(self):
        """Unit Stat Display"""
        attack_speed(self.unit, self.unitweapon)
        hitrate(self.unit, self.unitweapon)

    def bossdisplay(self):
        """Boss Stat Display"""
        attack_speed(self.boss, self.bossweapon)
        hitrate(self.boss, self.bossweapon)

    def enemy_avoid(self):
      """Enemy Avoid"""
      self.boss.avoid = (self.boss.AS) * 2 + self.boss.luck

    def bosshitchance(self):
      """Boss Hit Chance"""
      hitchance = min(((self.boss.hit - ((self.unit.AS) * 2 + self.unit.luck)) / 100), 1)
      self.boss.hitchance = max(0, hitchance)

    def precombat(self):
      """Pre-Combat Calculation"""
      get_attack(self.unit, self.unitweapon)
      physdamage(self.unit, self.boss)
      self.enemy_avoid()
      get_attack(self.boss, self.bossweapon)
      physdamage(self.boss, self.unit)
      self.bosshitchance()
      self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)
      self.unitavoid = 1 - self.boss.hitchance

    def doubling(self):
        """Doubling Calculation"""
        if self.unit.AS > self.boss.AS and self.unit.followup is True:
            self.unit.doubles = True
            self.boss.doubles = False
            self.dueltext += f"{self.unit.name} can make follow-up attacks. \n"
        elif self.boss.AS > self.unit.AS and self.boss.followup is True:
            self.boss.doubles = True
            self.unit.doubles = False
            self.dueltext += f"{self.boss.name} can make follow-up attacks. \n"
        else:
            self.unit.doubles = False
            self.boss.doubles = False

    def unitattack(self):
        """Unit Attack"""
        self.hitno += 1
        self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
        self.dueltext += f"{self.unit.name}'s attack leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"

    def bossmiss(self):
        """Boss Miss"""
        self.dueltext += f"{self.boss.name}'s attack misses.\n"

    def bossattack(self):
        """Boss Attack"""
        self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
        self.dueltext += f"{self.boss.name}'s attack leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"

    def playerphase(self):
        """Player Phase"""
        self.dueltext += "#### Player Phase:\n"
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            self.unitattack()
        if self.boss.hitpoints > 0 and self.unit.hitpoints > 0:
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            else:
                self.bossattack()
        if self.unit.doubles is True and self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            self.unitattack()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            else:
                self.bossattack()
        self.dueltext += "\n"

    def enemyphase(self):
        """Enemy Phase"""
        self.dueltext += "#### Enemy Phase:\n"
        if self.boss.hitpoints > 0 and self.unit.hitpoints > 0:
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            else:
                self.bossattack()
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            self.unitattack()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            else:
                self.bossattack()
        if (
            self.unit.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            self.unitattack()
        self.dueltext += "\n"

    def reset_text(self):
        """Reset"""
        self.dueltext = ""