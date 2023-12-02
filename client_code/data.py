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
class ActiveUnit:
  """Active Unit"""
  def __init__(self, keyword):
    unit = app_tables.unit_stats.get(Name=keyword)
    self.name = unit['Name']
    self.maxhp = unit['HP']
    self.strength = unit['Str']
    self.skill = unit['Skl']
    self.speed = unit['Spd']
    self.defense = unit['Def']
    self.luck = unit['Lck']
    self.hitpoints = 0
    self.doubles = False

@anvil.server.portable_class
class ActiveWeapon:
  """Active Weapon"""
  def __init__(self, keyword):
    weapon = app_tables.weapon_stats.get(Name=keyword)
    self.might = weapon['Mgt']
    self.weight = weapon['Wgt']
    self.hit = weapon['Hit']
    self.crit = weapon['Crit']
    self.minrange = weapon['Min Range']
    self.maxrange = weapon['Max Range']

@anvil.server.portable_class
class ActiveBoss:
  """Active Boss"""
  def __init__(self, keyword):
    boss = app_tables.boss_stats.get(Name=keyword)
    self.name = boss['Name']
    self.maxhp = boss['HP']
    self.strength = boss['Str']
    self.skill = boss['Skl']
    self.speed = boss['Spd']
    self.defense = boss['Def']
    self.hitpoints = 0
    self.doubles = False
    self.counter = False

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

  def precombat(self):
    """Pre-Combat Calculation"""
    anvil.server.call('attack_speed', self.unit, self.unitweapon)
    anvil.server.call('attack_speed', self.boss, self.bossweapon)
    anvil.server.call('hitrate', self.unit, self.unitweapon)
    anvil.server.call('hitrate', self.boss, self.bossweapon)
    anvil.server.call('get_attack', self.unit, self.unitweapon)
    anvil.server.call('get_attack', self.boss, self.bossweapon)
    anvil.server.call('unit_crit', self.unit, self.unitweapon)
    anvil.server.call('boss_crit', self.boss, self.bossweapon)
    anvil.server.call('damage', self.unit, self.boss)
    anvil.server.call('damage', self.boss, self.unit)
    anvil.server.call('bosshitchance', self.boss, self.unit)
    anvil.server.call('enemy_avoid', self.boss, self.terrain)
    self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)
    self.unitcrit = self.unit.crit / 100
    self.unitavoid = 1 - self.boss.hitchance
    self.unitdodge = 1 - self.boss.crit / 100

  def counterattack(self):
    """Counter Attack"""
    if self.bossweapon.minrange != self.bossweapon.maxrange:
      self.boss.counter = True
      self.dueltext += "%s can counter-attack. \n" % self.boss.name
    elif (
      self.bossweapon.minrange == self.unitweapon.minrange
      and self.bossweapon.maxrange == self.unitweapon.maxrange
    ):
      self.boss.counter = True
      self.dueltext += "%s can counter-attack. \n" % self.boss.name
    else:
      self.boss.counter = False
      self.dueltext += "%s cannot counter-attack. \n" % self.boss.name

  def doubling(self):
    """Doubling Calculation"""
    if self.unit.AS > self.boss.AS:
      self.unit.doubles = True
      self.boss.doubles = False
      self.dueltext += "%s can make follow-up attacks. \n" % self.unit.name
    if self.boss.AS > self.unit.AS:
      self.boss.doubles = True
      self.unit.doubles = False
      self.dueltext += "%s can make follow-up attacks. \n" % self.boss.name

  def unitattack(self):
    """Unit Attack"""
    self.hitno += 1
    if self.critno and self.unit.crit > 0:
      self.critno -= 1
      self.boss.hitpoints = max(0, self.boss.hitpoints - 3 * self.unit.damage)
      self.dueltext += "%s lands a critical hit and leaves %s with %d HP.\n" % (
        self.unit.name,
        self.boss.name,
        self.boss.hitpoints,
      )
    else:
      self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
      self.dueltext += "%s's attack leaves %s with %d HP.\n" % (
        self.unit.name,
        self.boss.name,
        self.boss.hitpoints,
      )

  def bossmiss(self):
    """Boss Miss"""
    self.avoidno -= 1
    self.dueltext += "%s's attack misses.\n" % self.boss.name

  def bosscrit(self):
    """Boss Crit"""
    if self.ddgno > 0:
      self.ddgno -= 1
      self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
      self.dueltext += "%s's attack leaves %s with %d HP.\n" % (
        self.boss.name,
        self.unit.name,
        self.unit.hitpoints,
      )
    else:
      self.unit.hitpoints = max(0, self.unit.hitpoints - 3 * self.boss.damage)
      self.dueltext += "%s lands a critical hit and leaves %s with %d HP.\n" % (
        self.boss.name,
        self.unit.name,
        self.unit.hitpoints,
      )

  def bossattack(self):
    """Boss Attack"""
    self.unit.hitpoints = max(0, self.unit.hitpoints - self.boss.damage)
    self.dueltext += "%s's attack leaves %s with %d HP.\n" % (
      self.boss.name,
      self.unit.name,
      self.unit.hitpoints,
    )

  def playerphase(self):
    """Player Phase"""
    self.dueltext += "Player Phase:\n"
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

  def enemyphase(self):
    """Enemy Phase"""
    self.dueltext += "Enemy Phase: \n"
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

  def reset_text(self):
    """Reset"""
    self.dueltext = ""
  