"""Unit 4 Panel"""
from ._anvil_designer import fe4unit4_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe4combat


class fe4unit4_panel(fe4unit4_panelTemplate):
  """Unit Template"""

  def __init__(self, **properties):
    self.init_components(**properties)

  def custombutton_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = True

  def unit_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.skillslist.content = ""
    self.parent.combat.duels[3].setunit(self.unit_drop.selected_value)
    self.parent.combat.duels[3].unit.setskills()
    self.hp.text = self.parent.combat.duels[3].unit.maxhp
    self.strength.text = self.parent.combat.duels[3].unit.strength
    self.magic.text = self.parent.combat.duels[3].unit.magic
    self.skill.text = self.parent.combat.duels[3].unit.skill
    self.speed.text = self.parent.combat.duels[3].unit.speed
    self.luck.text = self.parent.combat.duels[3].unit.luck
    self.defense.text = self.parent.combat.duels[3].unit.defense
    self.resistance.text = self.parent.combat.duels[3].unit.resistance
    self.startinghp.text = self.parent.combat.duels[3].unit.maxhp
    self.weapon_drop.selected_value = None
    self.weapon_drop.visible = True
    self.power_ring.checked = False
    self.magicring.checked = False
    self.skillring.checked = False
    self.speedring.checked = False
    self.shieldring.checked = False
    self.barrier_ring.checked = False
    self.renewalband.checked = False
    self.miracleband.checked = False
    self.followupring.checked = False
    self.circlet.checked = False
    for i, skill in enumerate(self.parent.combat.duels[3].unit.skills):
      self.skillslist.content += f"{skill} \n"

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[3].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[3].adjustunitskills()
    self.parent.combat.duels[3].unitstatadjust()
    self.parent.combat.duels[3].unitdisplay()
    self.skillslist.content = ""
    for i, skill in enumerate(self.parent.combat.duels[3].unit.skills):
      self.skillslist.content += f"{skill} \n"
    self.strength.text = self.parent.combat.duels[3].unit.strength
    self.magic.text = self.parent.combat.duels[3].unit.magic
    self.skill.text = self.parent.combat.duels[3].unit.skill
    self.speed.text = self.parent.combat.duels[3].unit.speed
    self.luck.text = self.parent.combat.duels[3].unit.luck
    self.defense.text = self.parent.combat.duels[3].unit.defense
    self.resistance.text = self.parent.combat.duels[3].unit.resistance
    self.attackspeed.text = self.parent.combat.duels[3].unit.AS
    self.hit.text = self.parent.combat.duels[3].unit.hit
    self.crit.text = self.parent.combat.duels[3].unit.crit

  def setinfo(self):
    """Set Info"""
    self.parent.combat.duels[3].setunithp(self.startinghp.text)
    self.parent.combat.duels[3].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[3].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[3].setddgno(int(self.dodge_drop.selected_value))
    self.parent.combat.duels[3].setiniaccost(int(self.accost_drop.selected_value))
    self.parent.combat.duels[3].setadeptno(int(self.adept_drop.selected_value))
    self.parent.combat.duels[3].setcanceladeptno(int(self.canceladept_drop.selected_value))
    self.parent.combat.duels[3].setsolno(int(self.sol_drop.selected_value))
    self.parent.combat.duels[3].setlunano(int(self.luna_drop.selected_value))
    self.parent.combat.duels[3].setastrano(int(self.astra_drop.selected_value))

  def reset(self):
    """Reset"""
    self.unit_drop.selected_value = None
    self.weapon_drop.selected_value = None
    self.visible = False
    self.customization.visible = False
    self.supportpanel.visible = False
    self.unitproc.visible = False
    self.bossproc.visible = False
    self.equip_panel.visible = False

  def leaderdrop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[3].unit.setleadership(self.leaderdrop.selected_value)
    self.parent.combat.duels[3].unitdisplay()
    self.hit.text = self.parent.combat.duels[3].unit.hit

  def noaccost_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].noaccost = self.noaccost.checked

  def support_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = True
    if self.parent.combat.duels[3].unit.name not in ("Naoise", "Alec", "Arden", "Azelle", "Lex", "Quan", "Finn", "Midir", "Dew", "Ayra", "Deirdre", "Jamke", "Chulainn", "Lachesis", "Beowolf", "Lewyn", "Silvia", "Erinys", "Tailtiu", "Claud", "Seliph", "Oifey", "Julia", "Iucharba", "Iuchar", "Shannan", "Ares", "Hannibal"):
      self.sibling.visible = True

  def hidesupport_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = False

  def lover_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].unit.setlover(self.lover.checked)
    self.parent.combat.duels[3].unitdisplay()
    self.hit.text = self.parent.combat.duels[3].unit.hit
    self.crit.text = self.parent.combat.duels[3].unit.crit

  def sibling_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].unit.setsibling(self.sibling.checked)
    self.parent.combat.duels[3].unitdisplay()
    self.crit.text = self.parent.combat.duels[3].unit.crit

  def skills_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.unitproc.visible = True
    if "Accost" in self.parent.combat.duels[3].unit.skills:
      self.accostlabel.visible = True
      self.accost_drop.visible = True
    else:
      self.accostlabel.visible = False
      self.accost_drop.selected_value = 0
      self.accost_drop.visible = False
    if "Adept" in self.parent.combat.duels[3].unit.skills:
      self.adeptlabel.visible = True
      self.adept_drop.visible = True
    else:
      self.adeptlabel.visible = False
      self.adept_drop.selected_value = 0
      self.adept_drop.visible = False
    if "Sol" in self.parent.combat.duels[3].unit.skills:
      self.sol_label.visible = True
      self.sol_drop.visible = True
    else:
      self.sol_label.visible = False
      self.sol_drop.selected_value = 0
      self.sol_drop.visible = False
    if "Luna" in self.parent.combat.duels[3].unit.skills:
      self.lunalabel.visible = True
      self.luna_drop.visible = True
    else:
      self.lunalabel.visible = False
      self.luna_drop.selected_value = 0
      self.luna_drop.visible = False
    if "Astra" in self.parent.combat.duels[3].unit.skills:
      self.astralabel.visible = True
      self.astra_drop.visible = True
    else:
      self.astralabel.visible = False
      self.astra_drop.selected_value = 0
      self.astra_drop.visible = False

  def hideskills_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.unitproc.visible = False

  def cancelproc_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.bossproc.visible = True
    if "Accost" in self.parent.combat.duels[3].boss.skills:
      self.noaccost.visible = True
    else:
      self.noaccost.checked = False
      self.noaccost.visible = False
    if "Adept" in self.parent.combat.duels[3].boss.skills:
      self.canceladept.visible = True
      self.canceladept_drop.visible = True
    else:
      self.canceladept.visible = False
      self.canceladept_drop.selected_value = 0
      self.canceladept_drop.visible = False

  def hidecancel_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.bossproc.visible = False

  def sol_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.lunalabel.visible = False
    self.luna_drop.visible = False
    self.astralabel.visible = False
    self.astra_drop.visible = False

  def luna_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.sol_label.visible = False
    self.sol_drop.visible = False
    self.astralabel.visible = False
    self.astra_drop.visible = False

  def astra_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.sol_label.visible = False
    self.sol_drop.visible = False
    self.lunalabel.visible = False
    self.luna_drop.visible = False

  def equipment_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.equip_panel.visible = True

  def hide_equip_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.equip_panel.visible = False

  def power_ring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Power Ring")
    self.parent.combat.duels[3].unitstatadjust()
    self.strength.text = self.parent.combat.duels[3].unit.strength

  def magicring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Magic Ring")
    self.parent.combat.duels[3].unitstatadjust()
    self.magic.text = self.parent.combat.duels[3].unit.magic

  def skillring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Skill Ring")
    self.parent.combat.duels[3].unitstatadjust()
    self.parent.combat.duels[3].unitdisplay()
    self.skill.text = self.parent.combat.duels[3].unit.skill
    self.hit.text = self.parent.combat.duels[3].unit.hit
    self.crit.text = self.parent.combat.duels[3].unit.crit

  def speedring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Speed Ring")
    self.parent.combat.duels[3].unitstatadjust()
    self.parent.combat.duels[3].unitdisplay()
    self.speed.text = self.parent.combat.duels[3].unit.speed
    self.attackspeed.text = self.parent.combat.duels[3].unit.AS

  def shieldring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Shield Ring")
    self.parent.combat.duels[3].unitstatadjust()
    self.defense.text = self.parent.combat.duels[3].unit.defense

  def barrier_ring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Barrier Ring")
    self.parent.combat.duels[3].unitstatadjust()
    self.resistance.text = self.parent.combat.duels[3].unit.resistance

  def renewalband_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Renewal Band")
    self.parent.combat.duels[3].adjustunitskills()
    self.skillslist.content += "Renewal \n"

  def miracleband_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Miracle Band")
    self.parent.combat.duels[3].adjustunitskills()
    self.skillslist.content += "Miracle \n"

  def followupring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Follow-Up Ring")
    self.parent.combat.duels[3].adjustunitskills()
    self.skillslist.content += "Follow-Up \n"

  def circlet_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].setunitequip("Circlet")
    self.parent.combat.duels[3].adjustunitskills()
    self.skillslist.content += "Renewal \n"
    self.skillslist.contet += "Miracle \n"

  def charmbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[3].unit.setcharm(self.charmbox.checked)
    self.parent.combat.duels[3].unitdisplay()
    self.hit.text = self.parent.combat.duels[3].unit.hit
