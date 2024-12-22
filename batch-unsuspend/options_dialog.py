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
from functools import partial
from . import create_rule_dialog
from . import const
from . import batch_logic

# Options window
class OptionsDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Batch-Unsuspend Options")
		self.setMinimumSize(950, 150) # can I pass the size here? 550 150

		# Initialise buttons
		self.create_rule_button = QPushButton("Add rule")
		self.create_rule_button.clicked.connect(self.show_create_rule_dialog)

		self.unsuspend_button = QPushButton("Un-suspend")
		self.unsuspend_button.clicked.connect(batch_logic.unsuspend_cards)
		# Then close the window after the cards have been unsuspended
		self.unsuspend_button.clicked.connect(self.reject)

        # Create a QWidget that will hold your QGridLayout
		self.gridWidget = QWidget()
		self.layout = QGridLayout(self.gridWidget)

        # Create a QScrollArea and set its widget to the QWidget
		self.scrollArea = QScrollArea()
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setWidget(self.gridWidget)

        # Set the QScrollArea as the main layout of your dialog
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(self.scrollArea)
		self.setLayout(self.mainLayout)

		self.populate_layout()

	def populate_layout(self):
		# Remove the create_rule_button from the layout
		self.layout.removeWidget(self.create_rule_button)
		try:
			self.layout.removeWidget(self.unsuspend_button)
		except:
			pass
		# Clear the layout
		while self.layout.count():
			child = self.layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

		# Constants for grid elements
		title_row = 0
		data_row = 1

		name_col = 0
		tag_col = 1
		cards_col = 2
		active_col = 3

		options_col = 5

		self.layout.addWidget(QLabel("<b>Rule Name</b>"), title_row, name_col, Qt.AlignmentFlag.AlignCenter)
		self.layout.addWidget(QLabel("<b>Tag</b>"), title_row, tag_col, Qt.AlignmentFlag.AlignCenter)
		self.layout.addWidget(QLabel("<b>Cards</b>"), title_row, cards_col, Qt.AlignmentFlag.AlignCenter)
		self.layout.addWidget(QLabel("<b>Active</b>"), title_row, active_col, Qt.AlignmentFlag.AlignCenter)

		# Logic for when there are no rules set
		if not const.CONFIG["Rules"]:
			self.layout.addWidget(QLabel("No current rules"), data_row, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
			data_row += 1
			# Remove Unsuspend button from persisting
			self.layout.removeWidget(self.unsuspend_button)
			self.unsuspend_button.hide()
			# Add the Create rule button to layout
			self.layout.removeWidget(self.create_rule_button)
			self.layout.addWidget(self.create_rule_button, data_row, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
			self.setLayout(self.layout)
		else:
			self.unsuspend_button.show()
			rules = const.CONFIG['Rules']
			for k, v in rules.items():
				self.layout.addWidget(QLabel(f"{k}"), data_row, 0, Qt.AlignmentFlag.AlignCenter)
				self.layout.addWidget(QLabel(f"{v['tag']}"), data_row, 1, Qt.AlignmentFlag.AlignCenter)
				self.layout.addWidget(QLabel(f"{v['cards_count']}"), data_row, 2, Qt.AlignmentFlag.AlignCenter)
				# Create a QRadioButton
				active_checkbox = QCheckBox()
				active_checkbox.setChecked(v['active'])
				# Connect its toggled signal to your slot function
				# Use a lambda function to capture the current rule name (k)
				active_checkbox.toggled.connect(partial(self.update_active_state, k))
				self.layout.addWidget(active_checkbox, data_row, active_col, Qt.AlignmentFlag.AlignCenter)
				# Incrememnt the data row
				data_row += 1

				# Add Unsuspend button to layout here so it is the first button created when Rules
				# are already present so it will be highlighted
				self.layout.addWidget(self.unsuspend_button, data_row, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
				# Create rule button
				self.layout.addWidget(self.create_rule_button, data_row, 2, 1, 2, Qt.AlignmentFlag.AlignCenter)
				self.setLayout(self.layout)

			# Return dimensions and update window size to fit elements horizontally
			size_hint = self.layout.sizeHint()
			width = size_hint.width()
			self.setMinimumSize(width+150, 550)

		# Place options buttons after create_rule_button so
		# create_rule button is the first button added to layout
		# and is given focus and stays blue (setFocus) doesn't work properly
		data_row = 1
		if not const.CONFIG:
			pass # This condition is already handled in the first above
		else:
			rules = const.CONFIG["Rules"]
			for k, v in rules.items():	
				# New QPushButton for the options
				options_button = QPushButton("Options")
				options_button.clicked.connect(lambda checked, b=options_button, rule_name=k: self.show_options_menu(rule_name, b))
				self.layout.addWidget(options_button, data_row, options_col, Qt.AlignmentFlag.AlignCenter)
				data_row += 1


	# Add Rule creation menu
	def show_create_rule_dialog(self):
		self.crd = create_rule_dialog.CreateRuleDialog(self)
		self.crd.exec()

	def refresh(self):
		# Reload the data
		try:
			const.CONFIG = mw.addonManager.getConfig(ADDON_NAME)
		except:
			pass
		self.populate_layout()  # Call this to re-populate the layout
		self.exec()

	def update_active_state(self, rule_name, state):
		# Update the dictionary value based on the new state of the radio button
		const.CONFIG["Rules"][rule_name]['active'] = state
		# The changes are going to be entered as a value to a config key by defaul so remove this here
		mw.addonManager.writeConfig(const.ADDON_NAME, const.CONFIG)
		# Reload config
		const.CONFIG = mw.addonManager.getConfig(const.ADDON_NAME)

	def show_options_menu(self, rule_name, button):
	# Create the QMenu and the actions
		menu = QMenu()
		edit_action = QAction("Edit", self)
		delete_action = QAction("Delete", self)
		# Connect the actions to their respective slots
		edit_action.triggered.connect(lambda _, b=button: self.edit_rule(rule_name, b))
		delete_action.triggered.connect(lambda _, b=button: self.delete_rule(rule_name, b))
		# Add the actions to the menu
		menu.addAction(edit_action)
		menu.addAction(delete_action)
		# Show the menu at the position of the button
		menu.exec(button.mapToGlobal(QPoint(0, button.height())))

	def delete_rule(self, rule_name, button):
		# writeConfig is jst writing to META, save config is saving to META remove all instances of META and just go through the CONFIG
		# Update the dictionary value to remove the rule_name key from config and meta
		const.CONFIG['Rules'].pop(rule_name, None)
		const.CONFIG = mw.addonManager.writeConfig(const.ADDON_NAME, const.CONFIG)
		# Reload the Meta file so that the version in RAM matches the version on disk
		const.CONFIG = mw.addonManager.getConfig(const.ADDON_NAME)
		# Then refresh the main options screen to get updated META
		self.refresh()

	def edit_rule(self, rule_name, button):
		# Show the create_rule_dialog and pass the rule name
		self.crd = create_rule_dialog.CreateRuleDialog(self, rule_edit=rule_name)
		self.crd.exec()