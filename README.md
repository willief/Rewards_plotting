# Rewards & Resource Tracking 
See https://javages.github.io

Track and plot Safe Network node rewards.

## Requirements

- recent Linux. preferably Ubuntu
- safe client
- safe node
- sudo access - (ONLY if venv is not already installed)

## Setup

- Ensure the script is executable:

  ```bash
  chmod +x path_to_script/setup.sh

  ```

- Execute the script

 ```bash
  ./path_to_script/setup.sh

  ```

> **Note**: This script will install a virtual environment using venv. This helps to avoid potential conflicts between packages and ensures a clean, isolated environment for your project. If venv is not on your system already, you will be prompted for your password to continue.

### 1. Script Placement & Permissions

This script will install to $(HOME)/.local/share/safe/tools/Rewards_plotting; modify as needed.
All necessary permissions and crontab entries are now set by the script.

### 2. Cron Job Setup

- The setup script will add the following entry to your crontab 

```bash
  */10 * * * * /bin/bash $(HOME)/.local/share/safe/tools/Rewards_plotting/resources.sh >> $(HOME)/.local/share/safe/tools/Rewards_plotting/resources.log 2>&1
  ```
  
This job will take a snapshot of your node/nodes resources and rewards balance every 10 minutes. The data will be appended to `resources.log`.

- To change this interval or data destination, open the crontab for editing:

  ```bash
  crontab -e

  Note: Don't forget to comment out or remove this cron job if you no longer need it (in between tests), as it will run indefinitely otherwise.
  Also remember to remove the resources.log file between runs!  ##TODO   cleanup script

### 3. Graph Generation

- Once you have run for a few hours and have enough data, you can generate the graph.
- Execute the script:

  ```bash
  ./create_graphs.sh
  ```

### 4. Viewing the Graph

- The resulting plot will be saved in the app directory as
`~/.local/share/safe/tools/rewards_plotting/rewards_balance_plot.html`.
- This graph is interactive: you can zoom in, select specific nodes, and more using most browsers.    Issues have been reported with Firefox, Brave is known to work well.

---

### resources.sh

This Bash script gathers data on your node/nodes.

base_dir="${HOME}/.local/share/safe/node": This line sets the base_dir variable to the path ~/.local/share/safe/node, which is typically located in the user's home directory.

declare -A dir_pid: This declares an associative array called dir_pid, which will be used to store directory names as keys and corresponding process IDs (PIDs) as values.

node_number=0: Initializes a variable node_number to 0, which will be used to keep track of the number of nodes being processed.

The script enters a for loop that iterates over each directory within the base_dir.
The loop checks if there is a file named safenode.pid inside each directory and, if found, retrieves the PID and stores it in the dir_pid associative array.

Another for loop iterates over the keys of the dir_pid associative array, which are directory names containing the nodes.

Inside the second loop, the script performs the following tasks for each node:

Prints timestamps in both local and global (UTC) time.
Displays the node number, directory name, and PID.
Uses the ps command to fetch memory and CPU usage information for the specified PID.
Prints the status, memory usage, and CPU usage.
Counts the number of file descriptors associated with the process.
Checks if a directory named record_store exists in the node's directory and, if so, counts the number of records and displays disk usage.

### create_graphs.sh

The script activates the virtual environment and calls a python program which identifies specific lines that contain data related to various metrics such as timestamps,
node information, process IDs (PIDs), memory usage, records, disk usage, CPU usage, file descriptors, and rewards balance.
The extracted data is converted into a Pandas DataFrame.

It uses the Plotly Express library to create an interactive line plot.
The plot displays the rewards balance over time for different nodes, with each node represented by a different color.
Custom hover templates are defined to display additional information when hovering over data points, including records, disk usage, memory usage, CPU usage, file descriptors, and rewards balance.
The plot layout is customized, including background colors, gridlines, and margins.
The resulting interactive plot is saved as an HTML file.
Main Execution:

The script calls the enhanced_extract_data function to extract data from a specified log file $(HOME)/.local/share/safe/tools/rewards_plotting/resources.log
The extracted data is then passed to the visualize function to generate the rewards balance plot.

![rewards](https://github.com/javages/Rewards_plotting/assets/59794857/1f26d8df-8b05-49b7-839a-a46dc39ff631)

![mem](https://github.com/javages/Rewards_plotting/assets/59794857/9b957814-068c-4e83-8c3f-dbe7d9b2b681)
![bubs](https://github.com/javages/Rewards_plotting/assets/59794857/f986880d-93d6-4854-b3f9-d1dbfa34fd93)



