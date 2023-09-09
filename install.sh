#!/bin/bash

#create install dir
install_dir="${HOME}/.local/share/safe/tools/rewards_plotting"
if [[ -d $install_dir ]]; then
    mkdir -p $install_dir
fi 

# copy assets to install dir

cd $install_dir

#sort perms
chmod +x \
  ./install_prereqs.sh \
  ./resources.sh \
  ./interactive_rewards.py

#get prereqs
