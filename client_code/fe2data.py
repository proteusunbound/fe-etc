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
        self.devil = 1

    def boosthp(self, number):
        """HP Boost"""
        self.maxhp = min(self.char["HP"] + number, 52)

    def boostluck(self, number):
        """Luck Boost"""
        self.luck = min(self.char["Lck"] + number, 40)

    def boost_speed(self, number):
        """Speed Boost"""
        self.speed = min(self.char["Spd"] + number, 40)

    def boost_strength(self, number):
        """Strength Boost"""
        self.strength = min(self.char["Str"] + number, 40)

    def boostdefense(self, number):
        """Defense Boost"""
        self.defense = min(self.char["Def"] + number, 40)

    def boost_skill(self, number):
        """Skill Boost"""
        self.skill = min(self.char["Skl"] + number, 40)

    def promote(self, keyword):
      """Promotion"""
      classdefault = app_tables.fe2_class_change.get(Class=keyword)
      self.charclass = classdefault["Class"]
      self.maxhp = max(self.char["HP"], classdefault["HP"])
      self.strength = max(self.char["Str"], classdefault["Str"])
      self.skill = max(self.char["Skl"], classdefault["Skl"])
      self.speed = max(self.char["Spd"], classdefault["Spd"])
      self.defense = max(self.char["Def"], classdefault["Def"])
      if self.charclass == "Hero":
        self.luck = max(self.char["Lck"], 10)
      if self.charclass == "Dread Fighter":
        self.resistance += 15


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
        self.effco = 1

    def magering(self):
      """Mage Ring"""
      if self.type == "Magical" and self.name != "Lightning Sword":
        self.range = 5


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
    keyword.attack = keyword.strength + weapon.might * weapon.effco


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
        self.devilno = 0
        self.iniavo = 0
        self.inicrit = 0
        self.iniddg = 0
        self.inidev = 0
        self.unithit = 0
        self.unitavoid = 0
        self.unitcrit = 0
        self.unitdodge = 0
        self.terrain = False
        self.unitequip = ""
        self.bossequip = ""

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

    def setunitequip(self, equipment):
      """Set Unit Equipment"""
      self.unitequip = equipment

    def setbossequip(self, equipment):
      """Set Boss Equipment"""
      self.bossequip = equipment

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

    def setdevilno(self, devilno):
        """Set Avoid Backfire Number"""
        self.devilno = devilno
        self.inidev = devilno

    def setbosshp(self, hitpoints):
        """Set Boss HP"""
        self.boss.hitpoints = hitpoints

    def devilcheck(self):
        """Devil Weapon"""
        if (
            self.unitweapon.name == "Shadow Sword"
            and self.unit.charclass != "Dread Fighter"
        ):
            self.unit.devil = 1 - max(0, 21 - self.unit.luck) / 100

    def hpthreshold(self):
        """HP Threshold"""
        if (
            self.boss.name == "Duma"
            and self.boss.hitpoints < 53
            and self.unitweapon.name not in ("Falchion", "Nosferatu")
        ):
            self.unit.damage = 0
        if self.bossweapon.name == "Medusa" and self.unit.hitpoints > 1:
            self.boss.crit = 0
            self.boss.damage = self.unit.hitpoints - 1
        if self.unitequip == "Prayer Ring" and self.unit.hitpoints < self.unit.maxhp / 2:
          self.unit.crit = 100

    def damage

    def unitstatadjust(self):
      """Adjust Unit Stats"""
      if self.unitequip == "Angel Ring":
        self.unit.luck = 40
      if self.unitequip == "Speed Ring":
        self.unit.speed = 40
      if self.unitequip == "Leather Shield":
        self.unit.defense += 3
      if self.unitequip == "Steel Shield":
        self.unit.defense += 5
      if self.unitequip == "Silver Shield":
        self.unit.defense += 7
      if self.unitequip == "Blessed Shield" and self.boss.charclass in ("Bonewalker", "Revenant", "Necrodragon", "Gargoyle", "Mogall"):
        self.unit.defense += 13
      if self.unitequip == "Dracoshield":
        self.unit.defense += 13
        self.unit.resistance += 13

    def boss_stat_adjust(self):
      """Adjust Boss Stats"""
      if self.bossequip == "Angel Ring":
        self.boss.luck = 40
      if self.bossequip == "Leather Shield":
        self.boss.defense += 3
      if self.bossequip == "Steel Shield":
        self.boss.defense += 5

    def unitdisplay(self):
        """Unit Stat Display"""
        attack_speed(self.unit, self.unitweapon)
        critical(self.unit, self.unitweapon)
        if (
            self.unitweapon.type == "Magical"
            and self.unitweapon.name != "Lightning Sword"
        ):
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
        """Enemy Avoid"""
        if self.unitweapon.type == "Magical":
            self.boss.avoid = self.boss.speed + self.boss.luck
        elif self.terrain == True:
            self.boss.avoid = self.boss.AS + 40
        else:
            self.boss.avoid = self.boss.AS

    def bosshitchance(self):
        """Boss Hit Chance"""
        if self.bossweapon.type == "Magical":
            if self.unitequip == "Hexlock Shield":
              self.boss.hitchance = 0.1
            else:
              self.boss.hitchance = min(
                (self.boss.hit - (self.unit.speed + self.unit.luck)) / 100, 1
              )
        else:
            self.boss.hitchance = min((self.boss.hit - self.unit.AS) / 100, 1)

    def precombat(self):
        """Pre-Combat Calculation"""
        if self.unitweapon.name == "Lightning Sword":
            self.unit.attack = self.unitweapon.might
        else:
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
        self.devilcheck()
        self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)
        self.unitcrit = self.unit.crit / 100
        self.unitavoid = 1 - self.boss.hitchance
        self.unitdodge = 1 - self.boss.crit / 100

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
        if self.bossequip == "Mage Ring":
          self.bossweapon.magering()
        if self.unitequip == "Mage Ring":
          self.unitweapon.magering()
        if self.bossweapon.range >= self.unitweapon.range:
            self.boss.counter = True
            self.dueltext += f"{self.boss.name} can counter-attack. \n"
        else:
            self.boss.counter = False
            self.dueltext += f"{self.boss.name} cannot counter-attack. \n"

    def unithpcost(self):
        """Unit Spell Cost"""
        if self.unitweapon.backfire > 0:
            self.unit.hitpoints = max(0, self.unit.hitpoints - self.unitweapon.backfire)
            self.dueltext += f"Casting {self.unitweapon.name} leaves {self.unit.name} with {self.unit.hitpoints} HP. \n"
        else:
            pass

    def bosshpcost(self):
        """Boss Spell Cost"""
        if self.bossweapon.backfire > 0:
            self.boss.hitpoints = max(0, self.boss.hitpoints - self.bossweapon.backfire)
            self.dueltext += f"Casting {self.bossweapon.name} leaves {self.boss.name} with {self.boss.hitpoints} HP. \n"
        else:
            pass

    def hprecover(self):
        """Player Phase HP Recover"""
        if self.unit.maxhp > self.unit.hitpoints:
          if self.unitweapon.name in (
            "Blessed Sword",
            "Falchion",
            "Royal Sword",
            "Blessed Lance",
            "Gradivus",
            "Astra",
            "Sol",
            "Luna",
            "Blessed Bow",
          ) or self.unitequip in ("Blessed Ring", "Angel Ring", "Mage Ring", "Prayer Ring", "Speed Ring", "Blessed Shield", "Dracoshield"):
              self.unit.hitpoints = min(self.unit.hitpoints + 5, self.unit.maxhp)
              self.dueltext += f"{self.unit.name} heals to {self.unit.hitpoints} HP at the start of the round.\n"

    def unit_crit(self):
      """Unit Crit"""
      self.hitno += 1
      self.unithpcost()
      if self.unit.devil == 1:
                self.boss.hitpoints = max(0, self.boss.hitpoints - 3 * self.unit.damage)
                self.dueltext += f"{self.unit.name} lands a critical hit and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
                if (
                    self.unitweapon.name == "Nosferatu"
                    and self.unit.hitpoints < self.unit.maxhp
                ):
                    self.unit.hitpoints = min(
                        self.unit.hitpoints + 3 * self.unit.damage, self.unit.maxhp
                    )
                    self.dueltext += (
                        f"{self.unit.name} restores to {self.unit.hitpoints} HP. \n"
                    )
      elif self.devilno > 0:
                self.devilno -= 1
                self.boss.hitpoints = max(0, self.boss.hitpoints - 3 * self.unit.damage)
                self.dueltext += f"{self.unit.name} lands a critical hit and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
      else:
                self.unit.hitpoints = max(0, self.unit.hitpoints - 3 * self.unit.damage)
                self.dueltext += f"{self.unit.name}'s attack backfires and leaves them with {self.unit.hitpoints} HP.\n"
      
    def unitattack(self):
        """Unit Attack"""
        self.hitno += 1
        self.unithpcost()
        if self.unit.devil == 1:
            self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
            self.dueltext += f"{self.unit.name}'s attack leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
            if (
                self.unitweapon.name == "Nosferatu"
                and self.unit.hitpoints < self.unit.maxhp
            ):
                self.unit.hitpoints = min(
                    self.unit.hitpoints + self.unit.damage, self.unit.maxhp
                )
                self.dueltext += (
                    f"{self.unit.name} restores to {self.unit.hitpoints} HP. \n"
                )
        elif self.devilno > 0:
            self.devilno -= 1
            self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
            self.dueltext += f"{self.unit.name}'s attack leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
        else:
            self.unit.hitpoints = max(0, self.unit.hitpoints - self.unit.damage)
            self.dueltext += f"{self.unit.name}'s attack backfires and leaves them with {self.unit.hitpoints} HP.\n"

    def bossmiss(self):
        """Boss Miss"""
        self.avoidno -= 1
        self.bosshpcost()
        self.dueltext += f"{self.boss.name}'s attack misses.\n"

    def bosscrit(self):
        """Boss Crit"""
        self.bosshpcost()
        if self.boss.crit < 100 and self.ddgno > 0:
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
            and self.boss.counter is True
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
