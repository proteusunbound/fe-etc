"""Data"""
import math
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import fe4skills

skills = fe4skills.skill_list

@anvil.server.portable_class
class ActiveUnit:
    """Active Unit"""

    def __init__(self, keyword):
        self.char = app_tables.fe4_unit_stats.get(Name=keyword)
        self.name = self.char["Name"]
        self.maxhp = self.char["HP"]
        self.strength = self.char["Str"]
        self.magic = self.char["Mag"]
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
        self.leader = 0
        self.charm = 0
        self.accostrate = 1
        self.adeptrate = 1
        self.adeptcancel = 1
        self.solrate = 1
        self.lunarate = 1
        self.astrarate = 1
        self.pavisecancel = 1
        self.skills = []
        self.hitbonus = 0
        self.critbonus = 0

    def setleadership(self, keyword):
      if keyword == "Sigurd":
        self.leader = 10
      if keyword == "Seliph":
        self.leader = 20

    def setcharm(self, charmcheck):
      if charmcheck is True:
        self.charm = 10

    def setskills(self):
      if self.name in skills:
        self.skills = skills[self.name]

    def setlover(self, lover):
      if lover is True:
        self.hitbonus = 10
        self.critbonus = 20
      
    def setsibling(self, sibling):
      if sibling is True:
        self.critbonus = 20

@anvil.server.portable_class
class ActiveWeapon:
    """Active Weapon"""

    def __init__(self, keyword):
        weapon = app_tables.fe4_weapon_stats.get(Name=keyword)
        self.name = weapon["Name"]
        self.might = weapon["Mgt"]
        self.weight = weapon["Wgt"]
        self.hit = weapon["Hit"]
        self.type = weapon["Type"]
        self.minrange = weapon["Min Range"]
        self.maxrange = weapon["Max Range"]
        self.weapontriangle = 0
        self.effective = False

@anvil.server.portable_class
class ActiveBoss:
    """Active Boss"""

    def __init__(self, keyword):
        boss = app_tables.fe4_boss_stats.get(Name=keyword)
        self.name = boss["Name"]
        self.maxhp = boss["HP"]
        self.strength = boss["Str"]
        self.magic = boss["Mag"]
        self.skill = boss["Skl"]
        self.speed = boss["Spd"]
        self.luck = boss["Lck"]
        self.defense = boss["Def"]
        self.resistance = boss["Res"]
        self.leader = boss["Leadership"]
        self.charclass = boss["Class"]
        self.level = boss["Level"]
        self.charm = 0
        self.hitpoints = 0
        self.doubles = False
        self.damage = 0
        self.hit = 0
        self.attack = 0
        self.avoid = 0
        self.hitchance = 0
        self.skills = []
        self.counter = False
        self.hitbonus = 0

    def setskills(self):
      if self.name in skills:
        self.skills = skills[self.name]

def attack_speed(keyword, weapon):
    """Attack Speed"""
    keyword.AS = keyword.speed - weapon.weight

def hitrate(keyword, weapon):
    """Hit Rate"""
    keyword.hit = keyword.skill * 2 + weapon.hit + keyword.leader + weapon.weapontriangle + keyword.hitbonus + keyword.charm

def physattack(keyword, weapon):
    """Physical Attack"""
    keyword.attack = keyword.strength + weapon.might

def magattack(keyword, weapon):
  """Magical Attack"""
  keyword.attack = keyword.magic + weapon.might

def physdamage(attacker, defender):
    """Physical Damage"""
    attacker.damage = max(1, attacker.attack - defender.defense)

def magdamage(attacker, defender):
    """Magical Damage"""
    attacker.damage = max(1, attacker.attack - defender.resistance)

def physcrit(attacker, defender):
  """Physical Crit"""
  attacker.critdamage = max(1, 2 * attacker.attack - defender.defense)

def magcrit(attacker, defender):
  """Magical Crit"""
  attacker.critdamage = max(1, 2 * attacker.attack - defender.resistance)

def effectiveness(weapon, keyword):
  """Effectiveness"""
  effcheck = app_tables.fe4_effectiveness.get(Name=weapon.name)
  weapon.effective = effcheck[keyword.charclass]

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
        self.iniaccost = 0
        self.iniadept = 0
        self.adeptno = 0
        self.inicanceladept = 0
        self.canceladeptno = 0
        self.inisol = 0
        self.solno = 0
        self.iniluna = 0
        self.lunano = 0
        self.iniastra = 0
        self.astrano = 0
        self.cancelpaviseno = 0
        self.unithit = 0
        self.unitavoid = 0
        self.unitcrit = 0
        self.unitdodge = 0
        self.terrain = False
        self.noaccost = False
        self.unitequip = []
        self.bossequip = []

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
      self.unitequip.append(equipment)

    def setbossequip(self, equipment):
      """Set Boss Equipment"""
      self.bossequip.append(equipment)

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

    def setiniaccost(self, accostnum):
      """Set Accost Number"""
      self.iniaccost = accostnum

    def setadeptno(self, adeptnum):
      """Set Adept Number"""
      self.iniadept = adeptnum
      self.adeptno = adeptnum

    def setcanceladeptno(self, adeptavo):
      """Set Adept Avoids"""
      self.inicanceladept = adeptavo
      self.canceladeptno = adeptavo

    def setsolno(self, solno):
      """Set Sol Number"""
      self.inisol = solno
      self.solno = solno

    def setlunano(self, lunano):
      """Set Luna Number"""
      self.iniluna = lunano
      self.lunano = lunano

    def setastrano(self, astrano):
      """Set Astra Number"""
      self.iniastra = astrano
      self.astrano = astrano

    def setbosshp(self, hitpoints):
        """Set Boss HP"""
        self.boss.hitpoints = hitpoints

    def weapontriangle(self):
      """Weapon Triangle"""
      if (self.unitweapon.type == "Sword" and self.bossweapon.type == "Axe") or (self.unitweapon.type == "Lance" and self.bossweapon.type == "Sword") or (self.unitweapon.type == "Axe" and self.bossweapon.type == "Lance") or (self.unitweapon.type == "Fire" and self.bossweapon.type == "Wind") or (self.unitweapon.type == "Thunder" and self.bossweapon.type == "Fire") or (self.unitweapon.type == "Wind" and self.bossweapon.type == "Thunder") or (self.unitweapon.type in ("Light", "Dark") and self.bossweapon.type in ("Fire", "Wind", "Thunder")):
        self.unitweapon.weapontriangle = 20
        self.bossweapon.weapontriangle = -20
      elif (self.bossweapon.type == "Sword" and self.unitweapon.type == "Axe") or (self.bossweapon.type == "Lance" and self.unitweapon.type == "Sword") or (self.bossweapon.type == "Axe" and self.unitweapon.type == "Lance") or (self.bossweapon.type == "Fire" and self.unitweapon.type == "Wind") or (self.bossweapon.type == "Thunder" and self.unitweapon.type == "Fire") or (self.bossweapon.type == "Wind" and self.unitweapon.type == "Thunder") or (self.bossweapon.type in ("Light", "Dark") and self.unitweapon.type in ("Fire", "Wind", "Thunder")):
        self.bossweapon.weapontriangle = 20
        self.unitweapon.weapontriangle = -20
      else:
        self.unitweapon.weapontriangle = 0
        self.bossweapon.weapontriangle = 0

    def hpthreshold(self):
      """HP Threshold"""
      if "Miracle" in self.unit.skills and self.unit.hitpoints <= 10:
        self.unitavoid = min(self.unitavoid + (11 - self.unit.hitpoints) / 10, 1)
      else:
        self.unitavoid = 1 - self.boss.hitchance
      if "Miracle" in self.boss.skills and self.boss.hitpoints <= 10:
        self.boss.avoid = self.boss.avoid + (11 - self.boss.hitpoints) * 10
        self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)
      else:
        self.enemy_avoid()
        self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)

    def unitstatadjust(self):
      """Adjust Unit Stats"""
      if "Power Ring" in self.unitequip:
        self.unit.strength += 5
      if "Magic Ring" in self.unitequip:
        self.unit.magic += 5
      if "Skill Ring" in self.unitequip:
        self.unit.skill += 5
      if "Speed Ring" in self.unitequip:
        self.unit.speed += 5
      if "Shield Ring" in self.unitequip:
        self.unit.defense += 5
      if "Barrier Ring" in self.unitequip:
        self.unit.resistance += 5

    def adjustunitskills(self):
      """Abjust Unit Skills"""
      if "Renewal Band" in self.unitequip:
        self.unit.skills.append("Renewal")
      if "Miracle Band" in self.unitequip:
        self.unit.skills.append("Miracle")
      if "Follow-Up Ring" in self.unitequip:
        self.unit.skills.append("Follow-Up")
      if "Circlet" in self.unitequip:
        self.unit.skills.append("Renewal")
        self.unit.skills.append("Miracle")
        

    def adjust_boss_skills(self):
      """Adjust Boss Skills"""
      if "Renewal Band" in self.bossequip:
        self.boss.skills.append("Renewal")

    def boss_stat_adjust(self):
      """Adjust Boss Stats"""
      if "Power Ring" in self.bossequip:
        self.boss.strength += 5
      if "Magic Ring" in self.bossequip:
        self.boss.magic += 5
      if "Skill Ring" in self.bossequip:
        self.boss.skill += 5
      if "Speed Ring" in self.bossequip:
        self.boss.speed += 5
      if "Shield Ring" in self.bossequip:
        self.boss.defense += 5
      if "Barrier Ring" in self.bossequip:
        self.boss.resistance += 5

    def unitdisplay(self):
        """Unit Stat Display"""
        attack_speed(self.unit, self.unitweapon)
        hitrate(self.unit, self.unitweapon)
        if "Critical" in self.unit.skills:
          self.unit.crit = self.unit.skill + self.unit.critbonus
        else:
          self.unit.crit = self.unit.critbonus

    def bossdisplay(self):
        """Boss Stat Display"""
        attack_speed(self.boss, self.bossweapon)
        hitrate(self.boss, self.bossweapon)
        if "Critical" in self.boss.skills:
          self.boss.crit = self.boss.skill
        else:
          self.boss.crit = 0

    def enemy_avoid(self):
      """Enemy Avoid"""
      if self.terrain is True:
        self.boss.avoid = (self.boss.AS * 2) + self.boss.luck + self.boss.leader + 30
      else:
        self.boss.avoid = (self.boss.AS) * 2 + self.boss.luck + self.boss.leader

    def bosshitchance(self):
      """Boss Hit Chance"""
      hitchance = min(((self.boss.hit - (self.unit.AS * 2 + self.unit.luck + self.unit.leader + self.unit.charm)) / 100), 1)
      self.boss.hitchance = max(0, hitchance)

    def precombat(self):
      """Pre-Combat Calculation"""
      self.weapontriangle()
      hitrate(self.unit, self.unitweapon)
      hitrate(self.boss, self.bossweapon)
      if self.unitweapon.type in ("Sword", "Lance", "Axe", "Bow"):
        physattack(self.unit, self.unitweapon)
        physdamage(self.unit, self.boss)
        physcrit(self.unit, self.boss)
      else:
        magattack(self.unit, self.unitweapon)
        magdamage(self.unit, self.boss)
        magcrit(self.unit, self.boss)
      self.enemy_avoid()
      if self.bossweapon.type in ("Sword", "Lance", "Axe", "Bow"):
        physattack(self.boss, self.bossweapon)
        physdamage(self.boss, self.unit)
        physcrit(self.boss, self.unit)
      else:
        magattack(self.boss, self.bossweapon)
        magdamage(self.boss, self.unit)
        magcrit(self.boss, self.unit)
      self.bosshitchance()
      self.unithit = min((self.unit.hit - self.boss.avoid) / 100, 1)
      self.unitcrit = self.unit.crit / 100
      self.unitavoid = 1 - self.boss.hitchance
      self.unitdodge = 1 - (self.boss.crit / 100)
      if "Adept" in self.unit.skills:
        self.unit.adeptrate = (self.unit.AS + 20) / 100
      if "Adept" in self.boss.skills:
        self.unit.adeptcancel = 1 - ((self.boss.AS + 20) / 100)
      if "Sol" in self.unit.skills:
        self.unit.solrate = self.unit.skill / 100
      if "Luna" in self.unit.skills:
        self.unit.lunarate = self.unit.skill / 100
      if "Astra" in self.unit.skills:
        self.unit.astrarate = self.unit.skill / 100
      if "Pavise" in self.boss.skills:
        self.unit.pavisecancel = 1 - (self.boss.level / 100)

    def effectivecheck(self):
      """Effectiveness Log"""
      effectiveness(self.unitweapon, self.boss)
      effectiveness(self.bossweapon, self.unit)
      if self.unitweapon.effective is True:
        self.dueltext += f"{self.unit.name}'s {self.unitweapon.name} deals effective damage against {self.boss.name}. \n"
      if self.bossweapon.effective is True:
        self.dueltext += f"{self.boss.name}'s {self.bossweapon.name} deals effective damage against {self.unit.name}. \n"

    def doubling(self):
        """Doubling Calculation"""
        if self.unit.AS > self.boss.AS and "Follow-Up" in self.unit.skills:
            self.unit.doubles = True
            self.boss.doubles = False
            self.dueltext += f"{self.unit.name} can make follow-up attacks. \n"
        elif self.boss.AS > self.unit.AS and "Follow-Up" in self.boss.skills:
            self.boss.doubles = True
            self.unit.doubles = False
            self.dueltext += f"{self.boss.name} can make follow-up attacks. \n"
        else:
            self.unit.doubles = False
            self.boss.doubles = False

    def counterattack(self):
      """Counter Attack"""
      if self.bossweapon.name in ("Meteor", "Bolting", "Blizzard", "Fenrir"):
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

    def hprecover(self):
      """Player Phase HP Recover""";
      if self.unit.maxhp > self.unit.hitpoints:
        if "Renewal" in self.unit.skills:
          self.unit.hitpoints = min(self.unit.hitpoints + 5, self.unit.maxhp)
          self.dueltext += f"{self.unit.name} heals to {self.unit.hitpoints} HP at the start of the round.\n"

    def unitadept(self):
      """Unit Adept"""
      if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
        self.dueltext += f"{self.unit.name} strikes twice consecutively. \n"
        if "Astra" in self.unit.skills and self.astrano > 0 and "Nihil" not in self.boss.skills:
          self.astrano -= 1
          self.astra()
        elif self.unit.crit == 100 and "Nihil" not in self.boss.skills:
          self.unit_crit()
        elif self.unit.crit > 0 and self.critno > 0 and "Nihil" not in self.boss.skills:
          self.critno -= 1
          self.unit_crit()
        else:
          self.unitattack()

    def astra(self):
      """Astra"""
      self.dueltext += f"{self.unit.name} activates Astra. \n"
      for i in range (0, 5):
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
          if self.unit.crit == 100:
            self.unit_crit()
          elif self.unit.crit > 0 and self.critno > 0:
            self.critno -= 1
            self.unit_crit()
          else:
            self.unitattack()

    def unit_crit(self):
      """Unit Crit"""
      self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.critdamage)
      self.dueltext += f"{self.unit.name} lands a critical hit and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
      if "Sol" in self.unit.skills and self.solno > 0 and self.unit.hitpoints < self.unit.maxhp:
        self.solno -= 1
        self.unit.hitpoints = min(self.unit.hitpoints + self.unit.critdamage, self.unit.maxhp)
        self.dueltext += f"{self.unit.name} restores to {self.unit.hitpoints} HP. \n"
      elif "Pavise" in self.boss.skills:
        self.cancelpaviseno += 1
        self.hitno += 1
      else:
        self.hitno += 1

    def unitattack(self):
        """Unit Attack"""
        if "Luna" in self.unit.skills and self.lunano > 0:
          self.lunano -= 1
          self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.attack)
          self.dueltext += f"{self.unit.name} activates Luna and leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
        else:
          self.boss.hitpoints = max(0, self.boss.hitpoints - self.unit.damage)
          self.dueltext += f"{self.unit.name}'s attack leaves {self.boss.name} with {self.boss.hitpoints} HP.\n"
          if "Sol" in self.unit.skills and self.solno > 0 and self.unit.hitpoints < self.unit.maxhp:
            self.solno -= 1
            self.unit.hitpoints = min(self.unit.hitpoints + self.unit.damage, self.unit.maxhp)
            self.dueltext += f"{self.unit.name} restores to {self.unit.hitpoints} HP. \n"
          elif "Pavise" in self.boss.skills:
            self.cancelpaviseno += 1
            self.hitno += 1
          else:
            self.hitno += 1

    def bossadept(self):
      """Boss Adept"""
      if self.canceladeptno > 0:
        self.canceladeptno -= 1
      elif self.boss.hitpoints > 0 and self.unit.hitpoints and self.boss.counter is True > 0:
        self.dueltext += f"{self.boss.name} strikes twice consecutively. \n"
        if self.boss.hitchance == 0:
          self.bossmiss()
        elif self.avoidno > 0:
          self.avoidno -= 1
          self.bossmiss()
        elif self.boss.crit > 0 and "Nihil" not in self.unit.skills:
          self.bosscrit()
        else:
          self.bossattack() 
  
    def bossmiss(self):
        """Boss Miss"""
        self.dueltext += f"{self.boss.name}'s attack misses.\n"

    def bosscrit(self):
      """Boss Crit"""
      if self.boss.crit < 100 and self.ddgno > 0 and self.bossweapon.effective is False:
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

    def playerphase(self):
        """Player Phase"""
        self.dueltext += "#### Player Phase:\n"
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            if "Astra" in self.unit.skills and self.astrano > 0 and "Nihil" not in self.boss.skills:
              self.astrano -= 1
              self.astra()
            elif (self.unit.crit == 100 or self.unitweapon.effective is True) and "Nihil" not in self.boss.skills:
                self.unit_crit()
            elif self.unit.crit > 0 and self.critno > 0 and "Nihil" not in self.boss.skills:
                self.critno -= 1
                self.unit_crit()
            else:
                self.unitattack()
            if "Adept" in self.unit.skills and self.adeptno > 0:
              self.adeptno -= 1
              self.unitadept()
        if self.boss.hitpoints > 0 and self.unit.hitpoints and self.boss.counter is True > 0:
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            elif (self.boss.crit > 0 or self.bossweapon.effective is True) and "Nihil" not in self.unit.skills:
                self.bosscrit()
            else:
                self.bossattack()
            if "Adept" in self.boss.skills:
              self.bossadept()
        if self.unit.doubles is True and self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            if "Astra" in self.unit.skills and self.astrano > 0 and "Nihil" not in self.boss.skills:
              self.astrano -= 1
              self.astra()
            elif (self.unit.crit == 100 or self.unitweapon.effective is True) and "Nihil" not in self.boss.skills:
                self.unit_crit()
            elif self.unit.crit > 0 and self.critno > 0 and "Nihil" not in self.boss.skills:
                self.critno -= 1
                self.unit_crit()
            else:
                self.unitattack()
            if "Adept" in self.unit.skills and self.adeptno > 0:
              self.adeptno -= 1
              self.unitadept()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
            and self.boss.counter is True
        ):
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            elif (self.boss.crit > 0 or self.bossweapon.effective is True) and "Nihil" not in self.unit.skills:
                self.bosscrit()
            else:
                self.bossattack()
            if "Adept" in self.boss.skills:
              self.bossadept()
        self.dueltext += "\n"

    def enemyphase(self):
        """Enemy Phase"""
        self.dueltext += "#### Enemy Phase:\n"
        if self.boss.hitpoints > 0 and self.unit.hitpoints > 0 and self.boss.counter is True:
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            elif (self.boss.crit > 0 or self.bossweapon.effective is True) and "Nihil" not in self.unit.skills:
                self.bosscrit()
            else:
                self.bossattack()
            if "Adept" in self.boss.skills:
              self.bossadept()
        if self.unit.hitpoints > 0 and self.boss.hitpoints > 0:
            if "Astra" in self.unit.skills and self.astrano > 0 and "Nihil" not in self.boss.skills:
              self.astrano -= 1
              self.astra()
            elif (self.unit.crit == 100 or self.unitweapon.effective is True) and "Nihil" not in self.boss.skills:
                self.unit_crit()
            elif self.unit.crit > 0 and self.critno > 0 and "Nihil" not in self.boss.skills:
                self.critno -= 1
                self.unit_crit()
            else:
                self.unitattack()
            if "Adept" in self.unit.skills and self.adeptno > 0:
              self.adeptno -= 1
              self.unitadept()
        if (
            self.boss.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
            and self.boss.counter is True
        ):
            if self.boss.hitchance == 0:
                self.bossmiss()
            elif self.avoidno > 0:
                self.avoidno -= 1
                self.bossmiss()
            elif (self.boss.crit > 0 or self.bossweapon.effective is True) and "Nihil" not in self.unit.skills:
                self.bosscrit()
            else:
                self.bossattack()
            if "Adept" in self.boss.skills:
              self.bossadept()
        if (
            self.unit.doubles is True
            and self.unit.hitpoints > 0
            and self.boss.hitpoints > 0
        ):
            if "Astra" in self.unit.skills and self.astrano > 0 and "Nihil" not in self.boss.skills:
              self.astrano -= 1
              self.astra()
            elif (self.unit.crit == 100 or self.unitweapon.effective is True) and "Nihil" not in self.boss.skills:
                self.unit_crit()
            elif self.unit.crit > 0 and self.critno > 0 and "Nihil" not in self.boss.skills:
                self.critno -= 1
                self.unit_crit()
            else:
                self.unitattack()
            if "Adept" in self.unit.skills and self.adeptno > 0:
              self.adeptno -= 1
              self.unitadept()
        self.dueltext += "\n"

    def accost(self):
      accostavoid = 1
      if "Accost" in self.boss.skills and self.noaccost is False:
        ceiling = math.floor((self.boss.maxhp - 25) / self.unit.damage)
        for i in range(0, ceiling):
          if self.boss.hitpoints >= 25 and self.unit.hitpoints > 0:
            self.dueltext += f"{self.boss.name} activates Accost. \n"
            self.enemyphase()
          else:
            break
      elif self.noaccost is True:
        accostavoid = 1 - (self.boss.AS - self.unit.AS + (self.boss.hitpoints / 2))
      if "Accost" in self.unit.skills and self.iniaccost > 0:
        for i in range (0, self.iniaccost):
          if self.unit.hitpoints >= 25:
            self.dueltext += f"{self.unit.name} activates Accost. \n"
            self.playerphase()
            self.unit.accostrate *= (self.unit.AS - self.boss.AS + (self.unit.hitpoints / 2))
            self.iniaccost -= 1
          else:
            break
      self.unit.accostrate *= accostavoid

    def reset_text(self):
        """Reset"""
        self.dueltext = ""