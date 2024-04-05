"""Unit 3 Panel"""
from ._anvil_designer import fe4unit3_panelTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import fe4combat


class fe4unit3_panel(fe4unit3_panelTemplate):
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
    self.hp.text = self.parent.combat.duels[2].unit.maxhp
    self.strength.text = self.parent.combat.duels[2].unit.strength
    self.magic.text = self.parent.combat.duels[2].unit.magic
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.luck.text = self.parent.combat.duels[2].unit.luck
    self.defense.text = self.parent.combat.duels[2].unit.defense
    self.resistance.text = self.parent.combat.duels[2].unit.resistance
    self.startinghp.text = self.parent.combat.duels[2].unit.maxhp
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
    for i, skill in enumerate(self.parent.combat.duels[2].unit.skills):
      self.skillslist.content += f"{skill} \n"
    if self.parent.combat.duels[2].unit.charclass in ("Junior Lord", "Princess", "Prince", "Cavalier", "Troubadour", "Free Knight", "Lance Knight", "Axe Knight", "Arch Knight", "Sword Armor", "Sword Fighter", "Axe Fighter", "Bow Fighter", "Thief", "Priest", "Bard", "Light Priestess", "Mage", "Thunder Mage", "Wind Mage", "Pegasus Knight", "Wyvern Rider"):
      self.promobox.visible = True

  def hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.customization.visible = False

  def weapon_drop_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.combat.duels[2].setunitweapon(self.weapon_drop.selected_value)
    self.parent.combat.duels[2].adjustunitskills()
    self.parent.combat.duels[2].unitstatadjust()
    self.parent.combat.duels[2].unitdisplay()
    self.skillslist.content = ""
    for i, skill in enumerate(self.parent.combat.duels[2].unit.skills):
      self.skillslist.content += f"{skill} \n"
    self.strength.text = self.parent.combat.duels[2].unit.strength
    self.magic.text = self.parent.combat.duels[2].unit.magic
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.luck.text = self.parent.combat.duels[2].unit.luck
    self.defense.text = self.parent.combat.duels[2].unit.defense
    self.resistance.text = self.parent.combat.duels[2].unit.resistance
    self.attackspeed.text = self.parent.combat.duels[2].unit.AS
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def setinfo(self):
    """Set Info"""
    self.parent.combat.duels[2].setunithp(self.startinghp.text)
    self.parent.combat.duels[2].setavoidno(int(self.avoid_drop.selected_value))
    self.parent.combat.duels[2].setcritno(int(self.crit_drop.selected_value))
    self.parent.combat.duels[2].setddgno(int(self.dodge_drop.selected_value))
    self.parent.combat.duels[2].setiniaccost(int(self.accost_drop.selected_value))
    self.parent.combat.duels[2].setadeptno(int(self.adept_drop.selected_value))
    self.parent.combat.duels[2].setcanceladeptno(
        int(self.canceladept_drop.selected_value)
    )
    self.parent.combat.duels[2].setsolno(int(self.sol_drop.selected_value))
    self.parent.combat.duels[2].setlunano(int(self.luna_drop.selected_value))
    self.parent.combat.duels[2].setastrano(int(self.astra_drop.selected_value))
    self.parent.combat.duels[2].setpaviseno(int(self.pavise_drop.selected_value))

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
    self.parent.combat.duels[2].unit.setleadership(self.leaderdrop.selected_value)
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit

  def noaccost_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].noaccost = self.noaccost.checked

  def support_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = True
    if self.parent.combat.duels[2].unit.name not in (
        "Naoise",
        "Alec",
        "Arden",
        "Azelle",
        "Lex",
        "Quan",
        "Finn",
        "Midir",
        "Dew",
        "Ayra",
        "Deirdre",
        "Jamke",
        "Chulainn",
        "Lachesis",
        "Beowolf",
        "Lewyn",
        "Silvia",
        "Erinys",
        "Tailtiu",
        "Claud",
        "Seliph",
        "Oifey",
        "Julia",
        "Iucharba",
        "Iuchar",
        "Shannan",
        "Ares",
        "Hannibal",
    ):
      self.sibling.visible = True

  def hidesupport_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.supportpanel.visible = False

  def lover_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].unit.setlover(self.lover.checked)
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def sibling_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].unit.setsibling(self.sibling.checked)
    self.parent.combat.duels[2].unitdisplay()
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def skills_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.unitproc.visible = True
    if "Accost" in self.parent.combat.duels[2].unit.skills:
      self.accostlabel.visible = True
      self.accost_drop.visible = True
    else:
      self.accostlabel.visible = False
      self.accost_drop.selected_value = 0
      self.accost_drop.visible = False
    if "Adept" in self.parent.combat.duels[2].unit.skills:
      self.adeptlabel.visible = True
      self.adept_drop.visible = True
    else:
      self.adeptlabel.visible = False
      self.adept_drop.selected_value = 0
      self.adept_drop.visible = False
    if "Sol" in self.parent.combat.duels[2].unit.skills:
      self.sol_label.visible = True
      self.sol_drop.visible = True
    else:
      self.sol_label.visible = False
      self.sol_drop.selected_value = 0
      self.sol_drop.visible = False
    if "Luna" in self.parent.combat.duels[2].unit.skills:
      self.lunalabel.visible = True
      self.luna_drop.visible = True
    else:
      self.lunalabel.visible = False
      self.luna_drop.selected_value = 0
      self.luna_drop.visible = False
    if "Astra" in self.parent.combat.duels[2].unit.skills:
      self.astralabel.visible = True
      self.astra_drop.visible = True
    else:
      self.astralabel.visible = False
      self.astra_drop.selected_value = 0
      self.astra_drop.visible = False
    if "Pavise" in self.parent.combat.duels[2].unit.skills:
      self.paviselabel.visible = True
      self.pavise_drop.visible = True
    else:
      self.paviselabel.visible = False
      self.pavise_drop.selected_value = 0
      self.pavise_drop.visible = False

  def hideskills_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.unitproc.visible = False

  def cancelproc_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.bossproc.visible = True
    if "Accost" in self.parent.combat.duels[2].boss.skills:
      self.noaccost.visible = True
    else:
      self.noaccost.checked = False
      self.noaccost.visible = False
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
    self.parent.combat.duels[2].setunitequip("Power Ring")
    self.parent.combat.duels[2].unitstatadjust()
    self.strength.text = self.parent.combat.duels[2].unit.strength

  def magicring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Magic Ring")
    self.parent.combat.duels[2].unitstatadjust()
    self.magic.text = self.parent.combat.duels[2].unit.magic

  def skillring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Skill Ring")
    self.parent.combat.duels[2].unitstatadjust()
    self.parent.combat.duels[2].unitdisplay()
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit

  def speedring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Speed Ring")
    self.parent.combat.duels[2].unitstatadjust()
    self.parent.combat.duels[2].unitdisplay()
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.attackspeed.text = self.parent.combat.duels[2].unit.AS

  def shieldring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Shield Ring")
    self.parent.combat.duels[2].unitstatadjust()
    self.defense.text = self.parent.combat.duels[2].unit.defense

  def barrier_ring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Barrier Ring")
    self.parent.combat.duels[2].unitstatadjust()
    self.resistance.text = self.parent.combat.duels[2].unit.resistance

  def renewalband_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Renewal Band")
    self.parent.combat.duels[2].adjustunitskills()
    self.skillslist.content += "Renewal \n"

  def miracleband_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Miracle Band")
    self.parent.combat.duels[2].adjustunitskills()
    self.skillslist.content += "Miracle \n"

  def followupring_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Follow-Up Ring")
    self.parent.combat.duels[2].adjustunitskills()
    self.skillslist.content += "Follow-Up \n"

  def circlet_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].setunitequip("Circlet")
    self.parent.combat.duels[2].adjustunitskills()
    self.skillslist.content += "Renewal \n"
    self.skillslist.contet += "Miracle \n"

  def charmbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].unit.setcharm(self.charmbox.checked)
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit

  def promobox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.parent.combat.duels[2].unit.promote()
    self.strength.text = self.parent.combat.duels[2].unit.strength
    self.magic.text = self.parent.combat.duels[2].unit.magic
    self.skill.text = self.parent.combat.duels[2].unit.skill
    self.speed.text = self.parent.combat.duels[2].unit.speed
    self.defense.text = self.parent.combat.duels[2].unit.defense
    self.resistance.text = self.parent.combat.duels[2].unit.resistance
    self.parent.combat.duels[2].unitdisplay()
    self.hit.text = self.parent.combat.duels[2].unit.hit
    self.crit.text = self.parent.combat.duels[2].unit.crit
    self.attackspeed.text = self.parent.combat.duels[2].unit.AS
    self.skillslist.content = ""
    for i, skill in enumerate(self.parent.combat.duels[2].unit.skills):
      self.skillslist.content += f"{skill} \n"

  def levelbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.parent.combat.duels[2].unit.setlevel(self.levelbox.text)
