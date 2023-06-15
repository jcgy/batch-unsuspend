from datetime import datetime, timedelta
from aqt import mw
from anki.notes import Note

from . import const

# Make this a function that is called when 'Unsuspend' is clicked


def unsuspend_cards():
	if mw.col is None:
		# Collection is not available so return
		return

	# Load current config
	META = const.CONFIG

	for rule_name, rule in META.get("config", {}).get("Rules", {}).items():
		tag = rule.get("tag")
		n = rule.get("cards_count")
		active = rule.get("active")
		# Set a checkpoint so batch unsuspend can be undone if needed
		mw.checkpoint(f"Unsuspend Cards")
		# Check if the rule is currently activated
		if active == True:
				# Find suspended cards for the tag
				card_ids = mw.col.findCards(f"tag:{tag} is:suspended")
				# Sort by their ID (which is equivalent to sorting by creation date)
				card_ids.sort()
				# Unsuspend the cards
				mw.col.sched.unsuspendCards(card_ids[:n])
		# Write the updated meta file
		mw.addonManager.writeConfig(const.ADDON_NAME, META)