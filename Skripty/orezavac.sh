#!/bin/bash
# Crop images to minimum 500x500px.

rpm -q gthumb
if [ $? -eq 1 ]; then
  echo "Gthumb missing"
  exit 1
else
  cd ../databaze
  for dir in *; do
    cd "$dir"
      echo "$dir"
      gthumb .
    cd ..
  done
fi

