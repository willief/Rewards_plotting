# Rewards_plotting

Track and plot Safe Network node rewards.

## Requirements

- Python3 (Ensure you have the required version, e.g., Python 3.7 or above)
- Ensure any dependencies required by `interactive_rewards.py` are installed:
  ```bash
  pip install <library-name>
  ```

## Setup

### 1. Script Placement & Permissions
  For simplicity I am use the home dir, modify as needed.

- Place `resources.sh` in your home directory. 
- Ensure the script is executable:
  ```bash
  chmod +x $HOME/resources.sh
  ```

### 2. Cron Job Setup

- Open the crontab for editing:
  ```bash
  crontab -e
  ```
- Add the following job to run the script every 10 minutes:
  ```bash
  */10 * * * * /bin/bash $HOME/resources.sh >> $HOME/resources.log 2>&1
  ```
  This job will take a snapshot of your node/nodes resources and rewards balance every 10 minutes. The data will be appended to `resources.log`.

### 3. Graph Generation
- Once you have run for a few hours and have enough data you can generate the graph.
- Before running `interactive_rewards.py`, modify the paths specified on lines 78 and 82.
- Execute the script:
  ```bash
  python3 interactive_rewards.py
  ```

### 4. Viewing the Graph

- The resulting plot will be saved in your home directory as `rewards_balance_plot.html`. This graph is interactive: you can zoom in, select specific nodes, and more.

![Screenshot from 2023-09-08 15-58-19](https://github.com/javages/Rewards_plotting/assets/59794857/7391838c-7f63-4dfb-bddb-87174d0baa42)
