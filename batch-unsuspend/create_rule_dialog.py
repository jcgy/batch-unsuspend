# Import the main window object (mw) from aqt
from aqt import mw
from anki.hooks import addHook
# Import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# Import all of the Qt GUI library
from aqt.qt import *
import glob
import os
from datetime import datetime, timedelta

from . import const

# Create Rule window
class CreateRuleDialog(QDialog):

	def __init__(self, parent=None, rule_edit=None):
		super(CreateRuleDialog, self).__init__(parent)
		self.setWindowTitle("Create Unsuspend Rule")
		self.parent = parent  # Store the parent
		self.rule_edit = rule_edit

		# Dialog layout
		layout = QGridLayout()
		self.setLayout(layout)
		# Create Save button
		self.save_button = QPushButton("Save")
		self.save_button.clicked.connect(self.save_options)

		layout.addWidget(QLabel("Name"), 0, 0, Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(QLabel("Tag"), 0, 1, Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(QLabel("Cards"), 0, 2, Qt.AlignmentFlag.AlignCenter)
		
		# Initialise values and handle editing of existing rules
		if self.rule_edit is not None:
			self.rule_name = QLineEdit(text=f"{rule_edit}")
			self.tag_box = QComboBox()
			tags = mw.col.tags.all()
			self.tag_box.addItems(tags)
			self.tag_box.setCurrentText(f"{ const.CONFIG['Rules'][rule_edit]['tag'] }")
			# Allow searching the tag box with popup
			self.tag_box.setEditable(True)
			self.tag_box.setInsertPolicy(QComboBox.NoInsert)
			self.tag_box.completer().setCompletionMode(QCompleter.PopupCompletion)
			self.tag_box.completer().setFilterMode(Qt.MatchContains)

			self.cards_box = QSpinBox(value=const.CONFIG['Rules'][rule_edit]['cards_count'], minimum=1, maximum=999)
		else:
			self.rule_name = QLineEdit()
			self.tag_box = QComboBox()
			tags = mw.col.tags.all()
			self.tag_box.addItems(tags)
			# Allow searching the tag box with popup
			self.tag_box.setEditable(True)
			self.tag_box.setInsertPolicy(QComboBox.NoInsert)
			self.tag_box.completer().setCompletionMode(QCompleter.PopupCompletion)
			self.tag_box.completer().setFilterMode(Qt.MatchContains)

			self.cards_box = QSpinBox(minimum=1, maximum=999)

		# Add widgets to gird
		layout.addWidget(self.rule_name, 1, 0)
		layout.addWidget(self.tag_box, 1, 1)
		layout.addWidget(self.cards_box, 1, 2)

		layout.addWidget(self.save_button, 2, 0, 2, 3, Qt.AlignmentFlag.AlignCenter)# Qt6,  alignment=Qt.AlignmentFlag.AlignRight)

	# Save options
	def save_options(self):
		selected_rule_name = self.rule_name.text()
		selected_tag = self.tag_box.currentText()
		selected_cards = self.cards_box.value()

		rule_dict = {}
		rule_dict["tag"] = selected_tag
		rule_dict["cards_count"] = selected_cards
		rule_dict["active"] = True

		# Check not to overwrite rules in the dictionary when not in edit mode
		if self.rule_edit is None: # Creating an entirely new rule
			if selected_rule_name in const.CONFIG["Rules"].keys():
				showInfo("Rule already exists with that name, please choose another name.")
			else:
				const.CONFIG["Rules"][selected_rule_name] = rule_dict
				mw.addonManager.writeConfig(const.ADDON_NAME, const.CONFIG)
				if self.parent is not None:
					self.parent.refresh()
				self.close()
		else: # Editing a currently exising rule
				# Edit the dictionary object in 2 steps to preserve the order
				# First rename the dictionary key in place (even if it hasn't changed)
				const.CONFIG["Rules"] = {selected_rule_name if k == self.rule_edit else k:v for k,v in const.CONFIG["Rules"].items()}
				# Then update the values
				const.CONFIG["Rules"][selected_rule_name] = rule_dict
				mw.addonManager.writeConfig(const.ADDON_NAME, const.CONFIG)
				if self.parent is not None:
					self.parent.refresh() 
				self.close()