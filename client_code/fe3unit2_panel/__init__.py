"""Unit 2 Panel"""
from ._anvil_designer import fe3unit2_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe3combat


class fe3unit2_panel(fe3unit2_panelTemplate):
  """Unit Template"""

  def __init__(self, **properties):
    self.init_components(**properties)

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[1].setunit(self.unit_drop.selected_value)
    self.parent.combat.duels[1].unit.setsupports()
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
    self.support1.checked = False
    self.support2.checked = False
    if self.parent.combat.duels[1].unit.name in ("Astram", "Abel", "Est", "Ogma", "Catria", "Gordin", "Samson", "Caeda", "Sheena", "Julian", "Sirius", "Cecil", "Palla", "Bantu", "Phina", "Merric", "Marth", "Midia", "Minerva", "Jubelo", "Yuliya", "Ryan", "Linde", "Luke", "Lena", "Roderick"):
      self.support.visible = True
      self.support1.text = self.parent.combat.duels[1].unit.supports[0]
      self.support2.text = self.parent.combat.duels[1].unit.supports[1]

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

  def setinfo(self):
    """Set Info"""
    self.parent.combat.duels[1].setunithp(self.startinghp.text)
    self.parent.combat.duels[1].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[1].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[1].setddgno(int(self.dodge_drop.selected_value))

  def reset(self):
    """Reset"""
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
    self.customization.visible = False
    self.supportpanel.visible = False

  def support_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = True

  def hidesupport_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = False

  def support1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[1].unit.setsupportbonus(self.support1.text, self.support1.checked)
    self.parent.combat.duels[1].unitdisplay()
    self.hit.text = self.parent.combat.duels[1].unit.hit
    self.crit.text = self.parent.combat.duels[1].unit.crit

  def support2_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[1].unit.setsupportbonus(self.support2.text, self.support2.checked)
    self.parent.combat.duels[1].unitdisplay()
    self.hit.text = self.parent.combat.duels[1].unit.hit
    self.crit.text = self.parent.combat.duels[1].unit.crit
