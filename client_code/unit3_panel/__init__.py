from ._anvil_designer import unit3_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import combat

class unit3_panel(unit3_panelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].setunit(self.unit_drop.selected_value)
    self.hp.text = self.parent.combat.duels[2].unit.maxhp
    self.strength.text = self.parent.combat.duels[2].unit.strength
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.luck.text = self.parent.combat.duels[2].unit.luck
    self.defense.text = self.parent.combat.duels[2].unit.defense
    self.resistance.text = self.parent.combat.duels[2].unit.resistance
    self.startinghp.text = self.parent.combat.duels[2].unit.maxhp

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[2].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[2].unit.AS
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.atk.text = self.parent.combat.duels[2].unit.attack
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def setinfo(self):
    self.parent.combat.duels[2].setunithp(self.startinghp.text)
    self.parent.combat.duels[2].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[2].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[2].setddgno(int(self.dodge_drop.selected_value))

  def reset(self):
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
