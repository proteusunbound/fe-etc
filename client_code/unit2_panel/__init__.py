from ._anvil_designer import unit2_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import combat

class unit2_panel(unit2_panelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[1].setunit(self.unit_drop.selected_value)
    self.hp.text = self.parent.combat.duels[1].unit.maxhp
    self.strength.text = self.parent.combat.duels[1].unit.strength
    self.skill.text = self.parent.combat.duels[1].unit.skill
    self.speed.text = self.parent.combat.duels[1].unit.speed
    self.luck.text = self.parent.combat.duels[1].unit.luck
    self.defense.text = self.parent.combat.duels[1].unit.defense
    self.resistance.text = self.parent.combat.duels[1].unit.resistance

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[1].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[1].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[1].unit.AS
    self.hit.text = self.parent.combat.duels[1].unit.hit
    self.atk.text = self.parent.combat.duels[1].unit.attack
    self.crit.text = self.parent.combat.duels[1].unit.crit

  def startinghp_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.parent.combat.duels[1].setunithp(self.startinghp.text)

  def avoid_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[1].setavoidno(int(self.avoid_drop.selected_value))

  def crit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[1].setcritno(int(self.crit_drop.selected_value))

  def dodge_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[1].setddgno(int(self.dodge_drop.selected_value))

  def reset(self):
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.avoid_drop.selected_value = None
    self.crit_drop.selected_value = None
    self.dodge_drop.selected_value = None
    self.startinghp.text = None
    self.visible = False