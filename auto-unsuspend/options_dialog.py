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

# Options window
class OptionsDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Auto-Unsuspend Options")
		self.setMinimumSize(450, 150)

		# Create rule button
		self.create_rule_button = QPushButton("Add rule")
		self.create_rule_button.clicked.connect(self.show_create_rule_dialog)

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
		count_col = 2
		days_col = 3
		active_col = 4

		self.layout.addWidget(QLabel("<b>Name</b>"), title_row, name_col, Qt.AlignCenter)
		self.layout.addWidget(QLabel("<b>Tag</b>"), title_row, tag_col, Qt.AlignCenter)
		self.layout.addWidget(QLabel("<b>Count</b>"), title_row, count_col, Qt.AlignCenter)
		self.layout.addWidget(QLabel("<b>Every (days)</b>"), title_row, days_col, Qt.AlignCenter)
		self.layout.addWidget(QLabel("<b>Active</b>"), title_row, active_col, Qt.AlignCenter)

		# Logic for when there are no rules set
		if not const.META:
			self.layout.addWidget(QLabel("No current rules"), data_row, 0, 2, 5, Qt.AlignCenter)
			data_row += 1
		else:
			rules = const.META['config']['Rules']
			for k, v in rules.items():
				self.layout.addWidget(QLabel(f"{k}"), data_row, 0, Qt.AlignCenter)
				self.layout.addWidget(QLabel(f"{v['tag']}"), data_row, 1, Qt.AlignCenter)
				self.layout.addWidget(QLabel(f"{v['count']}"), data_row, 2, Qt.AlignCenter)
				self.layout.addWidget(QLabel(f"{v['days']}"), data_row, 3, Qt.AlignCenter)
				# Create a QRadioButton
				active_button = QCheckBox()
				active_button.setChecked(v['active'])
				# Connect its toggled signal to your slot function
				# Use a lambda function to capture the current rule name (k)
				active_button.toggled.connect(partial(self.update_active_state, k))
				self.layout.addWidget(active_button, data_row, active_col, Qt.AlignCenter)
				data_row += 1

		# Add the Create rule button to layout
		self.layout.addWidget(self.create_rule_button, data_row, 0, 2, 5, Qt.AlignCenter)
		self.setLayout(self.layout)

	# Add Rule creation menu
	def show_create_rule_dialog(self):
		self.crd = create_rule_dialog.CreateRuleDialog(self)
		self.crd.exec()

	def refresh(self):
		# Reload the data
		const.META = const.load_meta(const.META_PATH)
		self.populate_layout()  # Call this to re-populate the layout
		self.exec()
	# Toggle active
	def update_active_state(self, rule_name, state):
		# Update the dictionary value based on the new state of the radio button
		const.META['config']['Rules'][rule_name]['active'] = state
		showInfo(f"state: {state}")
		showInfo(f"rule_name: {rule_name}")
		showInfo(f"what is being changed: {const.META['config']['Rules'][rule_name]['active']}")
		showInfo(f"{const.META}")
		mw.addonManager.writeConfig(const.ADDON_NAME, const.META)
