from ._anvil_designer import unit4_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import combat

class unit4_panel(unit4_panelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[3].setunit(self.unit_drop.selected_value)
    self.hp.text = self.parent.combat.duels[3].unit.maxhp
    self.strength.text = self.parent.combat.duels[3].unit.strength
    self.skill.text = self.parent.combat.duels[3].unit.skill
    self.speed.text = self.parent.combat.duels[3].unit.speed
    self.luck.text = self.parent.combat.duels[3].unit.luck
    self.defense.text = self.parent.combat.duels[3].unit.defense
    self.resistance.text = self.parent.combat.duels[3].unit.resistance
    self.startinghp.text = self.parent.combat.duels[3].unit.maxhp
    self.weapon_drop.selected_value = None

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[3].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[3].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[3].unit.AS
    self.hit.text = self.parent.combat.duels[3].unit.hit
    self.crit.text = self.parent.combat.duels[3].unit.crit

  def setinfo(self):
    self.parent.combat.duels[3].setunithp(self.startinghp.text)
    self.parent.combat.duels[3].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[3].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[3].setddgno(int(self.dodge_drop.selected_value))

  def reset(self):
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
