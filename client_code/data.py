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
        unit = app_tables.unit_stats.get(Name=keyword)
        self.name = unit["Name"]
        self.maxhp = unit["HP"]
        self.strength = unit["Str"]
        self.skill = unit["Skl"]
        self.speed = unit["Spd"]
        self.defense = unit["Def"]
        self.luck = unit["Lck"]
        self.resistance = unit["Res"]
        self.charclass = unit["Class"]
        self.hitpoints = 0
        self.doubles = False
        self.devil = 1
        self.damage = 0
        self.hit = 0
        self.attack = 0
      
    def boosthp (self, number):
      self.maxhp = min(self.maxhp + 9 * number, 52)


@anvil.server.portable_class
class ActiveWeapon:
    """Active Weapon"""

    def __init__(self, keyword):
        weapon = app_tables.weapon_stats.get(Name=keyword)
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
        boss = app_tables.boss_stats.get(Name=keyword)
        self.name = boss["Name"]
        self.maxhp = boss["HP"]
        self.strength = boss["Str"]
        self.skill = boss["Skl"]
        self.speed = boss["Spd"]
        self.defense = boss["Def"]
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


def unit_crit(unit, weapon):
    """Unit Crit"""
    unit.crit = math.floor(((unit.skill + unit.luck) / 2 + weapon.crit) / 2)


def boss_crit(boss, weapon):
    """Boss Crit"""
    boss.crit = math.floor((boss.skill / 2 + weapon.crit) / 2)


def enemy_avoid(boss, terrain):
    """Enemy Avoid"""
    if terrain is True:
        boss.avoid = boss.AS + 30
    else:
        boss.avoid = boss.AS


def damage(attacker, defender):
    """Damage"""
    attacker.damage = max(0, attacker.attack - defender.defense)


def bosshitchance(boss, unit):
    """Boss Hit Chance"""
    boss.hitchance = min((boss.hit - unit.AS) / 100, 1)


def effectiveness(weapon, keyword):
    """Effectiveness"""
    effcheck = app_tables.effectiveness.get(Name=weapon.name)
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
        self.terrain = False
        self.avoidno = 0
        self.critno = 0
        self.ddgno = 0
        self.devilno = 0
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

    def set_terrain(self, terrain):
        """Set Terrain"""
        self.terrain = terrain

    def setunithp(self, hitpoints):
        """Set Unit HP"""
        self.unit.hitpoints = hitpoints

    def setavoidno(self, avoidno):
        """Set Avoid Number"""
        self.avoidno = avoidno

    def setbosshp(self, hitpoints):
        """Set Boss HP"""
        self.boss.hitpoints = hitpoints

    def setcritno(self, critno):
        """Set Crit Number"""
        self.critno = critno

    def setddgno(self, ddgno):
        """Set Dodge Number"""
        self.ddgno = ddgno

    def setdevilno(self, devilno):
        """Set Avoid Backfire Number"""
        self.devilno = devilno

    def devilcheck(self):
        """Devil Weapon"""
        if self.unitweapon.name in ("Devil Sword", "Devil Axe"):
            self.unit.devil = 1 - (21 - self.unit.luck) / 100

    def effcoadjust(self):
        """Adjust Weapon Effectiveness"""
        if self.unitweapon.name == "Falchion" and self.bossweapon.name != "Earthstone":
            self.unitweapon.effco = 1
        if self.bossweapon.name == "Earthstone" and self.unitweapon.name != "Falchion":
            self.unitweapon.effco = 1

    def damageadjust(self):
        """Adjust Damage"""
        if (
            self.unitweapon.name == "Falchion"
            and self.bossweapon.maxrange == 1
            and self.bossweapon.name
            not in ("Firestone", "Divinestone", "Magestone", "Earthstone")
        ):
            self.boss.damage = 0
        if self.bossweapon.name == "Imhullu" and self.unitweapon.name != "Starlight":
            self.unit.damage = 0
        if self.bossweapon.name == "Magestone" and self.unitweapon.type == "Magical":
            self.unit.damage = 0
        if self.bossweapon.name == "Earthstone" and self.unitweapon.maxrange == 2:
            self.unit.damage = 0

    def unitstatadjust(self):
        """Adjust Unit Stats"""
        if self.unitweapon.name == "Firestone":
            self.unit.defense += 12
        if self.unitweapon.name == "Divinestone":
            self.unit.defense += 13

    def boss_stat_adjust(self):
        """Adjust Boss Stats"""
        if self.bossweapon.name == "Firestone":
            self.boss.defense += 12
        if self.bossweapon.name == "Divinestone":
            self.boss.defense += 13
        if self.bossweapon.name == "Magestone":
            self.boss.defense += 15
        if self.bossweapon.name == "Earthstone":
            self.boss.defense += 23

    def unitdisplay(self):
        """Unit Stat Display"""
        attack_speed(self.unit, self.unitweapon)
        unit_crit(self.unit, self.unitweapon)
        if self.unitweapon.type == "Magical":
            self.unit.hit = self.unitweapon.hit
        else:
            hitrate(self.unit, self.unitweapon)

    def bossdisplay(self):
        """Boss Stat Display"""
        attack_speed(self.boss, self.bossweapon)
        boss_crit(self.boss, self.bossweapon)
        if self.bossweapon.type == "Magical":
            self.boss.hit = self.bossweapon.hit
        else:
            hitrate(self.boss, self.bossweapon)

    def precombat(self):
        """Pre-Combat Calculation"""
        if self.unitweapon.type == "Magical":
            self.unit.attack = self.unitweapon.might * self.unitweapon.effco
            self.unit.damage = self.unit.attack
            self.boss.avoid = 0
        else:
            get_attack(self.unit, self.unitweapon)
            damage(self.unit, self.boss)
            enemy_avoid(self.boss, self.terrain)
        if self.bossweapon.type == "Magical":
            self.boss.attack = self.bossweapon.might * self.bossweapon.effco
            self.boss.damage = max(0, self.boss.attack - self.unit.resistance)
            self.boss.hitchance = min((self.boss.hit - self.unit.luck) / 100, 1)
        else:
            get_attack(self.boss, self.bossweapon)
            damage(self.boss, self.unit)
            bosshitchance(self.boss, self.unit)
        self.devilcheck()
        self.damageadjust()
        self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)
        self.unitcrit = self.unit.crit / 100
        self.unitavoid = 1 - self.boss.hitchance
        self.unitdodge = 1 - self.boss.crit / 100

    def effectivecheck(self):
        """Effectiveness Log"""
        effectiveness(self.unitweapon, self.boss)
        self.effcoadjust()
        if self.unitweapon.effco == 3:
            self.dueltext += f"{self.unit.name}'s {self.unitweapon.name} deals effective damage against {self.boss.name}. \n"
        effectiveness(self.bossweapon, self.unit)
        if self.bossweapon.effco == 3:
            self.dueltext += f"{self.boss.name}'s {self.bossweapon.name} deals effective damage against {self.unit.name}. \n"

    def counterattack(self):
        """Counter Attack"""
        if self.bossweapon.minrange != self.bossweapon.maxrange:
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

    def doubling(self):
        """Doubling Calculation"""
        if self.unit.AS > self.boss.AS and self.unitweapon.name not in (
            "Arrowspate",
            "Stonehoist",
            "Hoistflamme",
            "Thunderbolt",
            "Pachyderm",
        ):
            self.unit.doubles = True
            self.boss.doubles = False
            self.dueltext += f"{self.unit.name} can make follow-up attacks. \n"
        if self.boss.AS > self.unit.AS and self.bossweapon.name not in (
            "Arrowspate",
            "Stonehoist",
            "Hoistflamme",
            "Thunderbolt",
            "Pachyderm",
        ):
            self.boss.doubles = True
            self.unit.doubles = False
            self.dueltext += f"{self.boss.name} can make follow-up attacks. \n"

    def unitattack(self):
        """Unit Attack"""
        self.hitno += 1
        if self.critno > 0 and self.unit.crit > 0:
            self.critno -= 1
            if self.unit.devil == 1:
                self.boss.hitpoints = max(0, self.boss.hitpoints - 3 * self.unit.damage)
                self.dueltext += f"{self.unit.name} lands a critical hit and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
            elif self.devilno > 0:
                self.devilno -= 1
                self.boss.hitpoints = max(0, self.boss.hitpoints - 3 * self.unit.damage)
                self.dueltext += f"{self.unit.name} lands a critical hit and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
            else:
                self.unit.hitpoints = max(0, self.unit.hitpoints - 3 * self.unit.damage)
                self.dueltext += f"{self.unit.name}'s attack backfires and leaves them with {self.unit.hitpoints} HP.\n"
        else:
            if self.unit.devil == 1:
                self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
                self.dueltext += f"{self.unit.name}'s attack leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
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
        if self.ddgno > 0:
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
