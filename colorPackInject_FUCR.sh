#!/bin/bash
# cpi = color, pack, inject
# this script takes in a csv, and uses the contents to color, pack, and inject files into DATA.BIN
printf "searching for directories to color, pack, and inject\n\n"
sed 's/"//g' $1 | while IFS=, read id file directory paletteSize subId subDirectory;
do 
# echo "$id" "$file" "$directory" "$paletteSize" "$subId" "$subDirectory";
if [[ "$directory" ]]; then
    if [[ "$paletteSize" ]]; then
        paletteSize_cmd="-p $paletteSize "
    else
        paletteSize_cmd=""
    fi
    if [[ "$subDirectory" ]]; then
        subDirectory_cmd=" -s $subDirectory/002_image"
    else
        subDirectory_cmd=""
    fi
    directory_02_cmd="$paletteSize_cmd-d $directory/002_image$subDirectory_cmd"
    printf "colorizing $directory\n"
    python colorize.py $directory_02_cmd
    if [[ "$directory" == *"006"* ]]; then
        if [[ "$subDirectory" == *"006"* ]]; then
            subDirectory_06_cmd=" -s $subDirectory/006_image"
        else
            subDirectory_cmd=""
        fi
        directory_06_cmd="-p 2 -d $directory/006_image$subDirectory_06_cmd"
        python colorize.py $directory_06_cmd
    fi

    printf "packing $directory\n"
    java -jar mhtools.jar --rebuild ./$directory 6
    if [[ "$subDirectory" ]]; then
        java -jar mhtools.jar --rebuild ./$subDirectory 6
    fi

    printf "injecting $directory.pak into DATA.BIN in position $id\n"
    python data.py r DATA.BIN $id $directory.pak
    if [[ "$subDirectory" ]]; then
        printf "injecting $subDirectory.pak into DATA.BIN in position $subId\n"
        python data.py r DATA.BIN $subId $subDirectory.pak
    fi

    printf "removing created .paks\n\n"
    rm $directory.pak
    if [[ "$subDirectory" ]]; then
        rm $subDirectory.pak
    fi
fi
done