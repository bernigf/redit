#!/bin/bash

name="redit"
version="0.2.0"

folder_main=".redit"
folder_temp="tmp"
folder_cache="cache"
folder_hosts="hosts"

file_history="history.yaml"
file_config="config.yaml"

file_1_name="redit"
file_1_path="/usr/local/bin"

file_2_name="redit.py"
file_2_path="~/$folder_main"

echo ""
echo "$name installer v$version"
echo "======================"
echo ""
echo "Creating $name directories.."
echo ""

echo "Creating ~/$folder_main"
eval "mkdir ~/$folder_main"

echo "Creating ~/$folder_main/$folder_temp"
eval "mkdir ~/$folder_main/$folder_temp"

echo "Creating ~/$folder_main/$folder_cache"
eval "mkdir ~/$folder_main/$folder_cache"

#echo "Creating ~/$folder_main/$folder_cache/$folder_hosts"
#eval "mkdir ~/$folder_main/$folder_cache/$folder_hosts"

echo ""
echo "Creating $name config files..."
echo ""
echo "Creating ~/$folder_main/$file_config"
eval "touch ~/$folder_main/$file_config"
echo "Creating ~/$folder_main/$file_history"
eval "touch ~/$folder_main/$file_history"
echo ""

echo "Copying $name files..."
echo ""
echo "Copying $file_1_name to $file_1_path ..."
eval "sudo cp $file_1_name $file_1_path/"
echo "Copying $file_2_name to $file_2_path ..."
eval "sudo cp $file_2_name $file_2_path/"
echo ""

echo "Installation finished"
echo ""

