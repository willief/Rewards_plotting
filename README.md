# Rewards_plotting
Safe Network node rewards tracking/plotting.

Python3 required.

Add `resources.sh` to your home dir. 
(or modify as needed if you prefer elsewhere)

Start a cron job to log node data.
run `crontab -e`
Add the following job.
`**/10 * * * * /bin/bash $HOME/resources.sh >> $HOME/resources.log 2>&1`

This will take a snapshot of your node/nodes resources and rewards balance every 10 minutes and create a log thereof, `resources.log`.

Once you have logged sufficient data you can use `interactive_rewards.py` to create the graph.

Modify the`path` lines 78 and 82.

run `python3 interactive_rewards.py`

The plot will be saved in your home dir as `rewards_balance_plot.html`
The graph is interactive.
You can zoom, select specific nodes etc. 


![Screenshot from 2023-09-08 15-58-19](https://github.com/javages/Rewards_plotting/assets/59794857/7391838c-7f63-4dfb-bddb-87174d0baa42)
