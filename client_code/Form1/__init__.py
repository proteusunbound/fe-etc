from ._anvil_designer import Form1Template

from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import data



class Form1(Form1Template):

  def __init__(self, **properties):

    # Set Form properties and Data Bindings.

    self.init_components(**properties)


    # Any code you write here will run before the form opens.
  
  def drop_down_1_change(self, **event_args):
    unit = data.ActiveUnit(self.drop_down_1.selected_value)
    self.label_2.text = unit.maxhp
    """This method is called when an item is selected"""


    
    
