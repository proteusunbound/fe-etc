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
        self.devil = 1
        self.supports = []
        self.supportbonus = 0

    def setsupports(self):
        """Set Supports"""
        if self.name in supports:
            for name, number in supports[self.name].items():
                self.supports.append(name)
        else:
            self.supports = ["None", "None"]

    def setsupportbonus(self, keyword, check):
        """Set Support Bonus"""
        if check is True:
            self.supportbonus += supports[self.name][keyword]

    def booktwo(self, check):
        """Book 2 Stats"""
        if check is True:
            self.char = app_tables.fe3_book_2.get(Name=self.name)
            self.maxhp = self.char["HP"]
            self.strength = self.char["Str"]
            self.skill = self.char["Skl"]
            self.speed = self.char["Spd"]
            self.defense = self.char["Def"]
            self.luck = self.char["Lck"]
            self.resistance = self.char["Res"]
            self.charclass = self.char["Class"]

    def dismount(self):
      """Dismount"""
      if self.charclass == "Horseman":
        penalty = app_tables.fe3_class_change.get(FromClass=self.charclass)
      else:
        penalty = app_tables.fe3_class_change.get(FromClass=self.charclass, ToClass="Knight")
      self.charclass = penalty["ToClass"]
      self.strength += penalty["Str"]
      self.skill += penalty["Skl"]
      self.speed += penalty["Spd"]
      self.defense += penalty["Def"]
      self.resistance += penalty["Res"]

    def promote(self):
      "Promotion"
      if self.name == "Jubelo":
        bonus = app_tables.fe3_class_change.get(FromClass="Mage (M)")
      elif self.name == "Merric":
        bonus = app_tables.fe3_class_change.get(FromClass="Mage (Merric)")
      elif self.name == "Linde":
        bonus = app_tables.fe3_class_change.get(FromClass="Mage (F)")
      else:
        bonus = app_tables.fe3_class_change.get(FromClass=self.charclass, ToClass=q.none_of("Knight"))
      self.charclass = bonus['ToClass']
      self.maxhp = max(self.char["HP"], bonus["HP"])
      self.strength += bonus["Str"]
      self.skill += bonus["Skl"]
      self.speed += bonus["Spd"]
      self.defense += bonus["Def"]
      self.resistance += bonus["Res"]

    def boosthp(self, number):
        """Seraph Robe"""
        self.maxhp = min(self.char["HP"] + 7 * number, 52)

    def boostluck(self, number):
        """Goddess Icon"""
        self.luck = min(self.char["Lck"] + 5 * number, 20)

    def boost_speed(self, number):
        """Speed Ring"""
        self.speed = min(self.char["Spd"] + 5 * number, 20)

    def boost_strength(self, number):
        """Power Ring"""
        self.strength = min(self.char["Str"] + 4 * number, 20)

    def boostresistance(self, number):
        """Talisman"""
        self.resistance = min(self.char["Res"] + 3 * number, 20)

    def boostdefense(self, number):
        """Dracoshield"""
        self.defense = min(self.char["Def"] + 4 * number, 20)

    def boost_skill(self, number):
        """Secret Book"""
        self.skill = min(self.char["Skl"] + 5 * number, 20)

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

    def booktwo(self, check):
        """Book 2 Stats"""
        if check is True:
            boss = app_tables.fe3_book_2.get(Name=self.name)
            self.maxhp = boss["HP"]
            self.strength = boss["Str"]
            self.skill = boss["Skl"]
            self.speed = boss["Spd"]
            self.defense = boss["Def"]
            self.luck = boss["Lck"]
            self.resistance = boss["Res"]
            self.charclass = boss["Class"]


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
        self.devilno = 0
        self.inidev = 0
        self.unithit = 0
        self.unitavoid = 0
        self.unitcrit = 0
        self.unitdodge = 0
        self.terrain = False
        self.equipment = []

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

    def setequipment(self, equipment):
      """Set Equipment"""
      self.equipment.append(equipment)

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
        if self.unitweapon.name in ("Devil Sword", "Devil Axe"):
            self.unit.devil = 1 - (21 - self.unit.luck) / 100

    def hpthreshold(self):
        """HP Threshold"""
        if self.bossweapon.name == "Dulam" and self.unit.hitpoints > 1:
            self.boss.crit = 0
            self.boss.damage = self.unit.hitpoints - 1

    def damageadjust(self):
        """Adjust Damage"""
        if self.bossweapon.name == "Imhullu" and self.unitweapon.name != "Starlight":
            self.unit.damage = 0
        if self.boss.name == "Hardin" and "Lightsphere" not in self.equipment:
          self.unit.damage = 0

    def effcoadjust(self):
      """Adjust Weapon Effectiveness"""
      if ("Lightsphere", "Iote's Shield") in self.equipment:
        self.bossweapon.effco = 1
      if self.boss.name == "Michalis":
        self.unitweapon.effco = 1

    def equipadjust(self):
      """Adjust Based on Equipment"""
      if "Geosphere" in self.equipment:
        self.unit.hit += 10
        self.unit.crit += 10
      if "Lightsphere" in self.equipment:
        self.terrain = False
        self.boss.crit = 0

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
        if self.terrain is True and self.boss.charclass not in (
            "Dracoknight",
            "Wyvern",
        ):
            self.boss.avoid = self.boss.speed + self.boss.luck + 30
        else:
            self.boss.avoid = self.boss.speed + self.boss.luck

    def bosshitchance(self):
        """Boss Hit Chance"""
        self.boss.hitchance = min(
            (
                self.boss.hit
                - (self.unit.speed + self.unit.luck + self.unit.supportbonus)
            )
            / 100,
            1,
        )

    def precombat(self):
        """Pre-Combat Calculation"""
        self.equipadjust()
        if self.unitweapon.name == "Levin Sword":
            self.unit.attack = self.unitweapon.might
        else:
            get_attack(self.unit, self.unitweapon)
        if self.bossweapon.name == "Dark Breath":
            self.unit.attack = math.floor(self.unit.attack / 2)
        if self.unitweapon.type == "Magical":
            magdamage(self.unit, self.boss)
        elif self.unitweapon.name in (
            "Fire Breath",
            "Fog Breath",
        ) and self.boss.charclass not in (
            "Fire Dragon",
            "Mage Dragon",
            "Earth Dragon",
            "Wyvern",
            "Ice Dragon",
            "Shadow Dragon",
        ):
            self.unit.damage = self.unit.attack
        else:
            physdamage(self.unit, self.boss)
        self.enemy_avoid()
        get_attack(self.boss, self.bossweapon)
        if self.bossweapon.type == "Magical":
            magdamage(self.boss, self.unit)
        elif (
            self.bossweapon.name in ("Fire Breath", "Ice Breath", "Dark Breath")
            and self.unit.charclass != "Manakete"
        ):
            self.boss.damage = self.boss.attack
        else:
            physdamage(self.boss, self.unit)
        self.bosshitchance()
        self.devilcheck()
        self.damageadjust()
        self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)
        self.unitcrit = (self.unit.crit - self.boss.luck) / 100
        self.unitavoid = 1 - self.boss.hitchance
        self.unitdodge = 1 - max(
            0, (self.boss.crit - (self.unit.luck + self.unit.supportbonus)) / 100
        )

    def counterattack(self):
        """Counter Attack"""
        if self.bossweapon.name in (
            "Thunderbolt",
            "Arrowspate",
            "Stonehoist",
            "Hoistflamme",
            "Pachyderm",
            "Meteor",
            "Swarm",
        ):
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
        effectiveness(self.bossweapon, self.unit)
        self.effcoadjust()
        if self.unitweapon.effco == 3:
            self.dueltext += f"{self.unit.name}'s {self.unitweapon.name} deals effective damage against {self.boss.name}. \n"
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

    def hprecover(self):
      """HP Recover"""
      if "Lifesphere" in self.equipment:
        self.unit.hitpoints = self.unit.maxhp
        self.dueltext += f"{self.unit.name} heals to {self.unit.hitpoints} HP at the start of the round.\n"

    def unit_crit(self):
        """Unit Crit"""
        self.hitno += 1
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
        if self.boss.hitpoints > 0 and self.unit.hitpoints > 0 and self.boss.counter is True:
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
            and self.boss.counter is True
        ):
            if self.avoidno > 0:
                self.bossmiss()
            elif self.boss.crit - (self.unit.luck + self.unit.supportbonus) > 0:
                self.bosscrit()
            else:
                self.bossattack()
        self.dueltext += "\n"

    def enemyphase(self):
        """Enemy Phase"""
        self.dueltext += "#### Enemy Phase:\n"
        if self.boss.hitpoints > 0 and self.unit.hitpoints > 0 and self.boss.counter is True:
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
            and self.boss.counter is True
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
