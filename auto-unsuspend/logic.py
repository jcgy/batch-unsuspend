# Unsuspend Logic

# Have to write a file that will rack the last day the unsuspend_cards function was called
# so that time can be tracked while the computer is powered off. Then n can be multiplied
# by the number of days elapsed so that all of the cards for the period would be unsuspended
# as though they had accrued daily. This means the addon becomes tied to one system and you
# would have to rememver to de-activate all rules before moving to another machine otherwise
# on return you would get double the amount of unsuspended cards even thoguh you had dealt
# with all on a daily basis on the other machine.

# Would also need to deal with when there are no rules in meta.json to iterate over, even though
# the program had not been opened in a week

from datetime import datetime, timedelta
from aqt import mw
from anki.notes import Note

from . import const

def unsuspend_cards():
	# Load current config
	META = const.CONFIG

	for rule_name, rule in META.get("config", {}).get("Rules", {}).items():
		last_unsuspend = datetime.striptime(rule.get("last_unsuspend", None), "%Y-%m-%d")
		interval_days = rule.get("interval_days")
		tag = rule.get("tag")
		n = rule.get("cards_count")
		# Check if enough days have passed since last unsuspend
		elapsed_time = datetime.now() - last_unsuspend
		time_delta = timedelta(days=interval_days)
		if elapsed_time >= time_delta:
			# Set a checkpoint so action can be undone if needed
			mw.checkpoint(f"Unsuspend Cards ({rule_name})")
			# Find suspended cards for the tag
			card_ids = mw.col.findCards(f"tag:{tag} is:suspended")
			# Sort by their ID (which is equivalent to sorting by creation date)
			card_ids.sort()
			mw.col.sched.unsuspendCards(card_ids[:n])
			# Update the last_unsuspend date in the meta
			rule['last_unsuspend'] = datetime.now().strftime("%Y-%m-%d")
	# Write the updated meta file
	mw.addonManager.writeConfig(const.ADDON_NAME, META)

