# Rewards_plotting

Safe Network node rewards tracking/plotting.

## Requirements
- Python3

## Setup

1. Add `resources.sh` to your home directory. 
   - Alternatively, modify the location as needed if you prefer it elsewhere.

2. Start a cron job to log node data.
   - Run the command `crontab -e` to edit the crontab.
   - Add the following job:
     ```
     */10 * * * * /bin/bash $HOME/resources.sh >> $HOME/resources.log 2>&1
     ```
   This will take a snapshot of your node/nodes resources and rewards balance every 10 minutes and append it to the `resources.log` file in your home directory.

3. Once you have logged sufficient data, use `interactive_rewards.py` to create the graph.
   - Modify the `path` on lines 78 and 82 in the script.
   - Run the script with the command `python3 interactive_rewards.py`.

4. The plot will be saved in your home directory as `rewards_balance_plot.html`. This graph is interactive. You can zoom in, select specific nodes, and more.



![Screenshot from 2023-09-08 15-58-19](https://github.com/javages/Rewards_plotting/assets/59794857/7391838c-7f63-4dfb-bddb-87174d0baa42)
