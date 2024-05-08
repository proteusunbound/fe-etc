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

@anvil.server.portable_class
class ActiveWeapon:
    """Active Weapon"""
    def __init__(self, keyword):
        weapon = app_tables.fe5_weapon_stats.get(Name=keyword)
        self.name = weapon["Name"]
        self.might = weapon["Mgt"]
        self.weight = weapon["Wgt"]
        self.hit = weapon["Hit"]

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
        self.hitpoints = 0
        self.doubles = False
        self.damage = 0
        self.hit = 0
        self.attack = 0
        self.avoid = 0
        self.hitchance = 0

def attack_speed(keyword, weapon):
    """Attack Speed"""
    keyword.AS = keyword.speed - (weapon.weight - keyword.build)

def hitrate(keyword, weapon):
    """Hit Rate"""
    keyword.hit = weapon.hit + (2 * keyword.skill) + keyword.luck

def attack(keyword, weapon):
    """Attack"""
    keyword.attack = keyword.strength + weapon.might

def damage(attacker, defender):
    """Damage"""
    attacker.damage = max(0, attacker.attacker - defender.defense)