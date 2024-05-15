"""Unit 1 Panel"""

from ._anvil_designer import fe5unit1_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe5combat


class fe5unit1_panel(fe5unit1_panelTemplate):
  """Unit Template"""

  def __init__(self, **properties):
    self.init_components(**properties)

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[0].setunit(self.unit_drop.selected_value)
    self.hp.text = self.parent.combat.duels[0].unit.maxhp
    self.strength.text = self.parent.combat.duels[0].unit.strength
    self.magic.text = self.parent.combat.duels[0].unit.magic
    self.skill.text = self.parent.combat.duels[0].unit.skill
    self.speed.text = self.parent.combat.duels[0].unit.speed
    self.luck.text = self.parent.combat.duels[0].unit.luck
    self.defense.text = self.parent.combat.duels[0].unit.defense
    self.build.text = self.parent.combat.duels[0].unit.build
    self.startinghp.text = self.parent.combat.duels[0].unit.maxhp
    self.weapon_drop.selected_value = None
    self.weapon_drop.visible = True
    
  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[0].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[0].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[0].unit.AS
    self.hit.text = self.parent.combat.duels[0].unit.hit
    self.crit.text = self.parent.combat.duels[0].unit.crit

  def setinfo(self):
    """Set Info"""
    self.parent.combat.duels[0].setunithp(self.startinghp.text)
    self.parent.combat.duels[0].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[0].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[0].setddgno(int(self.dodge_drop.selected_value))

  def reset(self):
    """Reset"""
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
    self.customization.visible = False

  def starsbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[0].unit.leaderstars = self.starsbox.text
    self.parent.combat.duels[0].unitdisplay()
    self.hit.text = self.parent.combat.duels[0].unit.hit

  def hidecancel_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
