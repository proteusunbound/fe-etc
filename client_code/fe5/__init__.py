"""FE5 Calculator"""

from ._anvil_designer import fe5Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe5combat


class fe5(fe5Template):
  """GUI Interface"""

  def __init__(self, **properties):
    self.init_components(**properties)
    self.combat = fe5combat.CombatSim()
    self.unitpanels = [
      self.unit1_panel,
      self.unit2_panel,
      self.unit3_panel,
      self.unit4_panel
    ]

  def unit_number_change(self, **event_args):
    """This method is called when an item is selected"""
    self.combat.setduels(int(self.unit_number.selected_value))
    for i in range(0, int(self.unit_number.selected_value)):
      self.unitpanels[i].visible = True
    self.boss_panel.visible = True
    self.unit_number.visible = False
    self.reset.visible = True

  def boss_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.skilldisplay.content = ""
    for number, name in self.combat.duels.items():
        name.setboss(self.boss_drop.selected_value)
        name.boss.setskills()
    self.hp.text = self.combat.duels[0].boss.maxhp
    self.strength.text = self.combat.duels[0].boss.strength
    self.magic.text = self.combat.duels[0].boss.magic
    self.skill.text = self.combat.duels[0].boss.skill
    self.speed.text = self.combat.duels[0].boss.speed
    self.luck.text = self.combat.duels[0].boss.luck
    self.defense.text = self.combat.duels[0].boss.defense
    self.build.text = self.combat.duels[0].boss.build
    self.startinghp.text = self.combat.duels[0].boss.maxhp
    self.weapon_drop.selected_value = None
    self.weapon_drop.visible = True
    if "Adept" in self.combat.duels[0].boss.skills:
        for i in range(0, int(self.unit_number.selected_value)):
            self.unitpanels[i].cancelproc.visible = True
    for i, skill in enumerate(self.combat.duels[0].boss.skills):
        self.skilldisplay.content += f"{skill} \n"

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    for number, name in self.combat.duels.items():
      name.setbossweapon(self.weapon_drop.selected_value)
      name.bossdisplay()
    self.attackspeed.text = self.combat.duels[0].boss.AS
    self.hit.text = self.combat.duels[0].boss.hit
    self.crit.text = self.combat.duels[0].boss.crit

  def calculatebutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.combat.set_turns(int(self.turn_drop.selected_value))
    for number, name in self.combat.duels.items():
      name.setbosshp(self.startinghp.text)
    for i in range(0, int(self.unit_number.selected_value)):
      self.unitpanels[i].setinfo()
    for number, name in self.combat.duels.items():
      name.counterattack()
      name.doubling()
      name.precombat()
      name.skillprocs()
    self.combat.battle()
    self.combatlog.content = self.combat.text
    self.combatlog.visible = True
    self.combat.reset()

  def reset_click(self, **event_args):
    """This method is called when the button is clicked"""
    for i in range(0, int(self.unit_number.selected_value)):
      self.unitpanels[i].reset()
    self.combat.reset()
    self.combat.duels = {}
    self.boss_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.boss_panel.visible = False
    self.unit_number.visible = True
    self.unit_number.selected_value = None
    self.reset.visible = False
    self.combatlog.visible = False

  def turn_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.calculatebutton.visible = True

  def mainpage_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Landing")

  def terrain_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    for number, name in self.combat.duels.items():
        name.terrain = self.terrain_drop.selected_value
