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
    self.duel = combat.data.DuelSim()

    # Any code you write here will run before the form opens.

  def boss_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.duel.setboss(self.boss_drop.selected_value)
    self.hp.text = self.duel.boss.maxhp
    self.strength.text = self.duel.boss.strength
    self.skill.text = self.duel.boss.skill
    self.speed.text = self.duel.boss.speed
    self.defense.text = self.duel.boss.defense
