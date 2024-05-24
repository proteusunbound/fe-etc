"""Data"""
import math
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import fe5skills

skills = fe5skills.skills_list

@anvil.server.portable_class
class ActiveUnit:
    """Active Unit"""

    def __init__(self, keyword):
        self.char = app_tables.fe5_unit_stats.get(Name=keyword)
        self.name = self.char["Name"]
        self.maxhp = self.char["HP"]
        self.strength = self.char["Str"]
        self.magic = self.char["Mag"]
        self.skill = self.char["Skl"]
        self.speed = self.char["Spd"]
        self.defense = self.char["Def"]
        self.luck = self.char["Lck"]
        self.build = self.char["Bld"]
        self.hitpoints = 0
        self.doubles = False
        self.damage = 0
        self.hit = 0
        self.attack = 0
        self.crit = 0
        self.leaderstars = 0
        self.adeptrate = 1
        self.adeptcancel = 1
        self.skills = []

    def setskills(self):
        """Set Skills"""
        if self.name in skills:
            self.skills = skills[self.name]

@anvil.server.portable_class
class ActiveWeapon:
    """Active Weapon"""
    def __init__(self, keyword):
        weapon = app_tables.fe5_weapon_stats.get(Name=keyword)
        self.name = weapon["Name"]
        self.might = weapon["Mgt"]
        self.weight = weapon["Wgt"]
        self.hit = weapon["Hit"]
        self.crit = weapon["Crit"]
        self.type = weapon["Type"]
        self.weapontriangle = 0

@anvil.server.portable_class
class ActiveBoss:
    """Active Boss"""
    def __init__(self, keyword):
        boss = app_tables.fe5_boss_stats.get(Name=keyword)
        self.name = boss["Name"]
        self.maxhp = boss["HP"]
        self.strength = boss["Str"]
        self.magic = boss["Mag"]
        self.skill = boss["Skl"]
        self.speed = boss["Spd"]
        self.luck = boss["Lck"]
        self.defense = boss["Def"]
        self.build = boss["Bld"]
        self.leaderstars = boss["Leadership"]
        self.hitpoints = 0
        self.doubles = False
        self.damage = 0
        self.hit = 0
        self.attack = 0
        self.avoid = 0
        self.hitchance = 0
        self.crit = 0
        self.skills = []

    def setskills(self):
        """Set Skills"""
        if self.name in skills:
            self.skills = skills[self.name]

def attack_speed(keyword, weapon):
    """Attack Speed"""
    keyword.AS = keyword.speed - (weapon.weight - keyword.build)

def hitrate(keyword, weapon):
    """Hit Rate"""
    keyword.hit = weapon.hit + (2 * keyword.skill) + keyword.luck + weapon.weapontriangle + (3 * keyword.leaderstars)

def physattack(keyword, weapon):
    """Physical Attack"""
    keyword.attack = keyword.strength + weapon.might

def magattack(keyword, weapon):
    """Magical Attack"""
    keyword.attack = keyword.magic + weapon.might

def physdamage(attacker, defender):
    """Physical Damage"""
    attacker.damage = max(0, attacker.attack - defender.defense)

def magdamage(attacker, defender):
    """Magical Damage"""
    attacker.damage = max(0, attacker.attack - defender.magic)

def critical(keyword, weapon):
    """Critical"""
    keyword.crit = keyword.skill + weapon.crit

def physcrit(attacker, defender):
    """Physical Crit """
    attacker.critdamage = max(0, 2 * attacker.attack - defender.defense)

def magcrit(attacker, defender):
    """Magical Crit"""
    attacker.critdamage = max(0, 2 * attacker.attack - defender.magic)

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
        self.iniadept = 0
        self.adeptno = 0
        self.inicanceladept = 0
        self.canceladeptno = 0
        self.terrain = "None"

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

    def setadeptno(self, adeptnum):
        """Set Adept Number"""
        self.iniadept = adeptnum
        self.adeptno = adeptnum

    def setcanceladeptno(self, adeptavo):
        """Set Adept Avoids"""
        self.inicanceladept = adeptavo
        self.canceladeptno = adeptavo

    def setbosshp(self, hitpoints):
        """Set Boss HP"""
        self.boss.hitpoints = hitpoints

    def weapontriangle(self):
        """Weapon Triangle"""
        triangle_logic = {
            "Sword": "Axe",
            "Lance": "Sword",
            "Axe": "Lance",
            "Fire": "Wind",
            "Thunder": "Fire",
            "Wind": "Thunder",
        }
        anima = ["Fire", "Wind", "Thunder"]
        light_dark = ["Light", "Dark"]
        if (
            self.unitweapon.type in triangle_logic
            and triangle_logic[self.unitweapon.type] == self.bossweapon.type
        ) or (self.unitweapon.type in light_dark and self.bossweapon.type in anima):
            self.unitweapon.weapontriangle = 5
            self.bossweapon.weapontriangle = -5
        elif (
            self.bossweapon.type in triangle_logic
            and triangle_logic[self.bossweapon.type] == self.unitweapon.type
        ) or (self.bossweapon.type in light_dark and self.unitweapon.type in anima):
            self.bossweapon.weapontriangle = 5
            self.unitweapon.weapontriangle = -5
        else:
            self.unitweapon.weapontriangle = 0
            self.bossweapon.weapontriangle = 0

    def boss_stat_adjust(self):
        """Adjust Boss Stats"""
        if self.terrain == "Throne":
            self.boss.defense += 10
        elif self.terrain == "Seal":
            self.boss.magic += 10

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
        if self.terrain == "Throne":
            self.boss.avoid = (2 * self.boss.AS) + self.boss.luck + 30 + (3 * self.boss.leaderstars)
        elif self.terrain == "Seal":
            self.boss.avoid = (2 * self.boss.AS) + self.boss.luck + 20 + (3 * self.boss.leaderstars)
        else:
            self.boss.avoid = (2 * self.boss.AS) + self.boss.luck + (3 * self.boss.leaderstars)

    def bosshitchance(self):
        """Boss Hit Chance"""
        hitchance = min(((self.boss.hit - ((self.unit.AS * 2) + self.unit.luck) + (3 * self.unit.leaderstars)) / 100), 0.99)
        self.boss.hitchance = max(0.01, hitchance)

    def precombat(self):
        """Pre-Combat Calculation"""
        self.weapontriangle()
        hitrate(self.unit, self.unitweapon)
        hitrate(self.boss, self.bossweapon)
        attack(self.unit, self.unitweapon)
        damage(self.unit, self.boss)
        critdamage(self.unit, self.boss)
        self.enemy_avoid()
        attack(self.boss, self.bossweapon)
        damage(self.boss, self.unit)
        critdamage(self.boss, self.unit)
        self.bosshitchance()
        self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 0.99)
        self.unitavoid = 1 - self.boss.hitchance
        self.unitcrit = (self.unit.crit - (self.boss.luck / 2)) / 100
        self.unitdodge = 1 - max(0, (self.boss.crit - (self.unit.luck / 2)) / 100)

    def skillprocs(self):
        """Skill Procs"""
        if "Adept" in self.unit.skills:
            self.unit.adeptrate = self.unit.AS / 100
        if "Adept" in self.boss.skills:
            self.unit.adeptcancel = 1 - (self.boss.AS / 100)

    def doubling(self):
        """Doubling Calculation"""
        if self.unit.AS >= (self.boss.AS + 4):
            self.unit.doubles = True
            self.boss.doubles = False
            self.dueltext += f"{self.unit.name} can make follow-up attacks. \n"
        elif self.boss.AS >= (self.unit.AS + 4):
            self.boss.doubles = True
            self.unit.doubles = False
            self.dueltext += f"{self.boss.name} can make follow-up attacks. \n"
        else:
            self.boss.doubles = False
            self.unit.doubles = False

    def unitadept(self):
        """Unit Adept"""
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            self.dueltext += f"{self.unit.name} strikes twice consecutively. \n"
            if self.unit.crit == 100:
                self.unit_crit()
            elif (
                self.unit.crit > 0
                and self.critno > 0
            ):
                self.critno -= 1
                self.unit_crit()
            else:
                self.unitattack()

    def unit_crit(self):
        """Unit Crit"""
        self.hitno += 1
        self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.critdamage)
        self.dueltext += f"{self.unit.name} lands a critical hit and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"

    def unitattack(self):
        """Unit Attack"""
        self.hitno += 1
        self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
        self.dueltext += f"{self.unit.name}'s attack leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"

    def bossadept(self):
        """Boss Adept"""
        if self.canceladeptno > 0 and self.unit.adeptcancel > 0:
            self.canceladeptno -= 1
        elif (
            self.boss.hitpoints > 0
            and self.unit.hitpoints > 0
        ):
            self.dueltext += f"{self.boss.name} strikes twice consecutively. \n"
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            elif self.boss.crit > 0:
                self.bosscrit()
            else:
                self.bossattack()

    def bossmiss(self):
        """Boss Miss"""
        self.dueltext += f"{self.boss.name}'s attack misses.\n"

    def bosscrit(self):
        """Boss Crit"""
        if self.boss.crit < 100 and self.ddgno > 0:
            self.ddgno -= 1
            self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
            self.dueltext += f"{self.boss.name}'s attack leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"
        else:
            self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.critdamage)
            self.dueltext += f"{self.boss.name} lands a critical hit and leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"

    def bossattack(self):
        """Boss Attack"""
        self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
        self.dueltext += f"{self.boss.name}'s attack leaves {self.unit.name} with {self.unit.hitpoints} HP.\n"

    def dodamage(self):
        """Unit Attack Checks"""
        if self.unit.crit == 100:
            self.unit_crit()
        elif self.unit.crit > 0 and self.critno > 0:
            self.critno -= 1
            self.unit_crit()
        else:
            self.unitattack()
        if "Adept" in self.unit.skills and self.adeptno > 0:
            self.adeptno -= 1
            self.unitadept()

    def counterdamage(self):
        """Boss Attack Checks"""
        if self.boss.hitchance == 0:
            self.bossmiss()
        elif self.avoidno > 0:
            self.avoidno -= 1
            self.bossmiss()
        elif self.boss.crit > 0:
            self.bosscrit()
        else:
            self.bossattack()
        if "Adept" in self.boss.skills:
            self.bossadept()

    def playerphase(self):
        """Player Phase"""
        self.dueltext += "#### Player Phase:\n"
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            self.dodamage()
        if (
            self.boss.hitpoints > 0
            and self.unit.hitpoints > 0
        ):
            self.counterdamage()
        if (
            self.unit.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            self.dodamage()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            self.counterdamage()
        self.dueltext += "\n"

    def enemyphase(self):
        """Enemy Phase"""
        self.dueltext += "#### Enemy Phase:\n"
        if (
            self.boss.hitpoints > 0
            and self.unit.hitpoints > 0
        ):
            self.counterdamage()
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            self.dodamage()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            self.counterdamage()
        if (
            self.unit.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            self.counterdamage()
        self.dueltext += "\n"

    def reset_text(self):
        """Reset"""
        self.dueltext = ""
