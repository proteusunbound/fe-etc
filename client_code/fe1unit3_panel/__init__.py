"""Unit 3 Panel"""
from ._anvil_designer import fe1unit3_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe1combat


class fe1unit3_panel(fe1unit3_panelTemplate):
  """Unit Template"""

  def __init__(self, **properties):
    self.init_components(**properties)

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].setunit(self.unit_drop.selected_value)
    self.hp.text = self.parent.combat.duels[2].unit.maxhp
    self.strength.text = self.parent.combat.duels[2].unit.strength
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.luck.text = self.parent.combat.duels[2].unit.luck
    self.defense.text = self.parent.combat.duels[2].unit.defense
    self.resistance.text = self.parent.combat.duels[2].unit.resistance
    self.startinghp.text = self.parent.combat.duels[2].unit.maxhp
    self.weapon_drop.selected_value = None
    self.weapon_drop.visible = True
    self.promobox.checked = False
    self.trianglecheck.checked = False
    if self.parent.combat.duels[2].unit.charclass in ("Cavalier", "Mercenary", "Archer", "Curate", "Mage", "Pegasus Knight"):
      self.promobox.visible = True
    else:
      self.promobox.visible = False
    if self.parent.combat.duels[2].unit.name in ("Catria", "Palla", "Est"):
      self.trianglecheck.visible = True
    else:
      self.trianglecheck.visble = False

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[2].unitdisplay()
    self.parent.combat.duels[2].unitstatadjust()
    self.defense.text = self.parent.combat.duels[2].unit.defense
    self.attackspeed.text = self.parent.combat.duels[2].unit.AS
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit
    if self.parent.combat.duels[2].unitweapon.name in ("Devil Sword", "Devil Axe"):
      self.devil_label.visible = True
      self.devildrop.visible = True

  def setinfo(self):
    """Set Info"""
    self.parent.combat.duels[2].setunithp(self.startinghp.text)
    self.parent.combat.duels[2].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[2].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[2].setddgno(int(self.dodge_drop.selected_value))
    self.parent.combat.duels[2].setdevilno(int(self.devildrop.selected_value))

  def reset(self):
    """Reset"""
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
    self.customization.visible = False
    self.promobox.visible = False
    self.trianglecheck.visible = False

  def seraphrobe_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].unit.boosthp(int(self.seraphrobe.selected_value))
    self.hp.text = self.parent.combat.duels[2].unit.maxhp
    self.startinghp.text = self.parent.combat.duels[2].unit.maxhp

  def powerdrop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].unit.boost_strength(int(self.powerdrop.selected_value))
    self.strength.text = self.parent.combat.duels[2].unit.strength

  def secretdrop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].unit.boost_skill(int(self.secretdrop.selected_value))
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def speedring_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].unit.boost_speed(int(self.speedring_drop.selected_value))
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.parent.combat.duels[2].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[2].unit.AS

  def goddessdrop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].unit.boostluck(int(self.goddessdrop.selected_value))
    self.luck.text = self.parent.combat.duels[2].unit.luck
    self.parent.combat.duels[2].unitdisplay()
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def dracoshield_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].unit.boostdefense(int(self.dracoshield_drop.selected_value))
    self.defense.text = self.parent.combat.duels[2].unit.defense

  def talismandrop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].unit.boostresistance(int(self.talismandrop.selected_value))
    self.resistance.text = self.parent.combat.duels[2].unit.resistance

  def promobox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].unit.promote()
    self.hp.text = self.parent.combat.duels[2].unit.maxhp
    self.strength.text = self.parent.combat.duels[2].unit.strength
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.defense.text = self.parent.combat.duels[2].unit.defense
    self.startinghp.text = self.parent.combat.duels[2].unit.maxhp
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit
    self.attackspeed.text = self.parent.combat.duels[2].unit.AS

  def trianglecheck_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].unit.triangleattack = self.trianglecheck.checked
