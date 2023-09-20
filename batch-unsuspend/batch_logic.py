from aqt import mw
from anki.notes import Note
from . import const
from aqt.utils import showInfo

def unsuspend_cards():
	if mw.col is None:
		showInfo("mw.col is None")
		# Collection is not available so return
		return

	for rule_name, rule in const.CONFIG.get("Rules", {}).items():
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
				n_sus_available = len(card_ids)
				# Give user warning if not enough to unsuspend
				if n_sus_available == 0:
					showInfo(f"{rule_name} has no cards left available to un-suspend")
				elif n_sus_available < n:
					showInfo(f"{rule_name} had only {n_sus_available} card(s) left to un-suspend rather than {n}")
					# Unsuspend the remaining availanble cards
					mw.col.sched.unsuspendCards(card_ids[:n_sus_available])
				else:
					# Unsuspend the cards
					mw.col.sched.unsuspendCards(card_ids[:n])
		# Reset the collection to update UI
		mw.reset()