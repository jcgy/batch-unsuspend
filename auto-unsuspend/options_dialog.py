# Import the main window object (mw) from aqt
from aqt import mw
from anki.hooks import addHook
# Import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# Import all of the Qt GUI library
from aqt.qt import *
import glob
import os

from . import create_rule_dialog

# Options window
class OptionsDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Auto-Unsuspend Options")
		self.setMinimumSize(350, 150)

		# Create rule button
		self.create_rule_button = QPushButton("Add rule")
		self.create_rule_button.clicked.connect(self.show_create_rule_dialog)

		# Save buton
		self.save_button = QPushButton("Save")
		self.save_button.clicked.connect(self.save_options)

		# Dialog layout
		layout = QGridLayout()
		self.setLayout(layout)
		# Add titles here and then a thin separator line below
		# logic that if .config is empty show QLabel in grey that No current rules
		layout.addWidget(QLabel("<b>Name</b>"), 0, 0, Qt.AlignCenter)
		layout.addWidget(QLabel("<b>Tag</b>"), 0, 1, Qt.AlignCenter)
		layout.addWidget(QLabel("<b>Count</b>"), 0, 2, Qt.AlignCenter)
		layout.addWidget(QLabel("<b>Every (days)</b>"), 0, 3, Qt.AlignCenter)
		layout.addWidget(QLabel("<b>Active</b>"), 0, 4, Qt.AlignCenter)

		# Logic for when there are no rules set
		layout.addWidget(QLabel("No current rules"), 1, 0, 2, 5, Qt.AlignCenter)

		layout.addWidget(self.create_rule_button, 3, 0, 2, 5, Qt.AlignCenter)
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
		dialog = create_rule_dialog.CreateRuleDialog()
		dialog.exec()