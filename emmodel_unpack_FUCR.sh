#!/bin/bash

for f in DATABIN/data/emmodel/*.pac;
do
    java -jar mhtools.jar --extract $f 6
done