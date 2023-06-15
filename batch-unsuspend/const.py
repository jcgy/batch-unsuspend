import os
from aqt import mw
import glob
import os
import json
from aqt.utils import showInfo

def load_meta(path: str):
	"""Looks to see if the addon has created a meta.json and
	read the file"""
	if os.path.isfile(path):
		with open(path, "r") as file:
			META = json.load(file)
			return META
	else:
		pass
		
# Global variables
ADDON_NAME = "auto-unsuspend"
CONFIG = mw.addonManager.getConfig(ADDON_NAME)
META_PATH = os.path.join(mw.pm.base, f"addons21/{ADDON_NAME}/meta.json")
META = load_meta(META_PATH)

