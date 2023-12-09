#!/bin/bash

LEVEL=$(printf "%02d" $1)
[ -e ${LEVEL}.py ] || cp "00.py" ${LEVEL}.py
[ -e fixtures/level_${LEVEL}_part_1.txt ] || cp fixtures/level_00_part_1.txt fixtures/level_${LEVEL}_part_1.txt
[ -e fixtures/level_${LEVEL}_part_2.txt ] || cp fixtures/level_00_part_2.txt fixtures/level_${LEVEL}_part_2.txt