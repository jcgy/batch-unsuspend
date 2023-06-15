from aqt import mw
from anki.notes import Note
from . import const
from aqt.utils import showInfo

def unsuspend_cards():
	# Get current rules set
	META = const.CONFIG

	if mw.col is None:
		showInfo("mw.col is None")
		# Collection is not available so return
		return

	# Load current config
	META = const.CONFIG

	for rule_name, rule in const.META.get("config", {}).get("Rules", {}).items():
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
		# Reset the collection to update UI
		mw.reset()