from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import combat

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.duel = combat.data.DuelSim()

    # Any code you write here will run before the form opens.

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.duel.setunit(self.unit_drop.selected_value)
    self.hp.text = self.duel.unit.maxhp
    self.strength.text = self.duel.unit.strength
    self.skill.text = self.duel.unit.skill
    self.speed.text = self.duel.unit.speed
    self.luck.text = self.duel.unit.luck
    self.defense.text = self.duel.unit.defense
    self.resistance.text = self.duel.unit.resistance

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.duel.setunitweapon(self.weapon_drop.selected_value)
    self.duel.unitdisplay()
    self.attackspeed.text = self.duel.unit.AS
    self.hit.text = self.duel.unit.hit
    self.atk.text = self.duel.unit.attack
    self.crit.text = self.duel.unit.crit
