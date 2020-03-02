#!/bin/bash

export REGULAR="RictyDiminished-with-FiraCode-Regular.ttf"
export BOLD="RictyDiminished-with-FiraCode-Bold.ttf"
export REGULAR_DISCORD="RictyDiminishedDiscord-with-FiraCode-Regular.ttf"
export BOLD_DISCORD="RictyDiminishedDiscord-with-FiraCode-Bold.ttf"

sudo apt -y remove python3-fontforge;apt -y install fontforge
git clone https://github.com/fontforge/fontforge.git
sudo apt install -y gettext libjpeg-dev libtiff5-dev libpng-dev libfreetype6-dev libgif-dev libgtk-3-dev libxml2-dev libpango1.0-dev libcairo2-dev libspiro-dev libuninameslist-dev python3-dev ninja-build cmake build-essential;cd fontforge > /dev/null
mkdir build;cd build;cmake -GNinja .. > /dev/null;ninja > /dev/null;sudo ninja install;cd ../../;rm -rf fontforge/
for i in "$REGULAR" "$BOLD" "$REGULAR_DISCORD" "$BOLD_DISCORD"
do
  /usr/local/bin/fontforge -script nerd-fonts/font-patcher -c $i
done
