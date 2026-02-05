#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "This project requires the Experimental Auction Dataset."
echo ""
echo "Please download the following file manually:"
echo "  Experimental Auction on Tablea Dataset (Panel).xlsx.csv"
echo ""
echo "From:"
echo "  https://data.mendeley.com/datasets/7c5vfsgcnz/1"
echo ""
echo "Then place the file under the following directory:"
echo "  Pricing/Experimental Auction on Tablea Dataset (Panel).xlsx.csv/"
echo ""

DATASET_FILE="Experimental Auction on Tablea Dataset (Panel).xlsx.csv"

if [ -f "$DATASET_FILE" ]; then
  echo "$DATASET_FILE already exists."
else
  read -p "Press ENTER after you have downloaded the dataset (or Ctrl+C to quit)..."

  if [ ! -f "$DATASET_FILE" ]; then
    echo "ERROR: $DATASET_FILE not found."
    echo "Please check that the dataset file is placed correctly."
    exit 1
  fi
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
  echo "ERROR: load_data.py not found."
  exit 1
fi

python3 load_data.py

echo ""
echo "=============================="
echo "All done! You can start to generate or evaluate data quality!"
echo "=============================="

