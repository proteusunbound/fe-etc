from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    unit = app_tables.unit_stats.get(Name=self.unit_drop.selected_value)
    self.hp.text = unit['HP']
    self.strength.text = unit['Str']
    self.skill.text = unit['Skl']
    self.speed.text = unit['Spd']
    self.luck.text = unit['Lck']
    self.defense.text = unit['Def']
    self.resistance.text = unit['Res']
