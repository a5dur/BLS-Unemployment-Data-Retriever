#!/bin/sh

# Run the state unemployment script
python stateUnemployment.py
echo "State unemployment data fetched."

# Run the county unemployment script
python countyUnemployment.py
echo "County unemployment data fetched."

# Run the place unemployment script
python placeUnemployment.py
echo "Place unemployment data fetched."

# Run the merger script
python merger.py
echo "Unemployment Data Ready."
