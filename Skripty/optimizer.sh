#!/bin/bash
# Optimizes images cutting down size and applying jpeg optimization.
# Orig size: 574mb
# After optimization: 548mb

cd ../Databaze
files=$(find . -name *.jpg)

for f in $files; do
    echo "Optimizing: $f"    
    jpegoptim -w 5 -s "$f"
done



