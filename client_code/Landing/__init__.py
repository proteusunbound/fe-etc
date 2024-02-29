"""Landing Page"""
from ._anvil_designer import LandingTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Landing(LandingTemplate):
    """Interface"""

    def __init__(self, **properties):
        self.init_components(**properties)

    def fe1button_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("fe1")

    def fe2button_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("fe2")

    def fe3button_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("fe3")

    def fe4button_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("fe4")
