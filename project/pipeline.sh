#!/bin/bash
#"../node_modules/.bin/jv" data/brfss.jv
#!using windows therefore I use python instead of python3
jv ./data/brfss.jv
python ./data/gdc1a.py