"""Unit 5 Panel"""
from ._anvil_designer import unit5_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import combat

class unit5_panel(unit5_panelTemplate):
  """Unit Template"""
  def __init__(self, **properties):
    self.init_components(**properties)

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[4].setunit(self.unit_drop.selected_value)
    self.hp.text = self.parent.combat.duels[4].unit.maxhp
    self.strength.text = self.parent.combat.duels[4].unit.strength
    self.skill.text = self.parent.combat.duels[4].unit.skill
    self.speed.text = self.parent.combat.duels[4].unit.speed
    self.luck.text = self.parent.combat.duels[4].unit.luck
    self.defense.text = self.parent.combat.duels[4].unit.defense
    self.resistance.text = self.parent.combat.duels[4].unit.resistance
    self.startinghp.text = self.parent.combat.duels[4].unit.maxhp
    self.weapon_drop.selected_value = None

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[4].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[4].unitdisplay()
    self.parent.combat.duels[4].unitstatadjust()
    self.defense.text = self.parent.combat.duels[4].unit.defense
    self.attackspeed.text = self.parent.combat.duels[4].unit.AS
    self.hit.text = self.parent.combat.duels[4].unit.hit
    self.crit.text = self.parent.combat.duels[4].unit.crit
    if self.parent.combat.duels[4].unitweapon.name in ("Devil Sword", "Devil Axe"):
      self.devil_label.visible = True
      self.devildrop.visible = True

  def setinfo(self):
    """Set Info"""
    self.parent.combat.duels[4].setunithp(self.startinghp.text)
    self.parent.combat.duels[4].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[4].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[4].setddgno(int(self.dodge_drop.selected_value))
    self.parent.combat.duels[4].setdevilno(int(self.devildrop.selected_value))

  def reset(self):
    """Reset"""
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
