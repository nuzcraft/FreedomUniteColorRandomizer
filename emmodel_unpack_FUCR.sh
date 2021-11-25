#!/bin/bash
# run through all the .pac files in the emmodel folder and extract them
for f in DATABIN/data/emmodel/*.pac;
do
    java -jar mhtools.jar --extract $f 6
done