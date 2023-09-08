# Rewards_plotting
Safe Network rewards tracking

Python required.

Add `resources.sh` to your home dir. 
(or modify as needed if you prefer elsewhere)

Start a cron job to log node data.
run `crontab -e`
Add the following job.
`**/10 * * * * /bin/bash $HOME/resources.sh >> $HOME/resources.log 2>&1`

This will take a snapshot of you node/nodes resources and rewards balance every 10 minutes and creat a log thereof, `resources.log`.

Once you have logged sufficient data you can use interactive_rewards.py to create the graph.
Modify the`path` to yours lines 78 and 82.
run `python3 interactive_rewards.py`

The plot will be saved in your home dir as `rewards_balance_plot.html`
