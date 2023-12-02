import math
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from . import data

@anvil.server.callable
def attack_speed(keyword, weapon):
    """Attack Speed"""
    keyword.AS = max(0, keyword.speed - weapon.weight)

@anvil.server.callable
def hitrate(keyword, weapon):
    """Hit Rate"""
    keyword.hit = keyword.skill + weapon.hit

@anvil.server.callable
def get_attack(keyword, weapon):
    """Attack"""
    keyword.attack = keyword.strength + weapon.might

@anvil.server.callable
def unit_crit(unit, weapon):
    """Unit Crit"""
    unit.crit = math.floor(((unit.skill + unit.luck) / 2 + weapon.crit) / 2)

@anvil.server.callable
def boss_crit(boss, weapon):
    """Boss Crit"""
    boss.crit = math.floor((boss.skill / 2 + weapon.crit) / 2)

@anvil.server.callable
def enemy_avoid(boss, terrain):
    """Enemy Avoid"""
    if terrain is True:
      boss.avoid = boss.AS + 30
    else:
      boss.avoid = boss.AS

@anvil.server.callable
def damage(attacker, defender):
    """Damage"""
    attacker.damage = max(0, attacker.attack - defender.defense)

@anvil.server.callable
def bosshitchance(boss, unit):
    """Boss Hit Chance"""
    boss.hitchance = min((boss.hit - unit.AS) / 100, 1)
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
