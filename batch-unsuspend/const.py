import os
from aqt import mw
import glob
import os
import json
from aqt.utils import showInfo

# Global variables
ADDON_NAME = __name__.split(".")[0]
CONFIG = mw.addonManager.getConfig(ADDON_NAME)