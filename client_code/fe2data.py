import math
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

@anvil.server.portable_class
class ActiveUnit:
    """Active Unit"""

    def __init__(self, keyword):
        self.char = app_tables.fe2_unit_stats.get(Name=keyword)
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

@anvil.server.portable_class
class ActiveWeapon:
    """Active Weapon"""

    def __init__(self, keyword):
        weapon = app_tables.fe2_weapon_stats.get(Name=keyword)
        self.name = weapon["Name"]
        self.might = weapon["Mgt"]
        self.weight = weapon["Wgt"]
        self.hit = weapon["Hit"]
        self.crit = weapon["Crit"]
        self.range = weapon["Range"]
        self.type = weapon["Type"]
        self.backfire = weapon["Dmg"]

@anvil.server.portable_class
class ActiveBoss:
    """Active Boss"""

    def __init__(self, keyword):
        boss = app_tables.fe2_boss_stats.get(Name=keyword)
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
        self.counter = False
        self.damage = 0
        self.hit = 0
        self.attack = 0
        self.avoid = 0
        self.hitchance = 0

def attack_speed(keyword, weapon):
    """Attack Speed"""
    keyword.AS = max(0, keyword.speed - weapon.weight)

def hitrate(keyword, weapon):
    """Hit Rate"""
    keyword.hit = keyword.skill + weapon.hit

def get_attack(keyword, weapon):
    """Attack"""
    keyword.attack = keyword.strength + weapon.might

def critical(keyword, weapon):
    """Critical"""
    keyword.crit = math.floor(((keyword.skill + keyword.luck) / 2 + weapon.crit) / 2)

def physdamage(attacker, defender):
    """Physical Damage"""
    attacker.damage = max(1, attacker.attack - defender.defense)

def magdamage(attacker, defender):
  """Magical Damage"""
  attacker.damage = max(1, attacker.attack - defender.resistance)

def effectiveness(weapon, keyword):
    """Effectiveness"""
    effcheck = app_tables.fe2_effectiveness.get(Name=weapon.name)
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
        self.critno = 0
        self.ddgno = 0
        self.unithit = 0
        self.unitavoid = 0
        self.unitcrit = 0
        self.unitdodge = 0

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
        critical(self.unit, self.unitweapon)
        if self.unitweapon.type == "Magical":
          self.unit.hit = self.unitweapon.hit
        else:
          hitrate(self.unit, self.unitweapon)

    def bossdisplay(self):
        """Boss Stat Display"""
        attack_speed(self.boss, self.bossweapon)
        critical(self.boss, self.bossweapon)
        if self.bossweapon.type == "Magical":
          self.boss.hit = self.bossweapon.hit
        else:
          hitrate(self.boss, self.bossweapon)

    def enemy_avoid(self):
      if self.unitweapon.type == "Magical":
        self.boss.avoid = self.boss.speed + self.boss.luck
      else:
        self.boss.avoid = self.boss.AS

    def bosshitchance(self):
      if self.bossweapon.type == "Magical":
        self.boss.hitchance = min((self.boss.hit - (self.unit.speed + self.unit.luck)) / 100, 1)
      else:
        self.boss.hitchance = min((self.boss.hit - self.unit.AS) / 100, 1)

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
        self.unitcrit = self.unit.crit / 100
        self.unitavoid = 1 - self.boss.hitchance
        self.unitdodge = 1 - self.boss.crit / 100

    def doubling(self):
        """Doubling Calculation"""
        if self.unit.AS > self.boss.AS:
            self.unit.doubles = True
            self.boss.doubles = False
            self.dueltext += f"{self.unit.name} can make follow-up attacks. \n"
        if self.boss.AS > self.unit.AS:
            self.boss.doubles = True
            self.unit.doubles = False
            self.dueltext += f"{self.boss.name} can make follow-up attacks. \n"

    def counterattack(self):
        """Counter Attack"""
        if self.bossweapon.range >= self.unitweapon.range:
            self.boss.counter = True
            self.dueltext += f"{self.boss.name} can counter-attack. \n"
        else:
            self.boss.counter = False
            self.dueltext += f"{self.boss.name} cannot counter-attack. \n"

    def unithpcost(self):
      if self.unitweapon.backfire > 0:
        self.unit.hitpoints = max(0, self.unit.hitpoints - self.unitweapon.backfire)
        self.dueltext += f"Casting {self.unitweapon.name} leaves {self.unit.name} with {self.unit.hitpoints} HP. \n"
      else:
        pass

    def bosshpcost(self):
      if self.bossweapon.backfire > 0:
        self.boss.hitpoints = max(0, self.boss.hitpoints - self.bossweapon.backfire)
        self.dueltext += f"Casting {self.bossweapon.name} leaves {self.boss.name} with {self.boss.hitpoints} HP. \n"
      else:
        pass

    def unitattack(self):
        """Unit Attack"""
        self.hitno += 1
        self.unithpcost()
        if self.critno > 0 and self.unit.crit > 0:
            self.critno -= 1
            self.boss.hitpoints = max(0, self.boss.hitpoints - 3 * self.unit.damage)
            self.dueltext += f"{self.unit.name} lands a critical hit and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
        else:
            self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
            self.dueltext += f"{self.unit.name}'s attack leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
    
    def bossmiss(self):
        """Boss Miss"""
        self.avoidno -= 1
        self.bosshpcost()
        self.dueltext += f"{self.boss.name}'s attack misses.\n"

    def bosscrit(self):
        """Boss Crit"""
        self.bosshpcost()  
        if self.ddgno > 0:
            self.ddgno -= 1
            self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
            self.dueltext += f"{self.boss.name}'s attack leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"
        else:
            self.unit.hitpoints = max(0, self.unit.hitpoints - 3 * self.boss.damage)
            self.dueltext += f"{self.boss.name} lands a critical hit and leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"

    def bossattack(self):
        """Boss Attack"""
        self.bosshpcost()
        self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
        self.dueltext += f"{self.boss.name}'s attack leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"

    def playerphase(self):
        """Player Phase"""
        self.dueltext += "#### Player Phase:\n"
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            self.unitattack()
        if self.boss.hitpoints > 0 and self.unit.hitpoints > 0 and self.boss.counter is True:
          if self.avoidno > 0:
                self.bossmiss()
          elif self.boss.crit > 0:
                self.bosscrit()
          else:
                self.bossattack()
        if (
            self.unit.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            self.unitattack()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
            and self.boss.counter is True
        ):
          if self.avoidno > 0:
                self.bossmiss()
          elif self.boss.crit > 0:
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
            elif self.boss.crit > 0:
                self.bosscrit()
            else:
                self.bossattack()
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            self.unitattack()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            if self.avoidno > 0:
                self.bossmiss()
            elif self.boss.crit > 0:
                self.bosscrit()
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