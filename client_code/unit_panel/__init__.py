from ._anvil_designer import unit_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import combat

class unit_panel(unit_panelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.duel.setunit(self.unit_drop.selected_value)
    self.hp.text = self.parent.duel.unit.maxhp
    self.strength.text = self.parent.duel.unit.strength
    self.skill.text = self.parent.duel.unit.skill
    self.speed.text = self.parent.duel.unit.speed
    self.luck.text = self.parent.duel.unit.luck
    self.defense.text = self.parent.duel.unit.defense
    self.resistance.text = self.parent.duel.unit.resistance
    self.startinghp.text = self.parent.duel.unit.maxhp

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.duel.setunitweapon(self.weapon_drop.selected_value)
    self.parent.duel.unitdisplay()
    self.attackspeed.text = self.parent.duel.unit.AS
    self.hit.text = self.parent.duel.unit.hit
    self.atk.text = self.parent.duel.unit.attack
    self.crit.text = self.parent.duel.unit.crit

  def startinghp_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.parent.duel.setunithp(self.startinghp.select())

  def avoid_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.duel.setavoidno(self.avoid_drop.selected_value)

  def crit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.duel.setcritno(self.crit_drop.selected_value)

  def dodge_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.duel.setddgno(self.dodge_drop.selected_value)
