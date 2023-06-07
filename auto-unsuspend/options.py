# Import the main window object (mw) from aqt
from aqt import mw
from anki.hooks import addHook
# Import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# Import all of the Qt GUI library
from aqt.qt import *
import glob
import os

# Options window
class OptionsDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Auto-Unsuspend Options")

		# Create rule button
		self.create_rule_button = QPushButton("Create rule")
		self.create_rule_button.clicked.connect(self.show_create_rule_dialog)

		

		# Save buton
		self.save_button = QPushButton("Save")
		self.save_button.clicked.connect(self.save_options)

		# Dialog layout
		layout = QGridLayout()
		self.setLayout(layout)

		layout.addWidget(QLabel("<b> Rules: </b>"), 0, 0)
		layout.addWidget(self.create_rule_button, 1, 1)
		layout.addWidget(QLabel("        "), 1, 2) # look for better way
		#layout.addWidget(self.save_button)
		self.setLayout(layout)

	# Save options
	def save_options(self):
		selected_dictionary = self.dictionary_combo.currentData()
		CONFIG["dictionary"] = selected_dictionary
		mw.addonManager.writeConfig(ADDON_NAME, CONFIG)
		self.close()
	# Add Rule creation menu
	def show_create_rule_dialog(self):
		dialog = CreateRuleDialog()
		dialog.exec()

# Create Rule window
class CreateRuleDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Create Unsuspend Rule")

		# Dialog layout
		layout = QGridLayout()
		self.setLayout(layout)

# Add Rule creation menu
def show_create_rule_dialog():
	dialog = CreateRuleDialog()
	dialog.exec()

# Add the menu item to access the options dialog
def show_options_dialog():
	dialog = OptionsDialog()
	dialog.exec()

# Create a new menu item
action = QAction("Auto-Unsuspend Options", mw)
# set it to call options when it's clicked
qconnect(action.triggered, show_options_dialog)
# And add it to the tools menu
mw.form.menuTools.addAction(action)