from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.unit_drop.items = [(row["Name"], row) for row in app_tables.unit_stats.search()]
    self.weapon_drop.items = [(row["Name"], row) for row in app_tables.weapon_stats.search()]

    # Any code you write here will run before the form opens.
