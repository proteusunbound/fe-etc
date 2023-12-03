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
    self.startinghp.text = self.duel.boss.maxhp

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.duel.setbossweapon(self.weapon_drop.selected_value)
    self.duel.bossdisplay()
    self.attackspeed.text = self.duel.boss.AS
    self.hit.text = self.duel.boss.hit
    self.attack.text = self.duel.boss.attack
    self.crit.text = self.duel.boss.crit

  def startinghp_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.duel.setbosshp(self.startinghp.select())

  def terrainbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.duel.set_terrain(self.terrainbox.checked)

