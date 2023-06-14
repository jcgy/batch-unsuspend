# Unsuspend Logic

- Load Rules

- Load the time of day the unsuspend should happen - make it the same as the review day in main Anki

- Link in with internal clock somehow to know how much time has elapsed

- For each Rule
	- Search for Suspended cards in tag, order by creation date, unsuspend count


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

