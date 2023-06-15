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
	#showInfo("Unsuspend is running")

	for rule_name, rule in const.META.get("config", {}).get("Rules", {}).items():
		#showInfo(f"rule_name: {rule_name}")
		tag = rule.get("tag")
		#showInfo(f"tag: {tag}")
		n = rule.get("cards_count")
		#showInfo(f"n: {n}")
		active = rule.get("active")
		#showInfo(f"active: {active}")
		# Set a checkpoint so batch unsuspend can be undone if needed
		mw.checkpoint(f"Unsuspend Cards")
		# Check if the rule is currently activated
		if active == True:
				# Find suspended cards for the tag
				card_ids = mw.col.findCards(f"tag:{tag} is:suspended")
				# Sort by their ID (which is equivalent to sorting by creation date)
				card_ids.sort()
				# Unsuspend the cards
				#showInfo(f"card_ids to unsuspend: {card_ids[:n]}")
				mw.col.sched.unsuspendCards(card_ids[:n])
		# Reset the collection to update UI
		mw.reset()