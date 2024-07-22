"""
report

f
select item, cat, or item of cat
bar chart of n
list of top n items spent most time on
toggle day/week
based on toggle give date range
display of item, cat, item of cat in date range

b
func giving date range based on f output
func giving item, cat, item of cat, 's time based on f output(search algo)
func to pull item, cat, item of cat, 's time based
func to fulfill bar chart based on date range
func to fullfill list based on date range
helper func to convert data pulled to format that can display in f from TK APIs
"""

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

import reportB

class Report:
    def __init__(self, parent):
        pass