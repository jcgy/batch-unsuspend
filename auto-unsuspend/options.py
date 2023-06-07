# Import the main window object (mw) from aqt
from aqt import mw
from anki.hooks import addHook
# Import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# Import all of the Qt GUI library
from aqt.qt import *
import glob
import os

from . import options_dialog

# Add the menu item to access the options dialog
def show_options_dialog():
	dialog = options_dialog.OptionsDialog()
	dialog.exec()

# Create a new menu item
action = QAction("Auto-Unsuspend Options", mw)
# set it to call options when it's clicked
qconnect(action.triggered, show_options_dialog)
# And add it to the tools menu
mw.form.menuTools.addAction(action)