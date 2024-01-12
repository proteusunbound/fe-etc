"""Supports"""
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

supportlist = {
    "Astram": {"Midia": 10, "None": 0},
    "Abel": {"Est": 10, "None": 0},
    "Est": {"Minerva": 10, "Abel": 10},
    "Ogma": {"Caeda": 10, "None": 0},
    "Catria": {"Marth": 10, "Minerva": 10},
    "Gordin": {"Ryan": 5, "None": 0},
    "Samson": {"Sheena": 10, "None": 0},
    "Caeda": {"Marth": 10, "None": 0},
    "Sheena": {"Samson": 10, "None": 0},
    "Julian": {"Lena": 10, "None": 0},
    "Sirius": {"Nyna": 10, "None": 0},
    "Cecil": {"Roderick": 10, "None": 0},
    "Palla": {"Minerva": 10, "Abel": 10},
    "Bantu": {"Tiki": 10, "None": 10},
    "Phina": {"Navarre": 10, "None": 0},
    "Merric": {"Elice": 10, "None": 0},
    "Marth": {"Caeda": 10, "None": 0},
    "Midia": {"Astram": 10, "None": 0},
    "Minerva": {"Maria": 10, "None": 0},
    "Jubelo": {"Yuliya": 10, "None": 0},
    "Yuliya": {"Jubelo": 10, "None": 0},
    "Ryan": {"Gordin": 5, "None": 0},
    "Linde": {"Merric": 10, "None": 0},
    "Luke": {"Cecil": 5, "None": 0},
    "Lena": {"Julian": 10, "None": 0},
    "Roderick": {"Cecil": 5, "None": 0},
}
