"""Unit 5 Panel"""
from ._anvil_designer import fe2unit5_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe2combat


class fe2unit5_panel(fe2unit5_panelTemplate):
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
    self.weapon_drop.visible = True
    self.equip_drop.selected_value = None
    self.equip_drop.visible = True
    self.promodrop.selected_value = None
    self.trianglecheck.checked = False
    self.supportbox.checked = False
    if self.parent.combat.duels[4].unit.name in ("Catria", "Palla", "Est"):
      self.trianglecheck.visible = True
    else:
      self.trianglecheck.visible = False
    if self.parent.combat.duels[4].unit.name == "Alm":
      self.supportbox.visible = True
    else:
      self.supportbox.visible = False

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[4].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[4].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[4].unit.AS
    self.hit.text = self.parent.combat.duels[4].unit.hit
    self.crit.text = self.parent.combat.duels[4].unit.crit
    if self.parent.combat.duels[4].unitweapon.name == "Shadow Sword":
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
    self.promodrop.selected_value = None
    self.visible = False
    self.customization.visible = False
    self.equip_drop.selected_value = None
    self.supportbox.visible = False
    self.trianglecheck.visible = False

  def hpshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[4].unit.boosthp(self.hpshrine.text)
    self.hp.text = self.parent.combat.duels[4].unit.maxhp
    self.startinghp.text = self.parent.combat.duels[4].unit.maxhp

  def strshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[4].unit.boost_strength(self.strshrine.text)
    self.strength.text = self.parent.combat.duels[4].unit.strength

  def sklshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[4].unit.boost_skill(self.sklshrine.text)
    self.skill.text = self.parent.combat.duels[4].unit.skill
    self.parent.combat.duels[4].unitdisplay()
    self.hit.text = self.parent.combat.duels[4].unit.hit
    self.crit.text = self.parent.combat.duels[4].unit.crit

  def spdshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[4].unit.boost_speed(self.spdshrine.text)
    self.speed.text = self.parent.combat.duels[4].unit.speed
    self.parent.combat.duels[4].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[4].unit.AS

  def lckshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[4].unit.boostluck(self.lckshrine.text)
    self.luck.text = self.parent.combat.duels[4].unit.luck
    self.parent.combat.duels[4].unitdisplay()
    self.crit.text = self.parent.combat.duels[4].unit.crit

  def defshrine_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[4].unit.boostdefense(self.defshrine.text)
    self.defense.text = self.parent.combat.duels[4].unit.defense

  def promodrop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[4].unit.promote(self.promodrop.selected_value)
    self.hp.text = self.parent.combat.duels[4].unit.maxhp
    self.strength.text = self.parent.combat.duels[4].unit.strength
    self.skill.text = self.parent.combat.duels[4].unit.skill
    self.speed.text = self.parent.combat.duels[4].unit.speed
    self.defense.text = self.parent.combat.duels[4].unit.defense
    self.startinghp.text = self.parent.combat.duels[4].unit.maxhp
    self.parent.combat.duels[4].unitdisplay()
    self.hit.text = self.parent.combat.duels[4].unit.hit
    self.crit.text = self.parent.combat.duels[4].unit.crit
    self.attackspeed.text = self.parent.combat.duels[4].unit.AS

  def equip_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[4].setunitequip(self.equip_drop.selected_value)
    self.parent.combat.duels[4].unitstatadjust()
    self.speed.text = self.parent.combat.duels[4].unit.speed
    self.luck.text = self.parent.combat.duels[4].unit.luck
    self.defense.text = self.parent.combat.duels[4].unit.defense
    self.resistance.text = self.parent.combat.duels[4].unit.resistance

  def supportbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[4].unit.support = self.supportbox.checked

  def trianglecheck_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[4].unit.triangleattack = self.trianglecheck.checked
