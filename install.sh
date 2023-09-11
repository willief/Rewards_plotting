#!/bin/bash

#create install dir 
install_dir="${HOME}/.local/share/safe/tools/rewards_plotting"
if [[ ! -d $install_dir ]]; then
    mkdir -p $install_dir
    
fi 

# copy assets to install dir

for file in *;
do
    cp -v  $file $install_dir;
done    

#set up venv
python3 -m venv $install_dir/RPvenv
source $install_dir/RPvenv/bin/activate

#sort perms
chmod +x -v \
  install_prereqs.sh \
  ./resources.sh \
  ./interactive_rewards.py

#get prereqs

bash ./install_prereqs.sh

#set up cron job
echo ""
echo "This script will take a snapshot of your node/nodes resources and rewards balance every 10 minutes."
echo "The data will be appended to resources.log."
echo ""
echo ""
crontab -l > tmpcron
echo "*/10 * * * * /bin/bash $install_dir/resources.sh >> $install_dir/resources.log" >> tmpcron
crontab tmpcron 
rm tmpcron


echo ""
echo "--------------------------Rewards Plotting installation is complete------------------------------"
echo ""
echo ""
echo ""
echo "  Once you have run for a few hours and have enough data, you can generate the graph.  "
echo " Your graph will be stored as See README.md"