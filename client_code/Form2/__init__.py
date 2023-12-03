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
    self.combat.setduels(1)

    # Any code you write here will run before the form opens.

  def boss_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.combat.duels[0].setboss(self.boss_drop.selected_value)
    self.hp.text = self.combat.duels[0].boss.maxhp
    self.strength.text = self.combat.duels[0].boss.strength
    self.skill.text = self.combat.duels[0].boss.skill
    self.speed.text = self.combat.duels[0].boss.speed
    self.defense.text = self.combat.duels[0].boss.defense

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.combat.duels[0].setbossweapon(self.weapon_drop.selected_value)
    self.combat.duels[0].bossdisplay()
    self.attackspeed.text = self.combat.duels[0].boss.AS
    self.hit.text = self.combat.duels[0].boss.hit
    self.attack.text = self.combat.duels[0].boss.attack
    self.crit.text = self.combat.duels[0].boss.crit

  def startinghp_change(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.combat.duels[0].setbosshp(self.startinghp.text)
  
  def terrainbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.combat.duels[0].set_terrain(self.terrainbox.checked)

  def turn_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.combat.set_turns(int(self.turn_drop.selected_value))

  def calculatebutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.combat.duels[0].precombat()
    self.combat.duels[0].counterattack()
    self.combat.duels[0].doubling()
    self.combat.battle()
    self.combatlog.content = self.combat.text
    self.combat.reset()

  def reset_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.unit_panel_1.reset()
    self.boss_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.startinghp.text = None
    self.terrainbox.checked = False
    self.turn_drop.selected_value = None

