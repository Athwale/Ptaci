#!/bin/bash
# Renames JPG to jpg.

# TODO fix this, renamed files are not stored properly.

cd ../Databaze
files=$(find . -name *.JPG)

for f in $files; do
    echo "Renaming: $f"    
    filename="$(basename "$f" | awk -F '.' '{ print $1}').jpg"
    new_file="$(dirname "$f").$filename"
    mv "$f" "$new_file"
    echo "Target: $new_file"
done
