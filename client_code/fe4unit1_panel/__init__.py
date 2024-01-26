"""Unit 1 Panel"""
from ._anvil_designer import fe4unit1_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe4combat


class fe4unit1_panel(fe4unit1_panelTemplate):
  """Unit Template"""

  def __init__(self, **properties):
    self.init_components(**properties)

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[0].setunit(self.unit_drop.selected_value)
    self.parent.combat.duels[0].unit.setskills()
    self.hp.text = self.parent.combat.duels[0].unit.maxhp
    self.strength.text = self.parent.combat.duels[0].unit.strength
    self.magic.text = self.parent.combat.duels[0].unit.magic
    self.skill.text = self.parent.combat.duels[0].unit.skill
    self.speed.text = self.parent.combat.duels[0].unit.speed
    self.luck.text = self.parent.combat.duels[0].unit.luck
    self.defense.text = self.parent.combat.duels[0].unit.defense
    self.resistance.text = self.parent.combat.duels[0].unit.resistance
    self.startinghp.text = self.parent.combat.duels[0].unit.maxhp
    self.weapon_drop.selected_value = None
    self.weapon_drop.visible = True
    if "Accost" in self.parent.combat.duels[0].unit.skills:
      self.accostlabel.visible = True
      self.accost_drop.visible = True
    
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
    self.parent.combat.duels[0].setiniaccost(int(self.accost_drop.selected_value))

  def reset(self):
    """Reset"""
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
    self.customization.visible = False
    self.supportpanel.visible = False

  def leaderdrop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[0].unit.setleadership(self.leaderdrop.selected_value)
    self.parent.combat.duels[0].unitdisplay()
    self.hit.text = self.parent.combat.duels[0].unit.hit

  def noaccost_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[0].noaccost = self.noaccost.checked

  def support_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = True

  def hidesupport_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = False

  def lover_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[0].unit.setlover(self.lover.checked)
    self.parent.combat.duels[0].unitdisplay()
    self.hit.text = self.parent.combat.duels[0].unit.hit
    self.crit.text = self.parent.combat.duels[0].unit.crit

  def sibling_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[0].unit.setsibling(self.sibling.checked)
    self.parent.combat.duels[0].unitdisplay()
    self.crit.text = self.parent.combat.duels[0].unit.crit
    
