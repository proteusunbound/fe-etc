"""Unit 3 Panel"""

from ._anvil_designer import fe5unit3_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe5combat


class fe5unit3_panel(fe5unit3_panelTemplate):
  """Unit Template"""

  def __init__(self, **properties):
    self.init_components(**properties)

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.skillslist.content = ""
    self.parent.combat.duels[2].setunit(self.unit_drop.selected_value)
    self.parent.combat.duels[2].unit.setskills()
    self.parent.combat.duels[2].unit.setsupports()
    self.hp.text = self.parent.combat.duels[2].unit.maxhp
    self.strength.text = self.parent.combat.duels[2].unit.strength
    self.magic.text = self.parent.combat.duels[2].unit.magic
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.luck.text = self.parent.combat.duels[2].unit.luck
    self.defense.text = self.parent.combat.duels[2].unit.defense
    self.build.text = self.parent.combat.duels[2].unit.build
    self.startinghp.text = self.parent.combat.duels[2].unit.maxhp
    self.weapon_drop.selected_value = None
    self.weapon_drop.visible = True
    self.support1.checked = False
    self.support2.checked = False
    for i, skill in enumerate(self.parent.combat.duels[2].unit.skills):
      self.skillslist.content += f"{skill} \n"
    if self.parent.combat.duels[2].unit.name not in (
      "Ralf",
      "Ilios",
      "Sleuf",
      "Shannam",
      "Amalda",
    ):
      self.support.visible = True
      self.support1.text = self.parent.combat.duels[2].unit.supports[0]
      self.support2.text = self.parent.combat.duels[2].unit.supports[1]

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[2].unitdisplay()
    self.attackspeed.text = self.parent.combat.duels[2].unit.AS
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def setinfo(self):
    """Set Info"""
    self.parent.combat.duels[2].setunithp(self.startinghp.text)
    self.parent.combat.duels[2].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[2].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[2].setddgno(int(self.dodge_drop.selected_value))
    self.parent.combat.duels[2].setadeptno(int(self.adept_drop.selected_value))
    self.parent.combat.duels[2].setcanceladeptno(
      int(self.canceladept_drop.selected_value)
    )
    self.parent.combat.duels[2].setmiracleno(int(self.miracle_drop.selected_value))

  def reset(self):
    """Reset"""
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
    self.customization.visible = False
    self.unitproc.visible = False
    self.bossproc.visible = False

  def starsbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[2].unit.leaderstars = self.starsbox.text
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit

  def skills_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.unitproc.visible = True
    if "Adept" in self.parent.combat.duels[2].unit.skills:
      self.adeptlabel.visible = True
      self.adept_drop.visible = True
    else:
      self.adeptlabel.visible = False
      self.adept_drop.selected_value = 0
      self.adept_drop.visible = False
    if "Miracle" in self.parent.combat.duels[2].unit.skills:
      self.miraclelabel.visible = True
      self.miracle_drop.visible = True
    else:
      self.miraclelabel.visible = False
      self.miracle_drop.selected_value = 0
      self.miracle_drop.visible = False

  def hideskills_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.unitproc.visible = False

  def cancelproc_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.bossproc.visible = True
    if "Adept" in self.parent.combat.duels[2].boss.skills:
      self.canceladept.visible = True
      self.canceladept_drop.visible = True
    else:
      self.canceladept.visible = False
      self.canceladept_drop.selected_value = 0
      self.canceladept_drop.visible = False

  def hidecancel_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.bossproc.visible = False

  def hidesupport_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = False

  def support_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = True

  def support1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].unit.setsupportbonus(
      self.support1.text, self.support1.checked
    )
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def support2_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].unit.setsupportbonus(
      self.support2.text, self.support2.checked
    )
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit
