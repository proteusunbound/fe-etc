"""Data"""
import math
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import fe3support

supports = fe3support.supportlist

@anvil.server.portable_class
class ActiveUnit:
    """Active Unit"""

    def __init__(self, keyword):
        self.char = app_tables.fe3_unit_stats.get(Name=keyword)
        self.name = self.char["Name"]
        self.maxhp = self.char["HP"]
        self.strength = self.char["Str"]
        self.skill = self.char["Skl"]
        self.speed = self.char["Spd"]
        self.defense = self.char["Def"]
        self.luck = self.char["Lck"]
        self.resistance = self.char["Res"]
        self.charclass = self.char["Class"]
        self.hitpoints = 0
        self.doubles = False
        self.damage = 0
        self.hit = 0
        self.attack = 0
        self.supports = []
        self.supportbonus = 0

    def setsupports(self):
      if self.name in supports:
        for name, number in supports[self.name].items():
          self.supports.append(name)
      else:
        self.supports = ["None", "None"]

    def setsupportbonus(self, keyword, check):
      if check is True:
        self.supportbonus += supports[self.name][keyword]

@anvil.server.portable_class
class ActiveWeapon:
    """Active Weapon"""

    def __init__(self, keyword):
        weapon = app_tables.fe3_weapon_stats.get(Name=keyword)
        self.name = weapon["Name"]
        self.might = weapon["Mgt"]
        self.weight = weapon["Wgt"]
        self.hit = weapon["Hit"]
        self.crit = weapon["Crit"]
        self.minrange = weapon["Min Range"]
        self.maxrange = weapon["Max Range"]
        self.type = weapon["Type"]
        self.effco = 1

@anvil.server.portable_class
class ActiveBoss:
    """Active Boss"""

    def __init__(self, keyword):
        boss = app_tables.fe3_boss_stats.get(Name=keyword)
        self.name = boss["Name"]
        self.maxhp = boss["HP"]
        self.strength = boss["Str"]
        self.skill = boss["Skl"]
        self.speed = boss["Spd"]
        self.luck = boss["Lck"]
        self.defense = boss["Def"]
        self.resistance = boss["Res"]
        self.charclass = boss["Class"]
        self.hitpoints = 0
        self.doubles = False
        self.damage = 0
        self.hit = 0
        self.attack = 0
        self.avoid = 0
        self.hitchance = 0
        self.counter = False
        self.supportbonus = 0

def attack_speed(keyword, weapon):
    """Attack Speed"""
    keyword.AS = max(0, keyword.speed - weapon.weight)

def hitrate(keyword, weapon):
    """Hit Rate"""
    keyword.hit = keyword.skill * 2 + weapon.hit + keyword.supportbonus

def get_attack(keyword, weapon):
    """Attack"""
    keyword.attack = keyword.strength + weapon.might * weapon.effco

def critical(keyword, weapon):
  """Critical"""
  keyword.crit = keyword.skill + weapon.crit + keyword.supportbonus

def physdamage(attacker, defender):
    """Physical Damage"""
    attacker.damage = max(0, attacker.attack - defender.defense)

def magdamage(attacker, defender):
    """Magical Damage"""
    attacker.damage = max(1, attacker.attack - defender.resistance)

def effectiveness(weapon, keyword):
    """Effectiveness"""
    effcheck = app_tables.fe3_effectiveness.get(Name=weapon.name)
    if effcheck[keyword.charclass] is True:
        weapon.effco = 3
    else:
        weapon.effco = 1

@anvil.server.portable_class
class DuelSim:
    """Duel Simulator"""

    def __init__(self):
        self.dueltext = ""
        self.hitno = 0
        self.avoidno = 0
        self.iniavo = 0
        self.critno = 0
        self.inicrit = 0
        self.ddgno = 0
        self.iniddg = 0
        self.unithit = 0
        self.unitavoid = 0
        self.unitcrit = 0
        self.unitdodge = 0
        self.terrain = False

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

    def setcritno(self, critno):
        """Set Crit Number"""
        self.critno = critno
        self.inicrit = critno

    def setddgno(self, ddgno):
        """Set Dodge Number"""
        self.ddgno = ddgno
        self.iniddg = ddgno

    def setbosshp(self, hitpoints):
        """Set Boss HP"""
        self.boss.hitpoints = hitpoints

    def unitdisplay(self):
        """Unit Stat Display"""
        attack_speed(self.unit, self.unitweapon)
        hitrate(self.unit, self.unitweapon)
        critical(self.unit, self.unitweapon)

    def bossdisplay(self):
      """Boss Stat Display"""
      attack_speed(self.boss, self.bossweapon)
      hitrate(self.boss, self.bossweapon)
      critical(self.boss, self.bossweapon)

    def enemy_avoid(self):
      """Enemy Avoid"""
      if self.terrain is True:
        self.boss.avoid = self.boss.speed + self.boss.luck + 30
      else:
        self.boss.avoid = self.boss.speed + self.boss.luck

    def bosshitchance(self):
      """Boss Hit Chance"""
      self.boss.hitchance = min((self.boss.hit - (self.unit.speed + self.unit.luck + self.unit.supportbonus)) / 100, 1)

    def precombat(self):
      """Pre-Combat Calculation"""
      get_attack(self.unit, self.unitweapon)
      if self.unitweapon.type == "Magical":
        magdamage(self.unit, self.boss)
      else:
        physdamage(self.unit, self.boss)
      self.enemy_avoid()
      get_attack(self.boss, self.bossweapon)
      if self.bossweapon.type == "Magical":
        magdamage(self.boss, self.unit)
      else:
        physdamage(self.boss, self.unit)
      self.bosshitchance()
      self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)
      self.unitcrit = (self.unit.crit - self.boss.luck) / 100
      self.unitavoid = 1 - self.boss.hitchance
      self.unitdodge = 1 - max(0, (self.boss.crit - (self.unit.luck + self.unit.supportbonus)) / 100)

    def counterattack(self):
        """Counter Attack"""
        if self.bossweapon.name in ("Thunderbolt", "Arrowspate", "Stonehoist", "Hoistflamme", "Pachyderm"):
          self.boss.counter = False
          self.dueltext += f"{self.boss.name} cannot counter-attack. \n"
        elif self.bossweapon.minrange != self.bossweapon.maxrange:
            self.boss.counter = True
            self.dueltext += f"{self.boss.name} can counter-attack. \n"
        elif (
            self.bossweapon.minrange == self.unitweapon.minrange
            and self.bossweapon.maxrange == self.unitweapon.maxrange
        ):
            self.boss.counter = True
            self.dueltext += f"{self.boss.name} can counter-attack. \n"
        else:
            self.boss.counter = False
            self.dueltext += f"{self.boss.name} cannot counter-attack. \n"

    def effectivecheck(self):
        """Effectiveness Log"""
        effectiveness(self.unitweapon, self.boss)
        if self.unitweapon.effco == 3:
            self.dueltext += f"{self.unit.name}'s {self.unitweapon.name} deals effective damage against {self.boss.name}. \n"
        effectiveness(self.bossweapon, self.unit)
        if self.bossweapon.effco == 3:
            self.dueltext += f"{self.boss.name}'s {self.bossweapon.name} deals effective damage against {self.unit.name}. \n"
    
    def doubling(self):
        """Doubling Calculation"""
        if self.unit.AS >= (self.boss.AS + 3):
            self.unit.doubles = True
            self.boss.doubles = False
            self.dueltext += f"{self.unit.name} can make follow-up attacks. \n"
        elif self.boss.AS >= (self.unit.AS + 3):
            self.boss.doubles = True
            self.unit.doubles = False
            self.dueltext += f"{self.boss.name} can make follow-up attacks. \n"
        else:
          self.boss.doubles = False
          self.unit.doubles = False

    def unit_crit(self):
      """Unit Crit"""
      self.hitno += 1
      self.boss.hitpoints = max(0, self.boss.hitpoints - 3 * self.unit.damage)
      self.dueltext += f"{self.unit.name} lands a critical hit and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
  
    def unitattack(self):
      """Unit Attack"""
      self.hitno += 1
      self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
      self.dueltext += f"{self.unit.name}'s attack leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"

    def bossmiss(self):
        """Boss Miss"""
        self.avoidno -= 1
        self.dueltext += f"{self.boss.name}'s attack misses.\n"

    def bosscrit(self):
      """Boss Crit"""
      if self.boss.crit < 100 and self.ddgno > 0:
        self.ddgno -= 1
        self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
        self.dueltext += f"{self.boss.name}'s attack leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"
      else:
        self.unit.hitpoints = max(0, self.unit.hitpoints - 3 * self.boss.damage)
        self.dueltext += f"{self.boss.name} lands a critical hit and leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"

    def bossattack(self):
        """Boss Attack"""
        self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
        self.dueltext += f"{self.boss.name}'s attack leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"

    def playerphase(self):
        """Player Phase"""
        self.dueltext += "#### Player Phase:\n"
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            if self.unit.crit == 100:
              self.unit_crit()
            elif self.unit.crit > 0 and self.critno > 0:
              self.critno -= 1
              self.unit_crit()
            else:
              self.unitattack()
        if (
            self.boss.hitpoints > 0
            and self.unit.hitpoints > 0
        ):
            if self.avoidno > 0:
                self.bossmiss()
            elif self.boss.crit - (self.unit.luck + self.unit.supportbonus) > 0:
                self.bosscrit()
            else:
                self.bossattack()
        if (
            self.unit.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            if self.unit.crit == 100:
              self.unit_crit()
            elif self.unit.crit > 0 and self.critno > 0:
              self.critno -= 1
              self.unit_crit()
            else:
              self.unitattack()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            if self.avoidno > 0:
                self.bossmiss()
            elif self.boss.crit - (self.unit.luck + self.unit.supportbonus) > 0 :
                self.bosscrit()
            else:
                self.bossattack()
        self.dueltext += "\n"

    def enemyphase(self):
        """Enemy Phase"""
        self.dueltext += "#### Enemy Phase:\n"
        if self.boss.hitpoints > 0 and self.unit.hitpoints > 0:
            if self.avoidno > 0:
                self.bossmiss()
            elif self.boss.crit - (self.unit.luck + self.unit.supportbonus) > 0:
                self.bosscrit()
            else:
                self.bossattack()
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            if self.unit.crit == 100:
              self.unit_crit()
            elif self.unit.crit > 0 and self.critno > 0:
              self.critno -= 1
              self.unit_crit()
            else:
              self.unitattack()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            if self.avoidno > 0:
                self.bossmiss()
            elif self.boss.crit - (self.unit.luck + self.unit.supportbonus) > 0:
                self.bosscrit()
            else:
                self.bossattack()
        if (
            self.unit.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            if self.unit.crit == 100:
              self.unit_crit()
            elif self.unit.crit > 0 and self.critno > 0:
              self.critno -= 1
              self.unit_crit()
            else:
              self.unitattack()
        self.dueltext += "\n"

    def reset_text(self):
        """Reset"""
        self.dueltext = ""
