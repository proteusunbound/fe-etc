import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#
@anvil.server.portable_class
class ActiveUnit():
  def __init__(self, keyword):
    unit = app_tables.unit_stats.get(Name=keyword)
    self.name = unit['Name']
    self.maxhp = unit['HP']
    self.strength = unit['Str']
    self.skill = unit['Skl']
    self.speed = unit['Spd']
    self.defense = unit['Def']
    self.luck = unit['Lck']
