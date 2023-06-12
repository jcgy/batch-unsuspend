# Import the main window object (mw) from aqt
from aqt import mw
from anki.hooks import addHook
# Import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# Import all of the Qt GUI library
from aqt.qt import *
import glob
import os
import json
from . import create_rule_dialog
from . import const

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
		title_row = 0

		name_col = 0
		tag_col = 1
		count_col = 2
		days_col = 3
		active_col = 4

		layout.addWidget(QLabel("<b>Name</b>"), title_row, name_col, Qt.AlignCenter)
		layout.addWidget(QLabel("<b>Tag</b>"), title_row, tag_col, Qt.AlignCenter)
		layout.addWidget(QLabel("<b>Count</b>"), title_row, count_col, Qt.AlignCenter)
		layout.addWidget(QLabel("<b>Every (days)</b>"), title_row, days_col, Qt.AlignCenter)
		layout.addWidget(QLabel("<b>Active</b>"), title_row, active_col, Qt.AlignCenter)

		# Logic for when there are no rules set
		if not const.META:
			layout.addWidget(QLabel("No current rules"), 1, 0, 2, 5, Qt.AlignCenter)
		else:
			data_row = 1
			rules = const.META['config']['Rules']
			for k, v in rules.items():
				layout.addWidget(QLabel(f"{k}"), data_row, 0, Qt.AlignCenter)
				layout.addWidget(QLabel(f"{v['tag']}"), data_row, 1, Qt.AlignCenter)
				layout.addWidget(QLabel(f"{v['count']}"), data_row, 2, Qt.AlignCenter)
				layout.addWidget(QLabel(f"{v['days']}"), data_row, 3, Qt.AlignCenter)
				data_row += 1

		# Create rule button	
		layout.addWidget(self.create_rule_button, data_row, 0, 2, 5, Qt.AlignCenter)
		#layout.addWidget(self.save_button)
		self.setLayout(layout)

	# Save options
	def save_options(self):
		selected_dictionary = self.dictionary_combo.currentData()
		const.CONFIG["dictionary"] = selected_dictionary
		mw.addonManager.writeConfig(ADDON_NAME, const.CONFIG)
		self.close()
	# Add Rule creation menu
	def show_create_rule_dialog(self):
		dialog = create_rule_dialog.CreateRuleDialog()
		dialog.exec()
	# Refresh window
	def refersh_window(self):
		self.refresh