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

python3 -m venv $install_dir/RPvenv
source $install_dir/RPvenv/bin/activate

#sort perms
chmod +x -v \
  install_prereqs.sh \
  ./resources.sh \
  ./interactive_rewards.py

#get prereqs

# sh ./install_prereqs.sh
