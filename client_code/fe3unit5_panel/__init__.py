"""Unit 5 Panel"""
from ._anvil_designer import fe3unit5_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe3combat


class fe3unit5_panel(fe3unit5_panelTemplate):
  """Unit Template"""

  def __init__(self, **properties):
    self.init_components(**properties)

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[4].setunit(self.unit_drop.selected_value)
    self.parent.combat.duels[4].unit.setsupports()
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
    self.support1.checked = False
    self.support2.checked = False
    if self.parent.combat.duels[4].unit.name in (
      "Astram", 
      "Abel", 
      "Est", 
      "Ogma", 
      "Catria", 
      "Gordin", 
      "Samson", 
      "Caeda", 
      "Sheena", 
      "Julian", 
      "Sirius", 
      "Cecil", 
      "Palla", 
      "Bantu", 
      "Phina", 
      "Merric", 
      "Marth", 
      "Midia", 
      "Minerva", 
      "Jubelo",
      "Yuliya", 
      "Ryan", 
      "Linde", 
      "Luke", 
      "Lena", 
      "Roderick"):
      self.support.visible = True
      self.support1.text = self.parent.combat.duels[4].unit.supports[0]
      self.support2.text = self.parent.combat.duels[4].unit.supports[1]
    if self.parent.combat.duels[4].unit.name not in (
      "Jagen", 
      "Bord", 
      "Cord", 
      "Barst", 
      "Vyland", 
      "Sedgar", 
      "Wolf", 
      "Hardin", 
      "Caesar", 
      "Radd", 
      "Dolph", 
      "Macellan", 
      "Tomas", 
      "Boah", 
      "Lorenz"):
      self.book2box.visible = True
      self.book2box.checked = False

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
    self.customization.visible = False
    self.supportpanel.visible = False
    self.book2box.visible = False

  def support_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = True

  def hidesupport_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = False

  def support1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[4].unit.setsupportbonus(self.support1.text, self.support1.checked)
    self.parent.combat.duels[4].unitdisplay()
    self.hit.text = self.parent.combat.duels[4].unit.hit
    self.crit.text = self.parent.combat.duels[4].unit.crit

  def support2_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[4].unit.setsupportbonus(self.support2.text, self.support2.checked)
    self.parent.combat.duels[4].unitdisplay()
    self.hit.text = self.parent.combat.duels[4].unit.hit
    self.crit.text = self.parent.combat.duels[4].unit.crit

  def book2box_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[4].unit.booktwo(self.book2box.checked)
    self.hp.text = self.parent.combat.duels[4].unit.maxhp
    self.strength.text = self.parent.combat.duels[4].unit.strength
    self.skill.text = self.parent.combat.duels[4].unit.skill
    self.speed.text = self.parent.combat.duels[4].unit.speed
    self.luck.text = self.parent.combat.duels[4].unit.luck
    self.defense.text = self.parent.combat.duels[4].unit.defense
    self.resistance.text = self.parent.combat.duels[4].unit.resistance
    self.startinghp.text = self.parent.combat.duels[4].unit.maxhp
    self.weapon_drop.selected_value = None
