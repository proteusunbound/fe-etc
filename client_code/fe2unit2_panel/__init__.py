"""Unit 2 Panel"""
from ._anvil_designer import fe2unit2_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe2combat


class fe2unit2_panel(fe2unit2_panelTemplate):
  """Unit Template"""

  def __init__(self, **properties):
    self.init_components(**properties)

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
    self.startinghp.text = self.parent.combat.duels[1].unit.maxhp
    self.weapon_drop.selected_value = None
    self.weapon_drop.visible = True
    self.promodrop.selected_value = None

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[1].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[1].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[1].unit.AS
    self.hit.text = self.parent.combat.duels[1].unit.hit
    self.crit.text = self.parent.combat.duels[1].unit.crit
    if self.parent.combat.duels[1].unitweapon.name == "Shadow Sword":
      self.devil_label.visible = True
      self.devildrop.visible = True

  def setinfo(self):
    """Set Info"""
    self.parent.combat.duels[1].setunithp(self.startinghp.text)
    self.parent.combat.duels[1].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[1].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[1].setddgno(int(self.dodge_drop.selected_value))
    self.parent.combat.duels[1].setdevilno(int(self.devildrop.selected_value))

  def reset(self):
    """Reset"""
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.promodrop.selected_value = None
    self.visible = False
    self.customization.visible = False

  def hpshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[1].unit.boosthp(self.hpshrine.text)
    self.hp.text = self.parent.combat.duels[1].unit.maxhp
    self.startinghp.text = self.parent.combat.duels[1].unit.maxhp

  def strshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[1].unit.boost_strength(self.strshrine.text)
    self.strength.text = self.parent.combat.duels[1].unit.strength

  def sklshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[1].unit.boost_skill(self.sklshrine.text)
    self.skill.text = self.parent.combat.duels[1].unit.skill
    self.parent.combat.duels[1].unitdisplay()
    self.hit.text = self.parent.combat.duels[1].unit.hit
    self.crit.text = self.parent.combat.duels[1].unit.crit

  def spdshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[1].unit.boost_speed(self.spdshrine.text)
    self.speed.text = self.parent.combat.duels[1].unit.speed
    self.parent.combat.duels[1].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[1].unit.AS

  def lckshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[1].unit.boostluck(self.lckshrine.text)
    self.luck.text = self.parent.combat.duels[1].unit.luck
    self.parent.combat.duels[1].unitdisplay()
    self.crit.text = self.parent.combat.duels[1].unit.crit

  def defshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[1].unit.boostdefense(self.defshrine.text)
    self.defense.text = self.parent.combat.duels[1].unit.defense

  def promodrop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[1].unit.promote(self.promodrop.selected_value)
    self.hp.text = self.parent.combat.duels[1].unit.maxhp
    self.strength.text = self.parent.combat.duels[1].unit.strength
    self.skill.text = self.parent.combat.duels[1].unit.skill
    self.speed.text = self.parent.combat.duels[1].unit.speed
    self.defense.text = self.parent.combat.duels[1].unit.defense
    self.startinghp.text = self.parent.combat.duels[1].unit.maxhp
    self.parent.combat.duels[1].unitdisplay()
    self.hit.text = self.parent.combat.duels[1].unit.hit
    self.crit.text = self.parent.combat.duels[1].unit.crit
    self.attackspeed.text = self.parent.combat.duels[1].unit.AS
