### Batch-Unsuspend

Anki add-on to un-suspend a batch of cards based on custom rules targeted at the tag level.

#### Installation

Copy the  `batch-unsuspend`  directory to your  `addons21`  folder. 

#### Use

Select the current dictionary by going to  `Tools>Batch Unsuspend Options`  in the Anki menu bar. Click 'Add rule' to create a rule for targeting which card tag will be unsuspended and how many cards to un-suspend at a time. Cards are unsuspended in the order they were created.

![options](./assets/options_window.png)

![options](./assets/create_rule.png)

When 'Un-suspend' is clicked the selected rules will be executed. Rules can be toggled on or off using their checkbox. Rules can be deleted or edited from their respective options menu.

![options](./assets/rules_added.png)

Currently tested and working on  `macOS Qt5.14 Anki 2.1.64` and Windows `Qt6.4.3 Anki 2.1.64`