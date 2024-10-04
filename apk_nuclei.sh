#!/bin/bash

apktool d /mnt/c/Users/kipwo/Downloads/$1.apk -o ~/apps/$1
python3 ./exported.py ~/apps/$1
python3 ./customactions.py ~/apps/$1
python3 ./findkeys.py ~/apps/$1
echo "Nuclei Too????"
read -p "Enter to continue"
echo ~/apps/$1 | nuclei -t ./mobile-nuclei-templates
