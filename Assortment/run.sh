#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "This project requires the Sushi Preference Dataset."
echo ""
echo "Please download the following file manually:"
echo "  sushi3-2016.zip"
echo ""
echo "From:"
echo "  https://www.kamishima.net/sushi/"
echo ""
echo "Then unzip it so that the following directory exists:"
echo "  Assortment/sushi3-2016/"
echo ""

if [ -d "sushi3-2016" ]; then
  echo "sushi3-2016/ already exists. Nothing to do."
fi

read -p "Press ENTER after you have downloaded and unzipped the dataset (or Ctrl+C to quit)..."

if [ ! -d "sushi3-2016" ]; then
  echo "ERROR: demo/sushi3-2016/ not found."
  echo "Please check that the dataset is unzipped correctly."
  exit 1
fi

echo "Dataset is ready."

if [ -d "data_generation/src/baseline" ]; then
  echo "Removing data_generation/src/baseline ..."
  rm -rf data_generation/src/baseline
fi

if [ -d "data_generation/src" ]; then
  echo "Removing data_generation/src ..."
  rm -rf data_generation/src
fi

echo "Cleanup finished."

if [ ! -f "load_data.py" ]; then
  echo "ERROR: load.py not found."
  exit 1
fi

python3 load_data.py

echo ""
echo "=============================="
echo "All done! You can start to generate or evaluate data quality!"
echo "=============================="

