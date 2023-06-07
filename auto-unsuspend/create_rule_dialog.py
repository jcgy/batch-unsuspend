# Import the main window object (mw) from aqt
from aqt import mw
from anki.hooks import addHook
# Import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# Import all of the Qt GUI library
from aqt.qt import *
import glob
import os

# Create Rule window
class CreateRuleDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Create Unsuspend Rule")

		# Dialog layout
		layout = QGridLayout()
		self.setLayout(layout)

		# Create Save button
		self.save_button = QPushButton("Save")

		layout.addWidget(QLabel("Name"), 0, 0, Qt.AlignCenter)
		layout.addWidget(QLabel("Tag"), 0, 1, Qt.AlignCenter)
		layout.addWidget(QLabel("Count"), 0, 2, Qt.AlignCenter)
		layout.addWidget(QLabel("Every (days)"), 0, 3, Qt.AlignCenter)

		layout.addWidget(QLineEdit(), 1, 0)
		layout.addWidget(QComboBox(), 1, 1)
		layout.addWidget(QComboBox(), 1, 2)
		layout.addWidget(QComboBox(), 1, 3)

		layout.addWidget(self.save_button, 2, 0, 2, 4, Qt.AlignCenter)# Qt6,  alignment=Qt.AlignmentFlag.AlignRight)