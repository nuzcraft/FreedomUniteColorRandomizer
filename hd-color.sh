#!/bin/bash

printf "searching for directories to color\n"
sed 's/"//g' $1 | while IFS=, read directory bwcompress;
do
echo "$directory" "$bwcompress";
if [[ "$directory" ]]; then
    if [[ "$bwcompress" ]]; then
        compress_cmd=" -c True"
    else
        compress_cmd=""
    fi
    directory_cmd=" -d $directory"
    printf "colorizing $directory\n"
    python colorize.py $directory_cmd $compress_cmd
fi
done