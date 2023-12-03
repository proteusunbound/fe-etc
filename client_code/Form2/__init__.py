from ._anvil_designer import Form2Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import combat

class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.combat = combat.CombatSim()
    self.unitpanels = [self.unit1_panel, self.unit2_panel, self.unit3_panel]
    # Any code you write here will run before the form opens.
  
  def unit_number_change(self, **event_args):
    """This method is called when an item is selected"""
    self.combat.setduels(int(self.unit_number.selected_value))
    for i in range (0, int(self.unit_number.selected_value)):
      self.unitpanels[i].visible = True
    self.boss_panel.visible = True
    self.unit_number.visible = False
    self.reset.visible = True
        
  def boss_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    for number, name in self.combat.duels.items():
      name.setboss(self.boss_drop.selected_value)
    self.hp.text = self.combat.duels[0].boss.maxhp
    self.strength.text = self.combat.duels[0].boss.strength
    self.skill.text = self.combat.duels[0].boss.skill
    self.speed.text = self.combat.duels[0].boss.speed
    self.defense.text = self.combat.duels[0].boss.defense
    self.startinghp.text = self.combat.duels[0].boss.maxhp

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    for number, name in self.combat.duels.items():
      name.setbossweapon(self.weapon_drop.selected_value)
      name.bossdisplay()
    self.attackspeed.text = self.combat.duels[0].boss.AS
    self.hit.text = self.combat.duels[0].boss.hit
    self.attack.text = self.combat.duels[0].boss.attack
    self.crit.text = self.combat.duels[0].boss.crit
  
  def terrainbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    for number, name in self.combat.duels.items():
      name.set_terrain(self.terrainbox.checked)

  def calculatebutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.combat.set_turns(int(self.turn_drop.selected_value))
    for number, name in self.combat.duels.items():
      name.setbosshp(self.startinghp.text)
    for number, name in self.combat.duels.items():
      name.precombat()
      name.counterattack()
      name.doubling()
    for i in range(0, int(self.unit_number.selected_value)):
      self.unitpanels[i].setinfo()
    self.combat.battle()
    self.combatlog.content = self.combat.text
    self.combatlog.visible = True
    self.combat.reset()

  def reset_click(self, **event_args):
    """This method is called when the button is clicked"""
    for i in range (0, int(self.unit_number.selected_value)):
      self.unitpanels[i].reset()
    self.combat.reset()
    self.boss_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.terrainbox.checked = False
    self.boss_panel.visible = False
    self.unit_number.visible = True
    self.unit_number.selected_value = None
    self.reset.visible = False
    self.combatlog.visible = False