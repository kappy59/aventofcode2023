#!/bin/bash

YEAR=$1
LEVEL=$(printf "%02d" $2)

mkdir -p ${YEAR}/fixtures
[ -e ${YEAR}/${LEVEL}.py ] || cp "00.py" ${YEAR}/${LEVEL}.py
[ -e ${YEAR}/fixtures/level_${LEVEL}_part_1.txt ] || cp level_00_part_1.txt ${YEAR}/fixtures/level_${LEVEL}_part_1.txt
[ -e ${YEAR}/fixtures/level_${LEVEL}_part_2.txt ] || cp level_00_part_2.txt ${YEAR}/fixtures/level_${LEVEL}_part_2.txt